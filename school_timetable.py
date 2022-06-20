"""
# Import Libarary and Package
"""

import os
import pandas as pd
import numpy as np
# import pyomo.environ as pyo
# from pyomo.environ import * 
import itertools
from itertools import combinations_with_replacement
# from pyomo.opt import SolverStatus, TerminationCondition
from functools import reduce
from time import time
import random

"""# Classroom """

import os
import pandas as pd
import numpy as np


class Classroom:

    def __init__(self):
        # Read excel file
        filepath = 'D:/Nhóm nghiên cứu/Nghiên cứu ứng dụng/Bài toán lập lịch/SVNCKH 2022/DỮ LIỆU/TKB SIE ky 20212 (14.4.22)(1).xlsx'
        self.df = pd.read_excel(filepath, sheet_name='Phòng học')
        # Lấy duy nhất hai cột dữ liệu cần thiết 
        self.df = self.df[["Số phòng mới", "Số chỗ ngồi"]]

    def get_table(self):
        return self.df

    def get_classroom_list(self):
        '''Lấy danh sách các phòng học'''
        classroom_list = self.df["Số phòng mới"].to_list()
        return classroom_list

    def get_classroom_capacity(self, classroom_name):
        '''Lấy sức chứa của từng phòng học theo xác định. 
        classroom_name= ('tên của phòng học muốn lấy sức chứa')'''
        class_capacity_index = self.df.index[self.df['Số phòng mới'] == classroom_name].astype(int)[0]
        return self.df.at[class_capacity_index, "Số chỗ ngồi"]


"""# Information"""

import os
import pandas as pd
import numpy as np


class ClassInformation():

    def __init__(self):
        filepath = 'D:/Nhóm nghiên cứu/Nghiên cứu ứng dụng/Bài toán lập lịch/SVNCKH 2022/DỮ LIỆU/TKB SIE ky 20212 (14.4.22)(1).xlsx'
        self.df = pd.read_excel(filepath, sheet_name='Báo dạy 20212 (2)')

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
        participant_class_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        participant_class = self.df.at[participant_class_index, "Lớp"]
        participant_class_list = list(participant_class.split("+"))
        for i in participant_class_list:
            if i == 'B':
                B_index = participant_class_list.index('B')
                participant_class_list[B_index - 1] = participant_class_list[B_index - 1] + "+" + \
                                                      participant_class_list[B_index]
                participant_class_list.remove("B")
        return participant_class_list

    def get_class_code(self):
        class_code = self.df["Mã lớp"].to_list()
        return class_code

    def get_class_group(self, class_code):
        '''Trả về tên của các lớp con tham gia một Mã lớp'''
        participant_class_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        class_group = self.df.at[participant_class_index, "Lớp"]
        return class_group

    def get_class_code_each_class_group(self, class_group):
        class_code_index = self.df.index[self.df['Lớp'] == class_group].astype(int)[0]
        class_code = self.df.at[class_code_index, "Mã lớp"]
        return

    def get_class_group_student_number(self, class_group):
        '''Trả về tên của các lớp con tham gia một Mã lớp'''
        group_student_index = self.df.index[self.df['Lớp'] == class_group].astype(int)[0]
        class_group_student_number = self.df.at[group_student_index, "Số SV lớp cố định"]
        return class_group_student_number


"""# DataFrame"""

# Điều chỉnh DataFrame 
classroom = Classroom()
classroom_df = classroom.df
information = ClassInformation()
information_df = information.df

"""# G set (G_big and G_small)
An available set which contains all groups of students
"""

start_time = time()
"""Nhập các tập đầu vào của mô hình"""


# Tập hợp group_of_student là tập hợp chứa tất cả các nhóm học sinh
def G_set():
    """Đưa ra tập hợp chứa tất cả các nhóm lớp"""
    group_of_student = []
    for class_code in information.get_class_code():
        group_of_student.append(information.get_class_group(class_code))

    unique_class_group = []
    for class_group in group_of_student:
        if class_group not in unique_class_group:
            unique_class_group.append(class_group)

    group_of_student = unique_class_group
    ## Tạo tập hợp chứa các phần tử rỗng 
    group_of_student_dict = {}
    for n in range(len(group_of_student)):
        group_of_student_dict[f"G{n}"] = []

    ## Nhập dữ liệu các nhóm lớp
    for class_group in range(len(group_of_student)):
        group_of_student_dict[f"G{class_group}"] = group_of_student[class_group]

    ### Chia các lớp thành các phần tử nhỏ hơn
    for key in group_of_student_dict:
        group_of_student_dict[key] = group_of_student_dict[key].split("+")

    ### Chỉnh sửa lại các lớp con 
    for key in group_of_student_dict:
        for i in group_of_student_dict[key]:
            if i == 'B':
                B_index = group_of_student_dict[key].index('B')
                group_of_student_dict[key][B_index - 1] = group_of_student_dict[key][B_index - 1] + "+" + \
                                                          group_of_student_dict[key][B_index]
                group_of_student_dict[key].remove("B")
    return group_of_student_dict


# Tập hợp G_big chứa các nhóm lớp có nhiều hơn hai lớp con từ tập G
def G_big_set(G_set):
    G_big_dict = {}
    for key in G_set:
        if len(G_set[key]) >= 2:
            G_big_dict.update({key: G_set[key]})
    return G_big_dict


# Tập hợp G_small chứa các lớp con (chỉ gồm duy nhất một lớp) từ tập G
def G_small_set(G_set):
    G_small_dict = {}
    for key in G_set:
        if len(G_set[key]) < 2:
            G_small_dict.update({key: G_set[key]})
    return G_small_dict


# Tạo ra tập G
G_set = G_set()
# Lấy tập G lớn từ tập G
G_big_set = G_big_set(G_set)
# Lấy tập G nhỏ từ tập G
G_small_set = G_small_set(G_set)

"""# C set
An available set which contains all the courses in the semester
"""


# Tập C chứa tất cả các lớp mở trong kỳ
def C_set():
    course_dict = {}
    for class_code in information.get_class_code():
        course_dict[class_code] = {"Sub": information_df.loc[information.get_class_code().index(class_code), 'TÊN HP']}
    return course_dict


C_set = C_set()
## Loại lớp

"""# R_set
An available set which contains classrooms grouped by their capacity
"""


# Tập hợp chứa tất cả các phòng học có thể sử dụng
def R_all():
    global classroom
    R_all = []
    for classroom_name in classroom.get_classroom_list():
        R_all.append(classroom_name)
    R_all = set(R_all)
    return R_all


# Tập hợp chứa sức chứa có thể của các phòng
def classroom_capacity(R_all):
    global classroom
    classroom_capacity = []
    for classroom_name in R_all:
        classroom_capacity.append(classroom.get_classroom_capacity(classroom_name))

    classroom_capacity_unique = []

    for i in classroom_capacity:
        if i not in classroom_capacity_unique:
            classroom_capacity_unique.append(i)
    return classroom_capacity_unique


# Tập R là tập hợp chứa các phòng được nhóm lại theo sức chứa
def R_set(classroom_capacity):
    global classroom
    R_set = {}
    for class_capacity in classroom_capacity:
        R_set[class_capacity] = []

    for class_capacity in classroom_capacity:
        for classroom_name in classroom.get_classroom_list():
            if classroom.get_classroom_capacity(classroom_name) == class_capacity:
                R_set[class_capacity].append(classroom_name)
    return R_set


# Tạo ra tập R_all
R_all = R_all()
# Tạo ra tập R 
classroom_capacity = classroom_capacity(R_all)
R_set = R_set(classroom_capacity)
# Sắp xếp lại sức chứa của phòng theo thứ tự tăng dần 
classroom_capacity.sort()

"""# Rg Set
An available set which contains groups of students accompanied by the
classroom’s capacity that fits them

"""


def Rg_set():
    group_of_student = []
    for class_code in information.get_class_code():
        group_of_student.append(information.get_class_group(class_code))

    unique_class_group = []
    for class_group in group_of_student:
        if class_group not in unique_class_group:
            unique_class_group.append(class_group)

    group_student_number = {}
    for class_group in unique_class_group:
        group_student_number[class_group] = information.get_class_group_student_number(class_group)

    for class_group in group_student_number:
        for capacity in classroom_capacity:
            if group_student_number[class_group] <= capacity:
                group_student_number[class_group] = capacity
                break

    Rg_set = {}
    for i in range(len(G_set)):
        Rg_set[f"G{i}"] = group_student_number[unique_class_group[i]]
    return Rg_set


# Tạo tập Rg
Rg_set = Rg_set()

"""# Cg set (Cg_big and Cg_small)

A set which contains groups of students accompanied by the courses that
they need to register in the semester


"""


# Tập C chứa các nhóm lớp, đi cùng với các mã lớp mà nhóm lớp đó sẽ học trong kỳ
def Cg_set():
    Cg_set = {}

    group_of_student = []
    for class_code in information.get_class_code():
        group_of_student.append(information.get_class_group(class_code))

    unique_class_group = []
    for class_group in group_of_student:
        if class_group not in unique_class_group:
            unique_class_group.append(class_group)

    for class_group in unique_class_group:
        temp_list = []
        for i in range(len(information_df)):
            if information_df.iloc[i, 7] == class_group:
                temp_list.append(information_df.iloc[i, 0])
        Cg_set[f"G{unique_class_group.index(class_group)}"] = temp_list
    return Cg_set


# Tập Cg_big chứa các nhóm lớp đi cùng với mã lớp mà nhóm lớp đó sẽ học trong kỳ (số lượng mã lớp lớn hơn hoặc bằng 2)
def Cg_big_set(Cg_set):
    Cg_big_dict = {}
    for key in Cg_set:
        if len(Cg_set[key]) >= 2:
            Cg_big_dict.update({key: G_set[key]})
    return Cg_big_dict


# Tập Cg_small chứa các nhóm lớp đi cùng với mã lớp mà nhóm lớp đó sẽ học trong kỳ (số lượng mã lớp nhỏ hơn 2)
def Cg_small_set(Cg_set):
    Cg_small_dict = {}
    for key in Cg_set:
        if len(Cg_set[key]) < 2:
            Cg_small_dict.update({key: G_set[key]})
    return Cg_small_dict


# Tạo tập Cg
Cg_set = Cg_set()
# Tạo tập Cg_big 
Cg_big_set = Cg_big_set(Cg_set)
# Tạo tập Cg_small
Cg_small_set = Cg_small_set(Cg_set)

"""# D set
A set which contains all sessions in week
"""

D_set = {1, 2, 4, 5, 6, 7, 8, 9, 10}

"""# P set
A set which contains 6 periods in a session of a day (morning or afternoon), each period lasts 60 min
"""

P_set = {1, 2, 3, 4, 5, 6, 7}

"""# Create variable"""

v_dpgcr = []
for d in D_set:
    for p in P_set:
        for g in G_set:
            for c in C_set:
                for r in R_all:
                    v_dpgcr.append((d, p, g, c, r))

"""# Clean Variable Data

## Xóa các bộ mã lớp không đúng với nhóm lớp
"""

temp = []
for var in v_dpgcr:
    if var[3] in Cg_set[var[2]]:
        temp.append(var)

v_dpgcr = temp
"""## Xóa các bộ không đảm bảo về sức chứa của phòng """

temp = []
for var in v_dpgcr:
    if classroom.get_classroom_capacity(var[4]) == Rg_set[var[2]]:
        temp.append(var)
    continue
v_dpgcr = temp

"""## Lọc ra các mã lớp có khối lượng = 0, khối lượng = 1, khối lượng lớn hơn 1"""

no_periods_course = []
one_periods_course = []
temp = []
for var in v_dpgcr:
    if int(information.get_class_periods_number(var[3])) == 0:
        no_periods_course.append(var)
    elif int(information.get_class_periods_number(var[3])) == 1:
        one_periods_course.append(var)
    else:
        temp.append(var)

v_dpgcr = temp

"""## Tạo ra danh sách chứa các danh sách con, mỗi danh sách con gồm 2 bộ gồm tiết đầu và tiết của của mỗi mã lớp trong một phòng"""

available_to_sort = []
for key1 in v_dpgcr:
    for key2 in v_dpgcr:
        if key1[0] == key2[0] and key1[2] == key2[2] and key1[3] == key2[3] and key1[4] == key2[4]:
            periods_length = key2[1] - key1[1]
            if periods_length == int(information.get_class_periods_number(key1[3])):
                available_to_sort.append([key1, key2])

""" Tạo ra dictionary với key là phòng học, value1 là các phương án chấp nhận được của mã lớp 
học tại phòng đó, value2 là số tiết của mã lớp đó"""
class_dict = {}
for available_course in available_to_sort:
    class_dict[available_course[1][3]] = {f"classes": [], "periods:": information.get_class_periods_number(available_course[0][3])} 

for available_set in available_to_sort:
    for course_code in information.get_class_code():
        if available_set[0][3] == course_code:
            class_dict[course_code]["classes"].append({"class": available_set, "session": (available_set[0][1], available_set[1][1])})
            

'''Tạo ra các bộ tiết học có thể đối với một buổi học'''

session_list = []
for available_sess in available_to_sort:
    session_list.append((available_sess[0][1], available_sess[1][1]))

unique_session_list = []
for sess in session_list:
    if sess not in unique_session_list:
        unique_session_list.append(sess)
        
session_list = unique_session_list

session_set = []
for n in range(1, 4):
   session_set += list(itertools.permutations(session_list, n))

for i in range(8):
   for check_session in session_set:
       if len(check_session) == 1:
           pass
       elif len(check_session) == 2:
           for i in range(8):
               if check_session[0][1] - check_session[0][0] + check_session[1][1] - check_session[1][0] > 6:
                   session_set.remove(check_session)
               break
       elif len(check_session) == 3:
           for i in range(8):
               if check_session[0][1] - check_session[0][0] + check_session[1][1] - check_session[1][0] + check_session[2][1] - check_session[2][0] > 6: 
                   session_set.remove(check_session)
               break
for i in range(8):
   for check_session in session_set:
       if len(check_session) == 1:
           pass
       elif len(check_session) == 2:
           for i in range(8):
               if check_session[0][0] >= check_session[1][0]:
                   session_set.remove(check_session)
               break
       elif len(check_session) == 3:
           for i in range(8):
               if check_session[0][0] >= check_session[1][0] or check_session[0][0] >= check_session[2][0] or check_session[1][0] >= check_session[2][0]:
                   session_set.remove(check_session)
               break
for i in range(8):
    for check_different in session_set:
        if len(check_different) == 1:
            pass
        elif len(check_different) == 2:
            for i in range(8):
                if check_different[0][1] != check_different[1][0]:
                    session_set.remove(check_different)
                break
        elif len(check_different) == 3:
            for i in range(8):
                if check_different[0][1] != check_different[1][0] or check_different[1][1] != check_different[2][0]:
                    session_set.remove(check_different)
                break

for i in range(len(session_set)):
    session_set[i] = set(session_set[i])
    
''' Tạo ra dict với key là phòng học, bên trong là dict con chứa các lớp học ở phòng học đó, dict con có key là 
lớp đó '''
classroom_dict = {}
for room in classroom.get_classroom_list():
    classroom_dict[room] = {"classes": {}, "full": False}

for room in classroom.get_classroom_list():
    for course in class_dict:
        for _class_ in class_dict[course]["classes"]:
            if _class_["class"][0][4] == room:
                classroom_dict[room]["classes"][course] = _class_["class"]

sort_course = {}

def add_course_to_class():
    pass
# expected_timetable = {'Mã lớp': A_set,
#                       'Lớp tham gia': g_set,
#                       'Mã_HP': credit_code_list,
#                       'Tên HP': credit_name_list,
#                       'Thứ': study_day_output,
#                       'BĐ': start_period,
#                       'KT': end_period,
#                       'Kíp': study_half_day_output,
#                       'Sĩ số': class_population_list,
#                       'Phòng': room_output,
#                       'Sức chứa': room_capacity_output
#                       }

# expected_timetable = pd.DataFrame.from_dict(expected_timetable)

# Tính thời gian chạy 
end_time= time()
time = end_time - start_time
