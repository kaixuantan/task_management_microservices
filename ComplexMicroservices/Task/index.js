const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;


app.get('/users', async (req, res) => {
    try {
        const headers = {
            'X-User-AppId': 'ifZ1JapLTp14J63bxoIr',
            'X-User-Key': '40KLo5jw8LSUOaeqHAY3EJC8REWEU1',
        };
    
        // fetch all users 
        const usersResponse = await axios.get('https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user', {
            headers, 
        });

        const users = {};
        usersResponse.data.User.forEach(user => {
            users[user.userId] = user.username;
        });

        res.json({ users });
    } catch (error) {
        console.error('Error creating task:', error.message);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});
  
app.get('/', (req, res) => {
    res.send('Welcome to Task Creation Complex Microservice');
});


app.listen(PORT, () => {
    console.log(`Server is running on port http://localhost:${PORT}`);
});
