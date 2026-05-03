const express = require('express');
const app = express();
const PORT = process.env.PORT || 3002;

app.use(express.json());

let products = [
    { id: 1, name: 'Laptop', price: 999.99, category: 'Electronics', stock: 50 },
    { id: 2, name: 'Smartphone', price: 699.99, category: 'Electronics', stock: 100 },
    { id: 3, name: 'Book', price: 19.99, category: 'Education', stock: 200 },
    { id: 4, name: 'Headphones', price: 149.99, category: 'Electronics', stock: 75 }
];

app.get('/health', (req, res) => res.json({ service: 'product-service', status: 'healthy', timestamp: new Date().toISOString() }));

app.get('/products', (req, res) => {
    let filtered = [...products];
    const { category, minPrice, maxPrice } = req.query;
    if (category) filtered = filtered.filter(p => p.category.toLowerCase() === category.toLowerCase());
    if (minPrice) filtered = filtered.filter(p => p.price >= parseFloat(minPrice));
    if (maxPrice) filtered = filtered.filter(p => p.price <= parseFloat(maxPrice));
    res.json({ success: true, data: filtered, count: filtered.length });
});

app.get('/products/:id', (req, res) => {
    const product = products.find(p => p.id === parseInt(req.params.id));
    if (!product) return res.status(404).json({ success: false, message: 'Product not found' });
    res.json({ success: true, data: product });
});

app.post('/products', (req, res) => {
    const { name, price, category, stock } = req.body;
    if (!name || !price || !category) return res.status(400).json({ success: false, message: 'Name, price, category required' });
    const newProduct = { id: products.length + 1, name, price: parseFloat(price), category, stock: parseInt(stock) || 0 };
    products.push(newProduct);
    res.status(201).json({ success: true, data: newProduct, message: 'Product created successfully' });
});

app.patch('/products/:id/stock', (req, res) => {
    const product = products.find(p => p.id === parseInt(req.params.id));
    if (!product) return res.status(404).json({ success: false, message: 'Product not found' });
    if (req.body.quantity !== undefined) product.stock = parseInt(req.body.quantity);
    res.json({ success: true, data: product, message: 'Stock updated successfully' });
});

app.listen(PORT, '0.0.0.0', () => console.log(`Product Service running on port ${PORT}`));
