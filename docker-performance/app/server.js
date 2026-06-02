const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('OK - Fast endpoint\n');
  } else if (req.url === '/heavy') {
    // Simulate CPU work
    let sum = 0;
    for (let i = 0; i < 1000000; i++) sum += i;
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end(`OK - Heavy endpoint, sum=${sum}\n`);
  } else {
    res.writeHead(404);
    res.end('Not Found\n');
  }
});

server.listen(3000, '0.0.0.0', () => {
  console.log('Server running on port 3000');
});
