from selenium import webdriver
import time
import os
import requests


url = 'https://www.google.com.hk/search?q='+keyword+'&tbm=isch'


class Crawler_google_images:
    # 初始化
    def __init__(self,search_key=''):
        self.url = ''
        if type(search_key) == str:
            ## convert to list even for one search keyword to standalize the pulling.
            self.g_search_key_list = [search_key]
        elif type(search_key) == list:
            self.g_search_key_list = search_key
        else:
            print('keyword not of type str or list')
            raise

        self.g_search_key = ''
        self.target_url_str = ''


    def reformat_search_for_spaces(self):

        self.g_search_key = self.g_search_key.rstrip().replace(' ', '+')

    def formed_search_url(self):

        self.reformat_search_for_spaces()
        self.target_url_str = url = 'https://www.google.com.hk/search?q='+self.g_search_key+'&tbm=isch'

    def get_searchlist_fr_file(self, filename):

        with open(filename, 'r') as f:
            self.g_search_key_list = f.readlines()

    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        browser = webdriver.Chrome(chrome_options=chrome_options)

        print(self.target_url_str)
        browser.get(self.target_url_str)

        browser.maximize_window()
        return browser


    def download_images(self, browser,round=2):

        thisname = self.g_search_key.replace('+', '_').replace('DnD_','')
        file_path = "./Google_Image_Result/" + thisname
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        img_url_dic = []

        count = 1
        pos = 0
        for i in range(round):
            pos += 500

            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)
            img_elements = browser.find_elements_by_tag_name('img')

            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        if 'images' in img_url:
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    filename = file_path + "/" + thisname + '.' +str(count) + ".jpg"
                                    r = requests.get(img_url)
                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    count += 1
                                    print('this is '+str(count)+'st img')
                                    time.sleep(0.2)
                                except:
                                    print('failure')

    def run(self):
        # self.__init__()

        for indiv_search in self.g_search_key_list:
            print("现在搜的是" + indiv_search)
            self.g_search_key = indiv_search
            self.reformat_search_for_spaces()
            self.formed_search_url()
            browser = self.init_browser()
            self.download_images(browser,10)
            browser.close()
            print("爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images('')
    searchlist_path = 'C:\zl\Workplace\pachong\Image_search_list.txt'
    craw.get_searchlist_fr_file(searchlist_path)


    craw.run()

