from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.get("https://www.imdb.com/chart/top/")
time.sleep(5)
movies = driver.find_elements(
    By.XPATH,
    "//li[contains(@class,'ipc-metadata-list-summary-item')]")
ranks = []
titles = []
years = []
ratings = []
links = []
rank = 1
for movie in movies:
    try:
        title = movie.find_element(By.XPATH, ".//h3").text
        year = movie.find_element(
            By.XPATH,
            ".//span[contains(@class,'cli-title-metadata-item')]"
        ).text
        rating = movie.find_element(
            By.XPATH,
            ".//span[contains(@class,'ratingGroup')]//span"
        ).text
        link = movie.find_element(By.XPATH, ".//a").get_attribute("href")
        ranks.append(rank)
        titles.append(title)
        years.append(year)
        ratings.append(rating)
        links.append(link)
        rank += 1
    except:
        continue
df = pd.DataFrame({
    "Rank": ranks,
    "Movie Title": titles,
    "Release Year": years,
    "IMDb Rating": ratings,
    "Movie Link": links
})
print("\nIMDb TOP MOVIES LIST\n")
print(df.to_string(index=False))
df.to_csv("imdb_top_250_movies.csv", index=False, encoding="utf-8")
print("\nCSV file created successfully")
driver.quit()
