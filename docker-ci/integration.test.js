const request = require('supertest');
const { app, server } = require('./app');

describe('Integration Tests', () => {
    afterAll(() => {
        server.close();
    });

    test('Application should start successfully', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
    });

    test('Health endpoint should return correct format', async () => {
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('status');
        expect(response.body).toHaveProperty('uptime');
        expect(typeof response.body.uptime).toBe('number');
    });

    test('Root endpoint should return timestamp', async () => {
        const response = await request(app).get('/');
        expect(response.body).toHaveProperty('timestamp');
        expect(new Date(response.body.timestamp)).toBeInstanceOf(Date);
    });

    test('Application should handle invalid routes', async () => {
        const response = await request(app).get('/nonexistent');
        expect(response.status).toBe(404);
    });
});
