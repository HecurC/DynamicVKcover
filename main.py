import asyncio
import re
import os
import flet as ft
from flet import TextField, Container, Text, Markdown, ElevatedButton
import dotenv
from dotenv import load_dotenv
from vkbottle import API
from cover import CoverImage

load_dotenv()

TOKEN = os.getenv("TOKEN")
USER_ID = os.getenv("USERID")
api = API(TOKEN)
cover = CoverImage(api, USER_ID)

async def app(page: ft.Page):
    page.title = "Dynamic VK covers"
    page.theme_mode = ft.ThemeMode.DARK

    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

    async def openurl(e):
        await page.launch_url_async(e.data)

    # Variables

    Token: TextField = ft.TextField(
        label="URL-ссылка",
        text_align=ft.TextAlign.LEFT,
        width=500,
        border_radius=17,
        hint_text="Вставьте ссылку..."
    )
    Userid: TextField = ft.TextField(
        label="ID приложения",
        text_align=ft.TextAlign.LEFT,
        width=500,
        border_radius=17,
        hint_text="Вставьте ID приложения..."
    )
    Md: Markdown = ft.Markdown(
        "1) Перейдите по ссылке: [vkhost](https://vkhost.github.io/)\n"
        "2) Выберите пункт Настройки\n"
        "3) Скопируйте и вставьте содержимое пункта ID приложения\n"
        "4) Авторизуйтесь и скопируйте/вставьте содержимое адресной строки",
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=openurl
    )
    Reset: ElevatedButton = ft.ElevatedButton(
        "Сбросить настройки",
        on_click=lambda e: open('.env', 'w').close()
    )

    # Function
    async def send(e):
        try:
            realtoken = re.search(r'access_token=([^&]*)', Token.value).group(1)
            user_id = Userid.value

            data = open('.env', 'w')
            data.write(f'TOKEN={realtoken}\nUSERID={user_id}')
            data.close()

            success = ft.Text("Успешно!")
            page.snack_bar = ft.SnackBar(ft.Text(success.value))
            page.snack_bar.bgcolor = "#78DBE2"
            page.snack_bar.open = True

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

        except Exception as e:
            print(e)
            page.snack_bar = ft.SnackBar(ft.Text(str(e)))
            page.snack_bar.bgcolor = "#ffa500"
            page.snack_bar.open = True

        await page.update_async()

    sendbtt = ft.ElevatedButton("Применить!", on_click=send)

    await page.add_async(
        Md,
        Userid,
        Token,
        sendbtt,
        Reset
    )


ft.app(target=app)
