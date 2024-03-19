import time
import pika
import smtplib
import json
from dotenv import load_dotenv
import os

load_dotenv()

# RabbitMQ connection details
rabbitmq_host = os.getenv('HOSTNAME')
rabbitmq_port = os.getenv('PORT')
rabbitmq_queue = os.getenv('QUEUE_NAME')

# Email server details
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

# Connect to RabbitMQ
def create_connection(max_retries=12, retry_interval=5):
    print('notificationServer:create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('notificationServer: Trying connection')
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
            print("notificationServer: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"notificationServer: Failed to connect: {e}")
            retries += 1
            print(f"notificationServer: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        raise Exception("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

connection = create_connection()
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

def send_email(recipient, subject, body):
    """
    Send an email using SMTP server
    """
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient, message)

def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ consumer
    """
    notification = json.loads(body.decode('utf-8'))
    recipient = notification["recipient"]
    subject = notification["subject"]
    body = notification["body"]

    # Send the email
    send_email(recipient, subject, body)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages from the queue
print('Waiting for messages. To exit, press CTRL+C')
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=False)
channel.start_consuming()