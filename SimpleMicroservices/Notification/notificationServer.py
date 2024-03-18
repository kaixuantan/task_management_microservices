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
connection = pika.BlockingConnection(pika.ConnectionParameters
                                     (host=rabbitmq_host, port=rabbitmq_port,
                                      heartbeat=3600, blocked_connection_timeout=3600))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

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