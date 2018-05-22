def scrape():

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

execute_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **execute_path, headless=False)

#nasa mars news
url_news = 'https://mars.nasa.gov/news/'
browser.visit(url_news)
news_title = browser.find_by_css('.content_title').first.text
news_para = browser.find_by_css('.article_teaser_body').first.text
print(news_title, "\n" + news_para)

#mars images
url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_images)
browser.find_by_id('full_image').click()
mars_image = browser.find_by_css('.fancybox-image').first['src']
print(mars_image)

#weather
url_tweets = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url_tweets)
for text in browser.find_by_css('.tweet-text'):
    if text.text.partition(' ')[0] == 'Sol':
        weather_tweet = text.text
        break
print(weather_tweet)

#dataframe
url_space = 'http://space-facts.com/mars/'
df = pd.read_html(url_space, attrs = {'id': 'tablepress-mars'})[0]
df = df.set_index(0).rename(columns={1:"value"})
del df.index.name
space_facts = df.to_html()
print(space_facts)

#images
url_astro = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_astro)

hemi_links = []
images = bs(browser.html, 'html.parser')

hemi_images = images.find('div', class_='result-list')
all_hemis = hemi_images.find_all('div', class_='item')

for hemi in all_hemis:
    url_hemi = hemi.find('a')['href']
    url_pic = 'https://astrogeology.usgs.gov' + url_hemi    
    browser.visit(url_pic)
    hemi_links.append({'name': hemi.find('h3').text, 'url_hemi': bs(browser.html,'html.parser').find('div',class_='downloads').find('a')['href']})

print(hemi_links)

mars_full = {}
mars_full["news_title"] = news_title
mars_full["news_para"] = news_para
mars_full["mars_image"] = mars_image
mars_full["weather_tweet"] = weather_tweet
mars_full["space_facts"] = space_facts
mars_full["hemi_links"] = hemi_links

return(mars_full)