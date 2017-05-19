#coding: utf-8
from selenium import webdriver
from time import sleep
from db_wri import Lagou
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider():
    def __init__(self):
        self.dr = webdriver.PhantomJS()
        self.url = "https://www.lagou.com/"
        self.dr.get(self.url)
        self.map = {"beijing":5,
               "shanghai":6,
               "shenzhen":765,
               "guangzhou":763,
        }
        self.dr.find_element_by_id('cboxClose').click()
        self.spider_result = []
        
    
    def by_css(self, the_css):
        return self.dr.find_elements_by_css_selector(the_css)
    
    def by_one_css(self, the_css):
        return self.dr.find_element_by_css_selector(the_css)
    
    def is_nextpage(self):
        sleep(3)
        cur_page = self.by_one_css('span.curNum').text
        print cur_page
        page_num = self.by_one_css('span.span.totalNum').text
        if int(cur_page) < int(page_num):
            return True
        else:return False
        
    def click_nextpage(self):
        return self.by_one_css('#s_position_list > div.item_con_pager > div > span.pager_next').click()
        
    def search(self, city_id):
        js = "$('#search_input').val('神马');$('#search_button').click()"
        self.dr.execute_script(js)
        js = '$("a[data-id=%s]").click()'%(city_id)
        self.dr.execute_script(js)
        
    def get_onepage_data(self):
        content = self.by_css('#s_position_list > ul > li.con_list_item')
        for i in content:
            result = {}
            result['company'] =i.get_attribute('data-company')
            result['position'] =i.get_attribute('data-positionname')
            result['salary'] = i.get_attribute('data-salary')
            self.spider_result.append(result)
    
    def get_all_data(self,city):
        city_id = self.map[city]
        self.search(city_id)
        self.get_onepage_data()
        while self.is_nextpage():
            self.click_nextpage()
            sleep(2)
            self.get_onepage_data()
            sleep(2)
            continue
        return self.spider_result
    
    def end(self):
        self.dr.quit()
               
if __name__ == '__main__':
    city = sys.argv[1]
    lagou = spider(city)
    result = lagou.get_all_data()
    lagou.end()
    for i in result:
        Lagou.create(city=city,
                     company=i['company'],
                     position=i['position'],
                     salary=i['salary'],
                     )
