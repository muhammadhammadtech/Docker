const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.json({ message: "Hello CI/CD", version: "1.0.0" });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: "healthy" });
});

app.listen(port, () => console.log("Running on port 3000"));
