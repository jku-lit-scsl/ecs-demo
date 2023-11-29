import socket

mqtt_conf = dict(
    mqtt_ip_forward='localhost',
    mqtt_port_forward=1883,
    mqtt_ip_receive='localhost',
    mqtt_port_receive=1883,
)

network_conf = dict(
    my_ip=socket.gethostbyname(socket.gethostname()),
    server_ip='somestring'
)
