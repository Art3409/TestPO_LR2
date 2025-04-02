import unittest
from selenium import webdriver
from selenium.webdriver.edge.options import Options  # Импортируем опции для Edge
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

# Устанавливаем уровень логирования Selenium на WARNING, чтобы скрыть INFO-сообщения
LOGGER.setLevel(logging.WARNING)

class TestSSTUWebsite(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.use_chromium = True  # Используем движок Chromium для совместимости
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        self.driver = webdriver.Edge(options=options)  # Создаем экземпляр драйвера Edge
        self.addCleanup(self.driver.quit)
#
    def test_page_title(self):
        self.driver.get('https://www.sstu.ru/')
        self.assertIn('Саратовский государственный технический университет имени Гагарина Ю.А.', self.driver.title)
#
    def test_clicked_links(self):
        self.driver.get('https://www.sstu.ru/')
        wait = WebDriverWait(self.driver, 10)
        link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/abiturientu/"]')))
        link.click()
        self.assertIn('/abiturientu/', self.driver.current_url)
#
    def test_visibility(self):
        self.driver.get('https://www.sstu.ru/')
        element = self.driver.find_element(By.CLASS_NAME, 'logo')
        self.assertTrue(element.is_displayed())
#
    def test_social_media_link(self):
        self.driver.get('https://www.sstu.ru/')
        vk_link_button = self.driver.find_element(By.CSS_SELECTOR, 'a.vk')
        vk_link_button.click()
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.assertIn('vk.com/sstusaratov', self.driver.current_url.lower())
#
    def test_search_query(self):
        self.driver.get('https://www.sstu.ru/')
    
        wait = WebDriverWait(self.driver, 10)
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'header-search')))
        search_button.click()
        search_input = wait.until(EC.visibility_of_element_located((By.ID, 'inline-search__input')))
        search_input.send_keys('Институт прикладных информационных технологий и коммуникаций' + Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-page')))
        self.assertIn('search', self.driver.current_url)
#
    def test_menu_elements(self):
        self.driver.get('https://www.sstu.ru/')
        wait = WebDriverWait(self.driver, 10)
        menu_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.menu > li')))
        self.assertGreater(len(menu_elements), 0)
#
    def test_footer_links(self):
        self.driver.get('https://www.sstu.ru/')
        footer_links = self.driver.find_elements(By.CSS_SELECTOR, 'footer')
        for link in footer_links:
            self.assertTrue(link.is_displayed())
#
    def test_institute_page(self):
        self.driver.get('https://www.sstu.ru/obrazovanie/instituty/inpit/')

        title_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'slide-text')) 
        )
        self.assertTrue(title_element.is_displayed())
        self.assertIn('ИНСТИТУТ ПРИКЛАДНЫХ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ И КОММУНИКАЦИЙ', title_element.text)

        contacts_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'social-list'))
        )
        self.assertTrue(contacts_element.is_displayed())
#
    def test_admission_page(self):
        self.driver.get('https://www.sstu.ru/abiturientu/v-o/2025/')

        admission_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertIn('Прием 2025 года', admission_title.text)

        admission_links = self.driver.find_elements(By.CSS_SELECTOR, '.external-link')
        self.assertGreater(len(admission_links), 0)
#
    def test_news_section(self):

        self.driver.get('https://www.sstu.ru/')

        main_news_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.title-add a[href*="/main-news/"]'))
        )
        main_news_link.click()

        self.driver.switch_to.window(self.driver.window_handles[-1])

        news_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.news-item'))
        )
        self.assertGreater(len(news_items), 0, msg='Не найдено новостных элементов.')

        first_news_date = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.news-item__date'))
        )
        self.assertTrue(first_news_date.is_displayed(), msg='Дата первой новости не отображается.')


if __name__ == '__main__':
    unittest.main()