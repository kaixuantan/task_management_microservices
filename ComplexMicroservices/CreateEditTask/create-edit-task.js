require('dotenv').config();

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const amqp = require('amqplib');
const swaggerUI = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT;
const SubGrpAppId = process.env.SubGrpAppId;
const SubGrpKey = process.env.SubGrpKey;
const TaskAppId = process.env.TaskAppId;
const TaskKey = process.env.TaskKey;

// RabbitMQ connection details
const rabbitmq_host = process.env.RABBITMQ_HOST;
const rabbitmq_port = process.env.RABBITMQ_PORT;
const rabbitmq_exchange = process.env.EXCHANGE_NAME;
const rabbitmq_exchange_type = process.env.EXCHANGE_TYPE;
const rabbitmq_log_routing_key = process.env.LOG_ROUTING_KEY;
const rabbitmq_notif_routing_key = process.env.NOTIF_ROUTING_KEY;

// Email server details
const smtp_server = process.env.SMTP_SERVER;
const smtp_port = process.env.SMTP_PORT;
const smtp_username = process.env.SMTP_USERNAME;
const smtp_password = process.env.SMTP_PASSWORD;
const test_email = process.env.TEST_EMAIL;

// Serve Swagger UI
app.use('/api', swaggerUI.serve, swaggerUI.setup(swaggerDocument));

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
            obj.assigneeEmail = obj.email;
            delete obj.userId; 
            delete obj.username;
            delete obj.email;
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
    const { connection, channel } = await connectToRabbitMQ();
    var taskId = 0;

    try {
        const createTaskResponse = await axios.post(
            `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task`,
            {
                name: req.body.taskName,
                description: req.body.taskDesc,
                subGroupId: req.body.subGroupId,
                createdById: req.body.assignorUserId,
                createdByUsername: req.body.assignorUsername,
                assignorUserId: req.body.assignorUserId,
                assignorUsername: req.body.assignorUsername,
                dueDateTime: req.body.dueDateTime,
            },
            {
                headers: {
                    'Content-Type': "application/json",
                    'X-Task-AppId': TaskAppId,
                    'X-Task-Key': TaskKey,
                }
            }
        );

        taskId = createTaskResponse.data.TaskId;
        console.log(req.body.assignedTo)
        await assignTask(taskId, req.body.assignedTo, req.body.assignorUserId, req.body.assignorUsername);

        res.status(201).json({ message: 'Task created successfully', taskId });

        await sendLogMessage(channel, req.body, taskId, 'Create Task', 'A task has been created');
        await sendNotifications(channel, req.body, taskId);
    } catch (error) {
        console.log(error)
        if (error.code === 'ERR_BAD_RESPONSE') {
            res.status(500).json({ error: 'Internal Server Error' });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Create Task', 'Internal Server Error');
        } else if (error.response.status) {
            res.status(error.response.status).json({
                code: error.response.status + " " + error.response.statusText,
                error: error.response.data.Result.ErrorMessage
            });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Create Task', error.response.data.Result.ErrorMessage);
        } else {
            res.status(500).json({ error: error });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Create Task', error);
        }
    } finally {
        await closeConnection(connection, channel);
    }
});

app.put('/task/:taskId', async (req, res) => {
    const { connection, channel } = await connectToRabbitMQ();

    try {
        const taskId = req.params.taskId;
        console.log(req.body)
        await axios.put(
            `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task/${taskId}`,
            {
                name: req.body.taskName,
                description: req.body.taskDesc,
                subGroupId: req.body.subGroupId,
                createdById: req.body.createdById,
                createdByUsername: req.body.createdByUsername,
                createdDateTime: req.body.createdDateTime,
                assignorUserId: req.body.assignorUserId,
                assignorUsername: req.body.assignorUsername,
                lastUpdatedById: req.body.lastUpdatedById,
                lastUpdatedUsername: req.body.lastUpdatedUsername,
                dueDateTime: req.body.dueDateTime,
                status: req.body.status
            },
            {
                headers: {
                    'Content-Type': "application/json",
                    'X-Task-AppId': TaskAppId,
                    'X-Task-Key': TaskKey,
                }
            }
        );

        console.log(req.body.assignedTo)
        await assignTask(taskId, req.body.assignedTo, req.body.assignorUserId, req.body.assignorUsername);

        res.status(200).json({ message: 'Task updated successfully', taskId });

        await sendLogMessage(channel, req.body, taskId, 'Edit Task', 'A task has been updated');
        await sendNotifications(channel, req.body, taskId);
    } catch (error) {
        console.log(error)
        if (error.code === 'ERR_BAD_RESPONSE') {
            res.status(500).json({ error: 'Internal Server Error' });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Edit Task', 'Internal Server Error');
        } else if (error.response.status) {
            res.status(error.response.status).json({
                code: error.response.status + " " + error.response.statusText,
                error: error.response.data.Result.ErrorMessage
            });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Edit Task', error.response.data.Result.ErrorMessage);
        } else {
            res.status(500).json({ error: error });
            const connection = await connectToRabbitMQ();
            const channel = await connection.createChannel();
            await sendLogMessage(channel, req.body, taskId, 'Error in Edit Task', error);
        }
    } finally {
        await closeConnection(connection, channel);
    }
});

async function connectToRabbitMQ() {
    // Connect to RabbitMQ to send log
    const connection = await amqp.connect(`amqp://${rabbitmq_host}:${rabbitmq_port}`);
    const channel = await connection.createChannel();

    // Assert Exchange
    await channel.assertExchange(rabbitmq_exchange, rabbitmq_exchange_type, { durable: true });
    return { connection, channel };
}

async function closeConnection(connection, channel) {
    if (channel) await channel.close();
    if (connection) await connection.close();
}

async function assignTask(taskId, assignedTo, userId, username) {
    try {
        await axios.put(
            `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task/assign/${taskId}`,
        assignedTo,
        {
            headers: {
                'X-Task-AppId': TaskAppId,
                'X-Task-Key': TaskKey,
                'assignorId': userId,
                'assignorUsername': username,
            }
        }
        );
    } catch (error) {
        console.log(error);
        throw error;
    }
}

async function sendLogMessage(channel, reqBody, taskId, type, description) {
    try {
        const timestamp = getSingaporeTimestamp();

        const message = {
            userId: reqBody.userId,
            subGroupId: reqBody.subGroupId,
            taskId: taskId,
            type: type,
            description: description,
            timestamp: timestamp
        };

        await channel.publish(rabbitmq_exchange, rabbitmq_log_routing_key, Buffer.from(JSON.stringify(message)), { persistent: true });
        console.log(`Message sent to the exchange '${rabbitmq_exchange}' with routing key '${rabbitmq_log_routing_key}'.`);
    } catch (error) {
        console.log(error);
        throw error; 
    }
}

async function sendNotifications(channel, reqBody, taskId) {
    try {
        const formattedDate = formatDate(reqBody.dueDateTime);
        const taskURL = `http://localhost:5173/task/${taskId}`;

        for (i = 0; i < reqBody.assignedTo.length; i++) {
            const notifMsg = {
                recipient: reqBody.assignedTo[i].assigneeEmail,
                subject: '[TaskMaster] New Task Alert',
                body: `
                    Hello ${reqBody.assignedTo[i].assigneeUsername}!

                    A new task has been created by ${reqBody.username}:
                    Task Name: ${reqBody.taskName}
                    Description: ${reqBody.taskDesc}
                    Due On: ${formattedDate}
                    All assignees: ${reqBody.assignedTo.map(assignee => `${assignee.assigneeUsername}`).join(', ')}

                    You can login to view the task details here: ${taskURL}

                    Best regards,
                    TaskMaster
                `
            };

            await channel.publish(rabbitmq_exchange, rabbitmq_notif_routing_key, Buffer.from(JSON.stringify(notifMsg)), { persistent: true });
            console.log(`Message sent to RabbitMQ exchange '${rabbitmq_exchange}' with routing key '${rabbitmq_notif_routing_key}'.`);
        }
    } catch (error) {
        console.log(error);
        throw error; 
    }
}


function getSingaporeTimestamp() {
    const currentDate = new Date();
    const singaporeTimezone = 'Asia/Singapore'; // Singapore time zone
    const singaporeTime = currentDate.toLocaleString('en-US', { timeZone: singaporeTimezone });
    return singaporeTime;
}

function formatDate(dateString) {
    // Convert the input date string to a Date object
    const inputDate = new Date(dateString);

    // Format the date in the desired format
    const options = {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
        timeZone: 'Asia/Singapore' // Specify the time zone
    };
    const timeZoneOffset = -8 * 60; // Convert hours to minutes
    const adjustedDate = new Date(inputDate.getTime() + timeZoneOffset * 60 * 1000);

    return adjustedDate.toLocaleString('en-SG', options);
}

app.listen(PORT, () => {
    console.log(`Server is running on port http://0.0.0.0:${PORT}`);
});
