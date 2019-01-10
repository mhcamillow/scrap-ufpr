import requests
import re
import json
from bs4 import BeautifulSoup

uri = "http://www.prppg.ufpr.br/ppginformatica/index.php/matriculas/disciplinas/?lang=pb"

class Course:
    code = ""
    name = ""
    description = ""
    bibliography = ""

    def info(self):
        return self.code + "\t" + self.name + "\t" + self.description + "\t" + self.bibliography

def extract_line(info, obj):
    line = info.get_text().strip()

    if (line.startswith('DISCIPLINA')):
        temp = line.split(":")[1]
        obj.code = temp.split("–")[0].strip()
        obj.name = temp.split("–")[1].strip()

    if (line.startswith('EMENTA')):
        obj.description = line.split(":")[1].strip().replace('\n', ' ')

    if (line.startswith('BIBLIOGRAFIA')):
        obj.bibliography = line.split(":")[1].strip().replace('\n', ' ')


page = requests.get(uri)

soup = BeautifulSoup(page.content, 'html.parser')
courses = soup.findAll("div", {"id" : re.compile('conteudoDialog.*')})

result = []

for course in courses:
    new_course = Course()
    infos = course.find_all('p')
    
    for info in infos:
        extract_line(info, new_course)
        
    result.append(new_course)

text_file = open("output.csv", "w")
for res in result:
    text_file.write(
        res.info()
            .replace(';', ' ')
            .replace('\t', ';') + '\n')
text_file.close()