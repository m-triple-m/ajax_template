import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class Scrapper:
    def __init__(self):
        self.host = 'https://www.flipkart.com/search?q='

    def get(self, url):
        try:
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'lxml')
                return soup
            else:
                print('failed')
        except Exception as e:
            print(e)

    def collect(self, soup, container):
        if soup:
            try:
                url = soup.find_all('a',attrs={'class':'_3fVaIS'})[1]
            except:
                url = soup.find('a',attrs={'class':'_3fVaIS'})

            try:
                for item in soup.find_all('div', {'class':'_1UoZlX'}):
                    item_details = {}
                    details = item.find('div', {'class' : '_1-2Iqu'})
                    item_details["name"] = details.find('div', {'class' : '_3wU53n'}).text
                    item_details["link"] = 'http://www.flipkart.com'+item.find('a', {'class' : '_31qSD5'}).attrs.get('href')
                    item_details["features"] = ','.join([li.text for li in details.find('ul').find_all('li')])
                    item_details["price"] = details.find('div',{'class':'_1vC4OE _2rQ-NK'}).text
                    item_details["rating"] = details.find('span',{'class':'_38sUEc'}).find("span").text
                    item_details["avgrating"] = details.find('div',{'class':'hGSR34'}).text
                    container.append(item_details)
                    print(container[0].keys())
            
            except Exception as e:
                print('error parsing data')

            if url:
                url = url.attrs.get('href')
                curl = "https://www.flipkart.com"+url
                print('next page link ==>',curl)
                return curl,container
            else:
                print('no next url found')
                return None,container


    def save(self, datalist):
        data= pd.DataFrame(datalist)
        path = f"csvfiles/{self.product.replace('+', '_')}-{datetime.today().strftime('%d_%m_%Y')}.csv"
        data.to_csv(path)
        print('saved to', path)
        return path

    def start(self, product, max = 2):
        container = []
        self.product = product.replace(' ', '+')
        pre= 0
        self.url = self.host+self.product
        print(self.url)
        # self.url = "https://www.flipkart.com/search?q=mobiles"
        while True:
            soup = self.get(self.url)
            newurl,container = self.collect(soup,container)
            if not newurl or int(newurl[-1]) > max or int(newurl[-1])< int(pre):
                print('the end')
                break
            else:
                self.url = newurl
            pre = newurl[-1]
        csvpath = self.save(datalist=container)
        return container, csvpath

    
        

if __name__ == "__main__":
    scrap = Scrapper()
    scrap.start('realme 6', 5)