import logging
from io import BytesIO
from aiohttp import FormData, ClientSession

from vkbottle import API

import pendulum
from PIL import Image, ImageDraw, ImageFont


async def get_random_image(url) -> BytesIO:
    image_buffer = BytesIO()

    async with ClientSession() as session:
        response = await session.get(url)

        async for chunk in response.content.iter_chunked(1024):
            image_buffer.write(chunk)
    return image_buffer

class CoverImage:
    WIDTH, HEIGHT = 1920, 768
    FILL = "#FFFFFF"
    STROKE_FILL = "#000000"
    FONT = "Cruinn.ttf"

    def __init__(self, api: API, user_id: int) -> None:
        self._api = api
        self._user_id = user_id

        self.buffer = None

    async def draw_cover(self, url: str) -> None:
        random_image = await get_random_image(url=url)

        img = Image.open(BytesIO(random_image.getvalue())).convert("RGBA").resize((self.WIDTH, self.HEIGHT))

        draw = ImageDraw.Draw(img)
        font_time = ImageFont.truetype(self.FONT, 200)
        font_date = ImageFont.truetype(self.FONT, 100)
        font_alert = ImageFont.truetype(self.FONT, 25)

        current_datetime = pendulum.now()
        current_time = current_datetime.strftime("%H:%M")
        formatted_date = current_datetime.to_formatted_date_string()

        text_params = [
            ((self.WIDTH / 2, self.HEIGHT / 2), current_time, font_time, 3),
            ((self.WIDTH / 2, self.HEIGHT / 2 + 100), formatted_date, font_date, 3),
            ((self.WIDTH / 2 + 700, self.HEIGHT / 2 + 200), "Обложка меняется каждые 10 минут", font_alert, 2),
            ((self.WIDTH / 2 + 700, self.HEIGHT / 2 + 170), "@bogdanihoor4", font_alert, 2),
            ((self.WIDTH / 2 + 700, self.HEIGHT / 2 + 370), "Привет, человек с телефона!", font_alert, 2)
        ]

        for xy, text, font, stroke_width in text_params:
            draw.text(xy, text, self.FILL, font, "ms", stroke_width=stroke_width, stroke_fill=self.STROKE_FILL)

        self.buffer = BytesIO()
        img.save(self.buffer, "PNG")
        self.buffer.seek(0)

    async def upload_cover(self) -> None:
        upload_server = await self._api.request(
            "photos.getOwnerCoverPhotoUploadServer",
            dict(user_id=self._user_id, crop_width=self.WIDTH, crop_height=self.HEIGHT)
        )

        upload_url = upload_server["response"]["upload_url"]

        form_data = FormData()
        form_data.add_field("photo", self.buffer)

        async with ClientSession() as session:
            response = await session.post(upload_url, data=form_data)
            data = await response.json()

            await self._api.photos.save_owner_cover_photo(data["hash"], data["photo"])
