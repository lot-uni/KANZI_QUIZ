import re
import random
import jaconv
import pykakasi

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas

width, height = B5
text_color=False
image = Image.new("RGB", (int(height), int(width)), "white")
draw = ImageDraw.Draw(image)

text=""
flie_pas='context.txt'
text=""
with open(flie_pas, 'r') as file:
    text = file.read()
question_templates=["漢字書き取りテスト 学年　　クラス　　名前＝　　　　　　　＝","　　　　　　　　　　赤字のカタカナを漢字に直せ"]
explanation_templates=["漢字書き取りテスト解答例"]
questions=[]
answers=[]

sentences=[]
questions=[]
answers=[]
sign=r'[\u4e00-\u9fa5]'
kks = pykakasi.kakasi()


def create_question(content):
    word_list = []
    kangi_list = []
    result = kks.convert(content)
    for item in result:
        word_list.append(item["orig"])
    for item in word_list:
        if re.findall(sign,item)!=[]:
            kangi_list.append(item)
    random.shuffle(kangi_list)
    word = kangi_list[0]
    hira = kks.convert(word)[0]["hira"]
    kangi_yomi = re.sub('[一-龥]','',word)
    kangi_yomi = '^'+jaconv.hira2kata(re.sub(kangi_yomi,'',hira))+'^'
    word = re.sub(u'[ぁ-んァ-ン]','',word)
    return re.sub(word,kangi_yomi,content),word

def splitToSentences(text):
    text=text.replace(' ','')
    text=text.replace('\n','ע')
    text=text.replace('(','︽')
    text=text.replace('（','︽')
    text=text.replace(')','︾')
    text=text.replace('）','︾')
    text=text.replace('…','...')
    text=text.replace('\u3000', '')
    sentences = re.split(r'[ע\．，、 。！？,]', text)
    return sentences
def judge(text):
    pattern = re.compile(sign)
    return bool(pattern.search(text))

sample=splitToSentences(text)
for i in sample:
    if judge(i):
        sentences.append(i[:35])

if len(sentences)<10:
    sentences=random.sample(sentences,len(sentences))
else:
    sentences=random.sample(sentences,10)
for text in sentences:
    hoge=create_question(text)
    questions.append(hoge[0])
    answers.append(hoge[1])
def vertical_draw(text,size,x,y):
    font = ImageFont.truetype("fonts/GenShinGothic-Light.ttf", size)
    vertical_text = "\n".join(text)
    for line in vertical_text.split("\n"):
        draw.text((x, y), line, fill="black", font=font)
        y += size

def color_draw(character,size,x,y):
    font = ImageFont.truetype("fonts/GenShinGothic-Light.ttf", size)
    if text_color:
        draw.text((x, y),character, fill="red", font=font)
    else:
        draw.text((x, y),character, fill="black", font=font)
    y += size
    return y


x, y = 690, 10

for text in question_templates:
    vertical_draw(text,16,x,y)
    x-=30
for i in range(0,len(questions)):
    y=20
    x-=25
    text=questions[i]
    y=color_draw(str(i+1),12,x+3,y)
    y+=8
    for character in text:
        if character=="^":
            text_color=not text_color
        else:
            y=color_draw(character,12,x,y)

draw.line((360, 0, 360, 499),fill=(10),width=1)
x=340
for text in explanation_templates:
    y=20
    vertical_draw(text,16,x,y)
    x-=30
for i in range(0,len(answers)):
    y=20
    x-=25
    text=answers[i]
    y=color_draw(str(i+1),12,x+3,y)
    y+=8
    for character in text:
        if character=="^":
            text_color=not text_color
        else:
            y=color_draw(character,12,x,y)
print(questions)
print(answers)
image.save("output.png")
c = canvas.Canvas("files/output.pdf", pagesize=(height,width))
c.drawImage("output.png", 0, 0)
c.showPage()
c.save()