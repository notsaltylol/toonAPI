import flask
from flask import request, jsonify
import requests, bs4
import re


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/chapter/mangazuki')
def chapter_mangazuki():
    domain = 'https://mangazuki.co/manga/'
    query = {'manga': '', 'chapter': ''}
    for q in query:
        if q in request.args:
            query[q] = request.args[q]
        else:
            return "no " + q + " provided"
    url = domain + query['manga'] +'/' + query['chapter']
    
    '''
    try:
        res = requests.get(url)
    except requests.exceptions.HTTPError:
        return str(res.status_code)
    

    if not res.ok:
        return res.status_code
    '''
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imgElem = soup.select('img')
    chapter_imgs = []
    for elem in imgElem:
        if elem.get('data-src'):
            chapter_imgs.append(elem.get('data-src'))
    return jsonify(chapter_imgs)
    


#GET image hoster domain name before getting chapter
@app.route('/api/chapter/mangalife', methods=['GET'])
def chapter_mangalife():
    #?domain=s5.mangabeast.com&manga=Solo-Leveling&chapter=0
    #?domain=s5.mangabeast.com&manga=Tower-Of-God&season=3&chapter=1
    query = {'domain': '', 'manga': '', 'season': '', 'chapter': ''}
    for q in query:
        if q in request.args:
            query[q] = request.args[q]
        else:
            return "no " + q + " provided"
    chapter_imgs = []
    img_id = 1
    url = 'https://' + query['domain'] + '/manga/' + query['manga'] 
    if int(query['season']) > 1:
        url += '/S' + query['season']
    url += '/' + query['chapter'].zfill(4) + '-' 
    #https://s5.mangabeast.com/manga/Solo-Leveling/0000-001.png
    res = requests.get(url + str(img_id).zfill(3) + '.png')
    try:
        res.raise_for_status() 
    except requests.exceptions.HTTPError as e:
        return e + url + str(img_id).zfill(3) + '.png'
    while(res):
        chapter_imgs.append(url + str(img_id).zfill(3) + '.png')
        img_id += 1
        res = requests.get(url + str(img_id).zfill(3) + '.png')

    return jsonify(chapter_imgs)
    
    

@app.route('/api/imghost/mangalife', methods=['GET'])
def imghost_mangalife():
    url = 'https://manga4life.com/read-online/Solo-Leveling-chapter-0.html'


    res = requests.get(url)
    try:
        res.raise_for_status() 
    except requests.exceptions.HTTPError as e:
        return e


    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imgElem = soup.select('script')
    for elem in imgElem:
        x = re.search('vm.CurPathName = "(.*)";', str(elem))
        if(x):
            return(x.group(1))
    return 'could not find image host url'
app.run()