import bcrypt
import eel
from keyring import get_password, delete_password

from app.settings import settings
from front.auth import login
from requests import post


@eel.expose
def сhange_pwd(old, new):
    ema = get_password(service_name="Parser", username=f"{settings.USERNAME}_ema")
    resp = login(ema, old)
    if len(resp) == 2:
        pwd = bcrypt.hashpw(new.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        resp = post(f"http://localhost:80/change_pwd?email={ema}&password={pwd}")
        # delete_password()
