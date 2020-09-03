import requests
from lxml import html
from terminaltables import AsciiTable

f = open("users.txt", "r")
users=f.read().split("\n")
ranklist={}
for i in users:
    if(len(i.split(' '))<2 and i!=''):
        URL = 'https://leetcode.com/'+i+'/'
        page = requests.get(URL)
        tree = html.fromstring(page.content)
        solved = tree.xpath('//span[@class="badge progress-bar-success"]/text()')
        if(len(solved)==7):
            ranklist[i[:5]]=int(solved[1].strip().split(" ")[0])
        else:
            print(i+" no such username or connection error")
    elif(len(i.split(' '))>1):
        er="~".join(i.split(" "))
        print(er+" has space in the username where '~' is given")
ranklist={k: v for k, v in sorted(ranklist.items(), key=lambda item: item[1],reverse=True)}
table_data = [
    ['Rank','Username', 'SolvedQs']
]
r=1
for i in ranklist.keys():
    data=[r,i,ranklist[i]]
    table_data.append(data)
    r=r+1
table = AsciiTable(table_data)
print(table.table)