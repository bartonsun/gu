from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# ==========================================================
url_main = 'https://www.gosuslugi.ru/'
title = 'Портал государственных услуг Российской Федерации'
input_search_text = 'загран'
dropdown_element_text = 'загранпаспорт нового поколения 18 лет'
text_10 = 'Получение заграничного паспорта со сроком действия 10 лет'
title_10 = 'Оформление заграничного паспорта старого и нового образца'
title_catalog = 'Категории услуг'
url_drivers_license = 'https://www.gosuslugi.ru/situation/obtaining_drivers_license_first_time'
title_first_time = 'Как получить водительское удостоверение впервые?'
button_find_ds_text = 'Найти автошколу'
url_gbdd = 'https://xn--90adear.xn--p1ai/r/77/drivingschools/'
menu_servise_text = 'Сервисы'
menu_docs_text = 'Нормативные документы'
file_link_name = 'Приказ МВД России от 23.08.2017'
# ==========================================================
search_input_id = '_epgu_el1'
dropdown_element_xpath = '//div[@class="searchBox searchBox--main"]' \
                         '/descendant::span[contains(text(), "{}")]'.format(dropdown_element_text)
link_10_xpath = '//a[contains(text(), "{}")]'.format(text_10)
back_button_xpath = '//a[@data-ng-click="$root.backToCatalog()"]'
button_find_ds_xpath = '//a[contains(text(), "{}")]'.format(button_find_ds_text)
menu_servise_xpath = '//ul[@id="menu-1"]/descendant::a[contains(text(), "{}")]'.format(menu_servise_text)
menu_docs_xpath = '//div[@id="menu-1-sub"]/descendant::a[contains(text(), "{}")]'.format(menu_docs_text)
file_link_xpath = '//a[@class="file_a"][contains(text(), "{}")]'.format(file_link_name)
# ==========================================================


def test_gosuslugi(driver):
    # 1. Зайти на сайт https://www.gosuslugi.ru/
    driver.get(url_main)
    assert title in driver.title
    # 2. В строке поиска ввести «загран»
    search_input = driver.find_element_by_id(search_input_id)
    search_input.click()
    for ch in input_search_text:
        search_input.send_keys(ch)
    # 3. В выпадающем списке выбрать «загранпаспорт нового поколения 18 лет»
    dropdown_element = driver.find_element_by_xpath(dropdown_element_xpath)
    dropdown_element.click()
    # 4. Удостовериться, что появились Результаты поиска:
    # «Оформление и выдача заграничного паспорта нового поколения (сроком действия десять
    # лет)», нажать на ссылку
    # * на странице не нашел текст из ТЗ
    # использовал для поиска текст "Получение заграничного паспорта со сроком действия 10 лет"
    link_10 = driver.find_element_by_xpath(link_10_xpath)
    link_10.click()
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(title_10))
    finally:
        assert title_10 in driver.title
    # 5. Нажать на кнопку «Вернуться»
    # * тут опять же отошел от ТЗ, сделав нажатие на 2 кнопки
    # т.к. вернуться ведет на страницу "Паспорта, регистрации, визы", а не в каталог госуслуг
    back_button = driver.find_element_by_xpath(back_button_xpath)
    back_button.click()
    back_button = driver.find_element_by_xpath(back_button_xpath)
    back_button.click()
    # 6. Проверить, что отображен «Каталог услуг»
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(title_catalog))
    finally:
        assert title_catalog in driver.title
    # 7. Перейти по ссылке https://www.gosuslugi.ru/situation/obtaining_drivers_license_first_time
    driver.get(url_drivers_license)
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(title_first_time))
    finally:
        assert title_first_time in driver.title
    # 8. Нажать на кнопку Найти автошколу
    button_find_ds = driver.find_element_by_xpath(button_find_ds_xpath)
    button_find_ds.click()
    # 9. Перейти на отдельно открытую страницу сайта гибдд
    driver.switch_to.window(driver.window_handles[-1])
    try:
        WebDriverWait(driver, 10).until(EC.url_to_be(url_gbdd))
    finally:
        assert driver.current_url == url_gbdd
    # 10. Перейти на вкладку Сервисы – Нормативные документы
    # костыль в виде time.sleep, чтобы дождаться подгрузки скрипта
    # пока ничего лучше не придумал
    time.sleep(2)
    menu_servise = driver.find_element_by_xpath(menu_servise_xpath)
    menu_servise.click()
    menu_docs = driver.find_element_by_xpath(menu_docs_xpath)
    menu_docs.click()
    # 11. Скачать Приказ МВД России от 23.08.2017
    file_link = driver.find_element_by_xpath(file_link_xpath)
    file_name = file_link.get_attribute('href').split('/')[-1]
    file_link.click()
    # 12. Проверить, что файл скачен на диск
    try:
        counter = 0
        while counter <= 10:
            if os.path.isfile('tmp/' + file_name):
                break
            time.sleep(1)
            counter += 1
    finally:
        assert os.path.isfile('tmp/' + file_name), 'Нет файла: {}'.format(file_name)
    # 13. Удалить скаченный файл
    os.remove('tmp/' + file_name)
    assert os.path.isfile('tmp/' + file_name) is False, 'Файл не удален: {}'.format(file_name)
