import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Fixing Minor Warnings Incase you experience any
from selenium.webdriver.chrome.options import Options

# Fixing some minor Chrome errors and Windows OS errors
options = Options()
options.add_experimental_option('excludeSwitches', ['disable-logging'])

# Our target URL
url = "https://developers.google.com/products/"

# Initialise the driver
driver = webdriver.Chrome()

def web_wait_time():
    return driver.implicitly_wait(10)

def web_sleep_time(): 
    return time.sleep(10)

# Wait website loading
web_wait_time()

# We can do our get request
driver.get(url)

# We can dump them as lists for later use.
titles =  []
summaries = []

def all_products():
    """This is the main function that inspects and located the DOM that loads dynamically
        to get the title & summary of the product.
        
        You can inspect the DOM with dev tools. 
    """
    
    # From Inspection, this is our main content container
    data = driver.find_elements(By.CLASS_NAME, "devsite-card-content")

    # We loop through to get the subsets or children elements
    # where our data resides
    for data_elements in data:
        
        # Title & Summary Locators
        data_title = data_elements.find_elements(By.TAG_NAME,"h3")
        data_summary = data_elements.find_elements(By.CLASS_NAME,"devsite-card-summary")

        for title in data_title:
            titles.append(title.text)
            # print(title.text)

        for summary in data_summary:
            summaries.append(summary.text)
            # print(summary.text)

# Lets wait again to load -implicitly
web_wait_time()

# Lets Allow the DOM to load first before we start 
# getting the next dynamic pages.
web_sleep_time()

# I had to examine the number of pages
for page in range(1,17):
    driver.find_element(By.LINK_TEXT, str(page)).click()
    all_products()
    web_sleep_time()


# print(titles, summaries)

# Let's sanitize our data first
cleaned_titles = [data for data in titles if data != ""]
cleaned_summaries = [data for data in summaries if data != ""]
        
# print(len(cleaned_titles))
# print(len(cleaned_summaries))

# Let's Create Pandas dataframes to drop them in a CSV 
products_dataframe = pd.DataFrame(list(zip(cleaned_titles, cleaned_summaries)), columns =['Product', 'Summary'])
products_dataframe.to_csv('Google_Products.csv')


# data_2_csv = pd.DataFrame(clean_data_, columns=["column"])
# data_2_csv.to_csv("jumia.csv", mode="a", index=False)
# print(data_2_csv)

# Lets close ops
driver.quit()
