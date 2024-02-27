import re
import flet as ft
from flet import TextField, Container, Text

async def main(page: ft.Page):
    page.title = "Dynamic VK covers"
    page.theme_mode = ft.ThemeMode.DARK

    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

# Variables

    Token: TextField = ft.TextField(
        label="URL-ссылка",
        text_align=ft.TextAlign.LEFT,
        width=500,
        border_radius=17,
        hint_text="Вставьте ссылку..."
    )
    Instruction: Text = ft.Text(
        "1) Перейдите по ссылке: {0}\n2) Авторизуйтесь и скопируйте содержимое адресной строки\n3) Вставьте его в "
        "строку\n".format(())
    )


# Function

    async def send(e):
        try:
            # await CoverImage.draw_cover()
            # await CoverImage.upload_cover()
            realtoken = re.search(r'access_token=([^&]*)', Token.value).group(1)
            user_id = re.search(r'user_id=([^&]*)', Token.value).group(1)
            print(f"{realtoken}\n{user_id}")
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
        Instruction,
        Token,
        sendbtt
    )

ft.app(target=main)
