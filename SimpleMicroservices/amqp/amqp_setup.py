import time
import pika
from dotenv import load_dotenv
import os

load_dotenv()
# hostname = "localhost" # default hostname
# port = 5672            # default port
# exchangename = "order_topic" # exchange name
# exchangetype = "topic" # - use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
hostname = os.getenv('HOSTNAME') #localhost
port = os.getenv('PORT') #5672
exchangename = os.getenv('EXCHANGE_NAME') #esd_exchange
exchangetype = os.getenv('EXCHANGE_TYPE') #topic

queue_names = [
    os.getenv('QUEUE_NAME_1'),
    os.getenv('QUEUE_NAME_2'),
    os.getenv('QUEUE_NAME_3')
]

routing_keys = [
    os.getenv('ROUTING_KEY_1'),
    os.getenv('ROUTING_KEY_2'),
    os.getenv('ROUTING_KEY_3')
]

#to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print('amqp_setup:create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_setup: Trying connection')
            # connect to the broker and set up a communication channel in the connection
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) # these parameters to prolong the expiration time (in seconds) of the connection
                # Note about AMQP connection: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
                # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls.
                # If see: Stream connection lost: ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
                # - Try: simply re-run the program or refresh the page.
                # For rare cases, it's incompatibility between RabbitMQ and the machine running it,
                # - Use the Docker version of RabbitMQ instead: https://www.rabbitmq.com/download.html
            print("amqp_setup: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_setup: Failed to connect: {e}")
            retries += 1
            print(f"amqp_setup: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        raise Exception("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    return channel

def create_exchange(channel, exchange_name, exchange_type):
    print(f'amqp_setup:create exchange {exchange_name}')
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)

def create_queues(channel, exchange_name, queue_names, routing_keys):
    for queue_name, routing_key in zip(queue_names, routing_keys):
        print(f'amqp_setup:create queue {queue_name}')
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

if __name__ == "__main__":
    connection = create_connection()
    channel = create_channel(connection)

    create_exchange(channel, exchangename, exchangetype)
    create_queues(channel, exchangename, queue_names, routing_keys)

    print("Exchange and queues created successfully.")

    # Close the connection when done
    connection.close()
    
    