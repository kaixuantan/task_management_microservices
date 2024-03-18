require('dotenv').config();

const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const PORT = process.env.PORT;
const SubGrpAppId = process.env.SubGrpAppId;
const SubGrpKey = process.env.SubGrpKey;
const TaskAppId = process.env.TaskAppId;
const TaskKey = process.env.TaskKey;
const LogAppId = process.env.LogAppId;
const LogKey = process.env.LogKey;

app.get('/subgroup/:subGroupId', async (req, res) => {
    try {
        const subGroupId = req.params.subGroupId;
    
        const subGrpResponse = await axios.get(`https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/${subGroupId}`, {
            headers: {
                'X-SubGroup-AppId': SubGrpAppId,
                'X-SubGroup-Key': SubGrpKey,
            }
        });

        const assignees = {};
        subGrpResponse.data.SubGroup.subGroupUsers.forEach(assignee => {
            assignees[assignee.userId] = assignee.username;
        });

        res.json(assignees);
    } catch (error) {
        // console.log(error.message)
        sendLog(req.body.userId, 'Error retrieving assignees: ' + error.message);

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
        await axios.post(
            `https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/task`,
            {
                name: req.body.taskName,
                subGroupId: req.body.subGroupId,
                createdById: req.body.userId,
                assigneeId: req.body.assigneeId
            }, 
            {
                headers: {
                    'X-Task-AppId': TaskAppId,
                    'X-Task-Key': TaskKey,
                }
            }
        );

        res.status(201).json({ message: 'Task created successfully' });
    } catch (error) {
        sendLog(req.body.userId, 'Error creating task: ' + error.message);

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

async function sendLog(userId, message) {
    try {
        await axios.post(`https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/log`, 
        {
            userId: userId,
            type: "task",
            description: message
        },
        {
            headers: {
                'X-Log-AppId': LogAppId,
                'X-Log-Key': LogKey,
            },
        });
    } catch (error) {
        console.error('Error sending log to logging microservice:', error.message);
    }
}

app.listen(PORT, () => {
    console.log(`Server is running on port http://localhost:${PORT}`);
});
