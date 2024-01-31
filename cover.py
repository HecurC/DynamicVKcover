import logging
from io import BytesIO
from aiohttp import FormData, ClientSession

from vkbottle import API

import pendulum
from PIL import Image, ImageDraw, ImageFont


class CoverImage:
    WIDTH, HEIGHT = 1920, 768
    FILL = "#FFFFFF"
    STROKE_FILL = "#000000"
    FONT = "Cruinn.ttf"

    def __init__(self, api: API, user_id: int) -> None:
        self._api = api
        self._user_id = user_id

        self.buffer = None

    async def get_random_image(self, url) -> BytesIO:
        image_buffer = BytesIO()

        async with ClientSession() as session:
            response = await session.get(url)

            async for chunk in response.content.iter_chunked(1024):
                image_buffer.write(chunk)
        return image_buffer

    async def draw_cover(self, url) -> None:
        random_image = await self.get_random_image(url=url)

        img = Image.open(BytesIO(random_image.getvalue()))
        img = img.convert("RGBA").resize((self.WIDTH, self.HEIGHT))

        draw = ImageDraw.Draw(img)
        font_time = ImageFont.truetype(self.FONT, 200)
        font_date = ImageFont.truetype(self.FONT, 100)
        font_alert = ImageFont.truetype(self.FONT, 25)

        current_datetime = pendulum.now()
        current_time = current_datetime.strftime("%H:%M")
        formatted_date = current_datetime.to_formatted_date_string()

        draw.text(
            (self.WIDTH / 2, self.HEIGHT / 2), current_time, self.FILL, font_time, "ms", stroke_width=3,
            stroke_fill=self.STROKE_FILL
        )
        draw.text(
            (self.WIDTH / 2, self.HEIGHT / 2 + 100), formatted_date, self.FILL, font_date, "ms", stroke_width=3,
            stroke_fill=self.STROKE_FILL
        )
        draw.text(
            (self.WIDTH / 2 + 700, self.HEIGHT / 2 + 200), "Обложка меняется каждые 10 минут", self.FILL, font_alert,
            "ms", stroke_width=2,
            stroke_fill=self.STROKE_FILL
        )
        draw.text(
            (self.WIDTH / 2 + 700, self.HEIGHT / 2 + 170), "@bogdanihoor4", self.FILL,
            font_alert, "ms", stroke_width=2,
            stroke_fill=self.STROKE_FILL
        )
        draw.text(
            (self.WIDTH / 2 + 700, self.HEIGHT / 2 + 370), "Привет, человек с телефона!", self.FILL,
            font_alert, "ms", stroke_width=2,
            stroke_fill=self.STROKE_FILL
        )

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
