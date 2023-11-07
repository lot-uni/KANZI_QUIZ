import re
import random
import jaconv
import pykakasi
import argparse

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas


max = 15
width, height = B5
text_color=False

flie_pas='context.txt'
text=""
with open(flie_pas, 'r') as file:
    text = file.read()
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
    print(kangi_list)
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
for text in sample:
    short_text=text[:35]
    if judge(short_text):
        sentences.append(short_text)

if len(sentences)<max:
    sentences=random.sample(sentences,len(sentences))
else:
    sentences=random.sample(sentences,max)
for text in sentences:
    hoge=create_question(text)
    questions.append(hoge[0])
    answers.append(hoge[1])
print(questions[0])