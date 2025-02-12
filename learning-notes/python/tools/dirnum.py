# Hoạt động tương tự như subdomainEnum.py, dựa trên vòng lặp for và bỏ qua những status_code==404

import requests
import sys

# Đọc danh sách directory tìm năng từ wordlist2.txt
sub_list = open("D:/tryhackme/learning-notes/python/wordlist2.txt").read()
directories = sub_list.splitlines()

# Tạo vòng lặp duyệt qua từng directory
for dir in directories:
    dir_enum = f"http://{sys.argv[1]}/{dir}.html" #duyệt qua các file html
    r = requests.get(dir_enum)

    if r.status_code == 404:
        pass #bỏ qua lỗi
    else:
        print("valid directory: ,dir_enum");
