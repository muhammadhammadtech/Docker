const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({
        message: 'Hello from Docker on Heroku!',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
    });
});

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        uptime: process.uptime(),
        memory: process.memoryUsage()
    });
});

app.get('/api/info', (req, res) => {
    res.json({
        app_name: process.env.APP_NAME || 'Heroku Docker App',
        version: '1.0.0',
        author: process.env.AUTHOR_NAME || 'Student Developer'
    });
});

app.get('/api/env', (req, res) => {
    res.json({
        app_name: process.env.APP_NAME || 'Default App Name',
        author: process.env.AUTHOR_NAME || 'Unknown Author',
        node_env: process.env.NODE_ENV || 'development',
        debug_mode: process.env.DEBUG_MODE || 'true',
        port: process.env.PORT || 3000,
        heroku_app_name: process.env.HEROKU_APP_NAME || 'Not set'
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
