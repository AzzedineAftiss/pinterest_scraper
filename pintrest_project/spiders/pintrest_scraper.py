# div > div.XiG.sLG.zI7.iyn.Hsu > div > a
# div.mQ8.sLG.ujU.zI7.iyn.Hsu > div > div > div > div > div > span

import scrapy
import urllib
# import selenuim
from scrapy.selector import Selector

from scrapy.http import Request

class PintrestScraper(scrapy.Spider):
    name = "pintrest_scraper"
    start_urls = ["https://www.pinterest.com/"]

    def parse(self, response, **kwargs):
        # pins_lst = []
        pins = response.css("div.Yl-")
        pages_pins = response.meta.get("bodies")
        print("=" * 25, len(pages_pins), "=" * 25)
        # for pin in pins :
        #     pin_id = pin.css("div > div.XiG.sLG.zI7.iyn.Hsu > div > a::attr(href)").get()
        #     url = response.urljoin(pin_id)
        #     yield {
        #         "pin": url
        #     }
        for body in pages_pins:
            body_html = Selector(text=body)
            pins = body_html.css("div > div.XiG.sLG.zI7.iyn.Hsu > div > a::attr(href)").getall()
            urls = self.get_pin_url(pins, response)
            # url = response.urljoin(pin_id)
            for url in urls:
                yield Request(url, callback=self.parse_pin,  meta={'board': True})

                # yield {
                #     "pin": url
                # }
        # from selenium import webdriver
        # from selenium.webdriver.common.keys import Keys
        # driver = webdriver.Chrome(executable_path='chromedriver.exe')
        # driver.get("https://www.facebook.com/")
        # FB_ID = 'YOUR_FB_ID'
        # FB_PSD = 'YOUR_FB_PSD'
        # email = driver.find_element_by_id("email")  ## locating email input
        # email.send_keys(id)  ## Sending Username as input
        # Password = driver.find_element_by_id("pass")
        # Password.send_keys(password)
        # ## Clicking Login Button
        # button = driver.find_element_by_name("login").click()
        # or
        # button = driver.find_element_by_name("login")
        # button.send_keys(Keys.ENTER)

    def get_pin_url(self, pins, response):
        urls = []
        for pin_id in pins:
            url = response.urljoin(pin_id)
            urls.append(url)
        return urls
        #     yield {
        #         "pin": url
        #     }

    def parse_pin(self, response):

        pin_title = response.xpath("//div/div/div/div/div/a/h1/text()").get()
        pin_discription = response.xpath("//div[1]/span/span/span/span/text()").get()
        pin_user = response.xpath("//div[@class='tBJ dyH iFc j1A O2T zDA IZT H2s']/text()").get()
        # pin_followers = response.xpath("//div[@class='tBJ dyH iFc j1A O2T zDA IZT swG']//text()").get()
        pin_user_url = response.xpath("//div[3]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/a/@href").get()
        pin_img_url = response.xpath("//div[contains(@class, 'Pj7 sLG XiG eEj m1e')]//img/@src").extract()
        if isinstance(pin_img_url, list):
             pin_img_url = pin_img_url[0]
        pin_url = response.request.url
        print("pin_url_azzedine : ", pin_url)
        if pin_img_url is None:
            print("Found Image")
            pin_img_url = response.xpath("//div[contains(@class, 'Pj7 sLG XiG eEj m1e')]//video/@src").extract()[0]

        print("hack ", "="*25, pin_user_url, "="*25)
        url_user = "https://www.pinterest.com"
        if pin_user_url  is not None:
            url_user = "https://www.pinterest.com"+pin_user_url
        if pin_user_url:
            yield Request(url_user, callback=self.parse_pin_full, meta={'url_user': url_user, 'pin_title': pin_title, "pin_discription": pin_discription, 'pin_user': pin_user, "user_exist": True, 'pin_img_url': pin_img_url, 'pin_url': pin_url})
        else:
            yield Request(url_user, callback=self.parse_pin_full, meta={'pin_title': pin_title, "pin_discription": pin_discription, 'pin_user': pin_user, "user_exist": False , 'pin_img_url': pin_img_url, 'pin_url': pin_url})

        # yield {
        #     'pin_title' : pin_title,
        #     'pin_discription': pin_discription,
        #     'pin_user': pin_user,
        #     'pin_followers': pin_followers
        # }

    def parse_pin_full(self, response):
        img_urls_lst = []
        pin_title = response.request.meta.get("pin_title")
        request_url = response.request.url
        pin_discription = response.request.meta.get("pin_discription")
        pin_user = response.request.meta.get("pin_user")
        pin_img_url = response.request.meta.get("pin_img_url")
        pin_url = response.request.meta.get("pin_url")
        img_urls_lst.append(pin_img_url)
        data = {
            'user_exist' : response.request.meta.get("user_exist"),
            'url_user': response.request.meta.get("url_user"),
            'request_url' : request_url,
            'pin_title' : pin_title,
            'pin_discription': pin_discription,
            'pin_user': pin_user,
            'pin_url': pin_url,
            "pin_img": pin_img_url,
            'image_urls' : img_urls_lst
        }
        self.download_img(pin_img_url)
        user_exist = response.request.meta.get("user_exist")
        if user_exist:
            print("I am in user exist if-statement")
            # data["user_nbr_followers"] = response.xpath("//div[4]/div/div[1]/div/span/text()").get()
            data["user_nbr_followers"] = response.xpath("//div[contains(@class, 'gjz hs0 un8 C9i TB_')]/div/div/span/text()").get()
            print("data user nbr followers azzedine : ", data["user_nbr_followers"])
            # data["user_nbr_following"] = response.xpath("//div[4]/div/div[2]/div/span/text()").get()
            data["user_nbr_following"] = response.xpath("//div[contains(@class, 'gjz hs0 un8 C9i TB_')]/div/div/span/text()").get()



        yield data
#
# //div[contains(@class, 'Pj7 sLG XiG eEj m1e')]//img/@src

    def download_img(self, imageurl):
        imagename = imageurl.split("/")[-1]
        req = urllib.request.Request(imageurl, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'})
        resource = urllib.request.urlopen(req)
        output = open("../pin_images/" + imagename, "wb")
        output.write(resource.read())
        output.close()