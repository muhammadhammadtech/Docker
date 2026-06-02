const request = require('supertest');
const { app, server } = require('./app');

describe('App Tests', () => {
    afterAll(() => {
        server.close();
    });

    test('GET / should return welcome message', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
        expect(response.body.message).toBe('Hello from Dockerized Node.js App!');
    });

    test('GET /health should return health status', async () => {
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('healthy');
    });
});
