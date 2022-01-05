import json
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pymongo

URL = "https://www.forbes.com/billionaires/"
driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe')
driver.get(URL)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
except TimeoutException:
    print("Loading took just too much, sorry")
finally:
    print("Page loaded succesfully !")

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")
name_list = []
names_selector = soup.find_all("div", class_="personName")
for name in names_selector:
    name_list.append(name.get_text())

# print(name_list)
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.forbes200
col = db.people
# print(client.list_database_names())

for name in name_list:
    sep = '&'
    stripped = name.split(sep, 1)[0]
    stripped = stripped.lower()
    stripped = stripped.rstrip()
    stripped = stripped.replace(" ", "-")
    stripped = stripped.replace(",", "")
    stripped = stripped.replace(".", "")
    #   print(stripped)
    if stripped == "jensen-huang" or stripped == "zhang-yong" or stripped == "gerard-wertheimer":
        stripped = stripped + "-1"
    if stripped == "hank":
        stripped = "hank-doug-meijer"
    if stripped == "robert":
        stripped = "robert-philip-ng"
    if stripped == "beate-heister":
        stripped = "beate-heister-karl-albrecht-jr"
    if stripped == "françois-pinault":
        stripped = "francois-pinault"
    url = "https://www.forbes.com/profile/%s" % stripped
    # print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info_list = []
    title_list = []
    info_selector2 = soup.find_all("span", class_="profile-stats__title")
    info_selector = soup.find_all("span", class_="profile-stats__text")
    for info in info_selector:
        info_list.append(info.get_text())
    for title in info_selector2:
        title_list.append(title.get_text())
    i = 0
    if "Age" not in title_list:
        age = ""
    else:
        age = info_list[i]
        print(age)
        i = i + 1
    if "Source of Wealth" not in title_list:
        Source_of_Wealth = ""
    else:
        Source_of_Wealth = info_list[i]
        i = i + 1
    if "Self-Made Score" not in title_list:
        SelfMadeScore = ""
    else:
        SelfMadeScore = info_list[i]
        i = i + 1
    if "Philanthropy Score" not in title_list:
        PhilanthropyScore = ""
    else:
        PhilanthropyScore = info_list[i]
        i = i + 1
    if "Residence" not in title_list:
        Residence = ""
    else:
        Residence = info_list[i]
        i = i + 1
    if "Citizenship" not in title_list:
        Citizenship = ""
    else:
        Citizenship = info_list[i]
        i = i + 1
    if "Marital Status" not in title_list:
        Marital_Status = ""
    else:
        Marital_Status = info_list[i]
        i = i + 1
    if "Children" not in title_list:
        children = ""
    else:
        children = info_list[i]
        i = i + 1
    if "Education" not in title_list:
        education = ""
    else:
        education = info_list[i]
        i = i + 1
    print(age, Source_of_Wealth, SelfMadeScore, PhilanthropyScore, Residence, Citizenship, Marital_Status, children, education)
    dict = {"Name": name.split("', '"), "Age": age, "Source of Wealth" : Source_of_Wealth, "Self-Made Score" : SelfMadeScore,
            "Philanthropy Score": PhilanthropyScore, "Residence" : Residence, "Citizenship" : Citizenship,
            "Marital Status" : Marital_Status, "Children": children, "Education" : education}
    x = col.insert_one(dict)
    #col.drop()
    print(info_list)
    print(title_list)
    



# col.drop()

def youngest():
    print("Top cele mai tinere persoane din Forbes:")
    for j in col.find({"Age": {"$ne": ""}},
                      {"Name": 1, "Age": 2, "_id": False}).sort(
        [("Age", 1), ("_id", pymongo.ASCENDING)]).limit(10):
        print(j)
    print("\n")


def cetatenie():
    results = col.find({"Citizenship": "United States"},
                       {"Name": 1, "Age": 2, "citizenship": 3})
    count = 0
    for result in results:
        count = count + 1

    print("Numarul de persoane cu cetatenie americana:", count)
    print("Numarul de persoane fara cetatenie americana", (200 - count))
    print("\n")


def philantropy():
    print("Top 10 persoane cu cel mai mare scor filantropic: \n")
    for k in col.find({"Philanthropy Score": {'$ne': ""}},
                      {"Name": 1, "Philanthropy Score": 2, "_id": False}).sort([("Philanthropy Score", -1),
                                                                                ("_id", pymongo.DESCENDING)]).limit(10):
        print(k)
    print("\n")


youngest()
cetatenie()
philantropy()
