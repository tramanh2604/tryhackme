**1. IP & routing**
```
ip addr show            #xem tất cả các interface, IP, trạng thái
ip route show           #routing table - xem default gateway
cat /etc/resolv.conf    # DNS server dùng gì
```

**2. ARP table**
- Xem máy nào trong cùng Layer2 segment
```
arp -a
ip neigh show
ip neigh show dev eth0    #thay eth0 bằng interface xem từ ip addr show
```

**2. Kiểm tra outbount connnect - xem có ra ngoài được không**
