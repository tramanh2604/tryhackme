# File
- Trong python, bạn có thể đọc và viết vào file. Đó là cách phổ biến để viết script và import hoặc export nó từ file. 

- Open file:
```
f = open("file_name", "r")
print(f.read())
```
+ `read()`: đọc nội dung file
+ `readlines()`: đọc từng line trong file

- Create & write file:
+ File đã tồn tại, open file, dùng "a" (append). Nếu viết vào file mới, dùng "w" (write)
```
f = open("file_name.txt", "a") #append to an existing file
f.write("Hello World")
f.close()
```

```
f = open("file_name.txt", "w") # creating and writing to a new file
f.write("Hello World")
f.close()
```

# Import
- Các thư viện phổ biến cho pentester:
+ request: simple HTTP library
+ scapy: send, sniff, disect and forge network package
+ pwntools: a ctf and exploit development library

- Để cài đặt các thư viện python, dùng pip: `pip install [name]`. Ví dụ muốn cài thư viện scapy `pip install scapy`