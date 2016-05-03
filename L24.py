import csv, requests
from bs4 import BeautifulSoup

filename = 'londonarticles.csv'

# gets the tree structure for a page
def getPage(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    return soup


# parses the page for each news item and extracts title, time and text
def parseNewsPage(url):
    soup = getPage(url)
    article = soup.find("article")
    articleheader = article.find("div", "content-a")
    title = articleheader.find('h1')

    print "Title: " + title.text

    time = articleheader.find('p', 'updated')
    if time is None:
        time = articleheader.find("span", "publication-time")
    print "Time: " + time.getText()

    standfirsttag = articleheader.find('div', 'stand-first')
    text = standfirsttag.find('p').getText()

    ptags = articleheader.findAll('p', recursive=False)
    for p in ptags:
        if p.get("class") is None:
            text += p.text.strip()

    print "Text: " + text
    saveEntry(title.text, time.getText(), text)


# saves title, time and text of news item to csv
def saveEntry(titlestr, timestr, contentstr):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])


# parses the page with news listing and gets the url for each news item
def parseNewsListing(page):
    articlespart = page.find("div", "search-results inner-a col-sm-6 col-md-8")
    divs = articlespart.find_all("div", "teaser-image")

    numarticleswritten = 0
    for div in divs:
        linkelement = div.find('a')
        link = linkelement.get('href')
        if link.startswith("/news"):
            link = "http://www.london24.com" + link
        print link
        parseNewsPage(link)
        numarticleswritten += 1

    return numarticleswritten


# this function finds maxpage and starts sending requests to all pages upto maxpage
def navigatePages():
    numarticlesread = 0
    totalnumarticles = 0
    totalnumarticleswritten = 0
    pagenum = 122

    while numarticlesread <= totalnumarticles:

        print "PAGE: " + str(pagenum)

        # retrieve the listings page
        pageurl = "http://www.london24.com/home/search?sort=publishedDate_descending&numberOfItemsPerPage=40&submitted=true&toDate=02%2F05%2F2016&excludeSiteIds=%5B%5D&selectedCategories=%5B%5B%5B%5B%5B%5B%5B%5B%5B%5B%5B%5D%5D%5D%5D%5D%5D%5D%5D%5D%5D%5D&siteExternalID=london.d&excludedCategories=%5B%5B%5B%5B%5B%5B%5B%5B%5B%5B%5B%5D%5D%5D%5D%5D%5D%5D%5D%5D%5D%5D&category=tree_department.categorydimension.archant%3ACategory.General.Crime.NewsHard&includeSiteIds=%5BLondon.d%5D&distanceInMiles=0.0&siteId=2.3224&action=search&facetQueries=publishedDate%3A%5BNOW%2FDAY-7DAYS+TO+NOW%5D&facetQueries=publishedDate%3A%5BNOW%2FYEAR+TO+NOW%5D&facetQueries=publishedDate%3A%5BNOW%2FDAY-30DAYS+TO+NOW%5D&facetQueries=publishedDate%3A%5BNOW%2FDAY+TO+NOW%5D&numberOfItemsToSearchPerPage=10&facetFields=tree_department.categorydimension.archant&publishDateInterval=uk.co.polopoly.search.util.DateInterval%40750d907c&page=" + str(pagenum)
        page = getPage(pageurl)

        # parse listing, get article urls, retrieve article contents and write articles to csv
        totalnumarticleswritten += parseNewsListing(page)

        # update number of articles read
        resultselement = page.find("div", "search-results-scope")
        resultsstr = resultselement.find("p").getText()
        strparts = resultsstr.split()
        totalnumarticles = int(strparts[2].strip())

        resultsrange = strparts[0].split('-')
        numarticlesread = int(resultsrange[1])

        print "Read " + str(numarticlesread) + " articles out of " + str(totalnumarticles)

        pagenum += 1

    print "Total number of articles written: " + totalnumarticleswritten


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
    navigatePages()


##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()