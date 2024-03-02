import asyncio
import re
import os
import flet as ft
from flet import TextField, Container, Text, Markdown, ElevatedButton
import dotenv


def app(page: ft.Page):
    page.title = "Dynamic VK covers"
    page.theme_mode = ft.ThemeMode.DARK

    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

    def openurl(e):
        page.launch_url_async(e.data)

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
    def send(e):
        try:
            realtoken = re.search(r'access_token=([^&]*)', Token.value).group(1)
            user_id = Userid.value

            data = open('.env', 'w')
            data.write(f'TOKEN={realtoken}\nUSERID={user_id}')
            data.close()

            exec(open("main.py").read())

            success = ft.Text("Успешно!")
            page.snack_bar = ft.SnackBar(ft.Text(success.value))
            page.snack_bar.bgcolor = "#78DBE2"
            page.snack_bar.open = True

        except Exception as e:
            print(e)
            page.snack_bar = ft.SnackBar(ft.Text(str(e)))
            page.snack_bar.bgcolor = "#ffa500"
            page.snack_bar.open = True

        page.update()

    sendbtt = ft.ElevatedButton("Применить!", on_click=send)

    page.add(
        Md,
        Userid,
        Token,
        sendbtt,
        Reset
    )


ft.app(target=app)
