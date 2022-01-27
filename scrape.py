from bs4 import BeautifulSoup
import numpy as np
import requests

np.set_printoptions(suppress=True)

url = "https://en.wikipedia.org/wiki/Nvidia "
page = requests.get(url)
html = page.text

parsed_html = BeautifulSoup(html, 'html.parser')

# find and select the right table

# manual selection
# table = parsed_html.select("table")[1]

# automatic selection
h2 = parsed_html.find_all("h2")
for elm_ in h2:
    print(elm_.text.replace("[edit]", ""))
    if elm_.text.replace("[edit]", "")=="Finances":
        elm = elm_
        break

table = elm.find_next_sibling("table")

rows = []
for row in table.findAll('tr'):
    cells = []
    for cell in row.findAll(["th","td"]):
        text = cell.text
        cells.append(text)
    rows.append(cells)

# format the table
tab_num = []
label_row = rows[0]
for i in range(1, len(rows)):
    row_ = []
    for j in range(len(rows[0])):
        row_.append(float(rows[i][j].replace("\n", "").replace(",", "").replace("−", "-")))
    tab_num.append(row_)

source = np.asarray(tab_num)
arr = np.zeros([source.shape[0]+2, source.shape[1]])
arr[0:source.shape[0], 0:source.shape[1]] = source

for i in range(arr.shape[1]):
    arr[source.shape[0], i] = np.sum(source[:, i])
    arr[source.shape[0]+1,i] =  np.sum(source[:, i])/(source.shape[0])

# save the table
np.savetxt('table.csv', arr, delimiter=',',  newline='\n',  fmt="%f")

arr_noyear = arr[:, 1:]
np.savetxt('table_noyear.csv', arr_noyear, delimiter=',',  newline='\n',  fmt="%f")
