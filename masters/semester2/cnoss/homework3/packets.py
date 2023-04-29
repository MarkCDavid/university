from scapy.all import IP, TCP, send

src_ip = "192.168.0.11"  # Replace with your desired source IP address
dst_ip = "192.168.57.10"    # Replace with your firewall's IP address

# Create an IP packet with a specific source and destination IP address
ip_packet = IP(src=src_ip, dst=dst_ip)

# Create a TCP segment and add it to the IP packet
tcp_segment = TCP(sport=1234, dport=43534, flags="S")
ip_packet /= tcp_segment

# Send the packet to the destination IP address
send(ip_packet)