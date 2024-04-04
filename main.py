#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
#%%
'''
multi
?districtId=2008&districtId=1019&cuisineId=2009&cuisineId=2001
single
/cuisine/日本菜?districtId=2008

districtId
尖沙咀 2008
銅鑼灣 1019
旺角 2010

cuisineId
日本菜 2009
韓國菜 2001
'''
districtIDList = [2008,1019,2010,]
cuisineIDList = [2009, 2001,]
cuisineCatList = ['日本菜', '韓國菜']
districtIn = input('''
    地區：
    0.尖沙咀
    1.銅鑼灣
    2.旺角
    ''').split(' ')
cuisineIn = input('''
    地區：
    0.日本菜
    1.韓國菜
    ''').split(' ')
districtIn = list(map(int, districtIn))
cuisineIn = list(map(int, cuisineIn))
districtPost = ''

for index, i in enumerate(districtIn):
    if(index != 0):
        districtPost += '&'
    districtPost += f'districtId={districtIDList[i]}'
    
if len(cuisineIn) == 1:
    PostStr = f'/cuisine/{cuisineCatList[cuisineIn[0]]}?' + districtPost
else:
    cuisinePost = ''
    for index, i in enumerate(cuisineIn):
        if(index != 0):
            cuisinePost += '&'
        cuisinePost += f'cuisinePost={cuisineIDList[i]}'
        
    PostStr = '?' + districtPost + '&' + cuisinePost

#%%
driver = webdriver.Chrome('./chromedriver')
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}
url = f'https://www.openrice.com/zh/hongkong/restaurants{PostStr}'
print(url)
# response = requests.get(url, headers=headers)
driver.get(url)
scroll_pause_time = 2  # Pause between each scroll
screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
i = 1
for i in range(10):
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # i += 1
    time.sleep(scroll_pause_time)

    # Check if reaching the end of the page
    # scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # if screen_height * i > scroll_height:
    #     break
print('Finish')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
#%%
restaurants = soup.find_all('section', class_='poi-list-cell-desktop-right-top-info-section')
print(len(restaurants))
for i in restaurants:
    name = i.find('div', class_='text').text.replace('\n', '').replace('  ', '')
    address = i.find('div', class_='poi-list-cell-line-info').text
    for c in [' ', '/']:
        address = address.replace(c, '')
    address = address.split('\n')[1::2]
    address.insert(0, name)
    print(address)
# %%
