from utils.core import create_sessions
from utils.telegram import Accounts
from utils.yescoin import Start
from data.config import hello
import asyncio


async def main():
    print(hello)
    action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n>'))

    if action == 2:
        await create_sessions()

    if action == 1:
        accounts = await Accounts().get_accounts()

        tasks = []
        for thread, account in enumerate(accounts):
            tasks.append(asyncio.create_task(Start(account=account, thread=thread).main()))

        await asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

