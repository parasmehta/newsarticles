                                                                                                                        # IMPORTS
import csv

                                                                                                                        # LISTS
list_london_roads       = []
list_london_adminlevels = []
list_london_articles    = []

                                                                                                                        # FUNCTIONS
def main():

    isGeotagged  = 0                                                                                                    # initial value

    print("\nPreparing needed lists...\n")

    # streets
    f_roads_london = open('roads_roma.txt', 'rb')                                                                       # open file
    for tmp in csv.reader(f_roads_london, delimiter=';'):                                                                              # save content to dictionary
        # tmp = str(row).split(";")                                                                                       # |
        if len(tmp) < 10:
            print(tmp)
        list_entry = [tmp[2].replace('"',''), tmp[9].replace('"', '').replace('\'', '').replace(']', '')]               # |
        list_london_roads.append(list_entry)                                                                            # |
    f_roads_london.close()                                                                                              # close file
    print("\nFilling list with roads = done...\n")

                                                                                                                        # ADMIN LEVELS
    f_admin_london = open('admin_roma.txt', 'rb')                                                                       # open file
    for row in csv.reader(f_admin_london):                                                                              # save content to list
        tmp = str(row).split(";")                                                                                       # |
        list_entry = [tmp[1],tmp[2],tmp[3]]                                                                             # |
        list_london_adminlevels.append(list_entry)                                                                      # |
    f_admin_london.close()                                                                                              # close file
    print("\nFilling lists with admin levels = done...\n")

                                                                                                                        # ARTICLES

    f_articles_london = open('londonarticles.csv', 'rb')                                                                # open file
    for tmp in csv.reader(f_articles_london, delimiter='|'):                                                                           # save content to dictionary
        #tmp = str(row).split("|")                                                                                       # |
        if len(tmp) < 3:
            print(tmp)
        list_entry = [tmp[0].replace('[', '').replace('\'', ''), tmp[1].replace('\'', ''), tmp[2]]                      # |
        list_london_articles.append(list_entry)                                                                         # |
    f_articles_london.close()                                                                                           # close file
    print("\nFilling lists with articles = done...\n")

    print("\nStart tagging articles ...\n")
                                                                                                                        # GEOTAGGING

    if (not isGeotagged):                                                                                               # find roads mentioned in article
        for road  in list_london_roads:                                                                                 # |
            for article in list_london_articles:                                                                        # |
                if (road[0] in article[2]):                                                                             # |
                    if len(road) < 3:
                        print(road)
                    article.append(road[1])                                                                             # | tag article with a position (road)
                    isGeotagged = True                                                                                  # | mark article as tagged

    if (not isGeotagged):                                                                                               # find admin level mentioned in article
        for admlvl in list_london_adminlevels:                                                                          # |
            for article in list_london_articles:                                                                        # |
                if (admlvl[0] in article[2]):                                                                           # |
                    article.append(admlvl[2])                                                                           # | tag article with a position (admin level)
                    isGeotagged = True                                                                                  # | mark article as tagged

    # if (not isGeotagged):
    #     print("WARNING: Article: " + list_london_articles[j][1] + " could not be geotagged!\n")

                                                                                                                        # TIMETAGGING
                                                                                                                        # - done by using the second attribute "time" of the extracted articles

    print("\nAll articles have been tagged ...\n")
    print("\nTAGGING COMPLETED!\n")


# start with main()
if __name__ == '__main__':
    main()