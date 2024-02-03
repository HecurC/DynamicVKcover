@echo off

chcp 65001

@echo Ожидайте!

@echo 3агружаю aiohttp!
pip install aiohttp==3.8.6

@echo 3агружаю pendulum!
pip install pendulum==2.1.2

@echo 3агружаю pillow!
pip install Pillow==10.0.1

@echo 3агружаю dotenv!
pip install python-dotenv==1.0.0

@echo 3агружаю vkbottle!
pip install vkbottle==4.3.12

@echo 3агружаю код!

python main.py

sleep 30

@echo НАСЛАЖДАЙТЕСЬ!

rem ну и говнокод...