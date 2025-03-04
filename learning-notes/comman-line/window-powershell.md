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
- **Piping** là kỹ thuật 