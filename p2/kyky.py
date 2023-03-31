import requests
import lxml
import json
from bs4  import BeautifulSoup
import csv
import random
from time import sleep

# url='https://health-diet.ru/table_calorie/'


headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'
}
# red= requests.get(url)
# src=red.text
# print(src)

# with open('p2/index.html','w',encoding='utf-8') as file:
#     file.write(src)
# with open('p2/index.html','r',encoding='utf-8') as file:
#    src=file.read()

# soup=BeautifulSoup(src,'lxml')



# all_products_hrefs=soup.find_all(class_='mzr-tc-group-item-href')  

# all_categories_dict={}
# for item in  all_products_hrefs :
#     item_text=item.text
#     item_href= 'https://health-diet.ru'+item.get('href')
    

#     all_categories_dict[item.text] =item_href

# with open('1parsing/all_categories_dict.json','w',encoding='utf-8')as file:
#     json.dump(all_categories_dict,file,indent=4,ensure_ascii=False  )

with open('p2/all_categories_dict.json',encoding='utf-8')as file:
    all_categories=json.load(file)
interation_count= int(len(all_categories))-1
count=0
print('всего интераций:{interation_count}')

for category_name , category_href in all_categories.items():

    rep=[',',' ','-',"'"]
    for item in rep:
        if item in category_name:
            category_name=category_name.replace(item,"_")
    rep=requests.get(url=category_href, headers=headers)
    src=rep.text

    with open(f"p2/data/{count}_{category_name}.html","w",encoding="utf-8") as file:
        file.write( src)

    with open(f"p2/data/{count}_{category_name}.html",encoding="utf-8") as file:
        src=file.read()

    soup=  BeautifulSoup(src, 'lxml') 

    alert_blok =soup.find(class_= 'uk-alert-danger')
    if alert_blok is not None:
        continue

    table_head=soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product=table_head[0].text
    calories=table_head[1].text
    proteins=table_head[2].text
    fats=table_head[3].text
    carbohudrates=table_head[4].text
    
    with open(f"p2/data/{count}_{category_name}.csv","w",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(
            (
            product,
            calories,
            proteins,
            fats,
            carbohudrates   
            )
        )
    product_data=soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_into=[]

    for item in product_data:
        product_tds=item.find_all('td')

        title=product_tds[0].find('a').text
        calories=product_tds[1].text
        proteins=product_tds[2].text
        fats=product_tds[3].text
        carbohudrates=product_tds[4].text

        product_into.append(
            {
                'title':title,
                'calories':calories,
                'proteins':proteins,
                'fats':fats,
                'carbohudrates':carbohudrates
                
            }
        )

    with open(f"p2/data/{count}_{category_name}.csv","a",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(
            (
            title,
            calories,
            proteins,
            fats,
            carbohudrates   
            )
        )
    with open(f"p2/data/{count}_{category_name}.json","a",encoding="utf-8") as file:
        json.dump(product_into,file,indent=4, ensure_ascii=False)

    count+=1
    print(f'£ интерация {count}.{category_name} записан....')
    interation_count=interation_count-1

    if interation_count==0:
        print('Работа завершина')
        break
    print(f'Интераций осталсь:{interation_count}')
    sleep ( random.randrange(2 , 4) )


        












