# Chương trình hỗ trợ lập thời khóa biểu cho nhóm ngành quốc tế trường Đại học Bách Khoa Hà Nội

## Các thư viện sử dụng trong chương trình
- os: lấy và lưu trữ đường dẫn tới file Excel 
- pandas: Đọc và xử lý dữ liệu từ file Excel
- numpy: Thực hiện một số phép toán 
- itertools: Lấy hoán vị
- functools: 
- time: Tính thời gian chạy 
- random:
## Object Classroom
Lấy các dữ liệu cần thiết liên quan tới phòng học 
- get_table(): in ra màn hình dữ liệu về lớp học 
- get_classroom_list(): lấy danh sách các phòng học 
- get_classroom_capacity(classroom_name): lấy sức chứa của phòng học 
## Object ClassInfomation 
Lấy các thông tin cần thiết cho mô hình 
- get_table: in ra màn hình toàn bộ thông tin 
- get_student_number(class_code): trả về số sinh viên từng mã lớp 
- get_class_periods_number(class_code): trả về số tiết học của mã lớp 
- get_participant_class(class_code): trả về tên của các lớp con tham gia mã lớp 
- get_class_code(): lấy danh sách mã lớp trong kỳ 
- get_class_code_each_class_group(class_group): lấy mã lớp của nhóm lớp 
- get_class_group_student_number(class_group): trả về sĩ số của nhóm lớp đó 

## Tập G_set 
Tập hợp chứa tất cả các nhóm lớp 
![image](https://user-images.githubusercontent.com/93395558/174724666-4c764629-cfcb-489b-89b3-1c7175b45925.png)

### Tập G_big_set
Tập chứa các nhóm lớp có ít nhất hai lớp con từ tập G_set
![image](https://user-images.githubusercontent.com/93395558/174724933-fe5ca561-1fc8-4751-b45f-3c36613b4478.png)
### Tập G_small_set
Tập chứa các nhóm lớp có ít hơn hai lớp con từ tập G_set
![image](https://user-images.githubusercontent.com/93395558/174725014-d25be0fd-4316-4458-8f5c-b55a73512715.png)

### Tập G_in_set
Tập với key là lớp con, value là lớp ghép mà lớp con đó thuộc vào 
![image](https://user-images.githubusercontent.com/93395558/174874854-0d934b71-d428-4dd9-9847-9228562ee1a6.png)

## Tập C_set
Tập hợp chứa tất cả các lớp mở trong kỳ cùng với tên học phần 
![image](https://user-images.githubusercontent.com/93395558/174725178-11104224-42b5-49f3-95b5-938e0121d931.png)

## Tập R_all
Tập hợp chứa tất cả các phòng học có thể sử dụng 
![image](https://user-images.githubusercontent.com/93395558/174725283-e66b02a4-b4dd-4bfa-b820-b5899413a869.png)

## Tập R_set
Tập hợp các phòng học được nhóm lại theo sức chứa 
![image](https://user-images.githubusercontent.com/93395558/174725377-b8df9909-a2ff-4f8e-9432-0fc7ac3e9686.png)

## Tập Rg_set
Tập hợp chứa các nhóm lớp đi cùng với sức chứa của phòng phù hợp với nhóm lớp đó
![image](https://user-images.githubusercontent.com/93395558/174725497-4c585330-f4c3-47ac-888a-fe27be5edeee.png)

## Tập Cg_set
Tập chứa các nhóm lớp đi cùng với các mã lớp mà nhóm đó sẽ học trong kỳ 
![image](https://user-images.githubusercontent.com/93395558/174725644-3877b20e-d003-4e7c-a8f7-781ffe74a35f.png)

## Tập Cg_big_set 
Tập chứa các nhóm lớp đi cùng với mã lớp mà nhóm lớp đó sẽ học trong kỳ (số lượng mã lớp lớn hơn hoặc bằng 2)
![image](https://user-images.githubusercontent.com/93395558/174736056-95b1ca26-b0d9-47c4-b217-43c5e3286837.png)

## Tập Cg_small_set 
Tập chứa các nhóm lớp đi cùng với mã lớp mà nhóm lớp đó sẽ học trong kỳ (số lượng mã lớp nhỏ hơn 2)
![image](https://user-images.githubusercontent.com/93395558/174736097-104114e4-fe3e-4bfa-9e0a-c47b48cca549.png)

## Bộ các tiết học có thể với một buổi học là session_set 
![image](https://user-images.githubusercontent.com/93395558/174736405-a6202e1d-b390-4a1e-963b-bb94edf7afa8.png)

## Dictionary classroom_dict với key là tên phòng học 
![image](https://user-images.githubusercontent.com/93395558/174736675-bd8f11f6-3abd-4740-893f-86b6417c59d3.png)
### Mỗi phòng học có 2 key là "classes" và "slots"
![image](https://user-images.githubusercontent.com/93395558/174736846-02eb71fb-0811-4b1f-9558-f9ade4721197.png)
#### Trong đó key "classes" chứa tất cả các mã lớp sẽ học tại phòng đó
![image](https://user-images.githubusercontent.com/93395558/174736946-2212959f-a3a0-43c7-8f2b-d385150d7927.png)
- Bên trong mỗi mã lớp học tại phòng đó, là các phương án chấp nhận được có thể sắp xếp vào thời khóa biểu, gồm tiết bắt đầu và tiết kết thúc của mã lớp đó, tiếp đó 'session' là tuple lưu trữ tiếp bắt đầu và tiết kết thúc của phương án đó, sử dụng để so sánh với tập session_set
![image](https://user-images.githubusercontent.com/93395558/174744385-8c3d38e4-85ed-4608-8c07-81da7335d40d.png)
![image](https://user-images.githubusercontent.com/93395558/174737348-441aa760-a419-4aba-b887-2ba15da56736.png)
#### Còn key "slots" sẽ bao gồm hai tập hợp "used_by" là những phòng học sẽ học tại phòng đó vào buổi có thứ tự đó sau khi sắp xếp 'session set' là tập hợp các tiết học của các lớp được sắp xếp, để so sánh với tập "session_set" 
![image](https://user-images.githubusercontent.com/93395558/174737750-52ad1730-1514-493d-b702-2d58fdde8ece.png)

## Thuật toán dự định để giải bài toán
_Thuật toán được thực hiện trên tập classroom_dict_
1. Xét các nhóm phòng học theo sức chứa.
2. Lấy ra các mã lớp sẽ sử dụng nhóm phòng học đó. (Do trước đó đã có tập các phòng học cùng sức chứa, và đã sắp xếp các mã lớp theo phòng học có sức chứa phù hợp, nên hiện tại những lớp đó có chung nhóm phòng học)
3. Chọn ngẫu nhiên 2 mã lớp từ tập các mã lớp.
-  Nếu chỉ còn một lớp chưa xếp thì xếp ngay lớp đó vào phòng trống tiếp theo xét.
-  Nếu tổng số tiết của các mã lớp <= 4 thì chọn thêm một mã lớp nữa (nếu còn mã lớp chứa xếp) sao cho tổng số tiết của các mã lớp == 6 (do số tiết ít nhất là 2 và nhiều nhất là 4).
5. Sắp xếp các mã lớp 
-  Xếp các mã lớp đã chọn vào 'used_by' ứng với từng buổi của một phòng, song song với việc thêm vào 'session set' của buổi đó.
-  Mỗi khi thêm một phòng cũng như thêm vào 'session set' thì sẽ kiểm tra 'session set' nếu nằm trong tập session_set thì buổi đó của lớp đó được xếp xong. Nếu không thể xếp 'session set' thỏa mã thì quay lại chọn bộ khác.
-  Nếu xếp được thì xóa các lớp đó khỏi danh sách lớp cần xếp, chọn một bộ các mã lớp khác với danh sách lớp sau khi xóa, tiếp tục thực hiện các bước trên với các buổi còn lại của phòng đó.
-  Đến khi tất cả các buổi của phòng học đó đã đầy (một phòng được xét là đầy nếu như 'session set' mỗi buổi của phòng đó nằm trong tập "session_set") thì ta sẽ xóa phòng đó khỏi danh sách phòng trống.
-  Khi một phòng đầy thì chuyển sang phòng tiếp theo trong nhóm phòng học có cùng sức chứa với phòng đó.
-  Nếu như khi xếp hết các buổi của tất cả các phòng trong nhóm phòng học đó mà vẫn còn lớp chưa được xếp thì lớp đó sẽ được lưu vào một danh sách khác để sử dụng một nhóm phòng khác còn trống.
6. Sau khi đã xếp hết lớp ứng với một nhóm phòng mà nhóm phòng đó vẫn còn thừa chỗ thì những phòng còn chỗ sẽ được lưu vào một danh sách khác.
7. Xếp những lớp chưa được xếp vào các phòng còn chỗ trống và phù hợp về sức chứa cũng như sĩ số lớp đó.
8. Kiểm tra xem các mã lớp con có trùng tiết với các mã lớp ghép hay không, nếu có thì sẽ sắp xếp lại các phòng học và mã lớp đó (hoặc sắp xếp lại toàn bộ).
**Em sẽ suy nghĩ việc kiểm tra trùng mã lớp con và mã lớp ghép sau ạ, trước mắt thì em muốn xếp được đã rồi mới tính tới**

## Những vấn đề chưa giải quyết được của bài toán 
1. Do dữ liệu đầu vào thì số lượng lớp chưa nhiều, nên phòng học vẫn đủ để xếp, tuy vậy với số lượng lớp lớn hơn, cần bổ sung việc xét những lớp chưa được xếp do thiếu phòng.
2. Chưa giải quyết được sự trùng lặp tiết của lớp ghép và lớp đơn.
3. Các hàm được viết vẫn có điểm yếu, cần kiểm tra và cải thiện lại 
