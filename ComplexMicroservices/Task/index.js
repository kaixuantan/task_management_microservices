require('dotenv').config();

const express = require('express');
const cors = require('cors');
const axios = require('axios');

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
        // const assignees = {};
        // console.log(subGrpResponse.data.SubGroup.subGroupUsers)
        // subGrpResponse.data.SubGroup.subGroupUsers.forEach(assignee => {
        //     assignees[assignee.userId] = assignee.username;
        // });

        res.json(users);
    } catch (error) {
        // console.log(error.message)
        // sendLog(req.body.userId, 'Error retrieving assignees: ' + error.message);

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
                dueDate: req.body.dueDateTime,
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

        console.log(createTaskResponse)

        const taskId = createTaskResponse.data.TaskId;
        console.log(req.body.assignedTo)
        // const assigneeArray = req.body.assignedTo;
        
        // for (i = 0; i < assigneeArray.length; i++) {
            await axios.put(
                `https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/task/assign/${taskId}`,
                // [{
                //     // assigneeId: assigneeArray[i].userId,
                //     // assigneeUsername: assigneeArray[i].username
                //     assigneeId: assigneeArray[0].userId,
                //     assigneeUsername: assigneeArray[0].username
                // }], 
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
        // }

        res.status(201).json({ message: 'Task created successfully', taskId });

    } catch (error) {
        // sendLog(req.body.userId, 'Error creating task: ' + error.message);
        console.log(error)
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

// async function sendLog(userId, message) {
//     try {
//         await axios.post(`https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/log`, 
//         {
//             userId: userId,
//             type: "task",
//             description: message
//         },
//         {
//             headers: {
//                 'X-Log-AppId': LogAppId,
//                 'X-Log-Key': LogKey,
//             },
//         });
//     } catch (error) {
//         console.error('Error sending log to logging microservice:', error.message);
//     }
// }

app.listen(PORT, () => {
    console.log(`Server is running on port http://localhost:${PORT}`);
});
