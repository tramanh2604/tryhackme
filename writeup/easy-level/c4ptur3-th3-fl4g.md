# Task 1: Translation & Shifting

#### 1. Message One
- Dễ nhận thấy 1 vài kí tự trong đoạn mã được thay thế bởi các con số.

=> 4 - A, 0 - O, 7 - T, 2 - R, 3 - E, 1 - L, 9 - G

> Answer: can you capture the flag?

#### 2. Message Two
- Đoạn mã gồm các số 0 và 1, dễ nhận biết đó chính là binary.
- Chúng ta sẽ dùng [CyberChef](https://cyberchef.org/) để giải đoạn mã trên. Vào CyberChef và chọn "From Binary" ở phần recipe, ta sẽ có đáp án.

> Answer: lets try some binary out!

#### 3. Message Three
- Thông thường, Base64 luôn kết thúc bằng 0, 1 hoặc 2 dấu '=' để căn chỉnh độ dài phù hợp với quy tắc mã hóa.
- Trong trường hợp này, đoạn mã có đến 6 dấu '=' => không phải là Base64, dùng "From Base32" ở recipe ta sẽ có đáp án.

> Answer: base32 is super common in CTF's

#### 4. Message Four
- Có 2 dấu bằng ở cuối đoạn mã => Base64. Dùng CyberChef và chọn "From Base64" để giải mã.

> Answer: Each Base64 digit represents exactly 6 bits of data.

#### 5. Message Five
- Đoạn mã gồm các số 0-9 và các kí tự a-f => Hexadecimal. Dùng "From Hex" ở recipe để giải mã

> Answer: Each Base64 digit represents exactly 6 bits of data.

#### 6. Message Six
- Bên cạnh việc dùng CyberChef, ta còn có công cụ [Cipher Identifier](https://www.dcode.fr/cipher-identifier).
- Ta sẽ copy đoạn mã và paste vào ô textbox "Ciphertext to recognize", bấm "ANALYZE". Trang web sẽ tìm kỹ thuật mã hóa phù hợp nhất với đoạn mã. Ở đây là "ROT-13 Cipher".
- Bấm chọn "ROT-13 Cipher" => "Decrypt ROT13", ta được đáp án.

> Answer: Rotate me 13 places!

#### 7. Message Seven
- Thực hiện giải mã bằng Cipher tương tự như trên => ROT47.

> Answer: You spin me right round baby right round (47 times)

#### 8. Message Eight
- Đoạn mã gồm các kí tự '.' và '-' => mã Morse. Ta có thể dùng các công cụ giải mã Morse trên Google hoặc dùng Cipher.

> Answer: telecommunication encoding

#### 9. Message Nine
- Đoạn mã gồm 1 chuỗi các số => Có thể ASCII hoặc Decimal. Dùng CyberChef ta thu được kết quả.

> Answer: Unpack this BCD

#### 10. Message Ten
- Có 1 dấu '=' ở cuối đoạn mã => Có thể Base64.
- Đoạn mã lồng mã: Base64 > Morse > Binary > ROT47 > Decimal. Giải mã tuần tự ta thu được đáp án.

> Answer: Let's make this a bit trickier...

# Task 2: Spectrograms
- Spectrograms là 1 dạng phổ đồ âm thanh, có thể dùng các sound/wave analyst tool (e.g Audacity) để xem phổ đồ và biết được đáp án. 

> Answer: super secret message

# Task 3: Steganography
- Steganography là phương pháp che dấu dữ liệu trong file, message, image hoặc video.

- Ta có thể sử dụng platform sau để giải mã data trong image: [Aperi'Solve](https://www.aperisolve.com/). Sau khi thêm ảnh và submit, kéo xuống đến phần Steghide, ta có thấy có 1 file txt đã được giải mã *steganopayload2248.txt*, nội dung file chính là đáp án.

> Answer: SpaghettiSteg

# Task 4: Security through obscurity
- Bảo mật thông qua sự che dấu là phương pháp bảo mật dựa trên việc giữ bí mật về thiết kế hoặc cách triển khai hệ thống một cách chính xác để đảm bảo an toàn cho hệ thống. 
- Ví dụ: không công khai thuật toán bảo mật hoặc giấu dường dẫn URL của 1 trang web quan trọng

- Tìm string trong ảnh bằng lệnh sau trong linux:
`strings meme_1559010886025.jpg`

> Answer: hackerchat.png
> Answer: AHH_YOU_FOUND_ME!
