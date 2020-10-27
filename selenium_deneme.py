from selenium import webdriver
import pandas as pd
import time

class firefox_driver():
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get('https://www.sahibinden.com/satilik?pagingOffset=0&pagingSize=50&address_quarter=60688&address_quarter=22891&address_quarter=22892&address_quarter=51436&address_quarter=22893&address_quarter=22883&address_quarter=22884&address_quarter=51437&address_quarter=22885&address_quarter=22886&address_quarter=22887&address_town=434&address_city=34')
        
        self.metre_kare_list = []
        self.oda_sayisi_list = []
        self.tasinmaz_tipi_list = []
        self.ilan_baslik_list = []
        self.fiyat_list = []
        self.tarih_list = []
        self.mahalle_list = []
        self.currentPage_done = False

    def collect_searchPage(self):
        self.currentPage_done = False

        temporary_attribute_List = self.browser.find_elements_by_class_name('searchResultsAttributeValue')
        self.metre_kare_list += [item.text for item in temporary_attribute_List[0::2]]
        self.oda_sayisi_list += [item.text for item in temporary_attribute_List[1::2]]

        temporary_tagattr_list = self.browser.find_elements_by_class_name('searchResultsTagAttributeValue')
        self.tasinmaz_tipi_list += [item.text for item in temporary_tagattr_list]

        temporary_title_list = self.browser.find_elements_by_class_name('classifiedTitle')
        self.ilan_baslik_list += [item.get_attribute('title') for item in temporary_title_list]

        temporary_fiyat_list = self.browser.find_elements_by_xpath('//*[@class="searchResultsPriceValue"]/div')
        self.fiyat_list += [item.text.strip(" TL") for item in temporary_fiyat_list]

        temporary_tarih_list = self.browser.find_elements_by_xpath('//td[@class="searchResultsDateValue"]/span')
        ay_list = [item.text for item in temporary_tarih_list[0::2]]
        yil_list = [item.text for item in temporary_tarih_list[1::2]]
        self.tarih_list += [ay_list[item]+' '+yil_list[item] for item in range(len(ay_list))]
        
        temporary_location_list = self.browser.find_elements_by_class_name('searchResultsLocationValue')
        self.mahalle_list += [item.text for item in temporary_location_list]

        self.currentPage_done = True
        if self.currentPage_done == True:
            self.next_Page()
    
    def next_Page(self):
        try:  # /html/body/div[4]/div[4]/form/div/div[3]/div[3]/div[1]/ul/li[15]/a
            link = self.browser.find_element_by_css_selector('a.prevNextBut[title="Sonraki"]')
            time.sleep(10)
            self.browser.get(link.get_attribute('href'))
            self.collect_searchPage()
        except:
            self.create_dataframe()
    
    def create_dataframe(self):
        self.df = pd.DataFrame({'Taşınmaz Tipi':self.tasinmaz_tipi_list, 'Açıklama':self.ilan_baslik_list, 'MetreKare':self.metre_kare_list,'Oda':self.oda_sayisi_list, 'Fiyat':self.fiyat_list, 'İlan Tarihi':self.tarih_list, 'Mahalle':self.mahalle_list})
        writer = pd.ExcelWriter('sahibinden_aramaSayfasi.xlsx', engine="xlsxwriter")
        self.df.to_excel(writer, sheet_name="Arama Sayfası")
        writer.save()
        
deneme = firefox_driver()
deneme.collect_searchPage()