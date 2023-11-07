import re
import random
import jaconv
import pykakasi
from pykakasi import kakasi

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas


num_quiz = 10
flie_pas='context.txt'
words_list=[]
with open(flie_pas, 'r') as file:
    text = file.read()
def judge(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))
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

kakasi_instance = kakasi()
kana_text = kakasi_instance.convert(text)

sentences=list(filter(None,splitToSentences(text)))
# sentences=random.sample(sentences,num_quiz)
sentences_detail=kakasi_instance.convert(''.join(sentences))
for word in sentences_detail:
    if judge(word['orig']):
        words_list.append(re.sub(r'[^\u4e00-\u9fff]+', '',word['orig']))
words_list=list(set(words_list))
delete_list=[]
# for i in range(0,len(words_list)):
#     c=0
#     for sentence in sentences:
#         if(words_list[i] in sentence):
#             c+=1
#     if(c!=1):
#         delete_list.append(words_list[i])
# for word in delete_list:
#     words_list.remove(word)
# print(sentences,random.sample(words_list,10))
for text in sentences:
    for i in range(0,len(words_list)):
        if(words_list[i] in text):
            print(words_list[i],text)
random.sample(words_list,10)
# question_templates=[f'{title}名前＝　　　　　　　＝',"　　　　　　　　　　赤字のカタカナを漢字に直せ"]
# explanation_templates=[" ","解答例"]
# questions=[]
# answers=[]

# sentences=[]
# questions=[]
# answers=[]
# sign=r'[\u4e00-\u9fa5]'
# kks = pykakasi.kakasi()

# def create_question(content):
#     word_list = []
#     kangi_list = []
#     result = kks.convert(content)
#     for item in result:
#         word_list.append(item["orig"])
#     for item in word_list:
#         if re.findall(sign,item)!=[]:
#             kangi_list.append(item)
#     random.shuffle(kangi_list)
#     word = kangi_list[0]
#     hira = kks.convert(word)[0]["hira"]
#     kangi_yomi = re.sub('[一-龥]','',word)
#     kangi_yomi = '^'+jaconv.hira2kata(re.sub(kangi_yomi,'',hira))+'^'
#     word = re.sub(u'[ぁ-んァ-ン]','',word)
#     return re.sub(word,kangi_yomi,content),word

# def splitToSentences(text):
#     text=text.replace(' ','')
#     text=text.replace('\n','ע')
#     text=text.replace('(','︽')
#     text=text.replace('（','︽')
#     text=text.replace(')','︾')
#     text=text.replace('）','︾')
#     text=text.replace('…','...')
#     text=text.replace('\u3000', '')
#     sentences = re.split(r'[ע\．，、 。！？,]', text)
#     return sentences
# def judge(text):
#     pattern = re.compile(sign)
#     return bool(pattern.search(text))

# sample=splitToSentences(text)
# for text in sample:
#     short_text=text[:35]
#     if judge(short_text):
#         sentences.append(short_text)
# print(sentences)


# if len(sentences)<max:
#     sentences=random.sample(sentences,len(sentences))
# else:
#     sentences=random.sample(sentences,max)
# for text in sentences:
#     hoge=create_question(text)
#     questions.append(hoge[0])
#     answers.append(hoge[1])



# fジェウィ青jフィオアwジオfjわおいjフィオウェア女fjえわおいじ
# def vertical_draw(text,size,x,y):
#     font = ImageFont.truetype("fonts/GenShinGothic-Light.ttf", size)
#     vertical_text = "\n".join(text)
#     for line in vertical_text.split("\n"):
#         draw.text((x, y), line, fill="black", font=font)
#         y += size

# def color_draw(character,size,x,y):
#     font = ImageFont.truetype("fonts/GenShinGothic-Light.ttf", size)
#     if text_color:
#         draw.text((x, y),character, fill="red", font=font)
#     else:
#         draw.text((x, y),character, fill="black", font=font)
#     y += size
#     return y


# x, y = 690, 10
# for text in explanation_templates:
#     y=20
#     vertical_draw(text,16,x,y)
#     x-=30
# for i in range(0,len(questions)):
#     y=20
#     x-=25
#     text=answers[i]
#     y=color_draw(str(i+1),12,x+3,y)
#     y+=8
#     for character in text:
#         if character=="^":
#             text_color=not text_color
#         else:
#             y=color_draw(character,12,x,y)
# print(questions)
# print(answers)
# image.save("question.png")
# c = canvas.Canvas("files/question.pdf", pagesize=(height,width))
# c.drawImage("anser.png", 0, 0)
# c.showPage()
# c.save()