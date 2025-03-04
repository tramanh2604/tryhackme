# Window Command Line
# 1. Basic System Information
- Ban hành lệnh: issue the command.
- `set`: check your path. Kết quả bắt đầu bằng `Path=`
```
C:\>set
ALLUSERSPROFILE=C:\ProgramData
[...]
LOGNAME=strategos
NUMBER_OF_PROCESSORS=2
OS=Windows_NT
Path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Windows\system32\config\systemprofile\AppData\Local\Microsoft\WindowsApps;C:\Users\strategos\AppData\Local\Microsoft\WindowsApps;
[...]
```

- `ver`: xem version của OS.
```
C:\>ver                                        
Microsoft Windows [Version 10.0.17763.1821]
```

- `systeminfo`: in ra 1 list các thông tin về OS.
```
C:\>systeminfo

Host Name:                 WIN-SRV-2019
OS Name:                   Microsoft Windows Server 2019 Datacenter
OS Version:                10.0.17763 N/A Build 17763
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
[...]
```

- Nếu kết quả đầu ra quá dài, dùng lệnh `| more`, bạn có thể xem page một cách lần lượt. Thoát chế độ dùng **CTRL + C**.

- `help`: cung cấp thông tin về command.
- `cls`: clear the command prompt screen.

# 2. Network Troubleshooting
- CLI cung cấp rất nhiều lệnh để tra cứu cấu hình hiện tại, kiểm tra kết nối và troubleshoot networking issue.

## 2.1 Network Configuration
- `ipconfig`: check your network information. The termianl output show our IP address, subnet mask, default gateway.
```
C:\>ipconfig

Windows IP Configuration

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . : eu-west-1.compute.internal
   Link-local IPv6 Address . . . . . : fe80::90df:4861:ba40:f2a8%4
   IPv4 Address. . . . . . . . . . . : 10.10.230.237
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : 10.10.0.1
```

- `ipconfig /all`: để xem thêm thông tin cấu hình network, ví dụ như DNS server and DHCP.

![ipconfig /all](/images/ipconfig-all.PNG)

## 2.2 Network Troubleshooting
- Một tác vụ giúp khắc phục sự cố phổ biến là kiểm tra server có đang truy cập vào server nào trên Internet không. Dùng lệnh `ping <target_name>`. 
- Ta sẽ gửi các gói tin ICMP và listen to a respone. Nếu nhận đc respone, we know that we can reach the target and the target can reach us.
- Trong ảnh, ta đang ping đến example.com. Và nhận đc 4 reply thành công và 1 vài tính toán như tg trung bình (the average trip time) là 78 miliseconds.

![ping](/images/ping.PNG)

- Công phụ phổ biến khác là `tracert <target_name>` theo dõi tuyến đường mạng đã đi qua để tiếp cận target. Nó mong đợi mỗi router trên đường đi sẽ báo cho chúng ta nếu nó drop a packet vì time-to-live (TTL) đạt đến 0. 
- Ví dụ: terminal thông báo ta đi qua 15 router trc khi reach our target.

![tracert](/images/tracert.PNG)

## 2.3 More Networking Commands
- `nslookup`: tra cứu host hoặc domain rồi trả về đchi IP. 
   + `nslookup example.com`: dùng name server mặc định.
   + `nslookup example.com 1.1.1.1`: dùng name server **one.one.one.one**
   => Kết quả trả về là giống nhau nhưng lấy từ các name server khác nhau.

![nslookup](/images/nslookup.PNG)


- `netstat`: display current network and listening ports. Lệnh netstat k có đối số (argument) sẽ show các kết nối đã đc thiết lặp. 
   + Trong ảnh cho ta biết 1 kết nối SSH, vì SSH nằm trên port 22.

![netstat](/images/netstat.PNG)

   + Các argument và mục đích:
      + `netstat -h`: help pages.
      + `-a`: xem tất cả các kết nối và port
      + `-b`: hiển thị ctrinh liên kết vs từng cổng nghe và kết nối đc thiết lặp
      + `-o`: tiết lộ process ID (PID) liên kết vs connection.
      + `-n`: sdung biểu mẫu số cho đchi và port number.
      + Ta có thể kết hợp cả 4 argument và chạy lệnh `netstat -abon`. 

![netstat](/images/netstat2.PNG)

   + sshd.exe chịu trách nhiệm lắng nghe các kết nối trên port 22, và các PID liên kết vs kết nối.

# 3. File and Disk Management
## 3.1 Working with Directory
- `cd`: display the current drive and directory, giống pwd trong linux.
- `dir`: xem các directory con.
   + `dir /a`: xem các hidden file và các system file.
   + `dir /s`: xem các file trong dir hiện tại và tất cả các subdirectories.
- `tree`: xem các dir và dir con dưới dạng tổ chức cây.
- `cd <target_directory>`: đi đến dir, giống nhấp đúp vào **target_directory** trên máy tính. Hoặc dùng `cd ..` để quay về 1 cấp.
- `mkdir <directory_name>`: tạo thư mục.
- `rmdir <directory_name>`: xóa thư mục.

## 3.2 Working with files
- `type`: xem nội dung file ngắn.
- `more`: xem nội dung file dài, nó sẽ chỉ hiện thị nội dung vừa đủ độ dài terminal và chờ bạn nhấn **Spacebar** để đọc tiếp.
- `copy text.txt text2.txt`: copy file từ nơi này qua nơi khác.
- `move`: di chuyển file khỏi thư mục.
- `del` hoặc `erase`: xóa file.
- Có thể dùng * để đại diện cho nhiều file. Ví dụ `cop *.md C:\Markdown` sẽ copy tất cả file có phần mở rộng là **md** sang thư mục C:\Markdown.

# 4. Task and Process Management
- `tasklist`: list the running process.

![tasklist](/images/tasklist.PNG)

- `tasklist /?`: check the filtering for the long output. 
   + Ví dụ muốn tìm kiếm task liên quan đến **sshd.exe**, dùng lệnh `tasklist /FI "imagename eq sshd.exe"`. **/FI**
   dùng để set the filter *image name equals* **sshd.exe**.

![tasklist](/images/tasklist1.PNG)

- Với process ID (PID), bạn có thể dừng bất kì task nào bằng lệnh `taskkill /PID target_pid`. Ví dụ, nếu bạn muốn dừng (kill) process có PID là 4567, issue the command `taskkill /PID 4567`.

# 5. Conclusion
- `chkdsk`: check the file system and disk volumes for errors and bad sectors.
- `driverquery`: displays a list of installed device drivers.
- `sfc /scannow`: scan file system for corruption and repair them if possible.
- `shutdown /s`: shut down a system.
- `shutdown /r`: restart a system.
