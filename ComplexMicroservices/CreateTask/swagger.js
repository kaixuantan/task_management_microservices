const swaggerJsdoc = require('swagger-jsdoc');

const swaggerDefinition = {
    openapi: '3.0.0',
    info: {
        title: 'CreateTask API',
        version: '1.0.0',
        description: 'CreateTask API Description',
    }
};

const options = {
    swaggerDefinition,
    apis: ['./index.js'] // Path to the API routes in your Node.js application
};

const specs = swaggerJsdoc(options);
module.exports = specs;