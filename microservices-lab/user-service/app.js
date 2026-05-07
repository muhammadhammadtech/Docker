const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

let users = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'customer' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'admin' }
];

app.get('/health', (req, res) => {
    res.json({ service: 'user-service', status: 'healthy', timestamp: new Date().toISOString() });
});

app.get('/users', (req, res) => res.json({ success: true, data: users, count: users.length }));
app.get('/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) return res.status(404).json({ success: false, message: 'User not found' });
    res.json({ success: true, data: user });
});
app.post('/users', (req, res) => {
    const { name, email, role } = req.body;
    if (!name || !email) return res.status(400).json({ success: false, message: 'Name and email required' });
    const newUser = { id: users.length + 1, name, email, role: role || 'customer' };
    users.push(newUser);
    res.status(201).json({ success: true, data: newUser, message: 'User created successfully' });
});

app.listen(PORT, '0.0.0.0', () => console.log(`User Service running on port ${PORT}`));
