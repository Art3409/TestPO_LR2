import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestMSUWebsite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
    
    def test_page_title(self):
        self.driver.get('https://www.msu.ru/')
        self.assertIn('Московский государственный университет имени М.В.Ломоносова', self.driver.title) 

    def test_clicked_links(self):
        self.driver.get('https://www.msu.ru/')
        link = self.driver.find_element(By.LINK_TEXT, "Новости") 
        link.click()
        self.assertIn("https://www.msu.ru/news/", self.driver.current_url)  
    
    def test_visibility(self):
        self.driver.get('https://www.msu.ru/')
        element = self.driver.find_element(By.CLASS_NAME, "logo")
        self.assertTrue(element.is_displayed())
    
    def test_social_media_link(self):
        self.driver.get('https://www.msu.ru/')
        vk_link_button = self.driver.find_element(By.CSS_SELECTOR, ".social-links a[href*='vk.com']") 
        vk_link_button.click()
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.assertIn("vk.com/msu", self.driver.current_url.lower())
    
    def test_search_query(self):
        self.driver.get("https://www.msu.ru/")
        search_button = self.driver.find_element(By.CSS_SELECTOR, ".search-btn")
        search_button.click()
        search_input = self.driver.find_element(By.CSS_SELECTOR, ".search-input")
        search_input.send_keys("Факультет вычислительной математики и кибернетики") 
        search_input.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
        self.assertIn("search", self.driver.current_url)

    def test_menu_elements(self):
        self.driver.get("https://www.msu.ru/")
        menu_elements = self.driver.find_elements(By.CSS_SELECTOR,".main-menu li")
        self.assertGreater(len(menu_elements), 0)

    def test_footer_links(self):
        self.driver.get("https://www.msu.ru/")
        footer_links = self.driver.find_elements(By.CSS_SELECTOR, "footer a")
        for link in footer_links:
            self.assertTrue(link.is_displayed())

    def test_faculty_page(self):
        self.driver.get("https://www.msu.ru/info/struct/depts/mehmat.html")
        
        title_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        self.assertTrue(title_element.is_displayed())
        self.assertIn("Механико-математический факультет", title_element.text)

        contacts_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contacts"))
        )
        self.assertTrue(contacts_element.is_displayed())

    def test_admission_page(self):
        self.driver.get("https://www.msu.ru/entrance/")
        
        admission_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        self.assertIn("Поступление", admission_title.text)
        
        admission_links = self.driver.find_elements(By.CSS_SELECTOR, ".admission-links a")
        self.assertGreater(len(admission_links), 0)

    def test_news_section(self):
        self.driver.get("https://www.msu.ru/news/")
        
        news_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news-item"))
        )
        self.assertGreater(len(news_items), 0)
        
        first_news_date = self.driver.find_element(By.CSS_SELECTOR, ".news-item .news-date")
        self.assertTrue(first_news_date.is_displayed())

if __name__ == '__main__':
    unittest.main()