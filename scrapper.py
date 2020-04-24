import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class Scrapper:
    def __init__(self,product):
        self.product = product.replace(' ', '%20')
        self.url = f'https://www.flipkart.com/search?q={product}'
        self.soup = self.getsoup()

    def getsoup(self):
        data = requests.get(self.url)
        print(data.status_code)

        soup = BeautifulSoup(data.text, features="lxml")
        return soup

    def getdata(self):
        data =[]
        for item in self.soup.find_all('div', {'class':'_1UoZlX'}):
            item_details = {} 
            details = item.find('div', {'class' : '_1-2Iqu'})
            item_details["name"] = details.find('div', {'class' : '_3wU53n'}).text
            item_details["link"] = item.find('a', {'class' : '_31qSD5'}).attrs.get('href')
            item_details["features"] = ','.join([li.text for li in details.find('ul').find_all('li')])
            item_details["price"] = details.find('div',{'class':'_1vC4OE _2rQ-NK'}).text
            item_details["rating"] = details.find('span',{'class':'_38sUEc'}).find("span").text
            item_details["avgrating"] = details.find('div',{'class':'hGSR34'}).text
            data.append(item_details)
        # print(data[0].keys())
        df = pd.DataFrame(data)
        df.to_csv(f"{self.product.replace('%20', '_')}-{datetime.today().strftime('%d_%m_%Y')}.csv")

        return data
        

if __name__ == "__main__":
    scrap = Scrapper('real me 6')
    scrap.getdata()