from io import BytesIO
# import xlrd
from sys import argv
import vk_api
from PIL import Image, ImageFont, ImageDraw
from vk_api.longpoll import VkLongPoll

# import asyncio

script, first = argv

top_groupa = first
dirr = ''
# dirr = '/home/sammy/bot/'
img = Image.open(dirr + 'Untitled.png')

draw = ImageDraw.Draw(img)

fnt = ImageFont.truetype(dirr + "20327.ttf", 200)
Ww, Hh = img.size
w, h = draw.textsize("Расписание", font=fnt)

draw.text(((Ww-w)/2, 140), "Расписание", font=fnt, fill=(255, 255, 255))


fnt = ImageFont.truetype(dirr + "20327.ttf", 80)
w, h = draw.textsize("Самая крутая группа: " + top_groupa, font=fnt)

draw.text(((Ww-w)/2, Hh-150), "Самая крутая группа: " + top_groupa, font=fnt, fill=(0, 0, 0))

buf = BytesIO()
img.save(buf, 'PNG')
buf.seek(0)
image_bytes = buf.read()
buf.close()


vk_session = vk_api.VkApi(token="e2ea1be79721ff8ca20375322c2f996e376a28c0338fc228e64dc8cd2bbdf7cdeaad1ec9428ff0ad10fd6")
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

upload = vk_api.VkUpload(vk)



upload.photo_cover(photo=BytesIO(image_bytes), group_id=191083341, crop_x=0, crop_y=0, crop_x2=1590, crop_y2=530)
