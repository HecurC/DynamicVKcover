import re
import flet as ft
from flet import TextField, Container, Text, Markdown
import dotenv

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
    Md: Markdown = ft.Markdown(
        "1) Перейдите по ссылке: [vkhost](https://vkhost.github.io/)\n2) Авторизуйтесь и скопируйте содержимое адресной"
        "строки\n3) Вставьте его в "
        "строку\n",
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=openurl,

    )

    # Function

    async def send(e):
        try:
            realtoken = re.search(r'access_token=([^&]*)', Token.value).group(1)
            user_id = re.search(r'user_id=([^&]*)', Token.value).group(1)

            data = open('.env', 'w')
            data.write(f'TOKEN = "{realtoken}"\nUSERID = {user_id}')

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

        await page.update_async()

    sendbtt = ft.ElevatedButton("Применить!", on_click=send)

    await page.add_async(
        Md,
        Token,
        sendbtt
    )


ft.app(target=app)

if __name__ == '__main__':
    pass
