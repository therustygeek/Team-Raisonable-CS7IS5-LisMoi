from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Adaptive"]
collection=mydb['book']

def getBook():
    headers={'Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    resources=['https://www.dubraybooks.ie/crime','https://www.dubraybooks.ie/poetry','https://www.dubraybooks.ie/science-fiction-fantasy','https://www.dubraybooks.ie/philosophy','https://www.dubraybooks.ie/psychology','https://www.dubraybooks.ie/history','https://www.dubraybooks.ie/music-and-film','https://www.dubraybooks.ie/cookery','https://www.dubraybooks.ie/travel-literature','https://www.dubraybooks.ie/art','https://www.dubraybooks.ie/sport']
    for resource in resources:
        response=requests.get(resource,headers).text
        soup=BeautifulSoup(response,'html.parser')
        urls=soup.select('div.page-body>div.product-grid>div.item-box>div.product-item>div.picture>a')
        category=soup.select('div.page-title>h1')[0].text
        for url in urls:
            link="https://www.dubraybooks.ie"+url.get('href')
            # if link=="https://www.dubraybooks.ie/The-File-Note_9781912589081":
            #     continue
            booksite=requests.get(link,headers).text
            soupBook=BeautifulSoup(booksite,'html.parser')
            booktitle=soupBook.select('div.overview > div.product-name > h1')[0].text.lstrip().rstrip()
            author=soupBook.select('div.product-specs-box>span.value>a')[0].text.lstrip().rstrip()
            publicDate=soupBook.select('div.product-specs-box>span.value')
            if len(publicDate)<=3:
                continue
            ISBN=soupBook.select('div.sku>span.value')[0].text
            Description=soupBook.select('div.full-description>p')
            if len(Description)<=0:
                continue
            imageLink=soupBook.select('div.picture>img')[0].get('src')
            print(category)
            print(link)
            print(booktitle)
            print(author)
            print(publicDate[3].text)
            print(ISBN)
            print(len(Description))
            print(Description[0].text)
            print(imageLink)
            print('-----------------------------')
            bookInfo={"_id":ISBN,"name":booktitle,"author":author,"category":category,"PublishDate":publicDate[3].text,"decription":Description[0].text,"BookUrl":link,"imagelink":imageLink}
            collection.insert_one(bookInfo)

if __name__=='__main__':
    pool=Pool(processes=100)
    pool.map_async(getBook())
    pool.close()
    pool.join()

















