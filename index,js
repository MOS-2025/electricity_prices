const express = require('express');
const app = express();

// Use the port Heroku provides, or default to 3000 locally
const PORT = process.env.PORT || 3000;

// Middleware (optional)
app.use(express.json());

// Home route
app.get('/', (req, res) => {
  res.send('Hello, Heroku! 🚀');
});

// Example API route
app.get('/api', (req, res) => {
  res.json({ message: 'This is your API response' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});