from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
from credentials import login

def login_and_get_table_as_source():
    speed = 1 
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get('https://eportal.pmf.uns.ac.rs/')
    sleep(speed)
    username_input = driver.find_element_by_css_selector('input[data-ng-model="model.loginView.k_ime"]')
    password_input = log = driver.find_element_by_css_selector('input[data-ng-model="model.loginView.k_sifra"]')
    username_input.send_keys(login['username'])
    password_input.send_keys(login['password'])
    password_input.send_keys(Keys.RETURN)
    sleep(speed)
    driver.get('https://eportal.pmf.uns.ac.rs/#/app/polozeniispiti')
    sleep(speed)
    page_source = driver.page_source
    return page_source

def parse_table(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

def format_data(data):
    grades = []
    for entry in data:
        grade = {}
        grade['name'] = entry[0]
        grade['prof'] = entry[1]
        grade['time'] = entry[2]
        grade['grade'] = entry[4].replace('Položen\n','')
        grade['espb'] = entry[6]
        grades.append(grade)
    return grades

def calculate_sum(grades):
    return sum([int(grade['grade']) for grade in grades])/len(grades)

def calculate_espb(grades):
    return sum([int(grade['espb']) for grade in grades])

def full_report(grades):
    print("Polozeno",len(grades), "predmeta, sa prosekom", '{0:.3g}'.format(calculate_sum(grades)))
    print("Ostvareno", str(calculate_espb(grades)),"ESPB bodova")


if __name__ == "__main__":
    full_report(format_data(parse_table(login_and_get_table_as_source())))
#
