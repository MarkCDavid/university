sudo ip link add link eno2 veno2_1 type macvlan mode bridge
sudo ip addr add 192.168.56.10/24 dev veno2_1
sudo ip route add default via 192.168.56.1 dev veno2_1
sudo ip link set veno2_1 up