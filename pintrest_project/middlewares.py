# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class PintrestProjectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)


        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PintrestProjectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        print("I am in middlware")
        # driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=desired_capabilities, )
        # driver.get("https://openaq.org/#/countries")
        # driver.implicitly_wait(10)
        # try:
        #     element = WebDriverWait(driver, 5).until(
        #         EC.presence_of_element_located((By.ID, "mySuperId"))
        #     )
        # finally:
        #     driver.quit()
        # wait = WebDriverWait(driver, 5)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card__title")))

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signals.spider_closed)
        return s

    def process_request(self, request, spider):
        print(f"len(request.meta) = {len(request.meta)}")
        if not "board" in request.meta.keys() and not "user_exist" in request.meta.keys():
            print("i am in process_request!!!")
            self.driver.get(request.url)

            for cookie_name, cookie_value in request.cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'wc1')
                )
                )

            login_btn = self.driver.find_element("xpath", "//div[1]/div/div/div[1]/div/div[2]/div[2]/button")
            print(f"login button : {login_btn}")
            login_btn.click()
            time.sleep(10)
            input_email = self.driver.find_element("xpath", "//*[@id='email']")
            input_email.send_keys('azedineaftiss@gmail.com')

            input_password = self.driver.find_element("xpath", "//*[@id='password']")
            input_password.send_keys('1234585')

            login_btn_1 = self.driver.find_element("xpath", "//div[4]/form/div[7]/button")
            login_btn_1.click()
            time.sleep(10)
            # azedineaftiss19972006@gmail.com
            # 1928374651997
            # Scroll to Bottom of Webpage
            bodies = []
            for i in range(1):
                bodies.append(str.encode(self.driver.page_source))
                time.sleep(10)
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # Scroll to Pixel 600 of Webpage or document.body.scrollHeight
            # driver.execute_script("window.scrollTo(0,600))
            # input_email xpath : //*[@id="email"]
            # password xpath : //*[@id="password"]
            # button //div[4]/form/div[7]/button



            self.driver.get_screenshot_as_png()

            # if request.script:
            #     self.driver.execute_script(request.script)

            # time.sleep(100)
            self.driver.implicitly_wait(10)
            body = str.encode(self.driver.page_source)
            bodies.append(str.encode(self.driver.page_source))
            # Expose the driver via the "meta" attribute
            request.meta.update({'driver': self.driver, "bodies": bodies})

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request,

            )
        else:
            self.driver.get(request.url)
            # time.sleep(100)
            self.driver.implicitly_wait(20)
            time.sleep(10)
            body = str.encode(self.driver.page_source)
            # Expose the driver via the "meta" attribute
            # request.meta.update({'driver': self.driver, "bodies": bodies})

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request,
            )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        # self.driver.quit()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
