import scrapy
from playwright.sync_api import sync_playwright

class SamsPlaywrightSpider(scrapy.Spider):
    name = 'sams_playwright'
    allowed_domains = ['sams.com.mx']
    start_urls = ['https://www.sams.com.mx/electronica-y-computacion/cat30186']


    def parse(self, response):
        with sync_playwright() as p :
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(response.url)
            page.press('body','Enter')
            self.choose_store(page)
            products = page.query_selector_all('//div[@class="product-listing  desktop"]/div[contains(@class,"itemBox-container-wrp grid-itemBox-wrp")]')
            for product in products :
                loader = ItemLoader(SamsItem(),response)
                loader.add_value('product_url',product.query_selector('a.item-name').get_attribute('href'))
                loader.add_value('sku'.loader._values['product_url'][0].split('/')[-1])
                loader.add_value('image_url',product.query_selector('img[class="lazy-image lazyloaded"]').get_attribute('src'))
                loader.add_value('high_price',product.query_selector_all('span.normal')[-1].inner_text())
                loader.add_value('low_price',product.query_selector_all('div.item-oldprice')[-1].inner_text())
                loader.add_value('title',product.query_selector('a.item-name').inner_text())
                loader.add_value('tags',[tag.inner_text() for tag in product.query_selector_all('span.item-option-name')])
                yield loader.load_item()
        # data = response.json()
        # products = [product for product in nested_lookup('records',data) if product]
        # for product in products : 
        #     loader = ItemLoader(SamsItem(),response)
        #     loader.add_value('product_url',product[0]['attributes']['product.seoURL'][0])
        #     loader.add_value('sku',product[0]['attributes']['sku.repositoryId'][0]) 
        #     loader.add_value('image_url',self.image_template_url.format(loader._values['sku'][0]))
        #     loader.add_value('high_price',product[0]['attributes']['sku.lastPrice'][0])
        #     loader.add_value('low_price',product[0]['attributes']['sku.lastPrice'][0])
        #     loader.add_value('title',product[0]['attributes']['skuDisplayName'][0])
        #     #loader.add_value('tags')
        #     yield loader.load_item()


    def choose_store(self,page):
        page.hover('//div[@class="selector-box"]')
        page.wait_for_timeout('1000')
        page.query_selector('//select[@class="select-state"]').select_option('Ciudad de México')
        page.wait_for_timeout('1000')
        page.query_selector('//div[@class="address" and contains(text(),"Calzada Acoxpa")]').click()
        page.wait_for_timeout('1000')
        page.click('//button[contains(text(),"Confirmar")]')
        page.wait_for_timeout(5000)
        