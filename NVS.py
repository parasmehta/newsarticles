# IMPORTS
from bs4 import BeautifulSoup
import requests
import csv
import os


# FUNCTIONS

# this function returns a soup page object
def getPage(url):
    r = requests.get(url)
    data = r.text
    sobj = BeautifulSoup(data, "lxml")
    return sobj


# this function stores the headline into a .csv-file
def initFile():

    fobj = open('tmpSofiArticles.csv', 'w')
    csvw = csv.writer(fobj, delimiter='|')
    csvw.writerow(['title', 'time', 'content'])
    fobj.close()


# this function stores the collected data into a .csv-file
def saveEntry(titlestr, timestr, contentstr):

    fobj = open('tmpSofiArticles.csv', 'a')
    csvw = csv.writer(fobj, delimiter='|')
    csvw.writerow([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])
    print([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])
    fobj.close()


def clean_up_csv_file():
    input = open('tmpSofiArticles.csv', 'rb')
    output = open('CrimeRelatedArticlesFromSofia.csv', 'wb')
    writer = csv.writer(output)
    for row in csv.reader(input):
        if row:
            writer.writerow(row)
    input.close()
    output.close()
    os.remove("tmpSofiArticles.csv")

# this function finds all navigator pages
def find_all_navigator_pages(url):

    page = getPage(url)
    dct  = page.find_all("ul", { "id" : "pages"} )

    # find maxpage
    for x in dct:
        dcp = x.find_all("li")
        maxpage = int(dcp[10].text + "0") + 10

    # from maxpage to page 1
    for i in range(10,maxpage,10):
        url = "http://www.novinite.com/search_news.php?do_search=no&thequery=sofia&x=0&y=0&&s=" + str(i)
        search_page_for_crime_link(url)


# extracts all crime related links to sub-websites form a navigator websites
def search_page_for_crime_link(url):

    page = getPage(url)
    dct  = page.find_all("div", class_="text")

    for x in dct:
        if x.find_all("a", { "title" : "Crime News" }) != []:
            link = "http://www.novinite.com/"+str(x.find(href=True)['href'])
            store_crime_data_from_page(link)


# this function collectes all crime related data (title, date, content)
# from a given sub-website (url) form http://www.novinite.com/
def store_crime_data_from_page(url):

    page = getPage(url)
    content = page.find("div", { "id" : "content" })

    # title
    nvs_title = content.find("h1").text

    # date
    ed = content.find("div", { "class" : "date" }).text
    eventdate = ed.split("|")
    nvs_date = eventdate[1]

    # text
    content = content.find("div", { "id" : "textsize" })
    content = content.find_all("p")
    nvs_text = ""
    for t in content:
        nvs_text = nvs_text + t.text
    nvs_text = nvs_text.strip()

    # store title, date and text into .csv-file
    saveEntry(nvs_title, nvs_date, nvs_text)


#### MAIN PROGRAM ####

def main():

    # open and prepare file
    initFile()

    # DO NOT CHANGE THIS!
    start_url = "http://www.novinite.com/search_news.php?do_search=no&thequery=sofia&x=0&y=0&&s=0"

    # parse the website and store the collected data into file
    find_all_navigator_pages(start_url)

    clean_up_csv_file()

##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()