# 1. Detection techniques
- Signature-based detection: tìm kiếm các malicious pattern hoặc signature bên trong files.
- Heuristic detection: phân tích hành vi để đánh giá file đáng nghi.
- Dynamic detection: giám sát các system call và API, đồng thời kiểm tra và phân tích tệp trong một môi trường cách ly (isolated/sandbox).

# 2. Static detection
- Dùng pattern-matching để so sánh, ví dụ 1 unique string, CRC (Checksums), chuỗi bytecode/giá trị Hex, và các hàm băm mật mã (MD5, SHA1, v.v.).
- AV thực hiện 1 loạt so sánh các file trong OS với database of signatures. Nếu signatures tồn tại trong database => xác định file đó malicious.

# 3. Fingerprinting AV software
- Dựa vô service names, process names, domain names, registry keys, and filesystems.
| Antivirus Name        | Service Name                         | Process Name                          |
|-----------------------|--------------------------------------|---------------------------------------|
| Microsoft Defender    | WinDefend                             | MSMpEng.exe                           |
| Trend Micro           | TMBMSRV                              | TMBMSRV.exe                           |
| Avira                 | AntivirService, Avira.ServiceHost    | avguard.exe, Avira.ServiceHost.exe    |
| Bitdefender           | VSSERV                               | bdagent.exe, vsserv.exe               |
| Kaspersky             | AVP<Version #>                       | avp.exe, ksde.exe                     |
| AVG                   | AVG Antivirus                        | AVGSvc.exe                            |
| Norton                | Norton Security                      | NortonSecurity.exe                    |
| McAfee                | McAPExe, Mfemms                      | MCAPExe.exe, mfemms.exe               |
| Panda                 | PavPrSvr                             | PavPrSvr.exe                          |
| Avast                 | Avast Antivirus                      | afwServ.exe, AvastSvc.exe             |

- SharpEDRChecker 
