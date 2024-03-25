import pika
import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

# RabbitMQ connection details
rabbitmq_host = os.getenv('HOSTNAME')
rabbitmq_port = os.getenv('PORT')
rabbitmq_queue = os.getenv('QUEUE_NAME')
print(f"RabbitMQ Host: {rabbitmq_host}")

# REST API details
rest_api_url = os.getenv('REST_API_URL')
rest_api_app_id = os.getenv('REST_API_APP_ID')
rest_api_key = os.getenv('REST_API_KEY')

# Connect to RabbitMQ
def create_connection(max_retries=12, retry_interval=5):
    print('logServer:create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('LogServer: Trying connection')
            # connect to the broker and set up a communication channel in the connection
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=rabbitmq_host, port=rabbitmq_port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) # these parameters to prolong the expiration time (in seconds) of the connection
                # Note about AMQP connection: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
                # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls.
                # If see: Stream connection lost: ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
                # - Try: simply re-run the program or refresh the page.
                # For rare cases, it's incompatibility between RabbitMQ and the machine running it,
                # - Use the Docker version of RabbitMQ instead: https://www.rabbitmq.com/download.html
            print("logServer: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"logServer: Failed to connect: {e}")
            retries += 1
            print(f"logServer: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        raise Exception("logServer: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

connection = create_connection()
channel = connection.channel()

def call_rest_api(log_data):
    """
    Send a POST request to the REST API with the log data
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Log-AppId': rest_api_app_id,
        'X-Log-Key': rest_api_key
    }

    try:
        response = requests.post(rest_api_url, json=log_data, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        print(f"Log data sent to {rest_api_url} successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log data to {rest_api_url}: {e}")

def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ consumer
    """
    log_data = json.loads(body.decode('utf-8'))

    # Call the REST API with the log data
    call_rest_api(log_data)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages from the queue
print('Waiting for messages. To exit, press CTRL+C')
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=False)
channel.start_consuming()