# newsarticles

## Data collection

This software collects crime related information (news articles) from the following websites:

Rome:
- http://www.wantedinrome.com/news_category/crime/

Sofia:
- http://www.novinite.com/search_news.php?tag=sofia&&s=30. (Search by category 'Crime' and tag 'Sofia')


The collected infomation will be stored in a .csv-file for each website.

----

##  Data Processing

Some simple informations will be extracted from the collected information in the .csv-files:

- type of crime / category
- location of mentioned crime
- ...

Therefore some tools are used:

1. NLTK for text mining: http://www.nltk.org/book/ch07.html
2. Scikit-learn for machine learning: http://scikit-learn.org/stable/
