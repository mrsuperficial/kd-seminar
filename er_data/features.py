import eventregistry as ER
import datetime
import pandas as pd


er = ER.EventRegistry(apiKey = "5ba73408-ea81-459b-abf4-6fedd8cb8ec6")  #dany
#er = ER.EventRegistry(apiKey = "5fed3642-762a-4abc-aabf-ac6213c1bcea")  #philipp
analytics = ER.Analytics(er)

#DEFINE companies
companies = ['Samsung','BASF','Apple','Tesla','Airbus','Bayer','BMW','Telefonica','Google','Allianz','Total']


#DEFINE start and end date
startDate = datetime.date(2018, 4, 22)
endDate = datetime.date(2018, 5, 22)

#DEFINE df results columns
columns = ['Timestamp',"ID","articleCount","avgSentiment","stdSentiment","25quantileSentiment","50quantileSentiment","75quantileSentiment","maxSentiment","minSentiment"]
results = pd.DataFrame(index=range(0,pd.date_range(startDate,endDate).shape[0]*len(companies)),columns=columns)
result_index = 0

for company in companies:
    # QUERY articles related to current company
    q = ER.QueryArticlesIter(conceptUri=er.getConceptUri(company), dateStart=startDate, dateEnd=endDate)
    articles = q.execQuery(er,sortBy = "date")

    # Init Company Sentiment DF
    sentiment_df = pd.DataFrame(index=range(0,2000),columns=pd.date_range(startDate,endDate).format("%Y-%m-%d")[1:])
    # INITIALIZE local variables
    ibm_sentiment = 0
    article_count = 0
    stock_occurences = 0
    index= 0
    date = pd.date_range(startDate,endDate).format("%Y-%m-%d")[len(pd.date_range(startDate,endDate))]
    #ITERATE over all articles about the current company
    for article in articles:
        if date != article['date']:
            index = 0

        #TEXT FEATURES
        if 'stock' in article['body']:
             stock_occurences += 1

        #SENTIMENT
        #calculating sentiment value from 'article body'
        sentiment_value = analytics.sentiment(article['body'])['avgSent']
        sentiment_df[article['date']][index] = sentiment_value
        index += 1
        date = article['date']

    for day in sentiment_df.columns:

        # gefine the total number of articles

        results.iloc[result_index]['Timestamp'] = str(day)
        results.iloc[result_index]['ID'] = company
        results.iloc[result_index]['articleCount'] = sentiment_df[day].count()
        results.iloc[result_index]['avgSentiment'] = sentiment_df[day].mean()
        results.iloc[result_index]['stdSentiment'] = sentiment_df[day].std()
        result2s.iloc[result_index]['25quantileSentiment'] = sentiment_df[day].quantile(0.25)
        results.iloc[result_index]['50quantileSentiment'] = sentiment_df[day].quantile(0.50)
        results.iloc[result_index]['75quantileSentiment'] = sentiment_df[day].quantile(0.75)
        results.iloc[result_index]['maxSentiment'] = sentiment_df[day].min()
        results.iloc[result_index]['minSentiment'] = sentiment_df[day].max()
        result_index += 1


print(results)
results['Timestamp'] = pd.to_datetime(results['Timestamp'],format="%Y-%m-%d")
PATH = "data/companies.csv"
results.to_csv(PATH, sep=",", header=True)




##Faster approach. However sentiment is always 'None'. returnInfo needs to be understood better
# q = ER.QueryArticles(
#         # set the date limit of interest
#         dateStart = date, dateEnd = date,
#         # find articles mentioning the company Apple
#         conceptUri = er.getConceptUri(companies[0]))
# # return the list of top 30 articles, including the concepts, categories and article image
# q.setRequestedResult(ER.RequestArticlesInfo(returnInfo = ER.ReturnInfo(articleInfo = ER.ArticleInfoFlags(url = False, title = False, body = False, sentiment = True, concepts = True, categories = True))))
# res = er.execQuery(q)
# print(type(res['articles']))
# print(res['articles']['results'][0])




# Return vom Vortag als Feature rein für jede Zeile
# Returns so drinne lassen