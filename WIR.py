# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv

filename = 'romearticles.csv'
start_url = "http://www.wantedinrome.com/news_category/crime/"

# gets the tree structure for a page
def getPage(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    return soup

# saves title, time and text of news item to csv
def saveEntry(titlestr, timestr, contentstr):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])

# parses the page for each news item and extracts title, time and text
def parseNewsPage(url):
    soup = getPage(url)
    titletag = soup.find('h3')
    title = titletag.find('a')
    print "Title: " + title.text

    timetag = soup.find('span', 'date')
    time = timetag.text
    print "Time: " + time

    contenttag = soup.find('div', 'content')
    ptags = contenttag.findAll('p')
    text = ""
    for p in ptags:
        print p.text
        text += p.text
    text = text.strip()

    saveEntry(title.text, time, text)

# parses the page with news listing and gets the url for each news item
def parseNewsListingPage(url):
    page = getPage(url)
    lis = []
    uls = page.find_all("ul", "post-list mode-1")

    for ul in uls:
        for li in ul.findAll("h3"):
            lis.append(li)

    for li in lis:
        link = li.find('a')
        url = link.get('href')

        parseNewsPage(url)


# this function finds maxpage and starts sending requests to all pages upto maxpage
def navigatePages(url):

    page = getPage(url)

    paginator = page.find("ul", "pagination pagination-centered")

    lastpagetag = paginator.find("a", "last")
    lastpageurl = lastpagetag.get('href')

    lastpagenum = int(lastpageurl[-2:-1])

    print(lastpageurl)
    print(lastpagenum)

    # from maxpage to page 1
    for i in range(1, lastpagenum+1, 1):
        url = "http://www.wantedinrome.com/news_category/crime/page/" + str(i)
        parseNewsListingPage(url)


# this function stores the headline into a .csv-file
def initFile():

    fobj = open(filename, 'w')
    csvw = csv.writer(fobj, delimiter='|')
    csvw.writerow(['title', 'time', 'content'])
    fobj.close()

#### MAIN PROGRAM ####

def main():

    # open and prepare file
    initFile()

    # parse the website and store the collected data into file
    navigatePages(start_url)


##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()
