first = '''An
Anh
Bình
Chiêm
Chiến
Chinh
Cúc
Cương
Dũng
Duy
Duyên
Đạt
Đồng
Hà
Hà
Hạnh
Hằng
Hằng
Hân
Hiền
Hoa
Hòa
Họa
Hoàng
Hợp
Hùng
Huyền
Hưng
Hưng
Hương
Kha
Khải
Khanh
Kiệt
Linh
Lượng
Nga
Nghiệp
Ngọc
Nguyên
Nhài
Nhân
Nhơn
Oanh
Quy
Quyền
Quỳnh
Quỳnh
Sương
Thanh
Thắng
Thi
Thìn
Thoa
Thông
Thu
Thuỷ
Thủy
Toàn
Trang
Trang
Trang
Tuấn
Tuấn
Tùng
Xuân
Yên
Minh
Thủy
Sơn
Khánh
KHÁNH
Anh
Hạnh
Hà
Tuyết
Hương
Trang
Trung
Hải Yến
Thảo'''

last = '''Mai Xuân
Đinh Thị Hoàng
Nguyễn Thế Vũ
Nguyễn Thị Minh
Vũ Văn
Nguyễn Duy
Tạ Thị Hồng
Trần Hữu
Cao Vũ
Trần Nguyễn Bảo
Đào Thị Thanh
Bùi Doãn
Phan Tấn
Ngô Văn
Thân Thị
Nguyễn Thị Mỹ
Đỗ Thị
Trương Vĩnh Thị Lê
Hoàng Vũ Bảo
Vũ Văn
Phan Thị Kiều
Vũ Khánh
Hà Thị
Phạm Quốc
Vi Thị
Lê Anh
Ngô Thị Thu
Kiểu Quốc
Phạm Tuấn
Nguyễn Thị
Bùi Lê
Nguyễn Tiến
Võ Kim
Trần Anh
Đoàn Diệp
Nguyễn Hữu
Nguyễn Quỳnh
Liễu Thị
Nguyễn Như
Lê Thị Thảo
Nguyên Thị
Phan Hữu
Âu Vĩ
Trương Thị Kim
Nguyễn Văn
Lê Ngọc
Nguyễn Thị Trúc
Nguyễn Thị
Nguyễn Thị Hồng
Trương Thị
Phạm Minh
Nguyễn Hoàng
Nguyễn Mạnh
Nguyễn Thị
Nguyễn Đức
Phạm Thị
Nguyễn Thị
Trần Thị Thanh
Nguyễn Anh
Đỗ Nguyễn Thảo
Nguyễn Thuỳ
Nguyễn Thuỳ
Đinh Văn
Nguyễn Văn
Trần Duy
Lý Thị Thanh
Nguyễn Thị
Nguyễn thiên
Vũ Thị Thu
Trịnh thế
Nguyễn Quốc
NGUYỄN VĂN
Ngô Thị Thái
Lê Mỹ
Mai Thị Ngọc
Thôi Thị Ánh
Vương Thị Thu
Trịnh Thị
Vũ Văn
Trịnh Thị
Lại Thị'''


first = first.split('\n')
last = last.split('\n')
for i in range(len(first)):
    print(f'{i+1}. {last[i] + ' ' + first[i]}')