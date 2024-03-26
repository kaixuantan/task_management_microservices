const express = require('express');
const amqp = require('amqplib');
require('dotenv').config();

const app = express();
const rabbitmqHost = process.env.RABBITMQ_HOST;
const queueName = process.env.QUEUE_NAME;
const exchangeName = process.env.EXCHANGE_NAME;

// Middleware to parse request body
app.use(express.json());

// Endpoint for other microservices to call
app.post('/ideas', async (req, res) => {
  try {
    // Connect to RabbitMQ
    const connection = await amqp.connect(rabbitmqHost);
    const channel = await connection.createChannel();

    // Publish the message to the queue
    console.log(req.body);
    const { docId, message } = req.body;
    console.log(message);
    const buffer = Buffer.from(JSON.stringify(message));
    const routingKey = `idea.${docId}`
    // Publish the message to the exchange
    channel.publish(exchangeName, routingKey, buffer, { persistent: true });

    console.log(`Message published to ${queueName}`);

    // Close the RabbitMQ connection
    await channel.close();
    await connection.close();

    res.status(200).send('Message published successfully');
  } catch (error) {
    console.error('Error publishing message:', error);
    res.status(500).send('Error publishing message');
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});