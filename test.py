import requests
from bs4 import BeautifulSoup
import pandas as pd
BASE = "https://recordlinkage.azurewebsites.net/"
files =[('files[]', ('output1.csv', open('output1.csv', 'rb'), 'text/csv')),('files[]', ('output2.csv', open('output2.csv', 'rb'), 'text/csv'))]
response = requests.post(BASE, files=files)
DOWNLOAD = "https://recordlinkage.azurewebsites.net/download"
r = requests.get(DOWNLOAD)
soup = BeautifulSoup(r.text, 'html.parser')
link1=soup.find('a').get('href')
DOWNLOAD_FILE = BASE+link1
output=pd.read_csv(DOWNLOAD_FILE)
print(output.head(5))
