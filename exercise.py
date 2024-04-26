import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import unittest
import requests
from bs4 import BeautifulSoup

def convert_time(time):
    time = time[:10]
    ans = time[:4] + '/' + time[5:7] + '/' + time[8:]
    return ans

# load and format DATE
death = pd.read_csv('MD_COVID-19_-_Confirmed_Deaths_by_County.csv')
death = death.dropna(subset=['OBJECTID', 'DATE'])
death['DATE'] = death['DATE'].apply(lambda x: convert_time(x))

# get all county
county = death.keys().tolist()
county.remove('OBJECTID')
county.remove('DATE')

# load and format case data
case = pd.read_csv('MDCOVID19_CasesByCounty.csv')
case = case.dropna(subset=['DATE'])
case['DATE'] = case['DATE'].apply(lambda x: x[:10])

case_and_death = pd.merge(case, death, how='outer', on='DATE')

print("Case DataFrame:")
print(case)
print("\nDeath DataFrame:")
print(death)

# case&death graph
def plot_case_death_with_time(df, county):
    x = df['DATE'].tolist()

    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the figsize to set the graph size

    i = 0
    for c in county:
        if c in df.columns:
            hsv = ((1 / 25) * i, .8, .8)
            color = colors.hsv_to_rgb(hsv)
            ax.plot(x, df[c].tolist(), label=c, c=color)
            i += 1

    plt.xticks(rotation=90)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Adjust the number of x-axis ticks
    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 1), ncol=3, fancybox=True, shadow=True)
    plt.xlabel('DATE')
    plt.ylabel('Number')
    plt.tight_layout()
    plt.show()

class TestDataProcessing(unittest.TestCase):
    def test_convert_time(self):
        self.assertEqual(convert_time('2022-01-01'), '2022/01/01')
        self.assertEqual(convert_time('2023-12-31'), '2023/12/31')

    def test_data_loaded(self):
        self.assertFalse(death.empty)
        self.assertFalse(case.empty)

    def test_counties_exist(self):
        self.assertIn('Allegany', county)
        self.assertIn('Baltimore', county)
        self.assertIn('Montgomery', county)

    def test_merged_dataframe(self):
        self.assertFalse(case_and_death.empty)
        self.assertTrue('DATE' in case_and_death.columns)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    plot_case_death_with_time(case, county)
    plot_case_death_with_time(death, county)
    
def get_news_articles(keyword="covid", num_articles=10):
    api_key = "19edd102609947f0b67c7ce06479783b"
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    news_data = []
    for article in articles:
        title = article.get("title", "")
        link = article.get("url", "")
        source = article.get("source", {}).get("name", "")
        news_data.append({"title": title, "link": link, "source": source})
    return news_data

# Call the function to fetch news articles
scraped_data = get_news_articles("covid", num_articles=10)

# Print the scraped news data
for data in scraped_data:
    print("Title:", data["title"])
    print("Link:", data["link"])
    print("Source:", data["source"])
    print()