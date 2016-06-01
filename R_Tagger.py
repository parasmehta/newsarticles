# coding=utf-8

### FAMOUS FIRST WORDS ;-)
# - no names shorter than 3 letters are considered while tagging the articles
# - iff a road name is NOT a substring of another road it is used for tagging the articles
# - a road name is prefered against an administration level name (if a road name was found an administration level name will not be considered)
# - Let's go! ;-)

                                                                                                                        # IMPORTS
import csv

                                                                                                                        # LISTS
list_roma_roads       = []
list_roma_adminlevels = []
list_roma_articles    = []

                                                                                                                        # FUNCTIONS
def main():

    num_not_tagged = 0                                                                                                  # initial value
    num_tagged = 0                                                                                                      # initial value

    print("Preparing needed lists...\n")

                                                                                                                        # ROADS

    f_roads_roma = open('roma_roads.csv', 'rb')                                                                     # open file
    for tmp in csv.reader(f_roads_roma, delimiter=';'):                                                               # save content to list
        list_entry = [tmp[0], tmp[1]]                                                                                   # |
        list_roma_roads.append(list_entry)                                                                            # |
    f_roads_roma.close()                                                                                              # close file
    print("Filling list with roads = done...\n")

                                                                                                                        # ADMIN LEVELS
    f_admin_roma = open('roma_admin.csv', 'rb')                                                                     # open file
    for row in csv.reader(f_admin_roma):                                                                              # save content to list
        tmp = str(row).split(";")                                                                                       # |
        list_entry = [tmp[0].replace('"',''), tmp[1], tmp[2]]                                                           # | tmp[0]=name, tmp[1]=level, tmp[2]=geom
        list_roma_adminlevels.append(list_entry)                                                                      # |
    f_admin_roma.close()                                                                                              # close file
    print("Filling lists with admin levels = done...\n")

                                                                                                                        # ARTICLES

    f_articles_roma = open('roma_articles.csv', 'rb')                                                               # open file
    for tmp in csv.reader(f_articles_roma, delimiter='|'):                                                            # save content to list
        list_entry = [tmp[0], tmp[1], tmp[2].replace('\n',' ').replace('\r',' ')]                                       # | tmp[0]=title, tmp[1]=date, tmp[2]=content
        list_roma_articles.append(list_entry)                                                                         # |
    f_articles_roma.close()                                                                                           # close file
    print("Filling lists with articles = done...\n\n")

    print("Start tagging articles ...\n")

    output = open('roma_articles_tagged.txt', 'wb')
    writer = csv.writer(output)

    isTagged = [False] * len(list_roma_articles)                                                                      # create list with so many 'False' entries as we have articles

    for road in list_roma_roads:
        for id in range(0, len(list_roma_articles), 1):
            article = list_roma_articles[id]

            roadAlreadyFound = False
            if ((road[0] in article[0]) or (road[0] in article[2])) and (len(road[0])>3):                               # check if road name is in title or content of article
                if (not(len(article)<=3)):
                    for i in range(3,len(article),1):
                        if (road[0] in article[i]):
                            roadAlreadyFound = True
                if not(roadAlreadyFound):
                    article.append(road[0])                                                                             # tag article with a name (road)
                    article.append(road[1])                                                                             # tag article with a position (road)
                    writer.writerow(article)                                                                            # write article to file
                    isTagged[id] = True                                                                                 # set flag
                    num_tagged += 1
                    print(str(num_tagged)+' tagged article with a street name: "' + str(article[0]) + '"')

    print("Roads have been tagged ...\n")

    for admlvl in list_roma_adminlevels:
        for id in range(0, len(list_roma_articles), 1):
            article = list_roma_articles[id]                                                                          # just a helper

            if not isTagged[id]:                                                                                        # if article was not already tagged
                adminAlreadyFound = False
                if ((admlvl[0] in article[0]) or (admlvl[0] in article[2])) and (len(admlvl[0])>3):                     # contains the article an administrative level name?
                    if not(len(article)<=3):                                                                            #
                        for j in range(3,len(article),1):
                            if admlvl[0] in article[j]:
                                adminAlreadyFound = True
                if not(adminAlreadyFound):
                    article.append(admlvl[0])                                                                           # tag article with a name (admin level)
                    article.append(admlvl[2])                                                                           # tag article with a position (admin level)
                    writer.writerow(article)                                                                            # write article to file
                    isTagged[id] = True                                                                                 # set flag
                    num_tagged += 1
                    print(str(num_tagged)+' tagged article with an administration level name: "' + str(article[0]) + '"')

    print("Administration levels have been tagged ...\n")

    output.close()                                                                                                      # close the file london_articles_tagged.txt

    for id in range(0,len(isTagged),1):
        if (not isTagged[id]):
            print("WARNING: NOT TAGGED --> " + list_roma_articles[id][0])                                             # print title of articles that have not been tagged
            num_not_tagged += 1

                                                                                                                        # TIME TAGGING ?
                                                                                                                        # - done by using the second attribute "time" of the extracted articles

    print("Number of tagged articles: "+str(num_tagged)+" | Number of NOT tagged articles "+str(num_not_tagged)+" .\n")
    print("TAGGING COMPLETED!\n")


# start with main()
if __name__ == '__main__':
    main()