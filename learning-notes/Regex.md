- Charset (tập các ký tự): `[]`
  + Vd: `[abc]` sẽ khớp với a, b or c. 
- Hat symbol (loại trừ): `[^]`
  + Vd: `[^k]`
- Wildcard: `.`
- Optional: `?`
  + Vd: `files?` sẽ khớp file hoặc files
  + Nếu muốn regex chứa dấu . phải thêm slash để escape: `\.`
- `\d`: số
- `\D`: không phải số
- `\w`: chữ và số, _
- `\W`: không là chữ hay số, vd !, #
- `\s`: whitespace
- `\S`: mọi ký tự
- Số lần lặp: `{}`
  + `{12}`: lặp 12 lần
  + `{1,5}`: lặp từ 1-5
  + `{2,}`: lặp 2 hoặc hơn
  + `*`: 0 hoặc hơn
  + `+`: 1 hoặc hơn
- Bắt đầu với: `^`
- Kết thúc: `$`
- Hoặc: `(a|b)`
- Lặp cụm từ: `(no){5}`
