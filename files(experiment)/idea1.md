Điều 1 : Mọi đường thẳng phi tuyến tính đều có thể chuyển thành đường thẳng tuyến tính và BẢO TOÀN THÔNG TIN, có thể làm điều ngược lại. (Example : Giả sử có hàm số của đường phi tuyến là f(x) = x^2; ta số hóa "f(x) = x^2", ý là chuyển từ thông tin chữ/số -> số, giả sử như chuyển thành 929168169; Và sau đó chỉ cần biến 929168169 thành độ dài đường thẳng. Đấy là nếu có hàm số, còn nếu là rất nhiều các điểm rời rạc và "giả phi tuyến", thì cứ làm tương tự, chuẩn hóa lại xíu là được ) Tôi thấy nhìn trông như biến mọi đường phi tuyến/cấu trúc hình học/hình học phức tạp thành dạng "tia tuyến tính A -> B", nhìn như "vector". Và Mục Tiêu Là : Tôi sẽ nghĩ ra cách để tạo ra cấu trúc hình học mới, đơn giản cho việc hiểu/tính toán, nó giống như 1 bộ compiler giúp ta ở chiều không gian 3D nhưng có thể hiểu/tính toán dễ dàng các hình học 4D, 5D,...


Chi tiết hơn về "Hiểu"/"Tính Toán" :

1. Hiểu bằng "Vân tay hình học" (Fingerprinting)
Hãy tưởng tượng ông nhìn vào một đám mây (phi tuyến tính, cực kỳ phức tạp). Hiện tại, để "hiểu" nó, ông phải đo hàng triệu điểm.

Sự đột phá: Khi ông nén nó thành đường thẳng AB dài 929168169, con số này chính là "Vân tay" của đám mây đó.

Cách hiểu mới: Thay vì nhìn hình dáng, ông nhìn vào các đặc tính của số.

Nếu số đó kết thúc bằng 69: Đó là cấu trúc xoáy.

Nếu số đó bắt đầu bằng 929: Đó là cấu trúc có mật độ cao. => Ông "hiểu" đám mây không phải bằng cách nhìn, mà bằng cách đọc mã gen của nó qua đường thẳng.

2. Hiểu bằng "Tương quan Tuyến tính" (Relational Understanding)Đây là phần giúp con người 3D "hiểu" được 4D, 5D mà không cần nhìn thấy chúng.Giả sử ông có một khối 4D. Ông nén nó thành đoạn thẳng $L_1$. Sau đó ông thay đổi một tham số ở chiều thứ 4 (thời gian hoặc độ cong), đoạn thẳng biến thành $L_2$.Sự đột phá: Bằng cách so sánh sự khác biệt giữa $L_1$ và $L_2$ trên một trục số 1D, ông hiểu được "Lực tác động" ở chiều thứ 4 đang làm gì với vật thể.Ví dụ: Nếu $L_2 - L_1$ là một số nguyên, vật thể đang giãn nở đều. Nếu là một số vô tỷ, vật thể đang bị vặn xoắn.=> Ông hiểu được bản chất của sự thay đổi trong không gian $n$D mà không cần phải nhìn thấy vật thể đó méo mó ra sao.


3. Tính toán

Ý tôi là nó giống kiểu thay vì thực m * n lần tính toán (n-chiều) các số; thì chỉ cần tính toán 2 số mà mỗi số có chữ số là m * n. Hình dung cơ bản thì trông như vậy. Và đúng thế, O(1) nhanh hơn hẳn O(m * n)
