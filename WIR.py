from bs4 import BeautifulSoup
import requests
import csv

def getPage(url):
    r = requests.get(url)
    data = r.text
    soup1 = BeautifulSoup(data, "lxml")
    return soup1


def saveEntry(titlestr, timestr, contentstr):
    with open('articles.csv', 'a') as csvfile1:
        csvwriter1 = csv.writer(csvfile1, delimiter=',')
        csvwriter1.writerow([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])


def parseNewsPage(soup1):
    titletag = soup1.find('h3')
    title = titletag.find('a')
    print "Title: " + title.text

    timetag = soup1.find('span', 'date')
    time = timetag.text
    print "Time: " + time

    contenttag = soup1.find('div', 'content')
    ptags = contenttag.findAll('p')
    text = ""
    for p in ptags:
        print p.text
        text += p.text

    saveEntry(title.text, time, text)


with open('articles.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['title', 'time', 'content'])

url = "http://www.wantedinrome.com/news_category/crime/"
soup = getPage(url)

#print(soup.prettify())

lis = []
uls = soup.find_all("ul", "post-list mode-1")

for ul in uls:
    for li in ul.findAll("h3"):
        lis.append(li)
# if li.find('ul'):
#            break

i = 0
for li in lis:
    i += 1
    print(i)
    link = li.find('a')
    url = link.get('href')
    print(url)
    soup = getPage(url)

    parseNewsPage(soup)


#    print li.text.encode("utf-8")

#    r = requests.get(url)
#    data = r.text
#    soup1 = BeautifulSoup(data, "lxml")
