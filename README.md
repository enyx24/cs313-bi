# BI
Mục lục:<br>
1. [Requirement](#requirement)<br>
2. [Installation](#installation)<br>
3. [Features](#features)<br>

## Requirement
- python >= 3.12
- Dependencies: requirements.txt
- xampp MySQL hoặc SQL Database khác
- Scripts tiền xử lí data: [enyx24/cs313_data_scripts](https://github.com/enyx24/cs313_data_scripts)
## Installation
- Cài đặt các dependency: `pip install -r requirements.txt`
- Download và import database bằng file `bi.sql` từ [Google Drive](https://drive.google.com/drive/u/2/folders/19lSobnFv2e2DfnhcJtLDuqOdnlaf-ICO?fbclid=IwY2xjawKpVpZleHRuA2FlbQIxMQABHpWDA2qaLinnzGvROhjF0ZiaR0WiCd1uLRZgNw0hej4SN8g9OcvIDPK5R6RT_aem_wWBNdhpHmLbNhoayv2o4pg)
- Tải trước tất cả file data của nhóm cho Dashboard từ [Google Drive](https://drive.google.com/drive/folders/1Ja_wpWpy9Cq5JT419c4KKtpnvKODbDkE), đặt vào cùng thư mục gốc của dự án
- Thay connection string trong file `connectDB.py` <b>nếu không dùng xampp MySQL</b>
- Chạy `python app.py`
- Truy cập tại `localhost:8000`
## Features
  ### Trang chủ
  Giới thiệu cơ bản về
  - Bài toán
  - Mục tiêu
  - Input
  - Output
  - Dataset
  - MOOCCubeX
  - Tiền xử lí
  ### Dashboard
  Kiểm tra chất lượng dữ liệu có sẵn hoặc dữ liệu người dùng cung cấp thông qua datagrid và một số thang đo nhóm đã thực hiện
  ### Mô hình
  Dùng model có sẵn hiện tại
  - Dự đoán dữ liệu 
  - Đánh giá (Accuracy, F1)
  - Retrain model theo dữ liệu hiện tại
  ### Thống kê
  Thống kê dữ liệu hiện tại và dữ liệu giả lập trên hệ thống
  - Phân bố các nhãn dự đoán
  - Tỉ lệ dự đoán
  - Thống kê về khoá học, hoạt động,... thuộc hệ thống
  ### Tìm kiếm
  Tìm kiếm người dùng / khoá học
  - Thông tin cơ bản người dùng / khoá học đang xem
  - Nhãn và tiến độ người dùng hiện tại
  - Phân bố nhãn của người dùng đã đăng kí khoá học
  ### Database
  Giả lập thông tin lấy được từ hệ thống LMS/MOOC (các bảng) và sẽ được ghi vào (bảng user_predict)
  ### Lưu ý
  Thời gian truy vấn phụ thuộc khá nhiều vào DB.
