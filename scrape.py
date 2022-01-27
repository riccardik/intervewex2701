from bs4 import BeautifulSoup
import numpy as np
import requests

url = "https://en.wikipedia.org/wiki/Nvidia "
page = requests.get(url)
html = page.text

parsed_html = BeautifulSoup(html, 'html.parser')
table = parsed_html.select("table")[1]

rows = []
for row in table.findAll('tr'):
    cells = []
    for cell in row.findAll(["th","td"]):
        text = cell.text
        cells.append(text)
    rows.append(cells)

tab_num = []
for i in range(1, len(rows)):
    row_ = []
    for j in range(len(rows[0])):
        row_.append(float(rows[i][j].replace("\n", "").replace(",", "").replace("−", "-")))
    tab_num.append(row_)

source = np.asarray(tab_num)
arr = np.zeros([source.shape[0], source.shape[1]+2])
arr[0:source.shape[0], 0:source.shape[1]] = source

for i in range(arr.shape[0]):
    arr[i, source[0].shape[0]] = np.sum(arr[i, 0:source[0].shape[0]])
    arr[i, source[0].shape[0]+1] =  arr[i, source[0].shape[0]]/(source[0].shape[0])
np.set_printoptions(suppress=True)
np.savetxt('table.csv', arr, delimiter=',',  newline='\n',  fmt="%f")
