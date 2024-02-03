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


async def main():
    while True:
        try:
            await cover.draw_cover(url="https://minimalistic-wallpaper.demolab.com/?random")
        except Exception as e:
            print(f"An error occured: {e}")
            await cover.draw_cover(url="https://imgbly.com/ib/paOsXGoMl4.png")

        await cover.upload_cover()
        await asyncio.sleep(600)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
