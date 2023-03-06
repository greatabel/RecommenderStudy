import time
import csv
import requests
from bs4 import BeautifulSoup

'''
1.获取网页内容：使用requests库发送HTTP请求并获取返回的网页内容。
2.解析网页内容：使用beautifulsoup4库解析网页内容，提取我们需要的信息（如职位标题和职位描述）。
3.存储数据：使用csv库将提取的数据存储到CSV文件中。
4.翻页：对于需要翻页的网站，编写一个循环，不断发送请求并解析页面，直到所有页面都被处理

'''
url = 'https://findajob.dwp.gov.uk/search?cat=28'
page_number = 1

with open('data/jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Description'])

    while True:
        response = requests.get(f'{url}&page={page_number}')
        soup = BeautifulSoup(response.content, 'html.parser')

        job_listings = soup.find_all('div', class_='search-result')

        if len(job_listings) == 0:
            # No more job listings, break out of the loop
            break

        for job in job_listings:
            h3_content = job.find('h3').text.strip()
            title_words = h3_content.split()
            title = ' '.join(word for word in title_words if not word.isnumeric())
            description = job.find('p', class_='govuk-body search-result-description').text.strip()
            print(title, description)
            print('#'*20)
            writer.writerow([title, description])
            time.sleep(1)
        page_number += 1

