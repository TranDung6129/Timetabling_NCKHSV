import os
import pandas as pd
import numpy as np

class ClassInformation():
    
    def __init__(self):
        filepath = '/content/TKB SIE ky 20212 (14.4.22)(1).xlsx'
        self.df = pd.read_excel(filepath, sheet_name = 'Báo dạy 20212 (2)')
        
        # Thêm cột mã lớp
        new_class_code = []
        self.df['STT theo mã HP'] = self.df['STT theo mã HP'].astype(str).str.zfill(3)
        number_code = self.df["STT theo mã HP"].tolist()
        for i in number_code:
            new_code = "134" + str(i)
            new_class_code.append(new_code)
        self.df.insert(0, "Mã lớp", new_class_code, True)
        
    def get_table(self):
        return self.df
    
    def get_student_number(self, class_code):
        ''' Trả về số sinh viên từng Mã lớp.
        class_code = ('Mã lớp')'''
        class_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        return self.df.at[class_index, 'Số SV lớp cố định']

    def get_class_periods_number(self, class_code):
        '''Trả về số tiết học của một Mã lớp trong kỳ, dựa vào khối lượng'''
        period_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        periods_retrieve = self.df.at[period_index, 'KHỐI LƯỢNG ']
        if int(periods_retrieve[0]) <= 4:
            periods = str(periods_retrieve)[0]
        else: 
            periods = 0
        return periods
    
    def get_participant_class(self, class_code):
        '''Trả về tên của các lớp con tham gia một Mã lớp'''
        participant_class_index  = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        participant_class = self.df.at[participant_class_index, "Lớp"]
        participant_class_list = list(participant_class.split("+"))
        for i in participant_class_list:
            if i == 'B':
                B_index = participant_class_list.index('B')
                participant_class_list[B_index - 1] = participant_class_list[B_index - 1] + "+" + participant_class_list[B_index]
                participant_class_list.remove("B")
        return participant_class_list
    
    def get_class_code(self):
        class_code = self.df["Mã lớp"].to_list()
        return class_code
    
    def get_class_group(self, class_code):
        '''Trả về tên của các lớp con tham gia một Mã lớp'''
        participant_class_index  = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        class_group = self.df.at[participant_class_index, "Lớp"]
        return class_group
    
    def get_class_code_each_class_group(self, class_group):
        class_code_index  = self.df.index[self.df['Lớp'] == class_group].astype(int)[0]
        class_code = self.df.at[class_code_index, "Mã lớp"]
        return 
