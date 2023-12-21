import asyncio
import os
import logging
from dotenv import load_dotenv
from vkbottle import API
from cover import CoverImage

load_dotenv()

TOKEN = os.getenv("TOKEN")
USER_ID = 516887792

api = API(TOKEN)
cover = CoverImage(api, USER_ID)

async def main() -> None:
    try:
        while True:
            await cover.draw_cover()
            await cover.upload_cover()
            await asyncio.sleep(600)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
