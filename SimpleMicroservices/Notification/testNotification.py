import pika
import smtplib
import json
from dotenv import load_dotenv
import os

load_dotenv()

# RabbitMQ connection details
rabbitmq_host = os.getenv('HOSTNAME')
rabbitmq_port = os.getenv('PORT')
rabbitmq_exchange = os.getenv('EXCHANGE_NAME')
rabbitmq_queue = os.getenv('QUEUE_NAME')

# Email server details
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters
                                     (host=rabbitmq_host, port=rabbitmq_port,
                                      heartbeat=3600, blocked_connection_timeout=3600))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

# Define the message
message = {
    "recipient": "test@example.com",
    "subject": "Test Notification",
    "body": "This is a test notification message."
}

# Send the message to the queue
channel.basic_publish(
    exchange=rabbitmq_exchange,
    routing_key=rabbitmq_queue,
    body=json.dumps(message)
)

print(f"Message sent to the queue '{rabbitmq_queue}'.")

# Close the connection
connection.close()