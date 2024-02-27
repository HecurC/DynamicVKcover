import asyncio
import logging
import re
from dotenv import load_dotenv
from vkbottle import API
from cover import CoverImage
# import app

load_dotenv()

async def main(Token):
    realtoken = re.search(r'access_token=([^&]*)', Token.value).group(1)
    user_id = re.search(r'user_id=([^&]*)', Token.value).group(1)
    print(realtoken, user_id)

    TOKEN = realtoken
    USER_ID = user_id
    api = API(TOKEN)
    cover = CoverImage(api, USER_ID)

    while True:
        try:
            await cover.draw_cover(url="https://minimalistic-wallpaper.demolab.com/?random")
        except Exception as e:
            print(f"An error occurred while drawing the cover: {e}")
            await cover.draw_cover(url="https://imgbly.com/ib/paOsXGoMl4.png")
        try:
            await cover.upload_cover()
        except Exception as e:
            print(f"An error occurred while uploading the cover: {e}")

        await asyncio.sleep(600)


if __name__ == "__main__":
    logging.basicConfig()
    Token = app.Token
    asyncio.run(main(Token))
