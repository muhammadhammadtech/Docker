const express = require('express');
const os = require('os');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    message: 'Hello from Cross-Platform Docker!',
    platform: os.platform(),
    architecture: os.arch(),
    hostname: os.hostname(),
    uptime: os.uptime()
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Platform: ${os.platform()}`);
  console.log(`Architecture: ${os.arch()}`);
});
