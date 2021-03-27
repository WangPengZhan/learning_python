from docx import Document
import re

pattern = re.compile(r'(（([A-F]{0,4}|√|×)）)')
pattern1 = re.compile(r'(\(([A-F]{0,4}|√|×)\))')

filename = r'abcd.txt'
result = r'efgh.txt'

f = open(filename,'r', encoding='utf-8')
nf = open(result,'w', encoding='utf-8')
nf.close()
nf = open(result,'a', encoding='utf-8')
for line in f.readlines():
    new_line = re.sub(pattern, "(  )", line)
    new_line = re.sub(pattern1, "(  )", new_line)

    nf.write(new_line)
f.close()
nf.close()

docx = Document("abcd.docx")

i = 0
for paragraph in docx.paragraphs:
    i = i + 1
    paragraph.text = re.sub(pattern, "(  )", paragraph.text)
    paragraph.text = re.sub(pattern1, "(  )", paragraph.text)
    print(i)

docx.save("abcd.docx")