import eel
import bcrypt

from requests import post
from keyring import set_password, delete_password, get_password
from json import loads

from models import User
from settings import USERNAME, CURSOR


def set_auth():
    @eel.expose
    def reg(email, password, username):
        pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        resp = post(
            f"http://localhost:443/reg?email={email}&password={pwd}&username={username}"
        )
        info = loads(resp.content.decode("utf-8"))
        if resp.status_code == 200:
            set_password(
                service_name="Parser", username=USERNAME + "_pwd", password=password
            )
            set_password(
                service_name="Parser", username=USERNAME + "_ema", password=email
            )
        return info

    @eel.expose
    def login(email, password):
        resp = post(f"http://localhost:443/login?email={email}&password={password}")
        info = loads(resp.content.decode("utf-8"))
        print(info["text"])
        if resp.status_code == 200:
            if (
                get_password(service_name="Parser", username=USERNAME + "_pwd") is None
                or get_password(service_name="Parser", username=USERNAME + "_ema")
                is None
            ):
                set_password(
                    service_name="Parser", username=USERNAME + "_pwd", password=password
                )
                set_password(
                    service_name="Parser", username=USERNAME + "_ema", password=email
                )
        return info

    def auto_login():
        from settings import USERNAME

        name = USERNAME
        pwd = get_password(service_name="Parser", username=f"{name}_pwd")
        ema = get_password(service_name="Parser", username=f"{name}_ema")

        if ema is not None and pwd is not None:
            try:
                resp = login(email=ema, password=pwd)
                info = resp["user"]
                USER = User(
                    username=info["username"], email=info["email"], vk_id=info["vk_id"]
                )
                USERNAME = USER.username
            except Exception:
                print("Ошибка авторизации")

    @eel.expose
    def logout():
        delete_password(service_name="Parser", username=f"{USERNAME}_pwd")
        delete_password(service_name="Parser", username=f"{USERNAME}_ema")
        CURSOR.execute(f"UPDATE settings SET value = {None} WHERE title = username")

    auto_login()
