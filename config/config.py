import socket

network_conf = dict(
    my_ip=socket.gethostbyname(socket.gethostname()),
    server_ip='',
    client_ips=['192.168.1.200', '192.168.1.300']
)

CLOUD_SERVER = 0
FOG_DEVICE = 1
EDGE_DEVICE = 2
