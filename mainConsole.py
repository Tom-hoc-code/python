# Hiển thị menu
import pandas as pd
import timeit
import time
from DataCleaning import cleaningPart as cl
from Overview import Import_Overview_Data as ov
from CRUD import CRUD as cr
from datetime import datetime
import DataVisualization.statisticaldata as st
import DataVisualization.DataVisualize as vis
global checkClean 
global checkClean2 
checkClean = False
checkClean2 = False

def findByKey(df, search):
    #tìm theo hàng nếu record có chứa search
    mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
    result = df[mask]
    return result

def natural_key(string):
    result = []
    temp = ''
    for char in string:
        if char.isdigit():
            if temp and not temp[-1].isdigit():
                result.append(temp)
                temp = ''
            temp += char
        else:
            if temp and temp.isdigit():
                result.append(int(temp))
                temp = ''
            result.append(char)
    if temp:
        result.append(int(temp) if temp.isdigit() else temp)
    return result

def sortByColumnASC(df, search):
    list_col = ["show_id", "title", "minutes", "season", "release_year"]
    if search in list_col:
        if search == "show_id":
            sorted_df = df.sort_values(by=search, key=lambda x: x.apply(natural_key))
        else:
            sorted_df = df.sort_values(by=search)
    return sorted_df

def sortByColumnDESC(df, search):
    list_col = ["show_id", "title", "minutes", "season", "release_year"]
    if search in list_col:
        if search == "show_id":
            sorted_df = df.sort_values(by=search, key=lambda x: x.apply(natural_key), ascending=False)
        else:
            sorted_df = df.sort_values(by=search, ascending=False)
    return sorted_df

def show_menu(df):
    print("\n--- Đồ Án Phân Tích Dữ Liệu Phim Trên Netflix ---")
    print("1. Overview")
    print("2. Data Cleaning")
    print("3. CRUD")
    print("4. Data Analyzing")
    print("5. Data Visualization")
    print("6. Xuất ra Datasets hiện tại")
    print("7. Xem Dataframe hiện tại")
    print("8. Thoát")

def OverviewMenu(df):
    while(True):
        print("\n--- Overview về dataset ---")
        print("1. Dataset Overview")
        print("2. Về menu chính")
        overview = ov.OverviewData(df)
        mychoice = input("Nhập vào lựa chọn của bạn: ")
        if mychoice == '1':
            print("\n========= Overview ==========")
            overview.get_dtypes()
            overview.get_shape()
            overview.most_frequent_values()
            overview.get_overview()
            input("Nhấn phím bất kỳ để tiếp tục...")
        if mychoice == '2':
            break
    return df
    
def CleaningMenu(df, checkClean, checkClean2):
    while(True):
        print("\n-------- Data Cleaning --------")
        print("1. Xử lý giá trị null")
        print("2. Xử lý giá trị Duplicate")
        print("3. Chuẩn hóa kiểu dữ liệu")
        print("4. Chuẩn hóa Dataframe")
        print("5. DataType của dataframe")
        print("6. Về menu chính")
        cleaning = cl.DataCleaning(df)
        mychoice = input("Nhập vào lựa chọn của bạn: ")
        if mychoice == '1':
            cleaning.showNull()
            while(True):
                choice = input("Bạn có muốn xóa các giá trị null ?(yes/no): ")
                if choice.lower() == "yes":
                    df = cleaning.removeNull()
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                elif choice.lower() == "no":
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                else:
                    print("Nhập sai định dạng, nhập lại")
                    
        elif mychoice == '2':
            cleaning.showDup()
            while(True):
                choice = input("Bạn có muốn xóa các giá trị duplicate ?(yes/no): ")
                if choice.lower() == "yes":
                    df = cleaning.deleteDup()
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                elif choice.lower() == "no":
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                else:
                    print("Nhập sai định dạng, nhập lại")
                    
        elif mychoice == '3':
            while(True):
                choice = input("Chuẩn hóa cột date_added thành datetime và phân chia cột duration ?(yes/no): ")
                if choice.lower() == "yes":
                    df = cleaning.to_datetime()
                    df = cleaning.split_duration()
                    checkClean = True
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                elif choice.lower() == "no":
                    input("Nhấn phím bất kỳ để tiếp tục...")
                    break
                else:
                    print("Nhập sai định dạng, nhập lại")
        elif mychoice == '4':
            print("\n-------- Quy trình thực hiện --------")
            print("1. Chuẩn hóa và loại bỏ các kí tự lạ")
            print("2. Đổi tên cột")
            print("Bắt đầu thực hiện Chuẩn hóa Dataframe...")
            df = cleaning.Normalize_title()
            df = cleaning.delete_strange_symbol()
            df = cleaning.rename_genres()
            df = cleaning.getDataframe()
            checkClean2 = True
            input("Nhấn phím bất kỳ để tiếp tục...")
            
        elif mychoice == '5':
            print("\n----- Kiểu dữ liệu dataframe -----")
            print(df.dtypes)
            input("Nhấn phím bất kỳ để tiếp tục...")
        elif mychoice == '6':
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
    return df, checkClean, checkClean2

def CRUDMenu(df):
    while(True):
        print("\n---------- CRUD ----------")
        print("1. Thêm dòng record")
        print("2. Xóa dòng record")
        print("3. Cập nhật dòng record")
        print("4. Về menu chính")
        crud = cr.CRUD(df)
        mychoice = input("Nhập vào lựa chọn của bạn: ")
        if mychoice == '1':
            myshowID = ""
            myType = ""
            myRating = ""
            myMinute = 0
            mySeason = 0
            myDuration = ""
            date_year = ""
            while(True):
                myshowID = input("Nhập vào id của bạn: ")
                if crud.checkShowID(myshowID):
                    break
                else:
                    print(f"ID {myshowID} đã tồn tại. Vui lòng nhập lại ID khác!")
            while(True):
                myType = input("Nhập vào loại hình sản phẩm (Movie, TV Show): ")
                if myType in ["Movie", "TV Show"]:
                    break
                else:
                    print("Nhập sai định dạng")
            myTitle = input("Nhập vào tựa phim: ")
            myDirector = input("Nhập vào đạo diễn (ngăn cách bằng dấu phẩy): ")
            myCast = input("Nhập vào tên các diễn viên tham gia (ngăn cách bằng dấu phẩy): ")
            myCountry = input("Nhập vào quốc gia: ")
            while True:
                myDate = input("Nhập vào ngày phim được thêm vào Netflix (m/d/yyyy): ")
                try:
                    date_object = datetime.strptime(myDate, "%m/%d/%Y")
                    date_year = date_object.year
                    if date_object.year < 2007:
                        print("Năm không hợp lệ! Vui lòng nhập lại (Netflix ra mắt hình thức trực tuyến vào năm 2007).")
                        continue
                    break
                except ValueError:
                    print("Ngày không hợp lệ! Vui lòng nhập đúng định dạng m/d/yyyy.")
            while True:
                myYear = int(input("Nhập vào năm phát hành phim: "))
                if myYear >= 1888 and myYear <= 2024 and myYear <= date_year:
                    break
                else:
                    print("Năm không hợp lệ! Vui lòng nhập lại.")
            while(True):
                myRating = input("Nhập vào rating của bộ phim: ")
                if myRating in["PG-13", "TV-MA", "TV-14", "R", "PG", "TV-Y", "TV-PG", "TV-Y7", "TV-G", "NR"]:
                   break
                else:
                   print("Không tồn tại kiểu rating")
            while True:
                try:
                    myDuration = int(input("Nhập vào thời lượng: (nhập số nguyên) "))  # Chuyển giá trị nhập vào thành số nguyên
                    break  # Thoát khỏi vòng lặp nếu thành công
                except ValueError:  # Bắt lỗi nếu giá trị không phải là số nguyên
                    print("Giá trị không hợp lệ! Vui lòng nhập một số nguyên.")
            if myType == "Movie":
                myDuration = str(myDuration) + " min"
            else:
                myDuration = str(myDuration) + " Season"
            myMinute, mySeason = crud.split_col(myDuration, myMinute, mySeason)
            myGenres = input("Nhập vào thể loại phim (cách nhau bằng dấu phẩy): ")
            myDes = input("Nhập vào mô tả phim: ")
            new_record = {
                "show_id" : myshowID,
                "type" : myType,
                "title" : myTitle,
                "director" : myDirector,
                "cast" : myCast,
                "country" : myCountry,
                "date_added" : myDate,
                "release_year" : myYear,
                "rating" : myRating,
                "duration" : myDuration,
                "genres" : myGenres,
                "listed_in" : myGenres,
                "description" : myDes,
                "minutes" : myMinute,
                "season" : mySeason
                }
            df = crud.create_data(new_record)
            input("Nhấn phím bất kỳ để tiếp tục...")
        if mychoice == '2':
            while(True):
                delete_choice = input("Nhập vào những id cần xóa (cách nhau bằng dấu ,): ").split()
                if not crud.checkShowID(delete_choice):
                    df = crud.delete_data(delete_choice)
                    break
                else:
                    print("ID không tìm thấy")
            input("Nhấn phím bất kỳ để tiếp tục...")
        if mychoice == '3':
            new_data = {}
            item_id = ""
            while(True):
                item_id = input("Nhập ID record muốn chỉnh sửa: ")
                if not crud.checkShowID(item_id):
                    columns_to_update = input("Nhập tên các cột bạn muốn cập nhật (cách nhau bởi dấu phẩy): ").split(',')
                    for column in columns_to_update:
                        column = column.strip()
                        if column in df.columns:
                            new_value = input(f"Nhập giá trị mới cho {column}: ")
                            if new_value:
                                new_data[column] = new_value
                        else:
                            print(f"Cột '{column}' không tồn tại.")
                    df = crud.update_data(item_id, new_data)
                    break
                else:
                    print("ID không tồn tại")
            input("Nhấn phím bất kỳ để tiếp tục...")
        if mychoice == '4':
            break
    return df

def DataAnalyzingMenu(df, checkClean, checkClean2):
    if checkClean and checkClean2:
        an = st.NetflixDataAnalysis(df)
        an.preprocess_data()
        an.print_summary()
        input("Nhấn phím bất kỳ để quay về.")
    else:
        print("Bạn chưa thực hiện làm sạch dữ liệu !")
        input("Nhấn phím bất kỳ để quay về...")
    return df
def DataVisualization(df, checkClean, checkClean2):
    if checkClean and checkClean2:
        analyze = st.NetflixDataAnalysis(df)
        analyze.preprocess_data()
        visualize = vis.NetflixDataVisualization(analyze)
        print("Tỷ lệ Phim và Chương trình TV trên Netflix")
        visualize.plot_movie_vs_tv_show_distribution()
        print("Phân phối Thời lượng Phim trên Netflix")
        visualize.plot_duration_distribution()
        print("Số lượng phim và chương trình theo năm phát hành")
        visualize.plot_movies_shows_by_year()
        print("Số lượng Phim và Chương trình TV được đưa vào nền tảng Netflix theo năm")
        visualize.plot_added_year_trend()
        print("Số lượng Phim Độc Quyền phát hành bởi Netflix theo Năm")
        visualize.plot_exclusive_movies_by_year()
        print("Top 10 Quốc Gia có nhiều Phim và Chương Trình TV trên Netflix")
        visualize.plot_movie_tv_show_distribution_by_country()
        print("Top 5 Thể loại Phổ biến trên Netflix")
        visualize.plot_top_genres()
        print("Top 5 Diễn viên trong các Thể loại Phim phổ biến")
        visualize.plot_top_5_actors_by_genre()
        print("Top đạo diễn có nhiều phim nhất theo loại đánh giá")     
        visualize.plot_top_directors_by_rating()
        print("Biểu đồ tương quan của Movie và TV Show về Genres")     
        genre_correlation_tv_shows, genre_correlation_movies = analyze.genre_correlation()
        vis.plot_correlation_matrix_matrix(genre_correlation_movies, title="Movies Genres Correlation")
        vis.plot_correlation_matrix_matrix(genre_correlation_tv_shows, title="TV Shows Genres Correlation")
    else:
        print("Bạn chưa thực hiện làm sạch dữ liệu !")
        input("Nhấn phím bất kỳ để quay về...")
    
def main(checkClean, checkClean2):
    df = pd.read_csv("F:/visual studio code/python/BCPY/NetflixDataAnalyze-main/Dataset/netflix_titles.csv", encoding='ISO-8859-1')
    while True:
        show_menu(df)
        while(True):
            choice = input("Chọn một chức năng: ")
            if choice == '1':
                OverviewMenu(df)
                input("Nhấn phím bất kỳ để quay về...")
                break
            elif choice == '2':
                df, checkClean, checkClean2 = CleaningMenu(df, checkClean, checkClean2)
                break
            elif choice == '3':
                df = CRUDMenu(df)
                break
            elif choice == '4':
                df = DataAnalyzingMenu(df, checkClean, checkClean2)
                break
            elif choice == '5':
                DataVisualization(df, checkClean, checkClean2)
                break
            elif choice == '6':
                df.to_csv("F:/visual studio code/python/BCPY/NetflixDataAnalyze-main/Dataset/netflix_cleaned_data.csv",index=False, encoding='utf-8')
                print("DataFrame đã được xuất.")
                input("Nhấn phím bất kỳ để tiếp tục...")
                break
            elif choice == '7':
                print(df)
                input("Nhấn phím bất kỳ để tiếp tục...")
                break
            elif choice == '8':
                print("Thoát chương trình, tạm biệt")
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

        
    
if __name__ == "__main__":
    main(checkClean, checkClean2)
