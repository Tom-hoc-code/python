import pandas as pd

class CRUD:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_data_frame(self):
        return self.dataframe

#điền giá trị 0 vào các cột min hay Season tương ứng
    def split_col(self,myDuration, myMin, mySeason):
        if "min" in str(myDuration):
            myMin = int(myDuration.split()[0])
        if "Season" in str(myDuration):           
            mySeason = int(myDuration.split()[0])
        return myMin, mySeason
    
# kiểm tra ID tồn tại
    def checkShowID(self, myInput):
        if myInput in self.dataframe['show_id'].values:
            return False
        return True
    
    #thêm 1 dòng record
    def create_data(self, new_data):
        self.dataframe.loc[len(self.dataframe)] = new_data
        print("đã thêm một dòng mới vào dataframe")
        return self.dataframe

    def read_data(self):
        return self.dataframe

# cập nhật record
    def update_data(self, item_id, new_data):
        if item_id in self.dataframe['show_id'].values:
            index = self.dataframe[self.dataframe['show_id'] == item_id].index[0]
            for column, value in new_data.items():
                if column in self.dataframe.columns:
                    self.dataframe.at[index, column] = value
            return self.dataframe
        else:
            print("Không tìm thấy show cần cập nhật.")

#xóa 1 hay nhiều record
    def delete_data(self, item_id):
        item_id_exist = []
        for x in item_id:
            if not self.checkShowID(x):
                item_id_exist.append(x)
        indexes_to_drop = self.dataframe[self.dataframe['show_id'].isin(item_id_exist)].index
        self.dataframe = self.dataframe.drop(indexes_to_drop)
        return self.dataframe

    def save_to_csv(self, file_path):
        self.dataframe.to_csv(file_path, index=False)
