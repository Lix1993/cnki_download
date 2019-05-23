#!/usr/bin/env Python
# coding=utf-8
import  os
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


 

def do_download(driver,url):

    driver.get(url)
    paper_title = driver.title[:-7]
    print( u"准备下载:"+ paper_title)

    download_button = browser.find_element_by_xpath(u"//a[contains(text(),'整本下载')]")

    download_button.send_keys(Keys.ENTER)





def get_download_url(browser,keyword):
        
        browser.get("http://kns.cnki.net/kns/brief/default_result.aspx")

        element = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.ID,"txt_1_value1"))
        )

        element.send_keys(keyword)
        print( u"搜索:%s" %keyword)
        browser.find_element_by_id('btnSearch').click()
        browser.switch_to.frame('iframeResult')

        paper_link= browser.find_element_by_link_text(keyword)
        url = paper_link.get_attribute('href')
        url_part = url.split('&')[3:6]
        url_str = '&'.join(url_part)
        down_url = 'http://kns.cnki.net/KCMS/detail/detail.aspx?' + url_str

        return down_url



if __name__=="__main__":


    download_dir = 'Z:\\Downloads'

    to_be_downloaded = []
    success = []
    failed  = []

    with open("downfile.txt",encoding = "utf-8") as file:
        for line in file:
            to_be_downloaded.append(line.strip())

    print( "总共要下载%d篇论文" %len(to_be_downloaded))
    if(len(to_be_downloaded)) < 10:
        print("\n".join(to_be_downloaded))
    print()
    
    options = webdriver.ChromeOptions()
    prefs = { 'profile.default_content_settings.popups' : 0, 'download.default_directory' : download_dir}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    browser.implicitly_wait(10)

    for paper in to_be_downloaded:

        try:
            Link = get_download_url(browser,paper)
            # print(Link)
            do_download(browser,Link)
            success.append(paper)

        except:
            failed.append(paper)
            print("%s下载失败"%paper)
 
    download_status = False   
    while not download_status:
        download_status = True
        for i in os.listdir(download_dir):
            if i.endswith(".crdownload"):
                download_status = False
                sleep(2)

    browser.quit()



    print("成功下载%d篇论文" %len(success))
    print("%d篇论文下载失败" %len(failed))
    if len(failed) < 15:
        print("\n".join(failed))

