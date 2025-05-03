import ddddocr
import hashlib
import aiohttp
import certifi
import base64
import time
import ssl

class API:
    def __init__(self):
        self.inUse = False
        self.lastUsed = 0
        
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        
        self.ocr = ddddocr.DdddOcr(show_ad=False)
        
    async def init_session(self):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                ssl=ssl.create_default_context(cafile=certifi.where())
            )
        )
        
    async def login_user(self, id: str) -> tuple[bool, str, str, dict | None]:        
        now = time.time_ns()
        
        resp = await self.session.post(
            url="https://wos-giftcode-api.centurygame.com/api/player",
            data={
                "fid": id,
                "time": now,
                "sign": hashlib.md5(f"fid={id}&time={now}tB87#kPtkxqOS2".encode()).hexdigest()
            },
            headers=self.headers,
            timeout=30
        )
        
        now = time.time_ns()

        try:
            result = await resp.json()
        except Exception as _:
            return False, "error", "login error"
        
        if "msg" in result:
            if result["msg"] != "success":
                return False, "error", "login error", None
            else:
                return False, "success", "success", result
        else:
            return False, "error", "rate limited", None
        
    async def fetch_captcha(self, id: str) -> tuple[bool, bytes | None]:
        now = time.time_ns()
        
        captcha = await self.session.post(
            url="https://wos-giftcode-api.centurygame.com/api/captcha",
            data={
                "fid": id,
                "time": now,
                "init": 0,
                "sign": hashlib.md5(f"fid={id}&init=0&time={now}tB87#kPtkxqOS2".encode()).hexdigest()
            }
        )
        
        try:
            captcha_json = await captcha.json()
        except Exception as _:
            return True, None
        
        if captcha_json["err_code"] == 40100:
            return False, None
        elif captcha_json["err_code"] == 0:
            return True, base64.b64decode(captcha_json["data"]["img"].split(",", 1)[1])
        else:
            return False, None
        
    async def redeem_code(self, code: str, id: str) -> tuple[bool, str, str, dict]:
        exit, counter, message, player_data = await self.login_user(id)
        
        if exit:
            return exit, counter, message, None
        
        success, captcha_bytes = await self.fetch_captcha(id)
        
        if success:
            predicted_captcha = self.ocr.classification(captcha_bytes)
        else:
            return False, "error", "captcha error", None
        
        now = time.time_ns()
        
        resp = await self.session.post(
            url="https://wos-giftcode-api.centurygame.com/api/gift_code",
            data={
                "cdk": code, "fid": id, "time": now, "captcha_code": predicted_captcha,
                "sign": hashlib.md5(f"captcha_code={predicted_captcha}&cdk={code}&fid={id}&time={now}tB87#kPtkxqOS2".encode()).hexdigest()
            },
            headers=self.headers,
            timeout=30
        )
        
        try:
            result = await resp.json()
        except Exception as _:
            return True, "error", "unknown error", None
        
        if result["err_code"] == 40014:
            return True, None, "gift code does not exist", None
        elif result["err_code"] == 40007:
            return True, None, "gift code has expired", None
        elif result["err_code"] == 40005:
            return True, None, "gift code has been fully claimed", None
        elif result["err_code"] == 40008:
            return False, "already_claimed", "already claimed", player_data
        elif result["err_code"] == 20000:
            return False, "successfully_claimed", "successfully claimed", player_data
        elif result["err_code"] == 40103:
            return False, "error", "captcha error", None
        else:
            return False, "error", "unknown error", None