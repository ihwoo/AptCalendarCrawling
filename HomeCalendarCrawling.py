#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# In[2]:


data=[]


# In[3]:


#자이 홈페이지 크롤링
xi_res=requests.get('https://xi.co.kr/apt_info/calendar/index')
xi_soup=bs(xi_res.content,'html.parser')
xi_items=xi_soup.find_all(target='_blank')


# In[4]:


#자이 홈페이지 크롤링
for item in xi_items:
    datacol=["",item.string, item.attrs['href']]
    data.append(datacol)
    #print(datacol)
    #print(item.string, item.attrs['href'])


# In[5]:


#힐스테이트 크롤링
hill_hec_res=requests.get('https://www.hillstate-hec.co.kr/salesinfo/s_plan.aspx')
hill_hec_soup=bs(hill_hec_res.content,'html.parser')
hill_hec_list=hill_hec_soup.find(class_='s_schedule_list')
hill_hec_items=hill_hec_list.find_all('li')


# In[6]:


#힐스테이트 크롤링
for item in hill_hec_items:
    date=item.find(class_='date')
    name=item.find('dt')
    infolist=item.select('tbody > tr > td')
    datacol=[date.string, name.string.replace("\r","").replace("\n","").replace("  ",""), infolist[0].text.replace("\r","").replace("\n","").replace("  ","")]
    data.append(datacol)
    #print(datacol)
    #print(f'{date.string} {name.string} {infolist[0].text}')


# In[7]:


#롯데캐슬 크롤링
lotte_res=requests.get('https://www.lottecastle.co.kr/apt/lotsolid/list.do?cmsMenuCd=CM0062')
lotte_soup=bs(lotte_res.content,'html.parser')
lotte_apt_items=lotte_soup.find_all(class_='aptItem')


# In[8]:


#롯데캐슬 크롤링
for item in lotte_apt_items:
    try :
        link=""
        if item.find(class_='pic').has_attr('href'):
            link="https://www.lottecastle.co.kr"+item.find(class_='pic').attrs['href']
        name=item.find(class_='tit')
        info=item.find_all('span')
        datacol=[name.string,]
        #print(f'{name.string},\t ',end=' ')
        for i in info:
            if '분양예정' in i.get_text():
                if len(i.get_text())>5:
                    datacol.insert(0,i.get_text())
            else :
                datacol.append(i.get_text())
        datacol.append(link)
        
        data.append(datacol)
        print(datacol)
        #print(link)
    except :
        print('err')
    


# In[10]:


df=pd.DataFrame(data)
df.to_csv('HomeCal.csv',header=False, index=False)


# In[ ]:




