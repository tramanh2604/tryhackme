# HTTP (hypertext transfer protocol)
- HTTP đc dùng bất cứ khi nào bạn xem 1 trang web. HTTP là bộ quy tắc giao tiếp với máy chủ (web server) để truyền data của webpages (HTML, ảnh, video...)

# HTTPS (hypertext transfer protocol secure)
- Là 1 version của HTTP, data của HTTPS sẽ được mã hóa, stop people seeing data you are sending and receiving; đảm bảo bạn đang giao tiếp đúng với webserver.

# Requests and Respone
- Khi truy cập 1 website, browser sẽ make requests a web server để truy cập các data như HTML, images, và download the respone.
- Before that you need to tell the browser how and where to access these resources -> URLs 

## 1. URL (Uniform resource locator)
- URL là 1 instruction on how to access a resource on the internet.

![URL features](../images/url-features.PNG)

- Scheme: protocol nào đc dùng để truy cập tài nguyên (HTTP, HTTPS, FTP - file transfer protocol).
- User: 1 vài dịch vụ cần xác thực để đăng nhập, bạn có thể thêm username và password vào URL để đăng nhập.
- Host: domain name hoặc IP address của server muốn truy cập.
- Port: 80 for HTTP, 443 for HTTPS, (1-65535)
- Path: file name hoặc location của resource muốn truy cập.
- Query string: bit thông tin bổ sung. Ví dụ */blog?id=1* tức muốn tell the blog path muốn nhận blog article có id là 1.
- Fragment: a location on the actual page requested. This is the common use for pages with long content and can have a certain part of the page directly linked to it, so it is viewable to the user as soon as they access the page.

## 2. Making a request
```
GET / HTTP/1.1 #

Host: tryhackme.com

User-Agent: Mozilla/5.0 Firefox/87.0

Referer: https://tryhackme.com/


```

- Line 1: The request is sending GET method and telling the web server that we are using HTTP protocol version 1.1.
- Line 2: we tell the web server that we want the website *tryhackme.com*.
- Line 3: tell the webserver that we are using the Firefox version 87 browser.
- Line 4: telling the web server that the web page that referred us to this one is *https://tryhackme.com/*
- Line 5: HTTP requests always end with a blank line ti inform the web server that the request has finished.

## 3. Example respone
```
HTTP/1.1 200 OK

Server: nginx/1.15.8

Date: Fri, 09 Apr 2021 13:34:03 GMT

Content-Type: text/html

Content-Length: 98



<html>

<head>

    <title>TryHackMe</title>

</head>

<body>

    Welcome To TryHackMe.com

</body>

</html>
```

- Line 1: HTTP/1.1 là version mà web server dùng, *200 OK* is the HTTP Status code which tells us the request has completed thành công.
- Line 2: telling us the web server software and version number.
- Line 3: The current date, time and timezone of the web server.
- Line 4: The content-type header báo cho client biết loại thông sẽ đc gửi (HTML, images, video, pdf, XML).
- Line 5: content-length báo cho client biết độ dài của reponse, this way we can confirm that no data is missing.
- Line 6: HTTP respone chứa blank line để báo kết thúc HTTP respone.
- Line 7-14: Thông tin đc yêu cầu, trong trường hợp này là homepage.

 # HTTP Methods
 - A way for the client to show their intended action (hành động dự định) when making an HTTP request. 
 - Some common HTTP methods:
 	+ GET Request: nhận data từ web server.
 	+ POST Request: gửi data đến web server và tạo ra bản ghi mới.
 	+ PUT request: gửi data đến web server để cập nhật thông tin.
 	+ DELETE Request: xóa information/record từ web server.

 # HTTP Status Code
 ## 1. HTTP status code
 - Thông báo cho client kết quả xử lý request. Đc chia làm 5 mức độ:

 ![HTTP status code](../images/http-status-code.PNG)

 ## 2. Commong HTTP status code

 ![Common HTTP status code](../images/common-http-status-code.PNG)

 
 # Header
 - Header are additional bits of data you can send to the web server when making requests.

 ## Common Request Headers
 - From client (your browser) to the server
 1. Host: một vài web server chứa nhiều website, nếu cung cấp header bạn có thể nói rõ bạn cần website nào, nếu k chỉ nhận được website mặc định của server.

 2. User-Agent: this is your broswer software and version number, giúp web server căn chỉnh format phù hợp vs web browser, cũng như 1 số thành phần HTML, JavaScript, CSS chỉ phù hợp vs 1 số browser.

 3. Content-length: khi gửi data tới web server với dạng biểu mẫu, content-length báo cho web server có bao nhiêu data trong web request, giúp web server k bị mất data.

 4. Accept-Encoding: Cho web server biết loại phương pháp nén nào được browser hỗ trợ để data có thể được thu nhỏ lại để truyền qua internet.

 5. Cookie: data sent to the server to help remember your information.

 ## Common Respone Header
 - The headers returned to the client from the server after a request.

 1. Set-cookie: thông tin cần đc lưu trữ gửi lại web server ở mỗi request.

 2. Cache-control: thời gian lưu content của respone trong browser's cache trước khi đc request lại lần nữa.

 3. Content-type: giúp browser nhận biết các xử lý data (HTML, CSS, images,PDF...)

 4. Content-encoding: loại phương pháp nén được dùng để thu nhỏ data lại khi truyền qua internet.

 # Cookies
 - Cookies are just a small piece of data that is stored in your computer. Cookies được lưu khi nhận được *Set-cookie* ở header từ web server. Mỗi lần bạn gửi request, bạn sẽ gửi cookie data tới web server. 
 - Bởi vì HTTP là stateless, cookies được dùng để nhắc web server who you are, some personal settings for the website và liệu bạn có từng ghé thăm website đó chưa.

 ![Cookies](../images/cookies.PNG)

 - Cookies được dùng trong nhiều mục đích nhưng thường được dùng để xác thực trang web. Cookie thường k phải là clear-text-string mà là token (unique secret code that isn't easily humanly guesable).

 ## Viewing your cookies
 - Using developer tools, in your browser => Network tab