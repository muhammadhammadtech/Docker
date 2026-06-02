const express = require('express');
const os = require('os');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send(`
    <h1>Hello from AKS</h1>
    <p>Hostname: ${os.hostname()}</p>
    <p>Time: ${new Date().toISOString()}</p>
  `);
});

app.get('/health', (req, res) => {
  res.json({ status: "healthy" });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

