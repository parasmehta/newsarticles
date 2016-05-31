import csv

def main():

    list_london_statistics = []                                                                                         # create empty list

    f_statistics_london = open('london_articles_tagged_statistics.txt', 'rb')                                           # open file
    for row in csv.reader(f_statistics_london):                                                                         # save content to list
        list_entry = str(row).split(",")                                                                                # |
        list_london_statistics.append(list_entry)                                                                       # |
    f_statistics_london.close()                                                                                         # close file


# start with main()
if __name__ == '__main__':
    main()