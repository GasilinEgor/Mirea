from graphviz import Digraph
import requests
import re


# обращение к сайтам
res = requests.get("https://docs.python.org/3/library/re.html")
mask = r'<a\s+href="([^"]*)"\s+title='
allImport = ['re']
between = {}

while res.status_code == 200:
    href = re.findall(mask, str(res.content))[2]
    all = href.split('.')
    if allImport.count(all[0]) == 0:
        allImport.append(all[0])
    if len(all) > 2:
        for i in range(len(all) - 2):
            if not all[i] in between:
                between[all[i]] = set()
                between[all[i]].add(all[i + 1])
            else:
                between[all[i]].add(all[i + 1])
    print(href)
    res = requests.get("https://docs.python.org/3/library/" + href)

print(between)
print(allImport)
edges = []
dot = Digraph(comment='Пример графа')
dot.node(allImport[0], allImport[0])
for i in range(1, len(allImport)):
    while allImport[i].count('_') > 0:
        allImport[i] = allImport[i].replace('_', '')
    dot.node(allImport[i],  str(allImport[i]))
    edges.append(str(allImport[i - 1] + allImport[i]))
    dot.edge(allImport[i - 1], allImport[i])
for bib in between:
    for z in between[bib]:
        dot.edge(bib, z)
dot.render('граф.gv')
# Создание объекта графа
"""dot = Digraph(comment='Пример графа')

# Добавление узлов
dot.node('A', 'Узел A')
dot.node('B', 'Узел B')
dot.node('C', 'Узел C')

# Добавление ребер
dot.edges(['AB', 'AC'])

# Визуализация графа и сохранение в файл
dot.render('граф.gv')"""