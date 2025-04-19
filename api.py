import hashlib
import aiohttp
import certifi
import time
import ssl

class API:
    def __init__(self):
        self.inUse = False
        self.lastUsed = None
        
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        
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

        try:
            result = await resp.json()
        except Exception as _:
            return False, "error", "login error", None
        
        if "msg" in result:
            if result["msg"] != "success":
                return False, "error", "login error", None
            else:
                return False, "success", "success", result
        else:
            return False, "error", "rate limited", None
        
    async def redeem_code(self, code: str, id: str) -> tuple[bool, str, str]:
        exit, counter, message, _ = await self.login_user(id)
        
        if exit:
            return exit, counter, message
        
        now = time.time_ns()
        
        resp = await self.session.post(
            url="https://wos-giftcode-api.centurygame.com/api/gift_code",
            data={
                "cdk": code, "fid": id, "time": now,
                "sign": hashlib.md5(f"cdk={code}&fid={id}&time={now}tB87#kPtkxqOS2".encode()).hexdigest()
            },
            headers=self.headers,
            timeout=30
        )
        
        try:
            result = await resp.json()
        except Exception as _:
            return True, "error", "unknown error"
        
        if result["err_code"] == 40014:
            return True, None, "gift code does not exist"
        elif result["err_code"] == 40007:
            return True, None, "gift code has expired"
        elif result["err_code"] == 40005:
            return True, None, "gift code has been fully claimed"
        elif result["err_code"] == 40008:
            return False, "already_claimed", "already claimed"
        elif result["err_code"] == 20000:
            return False, "successfully_claimed", "successfully claimed"
        else:
            return False, "error", "unknown error"