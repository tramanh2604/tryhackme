# Linux Shells
# 1. How to interact with a Shell?
- Shell mặc định là Bash.
- Khi tương tác vs shell, bạn phải ở trong dir nơi bạn muốn thực hiện các hành động. 
- `pwd`: để xem thư mục đang làm việc
- `cd`: change dir
- `ls`: xem nội dung dir
- `cat file.txt`: xem nội dung file
- `grep`: search for any word of pattern inside of file.

# 2. Type of Linux Shells
- `echo $SHELL`: xem loại shell đang dùng trên Linux.
- `cat /etc/shells`để xem danh sách shell có sẵn trên Linux. File **/etc.shells** chứa các shell đã đc cài đặt trên Linux. 
- Để chuyển đổi giữa các shell, gõ tên shell vào họ OS, nó sẽ mở cho bạn. Ví dụ muốn đổi shell mặc định sang shell zsh, dùng lệnh `chsh -s /usr/bin/zsh`

## 2.1 Bourne Again Shell (Bash)
- Bash là shell mặc định cho Linux. Khi bạn mở terminal, bash sẽ đc trình chiếu khi bạn gõ lệnh. 
- Một số tính năng của Bash:
	+ Để xem lịch sử command, nhấn up hoặc down arrow key. Hoặc gõ `history`

## 2.2 Friendly Interactive Shell (Fish)
- K phải shell mặc định, nhưng có vài ưu điểm sau:
	+ Simple syntax, feasibe for beginner user.
	+ Auto spell correction

## 2.3 Z Shel (Zsh)
- Modern shell đc kết hợp từ 1 vài shell khác. 

# 3. Shell Scripting and Components
- Shell script là 1 tập hợp các lệnh. Giả sử 1 tác vụ lặp đi lặp lại và phải gõ nhiều lệnh, thay vì gõ từng lệnh một, kết hợp chúng vào 1 script. Để thực thi tất cả lệnh, thực thi script. Scripting giúp ta tự động hóa các task. 
- Trước hết tạo file bằng cách sử dụng text editor với extension **.sh** - extension for bash script.
	+ ví dụ: `nano first_script.sh`
- Mọi script đều bắt đầu bằng shebang, tập hợp các kí tự đc thêm vào đầu script: **#!** theo sau là tên của trình thông dịch đc dùng khi execute script.
	+ `#!/bin/bash`

## 3.1 Variables
- Biến chứa giá trị trong nó. Giả sử bạn cần dùng một vài giá trị phức tạp (URL, file path...) nhiều lần trong script. Thay vì phải nhớ và viết lại nó, bạn lưu nó trong variable và dùng variable name mỗi khi cần.
- `echo`: in văn bản ra terminal
- `read`: nhận input từ user
```
#defining the interperter
#!/bin/bash
echo "Hey, what's your name?"
read name
echo "Welcome, $name"
```
- Đoạn script trên in các dòng echo ra màn hình, name là biến mà input đc lưu trữ. Dòng cuối in ra tên đc lưu trong biến name ra màn hình
- Để execute script, cần cấp execution permission cho script. Dùng lệnh `chmod +x variable_script.sh`
- Giờ script có thể đc thực thi bằng lệnh `./<script_name.sh>`

## 3.2 Loops
- Ví dụ, bạn có 1 danh sách bạn bè, muốn gửi cùng 1 bức thư cho họ. Thay vì gửi từng người, bạn có thể tạo 1 vòng lặp trong script, để nó gửi thư.
- Script in ra terminal từ 1-10:
```
#!/bin/bash
for i in {1..10};
do
echo $i
done
```
- Dòng đầu chứ biến i lặp lại từ 1-10. **do** chỉ bắt đầu vòng lặp và **done** là kết thúc. Ở giữa, là đoạn code mà ta muốn execute trong loop. Vòng lặp for nhận mỗi số từ dấu ngoặc đơn và gán cho nó cho biến **i** ở mỗi vòng lặp. **echo $i** là in giá trị biến i ra màn hình.

## 3.3 Condition Statements
- Ví dụ bạn muốn thực hiện 1 script show mn bí mật. Nhưng chỉ muốn nó đc xem bởi 1 vài user, high-authority user. Bạn sẽ tạo condition statement hỏi tên user, và nếu trùng khớp vs high-authority user's name, nó sẽ in ra secret.
```
#!/bin/bash
echo "Please enter your name first:"
read name
if ["$name" = "John"]; then
	echo "Welcome John! here is the secret: THM_script"
else
	echo "Sorry! You are not authorized to access the secret"
fi
```

## 3.4 Comments
- Dùng dấu # để thực hiện comment trong script.

# 4. The Locker Script
```
#!/bin/bash
#defining the variable
username=""
companyname=""
pin=""

for i in {1..3}; do
if [ "$i" -eq 1 ]; then
echo "Enter your Username:"
read username
elif [ "$i" -eq 2 ]; then
echo "Enter your Company name:"
read companyname
else  
echo "Enter your PIN:"
read pin
fi
done

if [ "$username" = "John" ] && [ "$companyname" = "Tryhackme" ] &&>
echo "Authenticafin successful. You can access your locker>
else
echo "Authentication Denied!!"
fi
```