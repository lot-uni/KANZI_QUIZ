from pykakasi import kakasi
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas

import collections
import argparse
import re
import random
import pandas as pd

# オプションの内容を取得
parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', dest='quizSize', default='作成問題数')
parser.add_argument('-t', dest='title', default='問題のタイトル')
parser.add_argument('-l', dest='level', default='問題レベル')
args = parser.parse_args()

# 問題生成とpdfを作成する
with open('context.txt', 'r') as file:
    text = file.read()
    file.close()

# 必要な変数を定義
question_templates=[f'{args.title}　学年　クラス　名前＝　　　　　　　＝',"　　　　　　　赤字を漢字に直せ︽必要なら送り仮名も書くこと︾"]
explanation_templates=[" ",f'{args.title} 解答例']
questions=[]
answers=[]

kanji_list=[]
quiz_pool=[]
quiz=[]

level1=[]
level2=[]
level3=[]

max = int(args.quizSize)
title = args.title+str(int(19-len(args.title))*" ")
width, height = B5
text_color=False
image = Image.new("RGB", (int(height), int(width)), "white")
draw = ImageDraw.Draw(image)

text_color=False

sentence_list=re.split(r'[ע\．，、 。！？,]', text)# textのデータを整形する←要改善、自然に文章を具切るにはどうしたらいいのか？
sentence_list=[text for text in sentence_list if len(text)>4]
sentence_list=[text[:30] for text in sentence_list]

text=text.replace(' ','')
text=text.replace('\n','ע')
text=text.replace('(','︽')
text=text.replace('（','︽')
text=text.replace(')','︾')
text=text.replace('）','︾')
text=text.replace('…','...')
text=text.replace('\u3000', '')


# 漢字の含まれた単語を抽出
kakasi_instance=kakasi()
for word in kakasi_instance.convert(''.join(sentence_list)):
    if re.search(r'[\u4e00-\u9fa5]',word['orig']):
        kanji_list.append(word['orig'])

# 漢字のレベルを判定する
kanji_list_detail=collections.Counter((kanji_list))
df=pd.read_csv('json/kyoiku-kanji-2017.csv')
for k in kanji_list_detail:
    kanji_level_scores=[]
    for item in list(k):
        df_kanji=df[df["Kanji"].str.contains(item)]
        if(df_kanji.empty):
            kanji_level_scores.append(7)#
        else:
            kanji_level_scores.append(int(df_kanji["Grade_2017"].values))
    if(kanji_level_scores>=[7]):
        level3.append(k)
    elif(kanji_level_scores<=[1,2]):
        level1.append(k)
    else:
        level2.append(k)
if(args.level=="1"):
    for i in level3:
        kanji_list_detail.pop(i)
    for i in level2:
        kanji_list_detail.pop(i)
elif(args.level=="2"):
    for i in level1:
        kanji_list_detail.pop(i)
    for i in level3:
        kanji_list_detail.pop(i)
elif(args.level=="3"):
    for i in level3:
        kanji_list_detail.pop(i)
elif(args.level=="4"):
    for i in level1:
        kanji_list_detail.pop(i)
    for i in level2:
        kanji_list_detail.pop(i)

kanji_list=[]
for kanji in kanji_list_detail.items():
    if(kanji[1]==1):
        kanji_list.append(kanji[0])
for kanji in kanji_list:
    for text in sentence_list:
        if(kanji in text):
            quiz_pool.append(text)
quiz_pool=list(set(quiz_pool))

def kanji_word_mining(text):
    word_list=[]
    for word in kakasi_instance.convert(text):
        word_list.append(word['orig'])
    return list(filter(None, word_list))


for text in quiz_pool:
    for context in kanji_word_mining(text):
        for kanji in kanji_list:
            if(kanji==context):
                for word in kakasi_instance.convert(text):
                    if(word['orig']==kanji):
                        quiz.append([text,word['kana'],kanji])
                break
        else:
            continue
        break
if(len(quiz)>max):
    quiz_list=random.sample(quiz,max)
else:
    quiz_list=random.sample(quiz,len(quiz))

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