require('dotenv').config();

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const amqp = require('amqplib');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT;
const SubGrpAppId = process.env.SubGrpAppId;
const SubGrpKey = process.env.SubGrpKey;
const TaskAppId = process.env.TaskAppId;
const TaskKey = process.env.TaskKey;
const LogAppId = process.env.LogAppId;
const LogKey = process.env.LogKey;

// RabbitMQ connection details
const rabbitmq_host = process.env.RABBITMQ_HOST;
const rabbitmq_port = process.env.RABBITMQ_PORT;
const rabbitmq_exchange = process.env.EXCHANGE_NAME;
const rabbitmq_exchange_type = process.env.EXCHANGE_TYPE;
const rabbitmq_queue = process.env.QUEUE_NAME;
const rabbitmq_routing_key = process.env.ROUTING_KEY;


app.get('/subgroup/:subGroupId', async (req, res) => {
    try {
        const subGroupId = req.params.subGroupId;
    
        const subGrpResponse = await axios.get(`https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/${subGroupId}`, {
            headers: {
                'X-SubGroup-AppId': SubGrpAppId,
                'X-SubGroup-Key': SubGrpKey,
            }
        });

        const users = subGrpResponse.data.SubGroup.subGroupUsers;
        
        users.forEach(obj => {
            obj.assigneeUserId = obj.userId;
            obj.assigneeUsername = obj.username;
            delete obj.userId; 
            delete obj.username;
        });

        res.json(users);
    } catch (error) {
        if (error.code === 'ERR_BAD_RESPONSE') {
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            res.status(error.response.status).json({ 
                code: error.response.status + " " + error.response.statusText,
                error: error.response.data.Result.ErrorMessage
            });
        }
    }
});

app.post('/task', async (req, res) => {
    try {
        const createTaskResponse = await axios.post(
            `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task`,
            {
                name: req.body.taskName,
                description: req.body.taskDesc,
                dueDateTime: req.body.dueDateTime,
                subGroupId: req.body.subGroupId,
                createdById: req.body.userId,
                createdByUsername: req.body.username
            }, 
            {
                headers: {
                    'Content-Type': "application/json",
                    'X-Task-AppId': TaskAppId,
                    'X-Task-Key': TaskKey,
                }
            }
        );

        const taskId = createTaskResponse.data.TaskId;

        await axios.put(
            `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task/assign/${taskId}`,
            req.body.assignedTo,
            {
                headers: {
                    'X-Task-AppId': TaskAppId,
                    'X-Task-Key': TaskKey,
                    'assignorId': req.body.userId,
                    'assignorUsername': req.body.username
                }
            }
        )

        res.status(201).json({ message: 'Task created successfully', taskId });
        
        // Connect to RabbitMQ to send log
        const connection = await amqp.connect(`amqp://${rabbitmq_host}:${rabbitmq_port}`);
        const channel = await connection.createChannel();

        // Assert Exchange
        await channel.assertExchange(rabbitmq_exchange, rabbitmq_exchange_type, { durable: true });

        // Define the message
        const message = {
            userId: req.body.userId,
            subGroupId: req.body.subGroupId,
            taskId: taskId,
            type: 'Create Task',
            description: 'This is a test log message.',
            timestamp: '2021-01-01 00:00:00'
        };

        // Send the message to the exchange
        await channel.publish(rabbitmq_exchange, rabbitmq_routing_key, Buffer.from(JSON.stringify(message)), { persistent: true });

        console.log(`Message sent to the exchange '${rabbitmq_exchange}' with routing key '${rabbitmq_routing_key}'.`);

        // Close the connection
        await channel.close();
        await connection.close();

    } catch (error) {
        if (error.code === 'ERR_BAD_RESPONSE') {
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            res.status(error.response.status).json({ 
                code: error.response.status + " " + error.response.statusText,
                error: error.response.data.Result.ErrorMessage
            });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port http://localhost:${PORT}`);
});
