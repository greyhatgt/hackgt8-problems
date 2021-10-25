const crypto = require('crypto');
const express = require('express');
const db = require('better-sqlite3')('sqlite3.db');

const clean = (str) => {
  return String(str).replace(/<|>/g);
};

// 512 for security :0
const encrypt = (data) =>
  crypto.createHash('sha512').update(data).digest('hex');

// clear the database when the app starts
db.exec(`DROP TABLE IF EXISTS users;`);

// set up the single table
db.exec(`CREATE TABLE users(
  username TEXT,
  password TEXT
);`);

// create the admin account
const username = encrypt('admin');
const password = encrypt((test = crypto.randomUUID()));

db.exec(`INSERT INTO users (
  username, password
) VALUES (
  '${username}', '${password}'
)`);

const app = express();
app.use(require('body-parser').urlencoded({ extended: false }));

app.post('/login', (req, res) => {
  const username = req.body.username ?? '';
  const password = req.body.password ?? '';

  // prevent shenanigans
  if (username.includes(`'`))
    return res.redirect('/?result=Username contains illegal characters!');
  if (password.includes(`'`))
    return res.redirect('/?result=Password contains illegal characters!');

  try {
    const result = db
      .prepare(
        `SELECT * FROM users WHERE
         username = '${username}' AND
         password = '${password}'`
      )
      .get();
    if (result) return res.redirect(`/?result=${process.env.FLAG}`);
    else return res.redirect('/?result=Incorrect username or password!');
  } catch {
    return res.redirect('/?result=There was a problem with your query.');
  }
});

app.get('/', (req, res) => {
  res.send(`
    <div class="container">
      <h1>Log In</h1>
      <form>
        <label for="username">Username</label>
        <input type="text" name="username" id="username" />
        <label for="password">Password</label>
        <input type="password" name="password" id="password" />
        <input type="submit" value="Submit" />
      </form>
      <div class="message">${clean(req.query.result ?? '')}</div>
    </div>
    <script>
      (async() => {
        await new Promise((resolve) => (
          window.addEventListener('load', resolve)
        ));

        const encrypt = async (text) => {
          const data = new TextEncoder().encode(text);
          const hash = [...new Uint8Array(
            await crypto.subtle.digest('SHA-512', data)
            )].map(b => b.toString(16).padStart(2, '0'))
            .join('');
          return hash;
        }

        document
          .querySelector('form')
          .addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = document.createElement('form');
            form.setAttribute('action', '/login');
            form.setAttribute('method', 'POST');

            await Promise.all(Array.from(new FormData(e.target))
              .map(async ([k, v]) => {
                const input = document.createElement('input');
                input.setAttribute('name', k);
                input.setAttribute('value', await encrypt(v));
                form.appendChild(input);
              }));

            form.setAttribute('style', 'display: none');
            document.body.appendChild(form);
            form.submit();
          });
      })();
    </script>
    <style>
      * {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
        Roboto, 'Helvetica Neue', sans-serif;
        box-sizing: border-box;
      }

      html,
      body {
        margin: 0;
      }

      .container {
        padding: 2rem;
        width: 90%;
        max-width: 900px;
        margin: auto;
      }

      input:not([type='submit']) {
        width: 100%;
        padding: 8px;
        margin: 8px 0;
      }

      input[type='submit'] {
        margin-bottom: 16px;
      }
    </style>
  `);
});

app.listen(3000);
