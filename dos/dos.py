import logging
import random
import string
import threading
import time

import paho.mqtt.client as mqtt

# Global counter and lock for thread-safe increments
message_count = 0
count_lock = threading.Lock()


def publish_messages(broker_ip, qos=0):
    global message_count
    """
    Publishes messages to the specified MQTT broker.

    :param broker_ip: IP address of the MQTT broker
    :param qos: Quality of Service for the message
    """
    client_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    client = mqtt.Client(client_id)
    client.connect(broker_ip, 1883, 60)

    while True:
        payload = ''.join(random.choices(string.ascii_letters + string.digits, k=4096))  # Adjust payload size as needed
        client.publish("test/topic", payload, qos=qos)
        with count_lock:  # Ensure thread-safe increment
            message_count += 1
        # No sleep, for maximum throughput


def log_message_count():
    while True:
        time.sleep(300)  # Wait for 5 minutes
        with count_lock:
            logging.warning(f"Total messages published: {message_count}")
            # Reset counter if needed or just continue to log cumulative count


def start_load_test(broker_ips, clients_per_broker=75):
    """
    Starts load tests on the provided MQTT brokers, creating multiple clients per broker.

    :param broker_ips: List of IP addresses of the MQTT brokers
    :param clients_per_broker: Number of clients to simulate per broker
    """
    threads = []
    # Start a logging thread
    logging_thread = threading.Thread(target=log_message_count)
    logging_thread.start()

    time.sleep(300)
    for ip in broker_ips:
        for _ in range(clients_per_broker):  # Create specified number of clients per broker
            t = threading.Thread(target=publish_messages, args=(ip,))
            t.start()
            threads.append(t)
        time.sleep(300)
        # Note: The message logging is handled by log_message_count thread

    for t in threads:
        t.join()
    logging_thread.join()  # Ensure the logging thread also completes


broker_ips = ['192.168.68.70', '192.168.68.60', '192.168.68.50']
start_load_test(broker_ips)

# Produces the following amount of messages:
# WARNING:root:Total messages published: 0
# WARNING:root:Total messages published: 718663
# WARNING:root:Total messages published: 1414734
# WARNING:root:Total messages published: 2109872
