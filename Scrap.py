from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import os.path
from termcolor import colored

place_id = input("Enter Place ID: ")

initial_url = 'https://search.google.com/local/reviews?placeid=' + place_id
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(initial_url)
final_url = driver.current_url
print("Redirected URL : " + final_url)
driver.get(final_url)
html = driver.page_source

page_soup = soup(html, "html.parser")
title = page_soup.find("div", {"class": "P5Bobd"}).text
address = page_soup.find("div", {"class": "T6pBCe"}).text
print(colored("Place : ", "red") + title + ", " + address)
containers = page_soup.findAll("div", {"class": "jxjCjc"})
name = title + ".csv"
if os.path.isfile(name):
    os.remove(name)
f = open(name, "w", encoding='utf-8', errors='ignore')
writer = csv.writer(f)
writer.writerow(["Name", "Review Date", "Rating", "Comments"])
# print(containers[0])
print(len(containers))
for i, containers in enumerate(containers):
    print("Review : " + str(i + 1))
    if containers.div.a is not None:
        print(containers.div.a.text)
        Name = containers.div.a.text
    else:
        Name = ""
    if containers.find("span", {"class": "dehysf"}) is not None:
        print(containers.find("span", {"class": "dehysf"}).text)
        Review_Date = containers.find("span", {"class": "dehysf"}).text
    else:
        Review_Date = ""
    if containers.find("span", {"class": "r-iXumj_0JahN4"}) is not None:
        print(containers.find("span", {"class": "r-iXumj_0JahN4"}).text)
    if containers.find("span", {"class": "Fam1ne"}) is not None:
        print(containers.find("span", {"class": "Fam1ne"})['aria-label'])
        Rating = containers.find("span", {"class": "Fam1ne"})['aria-label']
    else:
        Rating = ""
    if containers.find("span", {"class": "review-full-text"}) is not None:
        print(containers.find("span", {"class": "review-full-text"}).text)
        Comments = containers.find("span", {"class": "review-full-text"}).text
    elif containers.find("div", {"class": "Jtu6Td"}).text is not None:
        print(containers.find("div", {"class": "Jtu6Td"}).text)
        Comments = containers.find("div", {"class": "Jtu6Td"}).text
    else:
        Comments = ""
    writer.writerow([Name, Review_Date, Rating, Comments])
    print(" ")
