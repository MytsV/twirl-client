# How to run

1) Clone this repo
2) Create an .env file:
```dotenv
AUTH_URL=http://<ip>:<port>
UDP_ADDRESS=<ip>
UDP_PORT=<ip>
LOCATION_ID=<id>
```
Please specify your server's settings and a desired location ID.
3) Populate assets/songs with mp3's relevant to the DB
4) `pip install -r requirements.txt`
5) `python main.py`