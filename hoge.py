import re
import random
import jaconv
import pykakasi
from pykakasi import kakasi

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import B5
from reportlab.pdfgen import canvas

flie_pas='context.txt'
words_list=[]
kakasi_instance = kakasi()
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
    sentences = re.split(r'[ע\．，、 。！？, ]', text)
    return sentences

sentences=list(filter(None,splitToSentences(text)))
sentences=random.sample(sentences,10)
sentences_detail=kakasi_instance.convert(''.join(sentences))
for word in sentences_detail:
    if judge(word['orig']):
        words_list.append(re.sub(r'[^\u4e00-\u9fff]+', '',word['orig']))
words_list=list(set(words_list))
print(words_list)
delete_list=[]
for i in range(0,len(words_list)):
    c=0
    for sentence in sentences:
        if(words_list[i] in sentence):
            c+=1
    if(c!=1):
        print(words_list[i])
        delete_list.append(words_list[i])
for word in delete_list:
    words_list.remove(word)
print(words_list)
print(sentences)