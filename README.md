# newsarticles

## Data collection

This software collects crime related information (news articles) from the following websites:

London: 
Possible source - http://www.london24.com/news/crime

Rome:
- WIR.py: http://www.wantedinrome.com/news_category/crime/

Sofia:
- NVS.py: http://www.novinite.com/search_news.php?tag=sofia&&s=30. (Search by tag 'Sofia' and exctracted category 'Crime')

The collected infomation will be stored in a .csv-file for each website.

----

##  Data Processing

Some simple informations will be extracted from the collected information in the .csv-files:

- type of crime / category
- location of mentioned crime
- time

Therefore some tools are used:

1. NLTK for text mining: http://www.nltk.org/book/ch07.html
2. Scikit-learn for machine learning: http://scikit-learn.org/stable/
3. Gensim package for topic modeling
4. Clavin for geotagging
