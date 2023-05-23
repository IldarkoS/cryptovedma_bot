from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from app.config import db, app
from app.bot.markups import months
from app.models.EconomistIssueModel import EconomistIssue

from datetime import datetime
from dataclasses import dataclass

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
service = FirefoxService(r"C:\Users\sayil\PycharmProjects\cryptovedmabot\geckodriver.exe")

base_url = "https://www.economist.com/weeklyedition/archive?year="

years = [i for i in range(1997, datetime.now().year + 1)]


@dataclass
class Edition:
    editionsUrl:str
    editionsName:str
    editionsDate:str
    editionsImageUrl:str


def parseAllEconomist(base_url: str=base_url):
    print("parseAllEconomist")
    try:
        driver = Firefox(service=service, options=options)
        edition_models = []
        for i in years:
            url = base_url + str(i)
            def parsePage(url: str = url):
                driver.get(url=url)
                editionsUrls = driver.find_elements(by=By.XPATH, value="//a[@class='headline-link']")
                editionsDates = driver.find_elements(by=By.XPATH, value="//time[@class='edition-teaser__subheadline']")
                editionsNames = driver.find_elements(by=By.XPATH, value="//span[@class='edition-teaser__headline']")
                editionsImagesUrl = driver.find_elements(by=By.XPATH, value="//meta[@itemprop='url']")

                editionsUrl = list(map(lambda x: x.get_attribute("href"), editionsUrls))
                editionsName = list(map(lambda x: x.text, editionsUrls))
                editionsDate = list(map(lambda x: x.text, editionsDates))
                editionsImageUrl = list(map(lambda x: x.get_attribute("content"), editionsImagesUrl))

                for i in range(len(editionsUrl)):

                    E = Edition(
                        editionsUrl = editionsUrl[i],
                        editionsDate = editionsDate[i],
                        editionsName = editionsName[i],
                        editionsImageUrl = editionsImageUrl[i]
                    )
                    edition_models.append(E)


            parsePage(url=url)

    except Exception as e:
        print(e)
    finally:
        driver.close()
        for i in edition_models:
            EconomistIssue(
                name=i.editionsName,
                year=i.editionsDate.split()[-1],
                url=i.editionsUrl,
                image_url=i.editionsImageUrl,
                month=months[i.editionsDate.split()[0]]
            )
        print("parseAllEconomistComplete")

new_url = "https://www.economist.com/weeklyedition/archive"

def parseNewEconomist(new_url: str=new_url):
    print("parseNewEconomist")
    try:
        driver = Firefox(service=service, options=options)
        edition_models = []
        def parsePage(url: str = new_url):
            driver.get(url=url)
            editionsUrls = driver.find_elements(by=By.XPATH, value="//a[@class='headline-link']")
            editionsDates = driver.find_elements(by=By.XPATH, value="//time[@class='edition-teaser__subheadline']")
            editionsNames = driver.find_elements(by=By.XPATH, value="//span[@class='edition-teaser__headline']")
            editionsImagesUrl = driver.find_elements(by=By.XPATH, value="//meta[@itemprop='url']")

            editionsUrl = list(map(lambda x: x.get_attribute("href"), editionsUrls))
            editionsName = list(map(lambda x: x.text, editionsUrls))
            editionsDate = list(map(lambda x: x.text, editionsDates))
            editionsImageUrl = list(map(lambda x: x.get_attribute("content"), editionsImagesUrl))
            for i in range(len(editionsUrl)):
                E = Edition(
                    editionsUrl = editionsUrl[i],
                    editionsDate = editionsDate[i],
                    editionsName = editionsName[i],
                    editionsImageUrl = editionsImageUrl[i]
                )
                edition_models.append(E)


        parsePage(url=new_url)

    except Exception as e:
        print(e)
    finally:
        driver.close()
        with app.app_context():
            editions = edition_models
            for edition in editions:
                if EconomistIssue.query.filter_by(url=edition.editionsUrl).first():
                    pass
                else:
                    print("Добавлен", edition.editionsName)
                    EconomistIssue(
                        name=edition.editionsName,
                        year=edition.editionsDate.split()[-1],
                        url=edition.editionsUrl,
                        image_url=edition.editionsImageUrl,
                        month=months[edition.editionsDate.split()[0]]
                    )