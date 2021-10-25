const crypto = require('crypto');
const express = require('express');

const app = express();
app.use(require('cookie-parser')());
app.use(require('body-parser').urlencoded({ extended: false }));

const clean = (str) => {
  return String(str).replace(/<|>/g);
};

// who needs a database anyway
const users = new Map();
users.set('admin', crypto.randomUUID());

const admins = new Set();
admins.add('admin');

app.use((req, _res, next) => {
  req.authState = {
    login: false,
    admin: false,
  };

  if (!req.cookies.token) return next();

  try {
    const { username, admin } = JSON.parse(atob(req.cookies.token));
    if (username && users.has(username)) req.authState.login = true;
    if (admin) req.authState.admin = true;
  } catch {}

  next();
});

app.get('/', (req, res) => {
  if (!req.authState.login) return res.redirect('/login');
  if (!req.authState.admin)
    return res.send(`
      You have logged in! Unfortunately, the flag is for admins only.
      <a href="/logout">Log Out</a>
    `);
  return res.send(process.env.FLAG);
});

app.get('/login', (req, res) => {
  if (req.authState.login) {
    return res.redirect('/');
  }
  res.send(`
    <h1>Log In</h1>
    <form method="POST" action="/login">
      <label for="username">Username</label>
      <input type="text" name="username" id="username" />
      <label for="password">Password</label>
      <input type="password" name="password" id="password" />
      <input type="submit" value="Submit" />
    </form>
    <h1>Register</h1>
    <form method="POST" action="/register">
      <label for="username">Username</label>
      <input type="text" name="username" id="username" />
      <label for="password">Password</label>
      <input type="password" name="password" id="password" />
      <input type="submit" value="Submit" />
    </form>
    <div class="message">
      ${clean(req.query.result ?? '')}
    </div>
  `);
});

app.get('/logout', (_req, res) => {
  res.clearCookie('token');
  return res.redirect('/login');
});

app.post('/login', (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);
  if (users.has(username) && users.get(username) == password) {
    res.cookie(
      'token',
      btoa(
        JSON.stringify({
          username,
          admin: false,
        })
      ),
      { expires: new Date(Date.now() + 900000), httpOnly: true }
    );
    return res.redirect('/');
  }
  return res.redirect('?result=Incorrect username or password!');
});

app.post('/register', (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);
  if (!users.has(username) && username.length > 1) {
    users.set(username, password);
    res.cookie(
      'token',
      btoa(
        JSON.stringify({
          username,
          admin: false,
        })
      ),
      { expires: new Date(Date.now() + 900000), httpOnly: true }
    );
    return res.redirect('/');
  }
  return res.redirect('/login?result=Username taken or invalid!');
});

app.listen(3000);
