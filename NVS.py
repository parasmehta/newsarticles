# IMPORTS
from bs4 import BeautifulSoup
import requests
import csv

# GLOBAL VARIABLES

# DO NOT CHANGE THIS!
start_url = "http://www.novinite.com/search_news.php?do_search=no&thequery=sofia&x=0&y=0&&s=0"
last_url = "http://www.novinite.com/search_news.php?do_search=no&thequery=sofia&x=0&y=0&s47660=&&s49290"


# FUNCTIONS


# this function returns a soup page object
def getPage(url):
    r = requests.get(url)
    data = r.text
    soup1 = BeautifulSoup(data, "lxml")
    return soup1


# this function stores the collected data into a .csv-file
def saveEntry(titlestr, timestr, contentstr):

    with open('sofiArticles.csv', 'a') as csvfile1:
        csvwriter1 = csv.writer(csvfile1, delimiter='|')
        csvwriter1.writerow([titlestr.encode('utf-8'), timestr.encode('utf-8'), contentstr.encode('utf-8')])

    with open('sofiArticles.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(['title', 'time', 'content'])


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


#        link = "http://www.novinite.com/"+str(x.find_next(href=True)['href'])

# extracts all crime related links to sub-websites form a navigator websites
def search_page_for_crime_link(url):

    page = getPage(url)
    dct  = page.find_all("div", class_="text")

    for x in dct:
        if x.find_all("a", { "title" : "Crime News" }) != []:
            link = "http://www.novinite.com/"+str(x.find(href=True)['href'])
            #print(link)
            store_crime_data_from_page(link)

# this function collectes all crime related data (title, date, content)
# from a given sub-website (url) form http://www.novinite.com/
def store_crime_data_from_page(url):

    page = getPage(url)
    content = page.find("div", { "id" : "content" })
    nvs_title = content.find("h1").text
    ed = content.find("div", { "class" : "date" }).text
    eventdate = ed.split("|")
    eventdate = eventdate[1]
    #txt = content.find_all("p", { "class" : "western" })


    print(nvs_title + " |" + nvs_date)
    #   =
    #nvs_date    = ...
    #nvs_content = ...


#### MAIN PROGRAM HERE ####

find_all_navigator_pages(start_url)