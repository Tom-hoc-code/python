import pandas as pd
from datetime import datetime

class DataCleaning:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        
    def getDataframe(self):
        return self.dataframe
    
    #hiển thị giá trị Duplicated
    def showDup(self):
        duplicate_rows = self.dataframe[self.dataframe.duplicated()]
        duplicate_count = self.dataframe.duplicated(keep = False).sum()
        print("---------Checking Duplicate-----------")
        print(f"số dòng trùng: {duplicate_count}")
        print("dòng dữ liệu bị trùng: ")
        print(duplicate_rows)
        
    #xóa giá trị Duplicated
    def deleteDup(self):
        initial_count = len(self.dataframe) 
        column_check = [col for col in self.dataframe.columns if col != "show_id"]
        self.dataframe = self.dataframe.drop_duplicates(subset = column_check, keep = "first")
        final_count = len(self.dataframe)  
        print(f"đã xóa {initial_count - final_count} records trùng.") 
        return self.dataframe
    
    #Hiển thị các record chứa giá trị null
    def showNull(self):
        print("----------Checking Null------------")
        null_count = self.dataframe.isnull().sum() 
        has_null = null_count.any() 
        if has_null:
            print("dataframe có chứa giá trị null")
            print(f"Có {null_count.sum()} giá trị null:")
            print(null_count)
            print("các dòng chứa giá trị null: ")
            print(self.dataframe[self.dataframe.isnull().any(axis = 1)])
            
        else:
            print("dataframe không chứa giá trị null")
        
    #xóa các giá trị null
    def removeNull(self):
        initial_count = len(self.dataframe) 
        self.dataframe = self.dataframe.dropna(axis = 0)
        final_count = len(self.dataframe)  
        print(f"đã xóa {initial_count - final_count} records trùng.") 
        return self.dataframe
    
    #chuyển cột date_added sang dạng datetime
    def to_datetime(self):
        # Chuyển đổi cột "date_added" với định dạng mixed
        self.dataframe["date_added"] = pd.to_datetime(self.dataframe["date_added"], dayfirst=True)

        # Chuyển đổi tất cả thành định dạng mục tiêu "%d/%m/%Y"
        self.dataframe["date_added"] = self.dataframe["date_added"].dt.strftime("%d/%m/%Y")

        print("Cập nhật thành công")
        return self.dataframe
    
    #các chuẩn hóa dataframe
    def Normalize_title(self):
        print("------- Chuẩn hóa title --------")  
        print("..........") 
        indices_to_drop = self.dataframe[~self.dataframe['title'].apply(lambda x: isinstance(x, str))].index      
        self.dataframe = self.dataframe.drop(index = indices_to_drop)
        is_datetime = self.dataframe[self.dataframe["title"].str.match(r'^\d{2}-[A-Za-z]{3}$')].index
        self.dataframe = self.dataframe.drop(index = is_datetime)
        self.dataframe["title"] = self.dataframe["title"].str.strip().str.title()
        return self.dataframe
    def delete_strange_symbol(self):
        print("------- Xóa kí tự đặc biệt --------")  
        print("..........")  
        indices_to_drop = self.dataframe[self.dataframe['title'].str.contains(r'\?\?', na=False)].index
        self.dataframe = self.dataframe.drop(index = indices_to_drop)
        self.dataframe['title'] = self.dataframe['title'].apply(lambda x: x[1:] if x.startswith(('#', '?')) else x)
        indices_to_drop3 = self.dataframe[self.dataframe['title'].str.isdigit()].index
        self.dataframe = self.dataframe.drop(index = indices_to_drop3)
        indices_to_drop4 = self.dataframe[self.dataframe['title'].apply(lambda x: pd.to_datetime(x, errors='coerce')).notna()].index
        self.dataframe = self.dataframe.drop(index = indices_to_drop4)
        return self.dataframe
        
# tách cột để phân tích
    def split_duration(self):
        print("------- Tách cột duration --------")  
        self.dataframe["minutes"] = self.dataframe["duration"].apply(lambda x : int(x.split()[0]) if "min" in str(x) else 0)
        self.dataframe["season"] = self.dataframe["duration"].apply(lambda x : int(x.split()[0]) if "Season" in str(x) else 0)
        print(self.dataframe["minutes"])
        print(self.dataframe["season"])
        return self.dataframe
        
    #dổi lại tên cột
    def rename_genres(self):
        print("------- Đổi tên cột listed_in --------")  
        print("..........")
        self.dataframe.rename(columns = {"listed_in" : "genres"}, inplace = True)
        return self.dataframe
        
    def save_to_csv(self, filename):
        self.dataframe.to_csv(filename, index=False, encoding='utf-8')
        print(f"DataFrame đã được lưu vào file: {filename}")
