import re
import random
import jaconv
import collections
from pykakasi import kakasi
import argparse

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser(description='オプションを取得')
parser.add_argument('-n', '--option', dest='quizSize', default='デフォルト値', help='オプションの説明')
parser.add_argument('-t', '--option1', dest='title', default='デフォルト値', help='オプションの説明')
args = parser.parse_args()

max = int(args.quizSize)
title = args.title+str(int(19-len(args.title))*" ")
width, height = B5
text_color=False
image = Image.new("RGB", (int(height), int(width)), "white")
draw = ImageDraw.Draw(image)

flie_pas='context.txt'
text=""
with open(flie_pas, 'r') as file:
    text = file.read()
question_templates=[f'{title}名前＝　　　　　　　＝',"　　　　　　　赤字を漢字に直せ︽必要なら送り仮名も書くこと︾"]
explanation_templates=[" ",f'{args.title} 解答例']
questions=[]
answers=[]

sentences=[]
questions=[]
answers=[]

# jfioewaffipawojeoiaj

kanji_list=[]
kanji_once=[]
quiz_candidate=[]
quiz=[]

kakasi_instance=kakasi()
def splitToSentences(context):
    context=context.replace(' ','')
    context=context.replace('\n','ע')
    context=context.replace('(','︽')
    context=context.replace('（','︽')
    context=context.replace(')','︾')
    context=context.replace('）','︾')
    context=context.replace('…','...')
    context=context.replace('\u3000', '')
    list_before=re.split(r'[ע\．，、 。！？,]', context)
    list_before=[text[:35] for text in list_before]
    list_after=[text for text in list_before if len(list_before)>3]
    return list_after
sentense_list=splitToSentences(text)

for word in kakasi_instance.convert(''.join(sentense_list)):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    if pattern.search(word['orig']):
        kanji_list.append(word['orig'])
        # kanji_list.append(re.sub(r'[^\u4e00-\u9fff]+', '',word['orig']))
kanji_list_detail=collections.Counter((kanji_list))

for kanji in kanji_list_detail.items():
    if(kanji[1]==1):
        kanji_once.append(kanji[0])
        
for kanji in kanji_once:
    for text in sentense_list:
        if(kanji in text):
            quiz_candidate.append(text)
quiz_candidate=list(set(quiz_candidate))

def kanji_word_mining(text):
    kanji_list=[]
    for word in kakasi_instance.convert(text):
        kanji_list.append(word['orig'])
    return list(filter(None, kanji_list))


for text in quiz_candidate:
    for context in kanji_word_mining(text):
        for kanji in kanji_once:
            if(kanji==context):
                for word in kakasi_instance.convert(text):
                    if(word['orig']==kanji):
                        quiz.append([text,word['kana'],kanji])
                break
        else:
            continue
        break
if(len(quiz)>=max):
    quiz_list=random.sample(quiz,max)
else:
    quiz_list=quiz
for context in quiz_list:
    questions.append(context[0].replace(context[2],"^"+context[1]+"^"))
    answers.append(context[0].replace(context[2],"^"+context[2]+"^"))
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

# 問題のpngを作成
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
x=340
image.save("question.png")

# 解答のpngを作成
image = Image.new("RGB", (int(height), int(width)), "white")
draw = ImageDraw.Draw(image)
x, y = 690, 10
for text in explanation_templates:
    y=20
    vertical_draw(text,16,x,y)
    x-=30
for i in range(0,len(questions)):
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
image.save("anser.png")

# ２枚のpngからpdfを生成する
c = canvas.Canvas("files/output.pdf", pagesize=(height, width))
c.drawImage("question.png", 0, 0, height, width)
c.showPage()
c.drawImage("anser.png", 0, 0, height, width)
c.showPage()
c.save()