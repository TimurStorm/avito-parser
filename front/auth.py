import eel
import bcrypt
from requests import post


@eel.expose
def reg(email, password, username):
    pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    resp = post(f"http://localhost:80/reg?email={email}&password={pwd}&username={username}")
    return resp


@eel.expose
def login(email, password):
    resp = post(f"http://localhost:80/login?email={email}&password={password}")
    return resp