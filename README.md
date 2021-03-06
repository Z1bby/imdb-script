# imdb-script
Script that gets the top 250 movies from imdb and adds a random one of them to the firebase realtime database.
Movies from the database are accessible to user via flask application that runs in localhost:5000

### Installation:
To make sure all the required packages are installed, run the following command:
```
pip install requests beautifulsoup4 pyrebase flask flask-restful flask-sqlalchemy itsdangerous jinja2 markupsafe pytz six werkzeug sqlalchemy==1.3.18 PyJWT==1.7.1 urllib3
```

### Running script:
1.  To start the server server run:
    ```
    python server.py
    ```
2.  To add movies run in next terminal:
    ```
    python randomizer.py
    ```

### Instructions for use:
* randomizer.py
    * Make sure the server is running
    * To add a random movie type: `add`
    * To delete specific movie type: `delete <id>`
    * In order to exit type: `q`
  
* server.py
    * To view unprotected movies in your web browser go to localhost:5000/unprotected
    * In order to view all movies you need to login (user: user, password: pass)
        * Go to localhost:5000/login
        * After authorisation go to localhost:5000/protected

### Authentication details
Firebase database is public and doesn't require any authentication.

Authentication with flask /protected endpoint is established via tokens.

Tokens are generated each time after successful authentication in /login endpoint (user: user, password: pass), and are returned as a json structure `{"token" : <token_utf8>}`.

Token key is stored in session "SECRET_KEY", and algorithm used for encoding is HS256.

Token validation can be checked in https://jwt.io/. To do that, paste the token returned from /login to Encoded section, specify secret key in Decoded section, and make sure algorithm HS256 is selected.

After token is validated all data can be requested from /protected endpoint, where it's parsed to json from python dictionary.
