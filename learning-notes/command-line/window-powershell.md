# 1. Introduction
- PowerShell đc thiết kế để dùng cho tự động hóa các task và quản lý cấu hình. Là sự kết hợp của giao diện dòng lệnh và scripting language .NET. PowerShell là hướng đối tượng, giúp xử lý các loại data phức tạp và giao tiếp vs os 1 cách hiệu quả. 
- **object** đại diện cho item có **properties** - thuộc tính và **methods** - hoạt động. Ví dụ object **car** có properties như **Color**, **Model** và methods như **Drive()**, **HonkHorm()**.
- Object trong PowerShell có thể chứa file names, usernames or size as data (**properties**) và chứa các function (**methods**) như copy file, dừng process.

# 2. PowerShell Basics
## 2.1 Basic Syntax: Verb-Noun
- Cmdlets (PowerShell) chứa quy ước đặt tên **Verb-Noun**. **Verb** mô tả hành động và **Noun** chỉ định đối tượng mà hđ thực hiện. Ví dụ:
	+ **Get-Content**: get content từ file và display trên màn hình console.
	+ **Set-Location**: thay đổi (set) lại working directory hiện tại.

## 2.2 Basic Cmdlets
-`Get-Command`: in ra danh sách các cmdlets, hàm, aliases và script có thể đc thực thi trong các phiên hiện tại. 
- `CommandInfo`: các thông tin hữu ích. Ví dụ muốn chỉ display các command of type "function" có sẵn, dùng `-CommandType "Function`.

![Get-Command](/images/getcommand.PNG)

- `Get-Help`: cung cấp thông tin chi tiết về cmdlets, gồm cách dùng, tham số và ví dụ. 

![Get-Help](/images/gethelp.PNG)

- `Get-Alias`: gồm các aliases (bí danh) phím tắt cho cmdlets. Ví dụ `dir` là viết tắt cho `Get-ChildItem`, cd là viết tắt cho `Set-Location`.

## 2.3 Where to Find & Download Cmdlets
- PowerShell có thể đc mở rộng bằng cách tải thêm các cmdlets từ online repositories (kho lưu trữ trực tuyến).
- `Find-Module`: tìm các module có sẵn trong kho.
- `Find-Module -Name "PowerShell*"`: tìm module khi k biết rõ tên chính xác. 

![Find-module](/images/findmodule.PNG)

- Khi đc xác nhận, module có thể đc download và cài đặt từ repository với lệnh `Install-Module`.

![Install-Module](/images/installmodule.PNG)

# 3. Navigating the File System (Điều hướng) and Working with Files
- `Get-ChildItem`: giống với **dir** hoặc **ls**, thêm vào tham số `-Path` để khám phá thư mục và xem nội dung của chúng. Nếu k có `Path`, cmdlet chỉ display nội dung của thư mục hiện tại.

![Get-ChildItem](/images/getchilditem.PNG)

- `Set-Location -Path ".\Document"`: chuyển đổi thư mục, giống **cd**.

![Set-Location](/images/setlocation.PNG)

- `New-Item -Path "<path>" -ItemType "Directory"/"File"`: tạo file hoặc dir dựa vào itemtype.

![New-Item](/images/newitem.PNG)

- `Remove-Item - Path "<path>"`: xóa thư mục/file; giống với **rmdir**, **del**.

- `Copy-Item -Path <path> -Destination <path>"`: copy file
- `Move-Item`: giống với move.
- `Get-Content -Path "<path>"`: xem nội dung file, giống với **type** hoặc **cat**.

# 4. Piping, Filtering and Sorting Data
- **Piping** là kỹ thuật đc dùng trong môi trường command-line, cho phép output của 1 lệnh đc dùng làm input của lệnh khác. Điều đó tạo ra 1 chuỗi các hđ trong đó data đi từ lệnh này sang lệnh kế tiếp. Đc đại diện bởi **|**.
- Piping trong PowerShell còn mạnh hơn vì nó duyệt qua object thay vì text. Những object này k chỉ chứa data mà còn là thuộc tính và phương thức mà nó mô tả và tương tác vs data.
- Ví dụ: muốn có 1 list các file trong 1 dir và xếp thêm size: `Get-ChildItem | Sort-Object Length`
	+ **Get-ChildItem** lấy các file (object) rồi lọc (**|**) gửi các file này đến **Sort-Object**, nó sẽ xếp file theo thuộc tính **Length** (size). Các object-based cho phép các lệnh chi tiết hoặc flexible hơn.

---
- `Where-Object`: Để lọc các object dựa trên các đối tượng đc chỉ định, chỉ trả lại các đối tượng đáp ứng tiêu chí.
- Ví dụ: chỉ liệt kê các file **.txt** trong dir: `Get-ChildItem | Where-Object -Property "Extension" -eq ".txt"`
	+ **Where-Object** lọc các file dựa vào thuộc tính **Extension**, đảm bảo rằng chỉ có các file với extension bằng với (equal) (-eq) **.txt** mới đc liệt kê.
- **Comparison Operators**:
	+ `-ne`: not equal, dùng để loại trừ object khỏi kết quả.
	+ `-gt`: greater than, chỉ lọc các object vượt gtri chỉ định, loại luôn kết quả bằng.
	+ `ge`: greater than or equal to.
	+ `lt`: less than, chỉ gồm các object nhỏ hơn giá trị chỉ định.
	+ `le`: less than or equal to.
- `like`: gần giống. Ví dụ `Get-ChildItem | Where-Object -Property "Name" -like "ship*"`, kết quả trả về là file **ship-flag.txt**

---
- `Select-Object`: chọn các thuộc tính cụ thể từ object hoặc hạn chế số lượng object trả về.
	+ Ví dụ: `Get-ChildItem | Select-Object Name,Length`

- **Bài Tập**: try and build a pipeline of cmdlets to sort and filter the output with the goal of displaying the largest in path...

`Get-ChildItem -Path C:\Users\captain\Documents\captain-cabin | Sort-Object Length -Descending | Seletc-Object -First 1`

---
- `Select-String`: tìm kiếm text pattern trong file, giống **grep** hoặc **findstr**. Nó cũng thường đc dùng để tìm các nội dung cụ thể trong log file hoặc document.
- Ví dụ: `Select-String -Path ".\captain-hat.txt" -Pattern "hat"` => kết quả: *captain-hat.txt:8:Don't touch my hat!*

# 5. System and Network Information
- `Get-ComputerInfo`: cung cấp thông tin hệ thống 1 cách toàn diện, gồm OS, hardware, BIOS detailed,... Nó cung cấp cấu hình của toàn bộ hệ thống trong 1 dòng lệnh. 
- `Get-LocalUser`: quản lý user và hiểu về the machine's security configuration. Nó sẽ in ra 1 list các local user account trên system. Thông tin mặc định về: username, account status, description.
- `Get-NetIPConfiguration`: tương tự **ipconfig**, cung cấp thông tin chi tiết về network interface của hệ thống, gồm đchi IP, DNS server, cấu hình gateway.
- `Get-NetIPAdress`: cung cấp chi tiết các đchi IP đc gán cho giao diện mạng, gồm cả các IP đang k hoạt động.

# 6. Real-Time System Analysis
- Để thu thập thêm các thông tin về HĐH, đc biệt là dynamic aspect như running processes, services, active network connection.
- `Get-Process`: cung cấp chi tiết các process đang chạy, gồm CPU và memory usage => monitoring & troubleshooting.
- `Get-Service`: cung cấp thông tin về tình trạng (running, stopped, paused) của các service trên máy.
- `Get-NetTCPConnection`: giám sát các kết nối mạng đang hoạt động, thường là TCP connection, đưa ra insight về cả local và remote enpoint. 
- `Get-FileHash`: tạo file hash.

# 7. Scripting
- **Scripting** là quá trình viết và thực thi 1 loạt các dòng lệnh nằm trong file text, gọi là script, để tự động hóa các task mà thường người ta thực hiện thủ công trong shell, PowerShell.
- Nói đơn giản, scripting giống như đưa cho máy tính 1 to-do list, mỗi dòng lệnh là 1 task mà máy tính phải thực hiện tự động. Nó tiết kiệm tg, giảm rủi ro và cho phép thực hiện các task quá phức tạp hoặc tẻ nhạt khi thực hiện thủ công. You'll discover that scripts can be powerful tools for managing systems, processing data, and much more.
- `Invoke-Command`: thực thi lệnh trên remote systems, making it fundamentals for system administrator, security engineers and penetration testers. Cho phép quản lý từ xa và kết hợp nó vs các tác vụ tự động trên nhiều máy tính. Nó cũng có thể thực hiện payload hoặc lệnh trên hệ thống đích trong suốt quá trình xâm nhập ở pentester.
- Ví dụ: `invoke-command -computername server1 -ScriptBlock { get-service }` -> `-ScriptBlock` giúp thực thi lệnh trong dấu {} trên máy remote.
