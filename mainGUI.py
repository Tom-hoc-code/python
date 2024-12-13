import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox
from io import StringIO
import pandas as pd
from DataCleaning import cleaningPart as cl
from Overview import Import_Overview_Data as ov
from datetime import datetime
import mainConsole
import DataVisualization.statisticaldata as st
import DataVisualization.DataVisualize as vis
global checkClean 
global checkClean2 
global df
activity_frame = None
button_frame = None
df = pd.read_csv("F:/visual studio code/python/BCPY/NetflixDataAnalyze-main/Dataset/netflix_titles.csv", encoding='ISO-8859-1')
checkClean = False
checkClean2 = False
search_entry = None
scrollbar_x = None
scrollbar_y = None
 
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

def read_csv(file_path):
    data = []
    try:
        with open(file_path, newline='', encoding='ISO-8859-1') as file:
            reader = csv.reader(file)
            print("Đọc thành công")
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Không tìm thấy tệp!")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc tệp: {e}")
        return None
    return data

#function overview dataframe
def OverView():
    # Khởi tạo đối tượng OverviewData từ DataFrame
    overview = ov.OverviewData(df)
    # Lấy số dòng và cột
    num_rows, num_cols = overview.dataframe.shape
    messagebox.showinfo("DataFrame Shape", f"Số lượng dòng: {num_rows}\nSố lượng cột: {num_cols}")

    dtypes_info = overview.dataframe.dtypes.to_string()
    messagebox.showinfo("===== Kiểu dữ liệu =====", dtypes_info)

    for column in ['type', 'country', 'director']:
        if column in overview.dataframe.columns:
            most_value = overview.dataframe[column].value_counts().idxmax()
            count_of_most_value = overview.dataframe[column].value_counts().max()
            messagebox.showinfo(
                f"Giá trị xuất hiện nhiều nhất trong cột {column}",
                f"Giá trị xuất hiện nhiều nhất: {most_value}\nSố lần xuất hiện: {count_of_most_value}"
            )
        else:
            messagebox.showinfo(
                f"Cột '{column}' không tồn tại trong DataFrame."
            )
    # Hiển thị thông tin tổng quan về dữ liệu
    buffer = StringIO()
    overview.dataframe.info(buf=buffer)
    info_str = buffer.getvalue()
    messagebox.showinfo("Thông tin tổng quan về dữ liệu:", info_str)

#function Cleaning
def handle_null_values():
    global df
    cleaning = cl.DataCleaning(df)
    initial_count = len(cleaning.dataframe) 
    cleaning.removeNull()
    final_count = len(cleaning.dataframe)  
    if initial_count - final_count <= 0:
        messagebox.showwarning("Xử lí giá trị NULL", "Bạn đã loại bỏ hết tất cả giá trị NULL")
        return
    response = messagebox.askyesno("Xử lí giá trị NULL", f"Bạn có muốn xử lí {initial_count - final_count} giá trị NULL ?")
    if response:  # Nếu người dùng chọn Yes
        df = cleaning.removeNull()
        messagebox.showinfo("Xử lí giá trị NULL", f"Đã xóa thành công {initial_count - final_count} giá trị NULL")

def handle_duplicates():
    global df
    cleaning = cl.DataCleaning(df)
    initial_count = len(cleaning.dataframe) 
    cleaning.deleteDup()
    final_count = len(cleaning.dataframe) 
    if initial_count - final_count <= 0:
        messagebox.showwarning("Xử lí giá trị Duplicate", "Bạn đã loại bỏ hết tất cả giá trị Duplicate")
        return 
    response = messagebox.askyesno("Xử lí giá trị Duplicate", f"Bạn có muốn xử lí {initial_count - final_count} giá trị Duplicate ?")
    if response:  # Nếu người dùng chọn Yes
            df = cleaning.deleteDup()
            messagebox.showinfo("Xử lí giá trị Duplicate", f"Đã xóa thành công {initial_count - final_count} giá trị Duplicate")
def normalize_data_types():
    global df
    global checkClean  
    cleaning = cl.DataCleaning(df)                 
    response = messagebox.askyesno("Chuẩn hóa kiểu dữ liệu","Chuẩn hóa cột date_added thành kiểu datetime và phân chia cột duration ?")
    if response:  # Nếu người dùng chọn Yes
        messagebox.showinfo("Chuẩn hóa kiểu dữ liệu", "Đã thực hiện chuẩn hóa cột date_added thành kiểu datetime và phân chia cột duration")
        df = cleaning.to_datetime()
        df = cleaning.split_duration()
        checkClean = True

def normalize_dataframe():
    global df
    global checkClean2  # Xác định sử dụng biến toàn cục
    cleaning = cl.DataCleaning(df)
    response = messagebox.askyesno("Chuẩn hóa Dataframe","Thực hiện Chuẩn hóa cột Title, Loại bỏ các kí tự đặc biệt và Đổi tên cột listed_in thành genres ?")
    if response:  # Nếu người dùng chọn Yes
        df = cleaning.Normalize_title()
        df = cleaning.delete_strange_symbol()
        df = cleaning.rename_genres()
        df = cleaning.getDataframe()
        messagebox.showinfo("Chuẩn hóa Dataframe", "Đã thực hiện Chuẩn hóa Dataframe")
        checkClean2 = True

def check_dataframe_dtypes():
    global df
    dtypes_data_frame = df.dtypes.to_string()
    messagebox.showinfo("===== Kiểu dữ liệu của DataFrame =====", dtypes_data_frame)    
#function commands_data_visualization
def visualize_movie_tv_ratio():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_movie_vs_tv_show_distribution()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def plot_duration_distribution():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_duration_distribution()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def count_by_release_year():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_movies_shows_by_year()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def count_by_added_year():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_added_year_trend()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def count_netflix_originals_by_year():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_exclusive_movies_by_year()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def top_countries_content():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_movie_tv_show_distribution_by_country()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def top_genres():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_top_genres()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
def top_actors_in_genres():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_top_5_actors_by_genre()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")    
def top_directors_by_rating():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        visualize.plot_top_directors_by_rating()
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")

def plot_correlation_Movie_TV_Shows():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        analysis = st.NetflixDataAnalysis(df)
        analysis.preprocess_data()
        genre_correlation_tv_shows, genre_correlation_movies = analysis.genre_correlation()
        vis.plot_correlation_matrix_matrix(genre_correlation_movies, title="Movies Genres Correlation")
        vis.plot_correlation_matrix_matrix(genre_correlation_tv_shows, title="TV Shows Genres Correlation")
        cleaning = cl.DataCleaning(df)
        df = cleaning.to_datetime()
    else:
        messagebox.showerror("Xem biểu đồ thống kê", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
        
#function commands_data_activity 
def analyze_data():
    global df
    global checkClean
    global checkClean2
    if checkClean and checkClean2:
        an = st.NetflixDataAnalysis(df)
        an.preprocess_data()
        message = ""
        # Các quốc gia có cột 'type' là 'TV show'
        message += "Các quốc gia có cột 'type' là 'TV show':\n"
        message += str(an.count_tv_shows()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Các quốc gia có cột 'type' là 'Movie'
        message += "Các quốc gia có cột 'type' là 'Movie':\n"
        message += str(an.count_movies()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Số lượng phim và show TV theo quốc gia
        message += "Số lượng phim và show TV theo quốc gia:\n"
        message += str(an.count_movies_and_shows_by_country()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Thời gian trung bình phim và show TV theo năm phát hành
        message += "Thời gian trung bình phim và show TV theo năm phát hành:\n"
        message += str(an.average_duration_by_year()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Thống kê số lượng phim độc quyền bởi Netflix
        message += "Thống kê số lượng phim độc quyền bởi Netflix:\n"
        message += str(an.exclusive_movies_count()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Thống kê số lượng phim và show TV theo năm được thêm vào Netflix
        message += "Thống kê số lượng phim và show TV theo năm được thêm vào Netflix:\n"
        message += str(an.count_by_year_added()) + "\n\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Top 5 diễn viên đóng nhiều phim nhất theo thể loại
        message += "Top 5 diễn viên đóng nhiều phim nhất theo thể loại:\n"
        top_actors = an.top_5_actors_by_genre()
        for genre, actors in top_actors.items():
            message += f"Thể loại {genre}:\n"
            message += str(actors) + "\n"  # Chuyển dictionary thành chuỗi
        message += "\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Top 5 đạo diễn có nhiều phim nhất theo loại đánh giá
        message += "Top 5 đạo diễn có nhiều phim nhất theo loại đánh giá:\n"
        top_directors = an.top_1_directors_by_rating()
        for rating, directors in top_directors.items():
            message += f"Rating {rating}:\n"
            message += str(directors) + "\n"  # Chuyển dictionary thành chuỗi
        message += "\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
        message = ""
        # Thống kê thời gian
        stats = an.calculate_duration_statistics()
        message += "Thống kê thời gian:\n"
        for key, value in stats.items():
            message += f"{key}: {value}\n"
        messagebox.showinfo("Phân tích dữ liệu Data Frame (Data Frame Analyze)", message)
    else:
        messagebox.showerror("Phân tích dữ liệu Data Frame (Data Frame Analyze)","Bạn chưa thực hiện làm sạch dữ liệu")
def export_current_dataset():
    global df
    response = messagebox.askyesno("Xuất Data Frame hiện tại","Bạn có muốn xuất file Data Frame hiện tại ?")
    if response:  # Nếu người dùng chọn Yes
        df.to_csv("F:/visual studio code/python/BCPY/NetflixDataAnalyze-main/Dataset/clean_data1.csv",index=False, encoding='utf-8')
        messagebox.showinfo("Xuất Data Frame hiện tại","Đã xuất File thành công, File được lưu ở đường dẫn ./Dataset/clean_data1.csv ")

#Hàm tạo bảng
def create_treeview(parent, columns):
    global tree

    # Xóa bảng Treeview cũ nếu nó tồn tại
    if 'tree' in globals() and tree.winfo_exists():
        tree.destroy()

    # Tạo bảng Treeview mới
    tree = ttk.Treeview(parent, columns=columns, show="headings")

    # Cài đặt tiêu đề cột
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Cài đặt màu nền cho các dòng
    tree.tag_configure("element", background="#90eeff")

    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True,pady=10)
    return tree

#function xem dataframe hiện tại cùng các thao tác trên dataframe
def show_dataframe(mydf):
    global df
    global activity_frame
    global button_frame
    global add_button
    global scrollbar_y
    global scrollbar_x
    # Kiểm tra dữ liệu có rỗng không
    if mydf is None or mydf.empty:
        print("Không có dữ liệu để hiển thị.")
        messagebox.showwarning("Cảnh báo", "Không tồn tại")
        return

    # Khai báo các biến và các tham số
    rows_per_page = 13  # Số dòng hiển thị mỗi trang
    current_page = 0
    total_pages = len(mydf) // rows_per_page  # Tổng số trang (bỏ qua tiêu đề)

    tree = create_treeview(root, list(mydf.columns))
    # Hàm cập nhật dữ liệu trong bảng theo trang
    def update_table(page):
        for item in tree.get_children():
            tree.delete(item)

        # Lấy dữ liệu cho trang hiện tại
        start = page * rows_per_page  # Bắt đầu từ dòng tiếp theo sau tiêu đề
        end = min(start + rows_per_page, len(mydf))

        # Thêm dữ liệu vào bảng và thay đổi màu cho từng dòng
        for index, row in mydf.iloc[start:end].iterrows():
            # Áp dụng tag cho dòng chẵn và lẻ
            tag = "element" 
            tree.insert("", tk.END, values=row.tolist(), tags=(tag,))

    # Hàm chuyển sang trang tiếp theo
    def next_page():
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_table(current_page)

    # Hàm chuyển về trang trước
    def previous_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            update_table(current_page)

    # Tạo khung cho các thao tác trên dataframe
    if activity_frame is not None:
        activity_frame.destroy()

    activity_frame = tk.Frame(root)
    activity_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    #Cập nhật dữ liệu
    def get_data_by_id(item_id):
        global df
        if item_id in df['show_id'].values:
            return df[df['show_id'] == item_id].iloc[0]
        else:
            return None
        
    def search_show(entries):
        item_id = entries[0].get()
        show_data = get_data_by_id(item_id)
        
        if show_data is not None:
            for i, entry in enumerate(entries[1:], start=1):
                entry.delete(0, tk.END)
                entry.insert(0, show_data[df.columns[i]])
        else:
            messagebox.showwarning("Cảnh báo", "show_id không tồn tại.")

    def submit_update(entries):

        # Lấy show_id từ ô đầu tiên
        item_id = entries[0].get()
        
        # Tạo dictionary cho dữ liệu mới
        new_data = {}
        
        # Sử dụng vòng lặp để lấy giá trị từ mọi ô nhập liệu
        temp_type = ""
        temp_duration = ""
        temp_year = ""
        value_error = False
        for i , column in enumerate(df.columns):
            try:
                if column != "minutes" and column != "season":
                    value = entries[i].get()
                    match i:
                        case 1:
                            if value not in ["Movie", "TV Show"]:
                                raise ValueError("Giá trị phải là Movie hoặc TV Show")
                            new_data[column] = value
                            temp_type = value
                        case 5:
                            if value.isdigit():
                                raise ValueError("Giá trị Country không hợp lệ")
                        case 6:
                            if not check_datetime(value):
                                raise ValueError("Giá trị phải theo dạng (%d/%m/%Y).")
                            date_object = datetime.strptime(value, "%d/%m/%Y")
                            formatted_date = date_object.strftime("%d/%m/%Y")
                            temp_year = date_object.year
                            if date_object.year < 2007:
                                raise ValueError("Giá trị năm phải lớn hơn 2007.")
                            new_data[column] = formatted_date
                        case 7:
                            if int(value) < 1888 or int(value) > 2024 or int(value) > temp_year:
                                raise ValueError("Giá trị không hợp lệ")
                            new_data[column] = value
                        case 8:
                            if value not in["PG-13", "TV-MA", "TV-14", "R", "PG", "TV-Y", "TV-PG", "TV-Y7", "TV-G", "NR"]:
                                raise ValueError("Giá trị không hợp lệ !!! Vui lòng nhập một trong các rating sau (PG-13, TV-MA, TV-14, R, PG, TV-Y, TV-PG, TV-Y7, TV-G, NR)")
                            new_data[column] = value
                        case 9:
                            
                            if temp_type == "Movie":
                                if "min" in value:
                                    new_data[column] = str(value)
                                    temp_duration = value.split()[0]
                                    if int(temp_duration) <= 0:
                                        raise ValueError("thời lượng không hợp lệ")
                                    new_data["minutes"] = int(temp_duration)
                                    new_data["season"] = 0
                                else:
                                    raise ValueError("Sai định dạng ! (số + min)")
                            else:
                                if "Season" in value:
                                    new_data[column] = str(value)
                                    temp_duration = value.split()[0]
                                    if int(temp_duration) <= 0:
                                        raise ValueError("thời lượng không hợp lệ")
                                    new_data["minutes"] = 0
                                    new_data["season"] = int(temp_duration)
                                else:
                                    raise ValueError("Sai định dang ! (số + Season)")
                        case _:
                            if column != "minutes" and column != "season":
                                new_data[column] = value
            except ValueError as e:
                    messagebox.showwarning("Cảnh báo", f"Lỗi với '{column}': {e}")
                    value_error = True

        # Bỏ qua các trường trống
        # new_data = {k: v for k, v in new_data.items() if v}  
        
        if not value_error :
            if get_data_by_id(item_id) is not None:
                # Cập nhật dữ liệu
                index = df[df['show_id'] == item_id].index[0]
                for column, value in new_data.items():
                    if column in df.columns:
                        df.at[index, column] = value
                messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy show cần cập nhật.")

    #hàm cập nhật dòng dữ liệu mới cho dataframe
    def update_row():
        # Tạo giao diện
        if checkClean and checkClean2:
            update = tk.Tk()
            update.title("Cập Nhật Dữ Liệu")
            update.geometry("350x550")
    
            entries = []
            # Tạo các trường nhập liệu cho mỗi cột trong dòng
            for i, column in enumerate(df.columns):
                label = tk.Label(update, text=column)
                label.grid(row=i, column=0, padx=20, pady=5, sticky='ew')
                entry = tk.Entry(update)
                entry.grid(row=i, column=1, padx=20, pady=5, sticky='ew')
                entries.append(entry)
    
            # Tạo một Frame để chứa nút
            temp_frame = tk.Frame(update)
            temp_frame.grid(row=len(df.columns), columnspan=2, pady=20)
    
            # Nút tìm kiếm
            search_button = tk.Button(temp_frame, text="Tìm kiếm", bg="darkblue", fg="white", font=("Arial", 12, "bold"), command=lambda: search_show(entries))
            search_button.pack(side=tk.LEFT, padx=10, pady=5)
    
            # Nút cập nhật
            save_button = tk.Button(temp_frame, text="Cập nhật", bg="darkblue", fg="white", font=("Arial", 12, "bold"), command=lambda: submit_update(entries))
            save_button.pack(side=tk.LEFT, padx=10, pady=5)
        else:
            messagebox.showerror("Lỗi", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
    
    update_button = tk.Button(activity_frame, text="Cập nhật dữ liệu", bg="darkorange", fg="white", font=("Arial", 12, "bold"), command=update_row)
    update_button.pack(side=tk.LEFT, padx=15, pady=10)

    #hàm xóa một dòng dữ liệu được click trên dataframe
    def remove_row():
        selected_items = tree.selection()  # Lấy tất cả các dòng được chọn
        if not selected_items:  # Nếu không có dòng nào được chọn
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một dòng để xóa.")
            return

        for item in selected_items:  # Lặp qua từng dòng được chọn
            selected_values = tree.item(item)['values']  # Lấy giá trị của dòng
            # Xóa bản ghi trong DataFrame
            df.drop(df[df.iloc[:, 0] == selected_values[0]].index, inplace=True)
            # Xóa dòng trong Treeview
            tree.delete(item)
        tk.messagebox.showinfo("Thông báo", "Dòng đã được xóa thành công.")
    
    remove_button = tk.Button(activity_frame, text="Xóa bản ghi", bg="black", fg="white", font=("Arial", 12, "bold"), command=remove_row)
    remove_button.pack(side=tk.LEFT, padx=15, pady=10)

    # Hàm thêm dòng trống vào bảng để nhập dữ liệu
    def add_empty_row():
        global df
        global checkClean
        global checkClean2
        if checkClean and checkClean2:
            empty_row = [''] * len(df.columns)  
            tree.insert("", tk.END, values=empty_row, tags=("element",))
            edit_row(empty_row)
        else:
            messagebox.showerror("Lỗi", "Bạn chưa thực hiện thao tác làm sạch dữ liệu ")
            
    def check_datetime(value):
        try:
            pd.to_datetime(value, format="%d/%m/%Y", errors='raise')
            return True
        except ValueError:
            return False
    
    # Hàm chỉnh sửa dòng trống
    def edit_row(empty_row):
        global df
        edit_popup = tk.Toplevel(root)
        edit_popup.title("Thêm dữ liệu")
        edit_popup.geometry("300x410")
        skip_row = ["minutes", "season", "show_id"]
        entries = []
        for i, column in enumerate(df.columns):
            if column in skip_row:
                continue
            label = tk.Label(edit_popup, text=column)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='e') 
            entry = tk.Entry(edit_popup)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')  
            entry.insert(0, empty_row[i])  # Hiển thị giá trị ban đầu (dòng trống)
            entries.append(entry) 
        
        # Nút xác nhận và cập nhật dữ liệu
        def submit_changes():
            global df
            temp_value = ""
            temp_duration = ""
            temp_release = ""
            try:
                new_row = []
                tempdf = mainConsole.sortByColumnDESC(df, "show_id")
                temp_show_id = tempdf.iloc[0, 0]
                temp_s = temp_show_id[0]
                temp_num = int(temp_show_id[1:]) + 1
                myvalue = temp_s + str(temp_num)
                new_row.append(myvalue)
                for entry, column in zip(entries, df.columns[1:]):
                    if column != "show_id":
                        value = entry.get()       
                        if column in ["release_year", "duration"]:
                            if not value.isdigit():
                                raise ValueError(f"Giá trị của '{column}' phải là số nguyên dương.")
                            if int(value) <= 0:
                                raise ValueError(f"Giá trị của '{column}' phải là số nguyên dương.")
                            value = int(value)
                        if column == "date_added":
                            if not check_datetime(value):
                                raise ValueError(f"Giá trị của '{column}' phải là ngày tháng.")
                            date_object = datetime.strptime(value, "%d/%m/%Y")
                            temp_release = date_object.year
                            if date_object.year < 2007:
                                raise ValueError(f"Giá trị của '{column}' phải lớn hơn 2007.")
                        if column == "release_year":
                            if value > 2024 or value > temp_release or int(value) < 1888:
                                raise ValueError(f"năm phát hành {column} không hợp lệ")
                        if column == "type":
                            if value != "Movie" and value != "TV Show":
                                raise ValueError(f"Giá trị của '{column}' Movie hoặc TV Show.")
                            else:
                                temp_value = value
                        if column == "country":
                            if value.isdigit():
                                raise ValueError(f"Giá trị của '{column}' phải là tên quốc gia.")
                        if column == "rating":
                            if value not in["PG-13", "TV-MA", "TV-14", "R", "PG", "TV-Y", "TV-PG", "TV-Y7", "TV-G", "NR"]:
                                raise ValueError("Giá trị không hợp lệ !!! Vui lòng nhập một trong các rating sau (PG-13, TV-MA, TV-14, R, PG, TV-Y, TV-PG, TV-Y7, TV-G, NR)")
                        if column == "duration":
                            if temp_value == "Movie":
                                value = str(value) + " min"
                            else:
                                value = str(value) + " Season"
                            temp_duration = value               
                        new_row.append(value)
                
                if "min" in temp_duration:
                    minute = int(temp_duration.split()[0])
                    season = 0
                    new_row.append(minute)
                    new_row.append(season)
                else:
                    minute = 0
                    season = int(temp_duration.split()[0])
                    new_row.append(minute)
                    new_row.append(season)
                # tree.item(tree.get_children()[-1], values=new_row)
                tree.insert("", tk.END, values=new_row)
        
                # Tạo DataFrame từ new_row
                new_df = pd.DataFrame([new_row], columns=df.columns)

                # Sử dụng concat để thêm dòng mới
                df = pd.concat([df, new_df], ignore_index=True)
                #mydf = pd.concat([mydf, new_df], ignore_index=True)
                messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!")
        
                edit_popup.destroy()
            except ValueError as e:
                tk.messagebox.showerror("Lỗi nhập liệu", str(e))
            return df
    
        submit_button = tk.Button(edit_popup, text="Lưu", bg="darkblue", fg="white", font=("Arial", 12, "bold"), command=submit_changes)
        submit_button.grid(row=len(df.columns), columnspan=3)

    add_button = tk.Button(activity_frame, text="Thêm bản ghi", bg="brown", fg="white", font=("Arial", 12, "bold"), command=add_empty_row)
    add_button.pack(side=tk.LEFT, padx=15, pady=10)

    list_col = ["show_id", "title", "minutes", "season", "release_year"]

    # Hàm sắp xếp tăng dần
    def ASC():
        selected_col = sort_var.get()
        if selected_col:  # Kiểm tra nếu có cột được chọn
            sorted_df = mainConsole.sortByColumnASC(mydf, selected_col)
            show_dataframe(sorted_df)

    # Hàm sắp xếp giảm dần
    def DESC():
        selected_col = sort_var.get()
        if selected_col:  # Kiểm tra nếu có cột được chọn
            sorted_df = mainConsole.sortByColumnDESC(mydf, selected_col)
            show_dataframe(sorted_df)

    # Tạo biến cho menu thả xuống
    sort_var = tk.StringVar(value=list_col[0])  # Giá trị mặc định

    # Tạo Combobox cho danh sách cột để sắp xếp
    label = tk.Label(activity_frame, text="Sắp xếp theo", font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=10, pady=10)
    combobox = ttk.Combobox(activity_frame, textvariable=sort_var)
    combobox['values'] = list_col  # Danh sách cột
    combobox.pack(side=tk.LEFT, padx=15, pady=10)  # Đặt sát bên trái, với khoảng cách bên phải

    # Nút sắp xếp tăng dần
    asc_button = tk.Button(activity_frame, text="Tăng dần", bg="#FFD700", fg="white", font=("Arial", 12, "bold"), command=ASC)
    asc_button.pack(side=tk.LEFT, padx=15, pady=10)  # Đặt sát bên trái, với khoảng cách bên phải
    
    # Nút sắp xếp giảm dần
    desc_button = tk.Button(activity_frame, text="Giảm dần", bg="#A2C2E5", fg="white", font=("Arial", 12, "bold"), command=DESC)
    desc_button.pack(side=tk.LEFT, padx=15, pady=10)  # Đặt sát bên trái, với khoảng cách bên phải
    
    #Tìm kiếm
    label = tk.Label(activity_frame, text="Tìm kiếm", font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=15, pady=10)
    search_entry = tk.Entry(activity_frame, width=25)
    search_entry.pack(side=tk.LEFT, padx=15, pady=5)
    def submit_search():
        search_text = search_entry.get().strip() 
        if search_text:  
            filtered_df = mainConsole.findByKey(df, search_text)
            show_dataframe(filtered_df) 
        else:
            tk.messagebox.showwarning("Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
    
    search_button = tk.Button(activity_frame, text="Tìm kiếm", bg="darkorange", fg="white", font=("Arial", 12, "bold"), command=submit_search)
    search_button.pack(side=tk.LEFT, padx=15, pady=10)

    # Thoát về dataframe hiện tại
    def exit_search():
        activity_frame.destroy()
        show_dataframe(df)
    
    exit_button = tk.Button(activity_frame, text="Thoát", bg="red", fg="white", font=("Arial", 12, "bold"), command=exit_search)
    exit_button.pack(side=tk.LEFT, padx=0, pady=10)

    if scrollbar_x and scrollbar_y is not None:
        scrollbar_x.destroy()
        scrollbar_y.destroy()
    # Thêm thanh cuộn dọc và ngang cho bảng
    scrollbar_y = tk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    tree.pack(fill="both", expand=True)
    
    if button_frame is not None:
        button_frame.destroy()
        
    # Nút "Back" và "Next"
    button_frame = tk.Frame(root)
    button_frame.pack()

    prev_button = tk.Button(
        button_frame,
        text="Back",
        command=previous_page,
        fg="white",
        bg="darkgreen",
        font=("Helvetica", 10, "bold"),
        width=10
    )
    prev_button.pack(side=tk.LEFT, padx=40, pady=1)

    next_button = tk.Button(
        button_frame,
        text="Next",
        command=next_page,
        fg="white",
        bg="darkblue",
        font=("Helvetica", 10, "bold"),
        width=10
    )
    next_button.pack(side=tk.LEFT, padx=40, pady=1)

    # Hiển thị dữ liệu trang đầu tiên
    update_table(current_page)
    root.mainloop()
    
commands_data_cleaning = {
    "Xử lý giá trị Null": handle_null_values,  # Handle Null Values
    "Xử lý giá trị Duplicate": handle_duplicates,  # Handle Duplicate Values
    "Chuẩn hóa kiểu dữ liệu": normalize_data_types,  # Normalize Data Types
    "Chuẩn hóa Dataframe": normalize_dataframe,  # Normalize DataFrame
    "DataType của DataFrame": check_dataframe_dtypes,  # Check DataFrame DataTypes
}

commands_data_visualization = {
    "Tỷ lệ Phim và Chương trình TV trên Netflix": visualize_movie_tv_ratio,  # Visualize Movie and TV Show Ratio
    "Phân phối Thời lượng Phim trên Netflix": plot_duration_distribution,  # Plot Duration Distribution
    "Số lượng phim và chương trình theo năm phát hành": count_by_release_year,  # Count by Release Year
    "Số lượng Phim và Chương trình TV được đưa vào nền tảng Netflix theo năm": count_by_added_year,  # Count by Year Added
    "Số lượng Phim Độc Quyền phát hành bởi Netflix theo Năm": count_netflix_originals_by_year,  # Count Netflix Originals by Year
    "Top 10 Quốc Gia có nhiều Phim và Chương Trình TV trên Netflix": top_countries_content,  # Top Countries by Content
    "Top 5 Thể loại Phổ biến trên Netflix": top_genres,  # Top 5 Popular Genres
    "Top 5 Diễn viên trong các Thể loại Phim phổ biến": top_actors_in_genres,  # Top 5 Actors in Popular Genres
    "Top Đạo diễn có nhiều phim nhất theo loại đánh giá": top_directors_by_rating,  # Top 5 Directors by Rating
    "Biểu đồ tương quan của Movie và TV Show về Genres": plot_correlation_Movie_TV_Shows,
}

commands_data_activity = {
    "Data Analyzing": analyze_data,  # Phân tích dữ liệu
    "Xuất ra Datasets hiện tại": export_current_dataset,  # Export Current Dataset
    "Xem Dataframe hiện tại": lambda: show_dataframe(df),  # View Current DataFrame
}

def main():
    global df
    global checkClean
    global checkClean2
    root.title("ỨNG DỤNG PHÂN TÍCH DỮ LIỆU HỆ THỐNG PHIM CỦA NETFLIX")
    title_label = tk.Label(root, text="PHÂN TÍCH DỮ LIỆU HỆ THỐNG PHIM CỦA NETFLIX", 
                           font=("Arial", 20, "bold"), fg="white", bg="#ff3131", borderwidth=4)
    title_label.pack(side="top", padx=300, pady=10, fill="both", anchor="center")
    dataset = tk.Label(root, text="====== BẢNG DỮ LIỆU ======",font=("Arial", 15, "bold"), fg="white", bg="#c6017e", borderwidth=4)
    dataset.pack(side="top", pady=15, fill="both", anchor="center")

    # Tạo Frame chính để chứa canvas và scrollbar
    main_frame = tk.Frame(root)
    main_frame.pack(side="bottom", fill="x", pady=20)
    # Tạo canvas
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)
    # Tạo thanh cuộn dọc
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    # Gắn thanh cuộn vào canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    # Tạo Frame con để chứa các nút
    button_frame = tk.Frame(canvas)
    # Đặt Frame con vào canvas
    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    
    # Hàm tạo button và trang trí:
    def display_button(commands_block, row_start, num_of_col,color,title):
        global df
        row, col = row_start, 0
        lable_menu = tk.Label(button_frame, text=title,font=("Arial", 15, "bold"), fg="white", bg="#d66a6a", borderwidth=4)
        lable_menu.grid(row=row, column=col,columnspan=4, pady=5, sticky="nsew")

        for button_title, call_function in commands_block.items():
            if col == 0:      
                row += 1  
            button = tk.Button(
                button_frame,
                text=button_title,
                command=call_function,
                font=("Arial", 11, "bold"),
                width=40,  # Độ rộng của nút
                height= 3,
                wraplength=200  # Độ dài tối đa trước khi xuống dòng (đơn vị: pixel)
                ,bg=color,fg="white"
            )
            button.grid(row=row, column=col, padx=10, pady=1, sticky="nsew")
            col += 1

            # Nếu số cột vượt quá `num_of_col`, chuyển sang hàng tiếp theo
            if col == num_of_col:
                col = 0
                row += 1
    display_button(commands_data_cleaning,0,4,"#022770","CLEANING")
    display_button(commands_data_activity,8,3,"#036b2d","ACTIVITY")
    display_button(commands_data_visualization,12,4,"#3b0070","VISUALIZATION DATA")
    def configure_frame(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    button_frame.bind("<Configure>", configure_frame)

    # Bắt sự kiện cuộn bằng chuột
    def scroll_canvas(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<MouseWheel>", scroll_canvas)
    show_dataframe(df)
    root.mainloop()


if __name__ == "__main__":
    main()