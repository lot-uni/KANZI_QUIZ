# import spacy
import random
import re
# nlp = spacy.load('ja_ginza')
f = open('context.txt', 'r', encoding='UTF-8')
content = f.read()
f.close()

content=re.sub(r'。(?![」、。])','。\n',content)
content=re.sub(r'。[ 　]+','。\n',content)
print(content)
s_n=content.split()
# random.shuffle(s_n)
# for i in range(len(s_n)):
#     print(s_n[0])
#     s_n.pop(0)
# doc = nlp(content)
# app = []
# for sent in doc.sents:
#   app.append(sent)

# random.shuffle(app)
# print('____')
# print(app[0])