import json
import random
import time
import requests
from parsel import Selector
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --------- if you need next_page data just uncomment block of of code of next page or comment uncommeted Flag = False which positioned after next page code which used for breaking while loop


def problem1(input_keyword):

    data = []

    urls = [f'https://www.flipkart.com/search?q={input_keyword}',f'https://www.amazon.in/s?k={input_keyword}']
    for url in urls:

        if 'amazon' in url:

            Flag = True

            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url,headers=headers)
                req1 = Selector(text=req.text)

                divs = req1.xpath('//*[@class="a-section"]//div[@class="a-section a-spacing-small a-spacing-top-small"]')
                for div in divs:

                    item = {}

                    item['Product_link'] = 'https://www.amazon.in' + div.xpath('.//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').get()

                    response = requests.get(item['Product_link'],headers=headers)
                    response1 = Selector(text=response.text)

                    item['Title'] = response1.xpath('//*[@id="productTitle"]/text()').get().strip()
                    item['Source'] = 'Amazon'
                    try:
                        Price = response1.xpath(
                            '//*[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').get()
                        if not Price:
                            Price = response1.xpath(
                                '//*[@id="tp_price_row_ww"]//span[@class="a-offscreen"]/text()').get()
                        item['Price'] = Price.replace("₹", '').replace(',','')
                    except:
                        item['Price'] = ''
                    try:
                        item['Brand'] = response1.xpath(
                            '//span[contains(text(),"Brand")]/parent::td/following-sibling::td/span/text()').get()
                        if not item['Brand']:
                            item['Brand'] = response1.xpath('//*[@id="bylineInfo"][contains(text(),"Brand:")]/text()').get()
                    except:
                        item['Brand'] = ''
                    try:
                        Model = response1.xpath('//th[contains(text(),"Item model number")]/following-sibling::td/text()').get()
                        if not Model:
                            Model = response1.xpath('//th[contains(text(),"Model")]/following-sibling::td/text()').get()
                        item['Model'] = Model.replace("\u200e", '').strip()
                    except:
                        item['Model'] = ''
                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()
                # if next_page:
                #     url = 'https://www.amazon.in' + next_page
                # else:
                #     Flag = False


                Flag = False

        else:

            Flag = True

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url, headers=headers)
                req1 = Selector(text=req.text)

                product_links = req1.xpath(
                    '//a[@class="_1fQZEK"]/@href').getall()
                for link in product_links:

                    item = {}

                    item['Product_link'] = 'https://www.flipkart.com' + link

                    response = requests.get(item['Product_link'], headers=headers)
                    response1 = Selector(text=response.text)

                    jsv = response1.xpath('//*[@type="application/ld+json"]/text()').get()
                    js = json.loads(jsv)
                    try:
                        item['Title'] = js[0]['name']
                    except:
                        try:
                            item['Title'] = response1.xpath('//span[@class="B_NuCI"]/text()').get()
                        except:
                            item['Title'] = ''
                    item['Source'] = 'Flipkart'
                    try:
                        item['Price'] = js[1]['offers']['price'].replace("₹", '').replace(',','')
                    except:
                        try:
                            item['Price'] = js[0]['offers']['price'].replace("₹", '').replace(',','')
                        except:
                            try:
                                item['Price'] = response1.xpath('//*[@class="_30jeq3 _16Jk6d"]/text()').get().replace("₹", '').replace(',','')
                            except:
                                item['Price'] = ''

                    try:
                        item['Brand'] = js[1]['brand']['name']
                    except:
                        try:
                            item['Brand'] = js[0]['brand']['name']
                        except:
                            item['Brand'] = ''

                    try:
                        item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[2]').get().rsplit(',', 1)[
                            1].replace(')', '')
                    except:
                        try:
                            item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[1]').get().rsplit(',', 1)[
                                1].replace(')', '')
                        except:
                            item['Model'] = ''

                    print(item)
                    data.append(item)



                next_page = req1.xpath('//*[@class="_1LKTO3"]/@href').get()
                if next_page:
                    url = 'https://www.flipkart.com' + next_page
                else:
                    Flag = False

                # Flag = False

    df = pd.DataFrame(data)

    file = "Amazon" + '.xlsx'
    writer = pd.ExcelWriter(
        file, engine='xlsxwriter', options={'strings_to_urls': False})
    print(file)
    df.to_excel(writer, 'Sheet1')
    writer.save()




def problem2(input_keyword,amazon_filter,flipkart_filter):

    data = []

    urls = [f'https://www.flipkart.com/search?q={input_keyword}&sort={flipkart_filter}',f'https://www.amazon.in/s?k={input_keyword}&s={amazon_filter}']
    for url in urls:

        if 'amazon' in url:

            Flag = True

            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url,headers=headers)
                req1 = Selector(text=req.text)

                divs = req1.xpath('//*[@class="a-section"]//div[@class="a-section a-spacing-small a-spacing-top-small"]')
                for div in divs:

                    item = {}

                    item['Product_link'] = 'https://www.amazon.in' + div.xpath('.//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').get()

                    response = requests.get(item['Product_link'],headers=headers)
                    response1 = Selector(text=response.text)

                    item['Title'] = response1.xpath('//*[@id="productTitle"]/text()').get().strip()
                    item['Source'] = 'Amazon'
                    try:
                        Price = response1.xpath(
                            '//*[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').get()
                        if not Price:
                            Price = response1.xpath(
                                '//*[@id="tp_price_row_ww"]//span[@class="a-offscreen"]/text()').get()
                        item['Price'] = Price.replace("₹", '').replace(',','')
                    except:
                        item['Price'] = ''
                    try:
                        item['Brand'] = response1.xpath(
                            '//span[contains(text(),"Brand")]/parent::td/following-sibling::td/span/text()').get()
                        if not item['Brand']:
                            item['Brand'] = response1.xpath('//*[@id="bylineInfo"][contains(text(),"Brand:")]/text()').get()
                    except:
                        item['Brand'] = ''
                    try:
                        Model = response1.xpath('//th[contains(text(),"Item model number")]/following-sibling::td/text()').get()
                        if not Model:
                            Model = response1.xpath('//th[contains(text(),"Model")]/following-sibling::td/text()').get()
                        item['Model'] = Model.replace("\u200e", '').strip()
                    except:
                        item['Model'] = ''
                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()
                # if next_page:
                #     url = 'https://www.amazon.in' + next_page
                # else:
                #     Flag = False


                Flag = False

        else:

            Flag = True

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url, headers=headers)
                req1 = Selector(text=req.text)

                product_links = req1.xpath(
                    '//a[@class="_1fQZEK"]/@href').getall()
                for link in product_links:

                    item = {}

                    item['Product_link'] = 'https://www.flipkart.com' + link
                    response = requests.get(item['Product_link'], headers=headers)
                    response1 = Selector(text=response.text)

                    jsv = response1.xpath('//*[@type="application/ld+json"]/text()').get()
                    js = json.loads(jsv)
                    try:
                        item['Title'] = js[0]['name']
                    except:
                        try:
                            item['Title'] = response1.xpath('//span[@class="B_NuCI"]/text()').get()
                        except:
                            item['Title'] = ''
                    item['Source'] = 'Flipkart'
                    try:
                        item['Price'] = js[1]['offers']['price'].replace("₹", '').replace(',', '')
                    except:
                        try:
                            item['Price'] = js[0]['offers']['price'].replace("₹", '').replace(',', '')
                        except:
                            try:
                                item['Price'] = response1.xpath('//*[@class="_30jeq3 _16Jk6d"]/text()').get().replace(
                                    "₹", '').replace(',', '')
                            except:
                                item['Price'] = ''

                    try:
                        item['Brand'] = js[1]['brand']['name']
                    except:
                        try:
                            item['Brand'] = js[0]['brand']['name']
                        except:
                            item['Brand'] = ''

                    try:
                        item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[2]').get().rsplit(',', 1)[
                            1].replace(')', '')
                    except:
                        try:
                            item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[1]').get().rsplit(',', 1)[
                                1].replace(')', '')
                        except:
                            item['Model'] = ''

                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//*[@class="_1LKTO3"]/@href').get()
                # if next_page:
                #     url = 'https://www.flipkart.com' + next_page
                # else:
                #     Flag = False

                Flag = False

    df = pd.DataFrame(data)

    file = "Amazon" + '.xlsx'
    writer = pd.ExcelWriter(
        file, engine='xlsxwriter', options={'strings_to_urls': False})
    print(file)
    df.to_excel(writer, 'Sheet1')
    writer.save()





def problem3(input_keyword):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # if you want headless browser just uncomment this
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    data = []

    urls = [f'https://www.flipkart.com/search?q={input_keyword}', f'https://www.amazon.in/s?k={input_keyword}']
    for url in urls:

        if 'amazon' in url:
            Flag = True

            while Flag:

                driver.get(url)

                time.sleep(random.randrange(5, 10))

                req1 = Selector(text=driver.page_source)

                divs = req1.xpath('//*[@class="a-section"]//div[@class="a-section a-spacing-small a-spacing-top-small"]')
                for div in divs:

                    item = {}

                    item['Product_link'] = 'https://www.amazon.in' + div.xpath(
                        './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').get()

                    driver.get(item['Product_link'])

                    time.sleep(random.randrange(5, 10))
                    response1 = Selector(text=driver.page_source)

                    item['Title'] = response1.xpath('//*[@id="productTitle"]/text()').get().strip()
                    item['Source'] = 'Amazon'
                    try:
                        Price = response1.xpath(
                            '//*[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').get()
                        if not Price:
                            Price = response1.xpath(
                                '//*[@id="tp_price_row_ww"]//span[@class="a-offscreen"]/text()').get()
                        item['Price'] = Price.replace("₹", '').replace(',','')
                    except:
                        item['Price'] = ''
                    try:
                        item['Brand'] = response1.xpath(
                            '//span[contains(text(),"Brand")]/parent::td/following-sibling::td/span/text()').get()
                        if not item['Brand']:
                            item['Brand'] = response1.xpath('//*[@id="bylineInfo"][contains(text(),"Brand:")]/text()').get()
                    except:
                        item['Brand'] = ''
                    try:
                        Model = response1.xpath('//th[contains(text(),"Item model number")]/following-sibling::td/text()').get()
                        if not Model:
                            Model = response1.xpath('//th[contains(text(),"Model")]/following-sibling::td/text()').get()
                        item['Model'] = Model.replace("\u200e", '').strip()
                    except:
                        item['Model'] = ''
                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()
                # if next_page:
                #     url = 'https://www.amazon.in' + next_page
                # else:
                #     Flag = False

                Flag = False

        else:

            Flag = True

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                driver.get(url)

                time.sleep(random.randrange(5, 10))

                req1 = Selector(text=driver.page_source)

                product_links = req1.xpath(
                    '//a[@class="_1fQZEK"]/@href').getall()
                for link in product_links:

                    item = {}

                    item['Product_link'] = 'https://www.flipkart.com' + link

                    driver.get(item['Product_link'])

                    time.sleep(random.randrange(5, 10))
                    response1 = Selector(text=driver.page_source)

                    jsv = response1.xpath('//*[@type="application/ld+json"]/text()').get()
                    js = json.loads(jsv)
                    try:
                        item['Title'] = js[0]['name']
                    except:
                        try:
                            item['Title'] = response1.xpath('//span[@class="B_NuCI"]/text()').get()
                        except:
                            item['Title'] = ''
                    item['Source'] = 'Flipkart'
                    try:
                        item['Price'] = js[1]['offers']['price'].replace("₹", '').replace(',', '')
                    except:
                        try:
                            item['Price'] = js[0]['offers']['price'].replace("₹", '').replace(',', '')
                        except:
                            try:
                                item['Price'] = response1.xpath('//*[@class="_30jeq3 _16Jk6d"]/text()').get().replace(
                                    "₹", '').replace(',', '')
                            except:
                                item['Price'] = ''

                    try:
                        item['Brand'] = js[1]['brand']['name']
                    except:
                        try:
                            item['Brand'] = js[0]['brand']['name']
                        except:
                            item['Brand'] = ''

                    try:
                        item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[2]').get().rsplit(',', 1)[
                            1].replace(')', '')
                    except:
                        try:
                            item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[1]').get().rsplit(',', 1)[
                                1].replace(')', '')
                        except:
                            item['Model'] = ''

                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//*[@class="_1LKTO3"]/@href').get()
                # if next_page:
                #     url = 'https://www.flipkart.com' + next_page
                # else:
                #     Flag = False

                Flag = False

    df = pd.DataFrame(data)

    file = "Amazon_selenium" + '.xlsx'
    writer = pd.ExcelWriter(
        file, engine='xlsxwriter', options={'strings_to_urls': False})
    print(file)
    df.to_excel(writer, 'Sheet1')
    writer.save()



def problem4(file_name):

    # ------------ if there was not any dublicate product with different price for amazon and flipkart you can add manually in Amazon.xlsx for check i checked its working

    df = pd.read_excel(file_name)
    df.sort_values(by=['Model',"Price"], inplace=True)
    df = df.drop_duplicates(subset=['Model'], keep='last') # if you want to also check for product_name you need to add "Title" in subset

    file = "Amazon_compare" + '.xlsx'
    writer = pd.ExcelWriter(
        file, engine='xlsxwriter', options={'strings_to_urls': False})
    print(file)
    df.to_excel(writer, 'Sheet1')
    writer.save()





def problem5(input_keyword):

    proxies = {
        "http": "http://scraperapi:df1a32d04b794153ad1c51a152bf520f@proxy-server.scraperapi.com:8001"
    }

    # ------------------- we need to add proxy for ip rotation for  protection against web-crawling which blocks our IP ------ #
    #--------------------it's added in requests as a proxies parameter ---------------------------------------------#

    data = []

    urls = [f'https://www.flipkart.com/search?q={input_keyword}', f'https://www.amazon.in/s?k={input_keyword}']
    for url in urls:

        if 'amazon' in url:

            Flag = True

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url, headers=headers,proxies=proxies)
                req1 = Selector(text=req.text)

                divs = req1.xpath(
                    '//*[@class="a-section"]//div[@class="a-section a-spacing-small a-spacing-top-small"]')
                for div in divs:

                    item = {}

                    item['Product_link'] = 'https://www.amazon.in' + div.xpath(
                        './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').get()

                    response = requests.get(item['Product_link'], headers=headers,proxies=proxies)
                    response1 = Selector(text=response.text)

                    item['Title'] = response1.xpath('//*[@id="productTitle"]/text()').get().strip()
                    item['Source'] = 'Amazon'
                    try:
                        Price = response1.xpath(
                            '//*[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').get()
                        if not Price:
                            Price = response1.xpath(
                                '//*[@id="tp_price_row_ww"]//span[@class="a-offscreen"]/text()').get()
                        item['Price'] = Price.replace("₹", '').replace(',', '')
                    except:
                        item['Price'] = ''
                    try:
                        item['Brand'] = response1.xpath(
                            '//span[contains(text(),"Brand")]/parent::td/following-sibling::td/span/text()').get()
                        if not item['Brand']:
                            item['Brand'] = response1.xpath(
                                '//*[@id="bylineInfo"][contains(text(),"Brand:")]/text()').get()
                    except:
                        item['Brand'] = ''
                    try:
                        Model = response1.xpath(
                            '//th[contains(text(),"Item model number")]/following-sibling::td/text()').get()
                        if not Model:
                            Model = response1.xpath('//th[contains(text(),"Model")]/following-sibling::td/text()').get()
                        item['Model'] = Model.replace("\u200e", '').strip()
                    except:
                        item['Model'] = ''
                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()
                # if next_page:
                #     url = 'https://www.amazon.in' + next_page
                # else:
                #     Flag = False

                Flag = False

        else:

            Flag = True

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

            while Flag:

                req = requests.get(url, headers=headers,proxies=proxies)
                req1 = Selector(text=req.text)

                product_links = req1.xpath(
                    '//a[@class="_1fQZEK"]/@href').getall()
                for link in product_links:

                    item = {}

                    item['Product_link'] = 'https://www.flipkart.com' + link
                    response = requests.get(item['Product_link'], headers=headers,proxies=proxies)
                    response1 = Selector(text=response.text)

                    jsv = response1.xpath('//*[@type="application/ld+json"]/text()').get()
                    js = json.loads(jsv)
                    try:
                        item['Title'] = js[0]['name']
                    except:
                        try:
                            item['Title'] = response1.xpath('//span[@class="B_NuCI"]/text()').get()
                        except:
                            item['Title'] = ''
                    item['Source'] = 'Flipkart'
                    try:
                        item['Price'] = js[1]['offers']['price'].replace("₹", '').replace(',', '')
                    except:
                        try:
                            item['Price'] = js[0]['offers']['price'].replace("₹", '').replace(',', '')
                        except:
                            try:
                                item['Price'] = response1.xpath('//*[@class="_30jeq3 _16Jk6d"]/text()').get().replace(
                                    "₹", '').replace(',', '')
                            except:
                                item['Price'] = ''

                    try:
                        item['Brand'] = js[1]['brand']['name']
                    except:
                        try:
                            item['Brand'] = js[0]['brand']['name']
                        except:
                            item['Brand'] = ''

                    try:
                        item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[2]').get().rsplit(',', 1)[
                            1].replace(')', '')
                    except:
                        try:
                            item['Model'] = response1.xpath('//span[@class="B_NuCI"]/text()[1]').get().rsplit(',', 1)[
                                1].replace(')', '')
                        except:
                            item['Model'] = ''

                    print(item)
                    data.append(item)

                # next_page = req1.xpath('//*[@class="_1LKTO3"]/@href').get()
                # if next_page:
                #     url = 'https://www.flipkart.com' + next_page
                # else:
                #     Flag = False

                Flag = False

    df = pd.DataFrame(data)

    file = "Amazon" + '.xlsx'
    writer = pd.ExcelWriter(
        file, engine='xlsxwriter', options={'strings_to_urls': False})
    print(file)
    df.to_excel(writer, 'Sheet1')
    writer.save()



problem1("refrigerator")  # ----- here was passed refrigerator as search term
# problem2("refrigerator","price-asc-rank","price_asc") # ----- here was passed refrigerator as search term or some other filter if you need to change it you need to pass as per site corresponding filter currently i passsed price filter
# problem3("refrigerator") # ----- here was passed refrigerator as search term
# problem4('Amazon.xlsx') # ----- here was passed excel file which containing data
# problem5("refrigerator") # ----- here was passed refrigerator as search term