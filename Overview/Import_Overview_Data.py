class OverviewData:
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    def get_data_frame(self):
        return self.dataframe
    
    def get_dtypes(self):
        print("===== Kiểu dữ liệu =====")
        print(self.dataframe.dtypes)

    def get_shape(self):
        num_rows, num_cols = self.dataframe.shape
        print(f"Số lượng dòng: {num_rows}")
        print(f"Số lượng cột: {num_cols}")

    def most_frequent_values(self):
        for column in ['type', 'country', 'director']:
            if column in self.dataframe.columns:
                most_value = self.dataframe[column].value_counts().idxmax()
                count_of_most_value = self.dataframe[column].value_counts().max()
                
                print(f"\nGiá trị xuất hiện nhiều nhất trong cột '{column}': {most_value}")
                print(f"Số lần xuất hiện: {count_of_most_value}")
            else:
                print(f"Cột '{column}' không tồn tại trong DataFrame.")

    def get_overview(self):
        print("\nThông tin tổng quan về dữ liệu:")
        self.dataframe.info()