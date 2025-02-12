# Chương trình sẽ đọc subdomain từ file wordlist2.txt và kiểm tra xem chúng có phản hồi không
# Giả định rằng những subdomain chấp nhận kết nối là những subdomain tồn tại

import requests #gửi request, xử lý respone
import sys

# Đọc danh sách subdomains từ file
sub_list = open("D:/tryhackme/learning-notes/python/wordlist2.txt").read()
sub_dom = sub_list.splitlines() #đọc toàn bộ file và tách thành danh sách các dòng

# kiểm tra từng subdomain
for sub in sub_dom:
    sub = sub.strip() # xóa khoảng trắng giữa
    sub_domain = f"http://{sub}.{sys.argv[1]}"

    #sys.argv[1]: đối số đầu tiên đc truyền vào
    # khi chạy lệnh `python3 SubdomainEnumeration.py example.com` thì chương trình sẽ
    # tạo ra các URL dạng http:// blog.example.com

    try:
        requests.get(sub_domain)

    except requests.ConnectionError:
        pass # bỏ qua nếu k thể kết nối

    else:
        print("Valid domain: ", sub_domain) # in domain hợp lệ
