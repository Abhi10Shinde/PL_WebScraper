#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from html.parser import HTMLParser
import urllib.request


# In[2]:


url = 'https://fbref.com/en/comps/9/Premier-League-Stats'


# In[3]:


data = requests.get(url)


# In[4]:


soup = BeautifulSoup(data.text)


# In[5]:


table = soup.select('table.stats_table')[0]


# In[6]:


table


# In[7]:


links = table.find_all('a')
links = [l.get('href') for l in links]


# In[8]:


links = [l for l in links if '/squads/' in l]


# In[9]:


team_urls = [f'https://fbref.com/{l}' for l in links]


# In[10]:


team_urls = team_urls[0]
team_urls


# In[11]:


data = requests.get(team_urls)


# In[12]:


matches = pd.read_html(data.text, match = 'Scores & Fixtures ')[0]


# In[13]:


matches


# In[14]:


soup = BeautifulSoup(data.text)
links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and 'all_comps/shooting/' in l]
links


# In[15]:


data = requests.get(f"https://fbref.com/{links[0]}")
data.text


# In[16]:


shooting = pd.read_html(data.text, match='Shooting')[0]


# In[17]:


shooting.head()


# In[18]:


shooting.columns = shooting.columns.droplevel()


# In[19]:


shooting.head()


# In[20]:


team_df = matches.merge(shooting[['Date','Sh','SoT','Dist','FK','PK','PKatt']],on='Date')


# In[21]:


team_df.head(10)


# In[22]:


years = list(range(2022,2019,-1))


# In[23]:


years


# In[24]:


all_matches = []
url = 'https://fbref.com/en/comps/9/Premier-League-Stats'


# In[29]:


for year in years:
    data = requests.get(url)
    soup = BeautifulSoup(data.text)
    table = soup.select('table.stats_table')[0]
    
    links = soup.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f'https://fbref.com/{l}' for l in links]
    
    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"
    
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace('-Stats','').replace('-',' ')
        
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match = 'Scores & Fixtures ')[0]
        
        soup = BeautifulSoup(data.text)
        links = soup.find_all('a')
        links = [l.get("href") for l in links]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        data = requests.get(f"https://fbref.com/{links[0]}")
        shooting = pd.read_html(data.text, match='Shooting')[0]
        shooting.columns = shooting.columns.droplevel()
        
        try:
            team_df = matches.merge(shooting[['Date','Sh','SoT','Dist','FK','PK','PKatt']],on='Date')
        except ValueError:
            continue
            
        team_df = team_df[team_df['Comp'] == 'Premier League']
        team_df['Season'] = year
        team_df['Team'] = team_name
        all_matches.append(team_df)
        time.sleep(1)
    


# In[ ]:


match_df = pd.concat(all_matches)


# In[ ]:


for year in years:
    data = requests.get(url)
    soup = BeautifulSoup(data.text)
    table = soup.select('table.stats_table')[0]
    
    links = soup.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f'https://fbref.com/{l}' for l in links]


# In[ ]:





# In[ ]:




