# this code is replicated from the youtube video of John Watson Rooney. 

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd


s = HTMLSession()
booklist = []

url = 'https://www.amazon.in/s?k=marathi&i=digital-text&rh=n%3A1571277031%2Cp_n_feature_nineteen_browse-bin%3A4729244031&dc&qid=1634444429&rnid=4729243031&ref=sr_pg_1'

def getsoup(url):
  r = s.get(url)
  r.html.render(timeout = 20)
  soup = BeautifulSoup(r.html.html, 'html.parser')
  return soup

def getdata(soup):
  products = soup.find_all('div', {'data-component-type':'s-search-result' })
  for item in products:
    title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
    link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']

    books = {
      'title': title,
      'link' : "www.amazon.in" + link
    }

    booklist.append(books)
  return

def getnextpage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.in' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

while True:
  soup = getsoup(url)
  getdata(soup)
  url = getnextpage(soup)
  if not url:
    break

df = pd.DataFrame(booklist)
df.to_csv('Kindle Book List.csv', index=False)
print("Done")
