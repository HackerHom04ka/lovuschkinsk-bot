from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests

def drawText(shablondraw, text, y, x=0):
    font = ImageFont.truetype("passportsr/19539.ttf", 100)
    shablondraw.text((1100 + x, y), text, (0, 0, 0), font=font)

def ImageOpenURL(url):
    response = requests.get(url, stream=True).raw
    return response

def createPassport(Name, Surname, Middlename, Gender, Data_of_Birth, Place_of_Birth, Place_of_residence, Nation, Sexsual_Orientation, Photo=None):
    # Image Open
    shablon = Image.open('passportsr/shablon1.png')
    shablondraw = ImageDraw.Draw(shablon)
    #Text
    drawText(shablondraw, Name, 1290)
    drawText(shablondraw, Surname, 1290)
    drawText(shablondraw, Middlename, 1490)
    drawText(shablondraw, Gender, 1590)
    drawText(shablondraw, Data_of_Birth, 1690)
    drawText(shablondraw, Place_of_Birth, 1790)
    drawText(shablondraw, Place_of_residence, 1890)
    drawText(shablondraw, Nation, 1990)
    drawText(shablondraw, Sexsual_Orientation, 2090, 70)
    # Add Photo
    Photo = Image.open(ImageOpenURL(Photo))
    Photo = Photo.resize((657, 845))
    shablon.paste(Photo, (120, 1319))
    # Return Image
    shablon.save('passportsr/passport.jpg')
    img = open('passportsr/passport.jpg', 'rb')
    return img
