import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from lxml import html
import requests

def getRecommendations(url):
    ds = pd.read_csv('test.csv')
    ds = ds[ds.url.str.contains("topics") == False]
    ds = ds[ds.url.str.contains("page") == False]
    ds = ds[ds['url']!='https://m.dailyhunt.in/news/india/english?tk=']
    ds = ds[ds['url']!='https://m.dailyhunt.in/news/india/english/hindustan+times-epaper-httimes']
    #ds = ds[ds.url.str.contains("english") == False]

    if (url is None):
        url = 'https://m.dailyhunt.in/news/india/english/curated+by+lever+ayush-epaper-ayush/5+hair+oiling+tips+from+ayurveda+for+hot+weather-newsid-85647725'
    
    page = requests.get(url, verify=False)
    tree = html.fromstring(page.content)

    id = ''.join(tree.xpath('//h1/text()'))
    id = id.strip()
    content = ''.join(tree.xpath('//p/text()'))
    data = {"id": [id], "content": [content],'url':[url]}
    sample_df = pd.DataFrame.from_dict(data=data, orient='columns')
    ds = pd.concat([ds,sample_df])



    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['content'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    pd_cosine= pd.DataFrame(data=cosine_similarities,    
                index=ds['url'],    
                columns=ds['url'])

    # url = 'https://m.dailyhunt.in/news/india/english/curated+by+lever+ayush-epaper-ayush/5+hair+oiling+tips+from+ayurveda+for+hot+weather-newsid-85647725'
    pd_cosine_reco = pd_cosine[[url]]
    pd_cosine_reco = pd_cosine_reco[pd_cosine_reco[url]<max(pd_cosine_reco[url].values)]
    reco_df=pd_cosine_reco.sort_values(by=[url], ascending=[False]).head(5)

    # print(reco_df)

    list_of_reco = list(reco_df.index)

    title_list = []
    for i in list_of_reco:
        
        
        page_i = requests.get(i, verify=False)
        tree_i = html.fromstring(page_i.content)

        title_i = ''.join(tree_i.xpath('//h1/text()'))
        title_list.append(title_i)

    title_list = [i.strip() for i in title_list] 
    return title_list
