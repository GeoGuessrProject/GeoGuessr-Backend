const express = require('express');
const app = express();

app.use(express.json());

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (username === 'admin' && password === 'password') {
    return res.json({ success: true, token: 'mock-token' });
  }

  res.status(401).json({ success: false, message: 'Invalid credentials' });
});

app.listen(3000, () => {
  console.log('Login service running on port 3000');
});
