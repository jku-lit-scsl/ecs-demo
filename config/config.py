import socket

network_conf = dict(
    my_ip=socket.gethostbyname(socket.gethostname()),
    server_ip='',
    children_ips=['192.168.1.200', '192.168.1.300']
)
