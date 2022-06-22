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

"""# G_in_set 
Tập hợp có key là lớp đơn, value là lớp ghép mà lớp đơn đó thuộc vào 
"""
G_in_set = {}
for g in G_small_set:
    for g_big in G_big_set:
        if G_small_set[g][0] in G_big_set[g_big]:
            G_in_set[G_small_set[g][0]] = G_big_set[g_big]
"""# C set
An available set which contains all the courses in the semester
"""


# Tập C chứa tất cả các lớp mở trong kỳ
def C_set():
    course_dict = {}
    for class_code in information.get_class_code():
        course_dict[class_code] = {"Sub": information_df.loc[information.get_class_code().index(class_code), 'TÊN HP'], "course_code": information_df.loc[information.get_class_code().index(class_code), 'MÃ HP']}
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


# Tập Cg chứa các nhóm lớp, đi cùng với các mã lớp mà nhóm lớp đó sẽ học trong kỳ
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
            Cg_big_dict.update({key: Cg_set[key]})
    return Cg_big_dict


# Tập Cg_small chứa các nhóm lớp đi cùng với mã lớp mà nhóm lớp đó sẽ học trong kỳ (số lượng mã lớp nhỏ hơn 2)
def Cg_small_set(Cg_set):
    Cg_small_dict = {}
    for key in Cg_set:
        if len(Cg_set[key]) < 2:
            Cg_small_dict.update({key: Cg_set[key]})
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
    class_dict[available_course[1][3]] = {f"classes": [], "periods": int(information.get_class_periods_number(available_course[0][3]))} 

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
''' Tập session_set chứa tất cả các bộ tiết học trên một buổi học có thể xảy ra'''
# Lấy các hoán vị của bộ các tiết học của mỗi mã lớp có thể học 
session_set = []
for n in range(1, 4):
   session_set += list(itertools.permutations(session_list, n))
# Nếu như tổng số tiết của bộ các tiết đó lớn hơn sau thì loại bộ đó 
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
# Nếu tiết đầu tiên của tiết sau nhỏ hơn hoặc bằng tiết đầu tiên của tiết trước thì loại bộ đó 
for i in range(8):
   for check_session in session_set:
       if len(check_session) == 1:
           pass
       elif len(check_session) == 2:
           for i in range(8):
               if check_session[0][0] > check_session[1][0]:
                   session_set.remove(check_session)
               break
       elif len(check_session) == 3:
           for i in range(8):
               if check_session[0][0] > check_session[1][0] or check_session[0][0] > check_session[2][0] or check_session[1][0] >= check_session[2][0]:
                   session_set.remove(check_session)
               break
# Nếu tiết đầu tiên của tiết sau nhỏ hơn tiết cuối cùng của tiết trước thì loại bộ đó 
for i in range(8):
    for check_different in session_set:
        if len(check_different) == 1:
            pass
        elif len(check_different) == 2:
            for i in range(8):
                if check_different[0][1] > check_different[1][0]:
                    session_set.remove(check_different)
                break
        elif len(check_different) == 3:
            for i in range(8):
                if check_different[0][1] > check_different[1][0] or check_different[1][1] > check_different[2][0]:
                    session_set.remove(check_different)
                break
# Nếu bộ 2 tiết nằm trong bộ 3 tiết thì loại bộ 2 tiết đó 
for i in range(4):
    for check_distance in session_set:
        if len(check_distance) == 2:
            if check_distance[0] in session_set[-1] and check_distance[1] in session_set[-1]:
                session_set.remove(check_distance)
                break
# Chuyển thành list
for i in range(len(session_set)):
    session_set[i] = list(session_set[i])
# Loại bỏ các bộ chỉ có một phần tử (do số tiết nhỏ hơn hoặc bằng 4 nên một buổi sẽ luôn ít nhất có 2 tiết)
session_length_1 = []
for i in range(4):
    for session_i in session_set:
        if len(session_i) == 1:
            session_length_1.append(session_i)
            session_set.remove(session_i)
            
session_temp = {2: [], 3: [], 4: [], 5: [], 6: []}
for session_length in range(4, 7):
    for session in session_set:
        if session[1][1] - session[1][0] + session[0][1] - session[0][0] == session_length:
            session_temp[session_length].append(session)
            
for session_length in range(1, 4):
    for session in session_length_1:
        if session[0][1] - session[0][0] == session_length:
            session_temp[session_length].append(session)
            
session_set = session_temp
''' Tạo ra dict với key là phòng học, bên trong là dict con chứa các lớp học ở phòng học đó, số tiết 
mỗi buổi mà phòng đó có thể xếp và phòng học đó đã xếp đủ chỗ hay chưa'''
classroom_slots = {}
for room in classroom.get_classroom_list():
    classroom_slots[room] = {1: {"used_by": [], "session set": []}, 2: {"used_by": [], "session set": []}, 3: {"used_by": [], "session set": []}, 4: {"used_by": [], "session set": []}, 5: {"used_by": [], "session set": []}, 6: {"used_by": [], "session set": []}, 7: {"used_by": [], "session set": []}, 8: {"used_by": [], "session set": []}, 9: {"used_by": [], "session set": []}, 10: {"used_by": [], "session set": []}}

classroom_dict = {}
for room in classroom.get_classroom_list():
    classroom_dict[room] = {"classes": {}, "slots": classroom_slots[room]}

for room in classroom.get_classroom_list():
    for course in class_dict:
        for _class_ in class_dict[course]["classes"]:
            if _class_["class"][0][4] == room:
                classroom_dict[room]["classes"][course] = []

for room in classroom.get_classroom_list():
    for course in class_dict:
        for _class_ in class_dict[course]["classes"]:
            if _class_["class"][0][4] == room:
                classroom_dict[room]["classes"][course].append(_class_)

""" 
1. Xét các nhóm phòng học theo sức chứa.
2. Lấy ra các mã lớp sẽ sử dụng nhóm phòng học đó. (Do trước đó đã có tập các phòng học cùng sức chứa, và đã sắp xếp các mã lớp theo phòng học có sức chứa phù hợp, nên hiện tại những lớp đó có chung nhóm phòng học)
3. Chọn ngẫu nhiên 2 mã lớp từ tập các mã lớp.
-  Nếu tổng số tiết của các mã lớp <= 4 thì chọn thêm một mã lớp nữa sao cho tổng số tiết của các mã lớp == 6 (do số tiết ít nhất là 2 và nhiều nhất là 4)
4. Sắp xếp các mã lớp 
-  Xếp các mã lớp đã chọn vào 'used_by' ứng với từng buổi của một phòng, song song với việc thêm vào 'session set' của buổi đó.
-  Mỗi khi thêm một phòng cũng như thêm vào 'session set' thì sẽ kiểm tra 'session set' nếu nằm trong tập session_set thì buổi đó của lớp đó được xếp xong. Nếu không thể xếp 'session set' thỏa mã thì quay lại chọn bộ khác.
-  Nếu xếp được thì xóa các lớp đó khỏi danh sách lớp cần xếp, chọn một bộ các mã lớp khác với danh sách lớp sau khi xóa, tiếp tục thực hiện các bước trên với các buổi còn lại của phòng đó.
-  Đến khi tất cả các buổi của phòng học đó đã đầy (một phòng được xét là đầy nếu như 'session set' mỗi buổi của phòng đó nằm trong tập "session_set") thì ta sẽ xóa phòng đó khỏi danh sách phòng trống.
-  Khi một phòng đầy thì chuyển sang phòng tiếp theo trong nhóm phòng học có cùng sức chứa với phòng đó.
-  Nếu như khi xếp hết các buổi của tất cả các phòng trong nhóm phòng học đó mà vẫn còn lớp chưa được xếp thì lớp đó sẽ được lưu vào một danh sách khác để sử dụng một nhóm phòng khác còn trống.
5. Sau khi đã xếp hết lớp ứng với một nhóm phòng mà nhóm phòng đó vẫn còn thừa chỗ thì những phòng còn chỗ sẽ được lưu vào một danh sách khác.
6. Xếp những lớp chưa được xếp vào các phòng còn chỗ trống và phù hợp về sức chứa cũng như sĩ số lớp đó.
7. Kiểm tra xem các mã lớp con có trùng tiết với các mã lớp ghép hay không, nếu có thì sẽ sắp xếp lại các phòng học và mã lớp đó (hoặc sắp xếp lại toàn bộ).
"""
       
# Danh sách các phòng đã được xếp đầy chỗ 
used_room = []
course_sorted = []
# Lấy ra nhóm phòng cùng cỡ và nhóm lớp học các phòng đó 
def get_room_set(capacity):
    room_set = R_set[capacity]
    return room_set

# Kiểm tra xem phòng học đó còn chỗ hay không 
def get_course_take_part_in(room_set):
    course_take_part_in = []
    for _course_ in classroom_dict[room_set[0]]["classes"].keys():
        course_take_part_in.append(_course_)
    return course_take_part_in

# Chọn ra phòng có thể sử dụng trong nhóm phòng đã chọn
def room_can_use(room_set):
    for room in room_set:
        available_session = []
        for i in range(1, 11):
            if len(classroom_dict[room]["slots"][i]["session set"]) == 0:
                available_session.append(i)
        if len(available_session) > 0:
            return room
# Kiểm tra xem phòng đó còn buổi trống hay không 
def room_available_session(room):
    available_session = []
    for i in range(1, 11):
        if len(classroom_dict[room]["slots"][i]["session set"]) == 0:
            available_session.append(i)
    return available_session
# Chọn các mã lớp sẽ xếp vào thời khóa biểu
def get_course_to_sort(course_take_part_in):
    if len(course_take_part_in) >= 2:
        course_to_sort = random.sample(course_take_part_in, 2)
    elif len(course_take_part_in) == 1:
        course_to_sort = course_take_part_in
    return course_to_sort

# Chia mã lớp thành các nhóm 2-3 lớp con thỏa mãn số lượng tiết trong một buổi
def choose_sort_day(room):
    for i in range(1, 11):
        if len(classroom_dict[room]["slots"][i]["session set"]) == 0:
            return i

# Chọn session từ session_set theo số lượng các mã lớp tham gia 
def choose_session_set_for_course(course_to_sort, course_take_part_in):
    periods_chosen_course = []
    for course in course_to_sort:
        periods_chosen_course.append(class_dict[course]["periods"])
    while sum(periods_chosen_course) > 6:
        periods_chosen_course = []
        course_to_sort = random.sample(course_take_part_in, 2)
        for course in course_to_sort:
            periods_chosen_course.append(class_dict[course]["periods"])
    session_set_chosen = random.choice(session_set[sum(periods_chosen_course)])
    return session_set_chosen

# Kiểm tra xem lớp con có bị trùng tiết với lớp ghép hay không
def check_small_group_in_big_group():
    pass

# Xếp các mã lớp vào phòng 
def add_course_to_room(room, course_to_sort, chosen_session, session_set_chosen):
    classroom_dict[room]["slots"][chosen_session]["used_by"] = course_to_sort
    classroom_dict[room]["slots"][chosen_session]["session set"] = session_set_chosen 
    
# Kiểm tra xem đã hết phòng sử dụng hay chưa 
# def out_of_room(used_room, room_set):
#     return used_room == len(room_set)

''' Xếp thời khóa biểu'''
# Xếp thời khóa biểu cho từng nhóm phòng theo sức chứa
def sort_class_to_room_set(capacity):
    room_set = get_room_set(capacity)
    course_take_part_in = get_course_take_part_in(room_set)
    while len(course_take_part_in) != 0 and len(room_set) != 0:
        room = room_can_use(room_set)
        course_to_sort = get_course_to_sort(course_take_part_in)
        sort_session = choose_sort_day(room)
        session_set_chosen = choose_session_set_for_course(course_to_sort, course_take_part_in)
        add_course_to_room(room, course_to_sort, sort_session, session_set_chosen)
        course_sorted.append(course_to_sort)
        if len(course_take_part_in) <= 1:
            break
        if len(course_take_part_in) > 1:
            course_take_part_in.remove(course_to_sort[0])
            course_take_part_in.remove(course_to_sort[1])
        if room_available_session(room) == 0:
            used_room.append(room)
            room_set.remove(room)

for capacity in classroom_capacity:
    sort_class_to_room_set(capacity)

sorted_course = []

def reemovNestings(l):
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            sorted_course.append(i)

reemovNestings(course_sorted)
"""Xử lý đầu ra"""
# Lấy phòng lớp đó học 
def get_classroom_used(class_code):
    for room in classroom_dict:
    	for i in range(1, 11):
    		if class_code in classroom_dict[room]["slots"][i]["used_by"]:
    			return room 

# Lấy ngày lớp đó học 
def get_learning_day(class_code):
    for room in classroom_dict:
        for day in range(1, 11):
            if class_code in classroom_dict[room]["slots"][day]["used_by"]:
                study_day = day
    if study_day in (1, 2):
        return 2
    if study_day in (3, 4):
        return 3
    if study_day in (5, 6):
        return 4
    if study_day in (7, 8):
        return 5
    if study_day in (9, 10):
        return 6

# Lấy kíp lớp đó học 
def get_learning_day_part(class_code):
    for room in classroom_dict:
        for day in range(1, 11):
            if class_code in classroom_dict[room]["slots"][day]["used_by"]:
                study_day = day
    if study_day in (1, 3, 5, 7, 9):
        return "Sáng"
    else: 
        return "Chiều"
    
# Lấy tiết học bắt đầu và kết thúc của mã lớp trong buổi đó
def get_start_period(class_code):
    for room in classroom_dict:
        for day in range(1, 11):
            if class_code in classroom_dict[room]["slots"][day]["used_by"]:
                class_index = classroom_dict[room]["slots"][day]["used_by"].index(class_code)
                start_period = classroom_dict[room]["slots"][day]["session set"][class_index][0]       
    return start_period

def get_end_period(class_code):
    for room in classroom_dict:
        for day in range(1, 11):
            if class_code in classroom_dict[room]["slots"][day]["used_by"]:
                class_index = classroom_dict[room]["slots"][day]["used_by"].index(class_code)
                end_period = classroom_dict[room]["slots"][day]["session set"][class_index][1]       
    return end_period

data = {}
for class_code in sorted_course:
    data[class_code] = [class_code, information.get_class_group(class_code), C_set[class_code]["course_code"], C_set[class_code]["Sub"], get_learning_day(class_code), get_learning_day_part(class_code), information.get_student_number(class_code), get_classroom_used(class_code), classroom.get_classroom_capacity(get_classroom_used(class_code))]

expected_timetable = pd.DataFrame.from_dict(data, orient='index', columns=["Mã lớp", "Lớp tham gia", "Mã HP", "Tên HP", "Thứ", "Kíp", "Sĩ số", "Phòng", "Sức chứa"])

# Tính thời gian chạy 
end_time= time()
time = end_time - start_time
