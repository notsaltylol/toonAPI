import requests, bs4
import re


url = 'https://manga4life.com/read-online/Solo-Leveling-chapter-0.html'


res = requests.get(url)
res.raise_for_status() 


soup = bs4.BeautifulSoup(res.text, 'html.parser')
imgElem = soup.select('script')
for elem in imgElem:
    x = re.search('vm.CurPathName = "(.*)";', str(elem))
    if(x):
        print(x.group(1))