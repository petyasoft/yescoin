from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
from utils.core import logger

from fake_useragent import UserAgent
from pyrogram import Client
from data import config

import random
import aiohttp
import asyncio


class Start:
    def __init__(self, thread: int, account: str):
        self.thread = thread
        self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR)

        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True)

        self.token = None

    async def main(self):
        while True:
            try:
                await asyncio.sleep(random.uniform(config.ACC_DELAY[0], config.ACC_DELAY[1]))

                tg_web_data = await self.get_tg_web_data()
                await self.login(tg_web_data=tg_web_data)
                answer = await self.claim()
                if answer == True:
                    while answer:
                        answer = await self.claim()
                sleep_time = random.randint(60*10,60*20)
                logger.info(f"Поток {self.thread} | уснул на {sleep_time} сек")
                await asyncio.sleep(random.randint(60*10,60*20))
            except Exception as e:
                logger.error(f"Поток {self.thread} | Ошибка: {e}")

    async def get_tg_web_data(self):
        await self.client.connect()

        await self.client.send_message(chat_id="theYescoin_bot", text="/start")
        await asyncio.sleep(random.randint(5,10))

        web_view = await self.client.invoke(RequestWebView(
            peer=await self.client.resolve_peer('theYescoin_bot'),
            bot=await self.client.resolve_peer('theYescoin_bot'),
            platform='android',
            from_bot_menu=False,
            url='https://www.yescoin.gold'
        ))
        auth_url = web_view.url
        await self.client.disconnect()
        return unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

    async def login(self, tg_web_data):
        json_data = {"code": tg_web_data}
        resp = await self.session.post("https://api.yescoin.gold/user/login", json=json_data)

        resp_json = await resp.json()
        self.session.headers['token']=resp_json['data']["token"]
    
    async def claim(self):
        count = random.randint(20,85)
        response = await self.session.post('https://api.yescoin.gold/game/collectCoin',json=count)
        text = await response.json()
        await asyncio.sleep(random.randint(3,6))
        if text['code'] == 0:
            return True
        else:
            return False
