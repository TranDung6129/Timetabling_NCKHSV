import os
import pandas as pd
import numpy as np


class Classroom:

    def __init__(self):
        # Read excel file
        filepath = '/content/TKB SIE ky 20212 (14.4.22)(1).xlsx'
        self.df = pd.read_excel(filepath, sheet_name='Phòng học')
        # Lấy duy nhất hai cột dữ liệu cần thiết 
        self.df = self.df[["Số phòng mới", "Số chỗ ngồi"]]
        
    def get_table(self):
        return self.df
    
    def get_class_room_list(self):
        '''Lấy danh sách các phòng học''' 
        classroom_list = self.df["Số phòng mới"].to_list()
        return classroom_list
    
    def get_classroom_capacity(self, classroom_name):
        '''Lấy sức chứa của từng phòng học theo xác định. 
        classroom_name= ('tên của phòng học muốn lấy sức chứa')'''
        class_capacity_index = self.df.index[self.df['Số phòng mới'] == classroom_name].astype(int)[0]
        return self.df.at[class_capacity_index, "Số chỗ ngồi"]
