import requests #hits the address of the website we are scrapping
from bs4 import BeautifulSoup , Tag #handles website tags while collecting content from the website.
import pandas as pd #organizes scrapped data intocsv format
import time
import random
import streamlit as st

Base_URL = "http://quotes.toscrape.com" #the website we are hitting to get the data. (It is legal to do so for this website)

# HEADERS is a trick to not to let the website understand that a python code is visiting the page. Sometimes when the websites detect robots visiting their page they will block access.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


#this function takes page number as input, uses requests library to fetch the page and stores that in a variable called response. Then the function returns the variable response.text
def fetch_page(page_number):
  url = f'{Base_URL}/page/{page_number}/'
  try :
    print(f'Fetching {url}....')
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
      return response.text
    else:
      print(f'Failed to Retrieve page{page_number}')
      return None
  except Exception as e:
    print(f'An error occured while fetching page{page_number}:{e}')
    return None


#this function takes the html syntax of the page as input, find the quotes using BeautifulSoup library, cleans the quote and returns a list of dictionaries with quotes,author and tags keys.
def extract_quotes_from_page(html_content):
  soup = BeautifulSoup(html_content,'html.parser')#the MAGIC happens here. our html content is just a messy giant string that python doesn't understand.We use BeautifulSoup+'html.parser' that knows how to convert this mess into a stuctured treelike object that python can easily navigate. 
  quote_elements = soup.find_all('div', class_='quote')
  #soup is the variable that holds the structured treelike object that we can easily navigate through by using soup.find_all() method.
  extracted_data = []

  for element in quote_elements:
    #Look inside the current container (element), hunt down the span tag labeled as 'text', grab the words inside it, and trim off any messy whitespace from the start and end."

    if isinstance(element, Tag):#In plain English, this line of code is asking a simple True/False question:"Is this item a 'Tag' (an HTML container)?"
      text = element.find('span', class_='text').get_text(strip=True).replace('“','').replace('”','').replace('"', '')  #Here we are cleaning the quote text by removing leading and trailing double quotes and extra spaces.
      author = element.find('small',class_='author').get_text(strip=True)
      tags = [] 
        
      tags_container = element.find('div', class_='tags')
        
      # If we find tags, we overwrite the empty list with the actual tags.
      if tags_container:
          tags = [tag.get_text(strip=True) for tag in tags_container.find_all('a', class_='tag')]
      #here we are appending each dictionary with 3 key,value pair into the extracted_data list.    
      extracted_data.append({
          'quote': text,
          'author' : author,
          'tags' : ", ".join(tags)
          # ", ".join() --> takes every item in the list of tags and "glues" them together into a single string.example:
          #Before: ['inspirational', 'life', 'wisdom'] (A List)
          #After: "inspirational, life, wisdom" (A single String)
      })
  return extracted_data



  #Building the user Interface



# --- 1. SETUP STREAMLIT ---
st.title("🕷️ Web Scraper Dashboard")
st.markdown("Welcome, **User**! Enter the number of pages you want to scrape from *quotes.toscrape.com*.")

# THE INPUT: A slider or number box
max_pages = st.number_input("Number of Pages to Scrape:", min_value=1, max_value=10, value=3)


if st.button("Start Scraping Engine"):
    
# Create a placeholder for status updates (so it looks dynamic)
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    all_quotes = []
    
# THE LOOP
    for page in range(1,max_pages+1):
      html_text = fetch_page(page)#call to function_1
    #we will now extract our quotes from each pages
      if html_text:
        page_data =extract_quotes_from_page(html_text)#call to function_2
        all_quotes.extend(page_data) 
# list.append vs extend: all_quotes.extend(page_data): This takes every item out of the page_data list and unpacks them into individual item before putting the items into the all_quotes list.
            
# Update Progress Bar (Math: current / total)
        progress_bar.progress(page / max_pages)
            
# Polite delay
        time.sleep(random.uniform(0.5, 1.5))
      else:
          st.error(f"Failed to fetch page {page}")
          break
            
# --- 4. SHOW RESULTS ---
    status_text.success("Scraping Completed Successfully!")
    
# Create DataFrame
    df = pd.DataFrame(all_quotes)
    #df["quote"] = df["quote"].str.replace('""', '"', regex=False)
    df["quote"] = df["quote"].str.strip('"')  #Remove leading and trailing double quotes')

    
# Display Data on screen
    st.subheader("Preview Data")
    st.dataframe(df) # Interactive table
    
# Display Stats
    st.write(f"Total Quotes Collected: **{len(df)}**")
    
# --- 5. DOWNLOAD BUTTON ---
    csv_data = df.to_csv(index=False, encoding='utf-8-sig')

    st.download_button(
        label="Download CSV for Excel",
        data=csv_data,
        file_name="output.csv",
        mime="text/csv"
    )


