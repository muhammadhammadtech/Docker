const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const app = express();
const PORT = process.env.PORT || 3000;

const limiter = rateLimit({ windowMs: 15*60*1000, max: 100 });
app.use(limiter);
app.use(express.json());

const services = {
    user: process.env.USER_SERVICE_URL || 'http://user-service:3001',
    product: process.env.PRODUCT_SERVICE_URL || 'http://product-service:3002',
    order: process.env.ORDER_SERVICE_URL || 'http://order-service:3003'
};

app.use('/api/users', createProxyMiddleware({ target: services.user, pathRewrite: {'^/api/users': '/users'}, changeOrigin: true }));
app.use('/api/products', createProxyMiddleware({ target: services.product, pathRewrite: {'^/api/products': '/products'}, changeOrigin: true }));
app.use('/api/orders', createProxyMiddleware({ target: services.order, pathRewrite: {'^/api/orders': '/orders'}, changeOrigin: true }));

app.get('/health', (req, res) => res.json({ service: 'api-gateway', status: 'healthy', timestamp: new Date().toISOString() }));
app.listen(PORT, '0.0.0.0', () => console.log(`API Gateway running on port ${PORT}`));
