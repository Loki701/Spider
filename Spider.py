import requests
from bs4 import BeautifulSoup
import sqlite3
from RollingHashSet import RollingHashSet

rolling_hash_set = RollingHashSet(50)

def crawl(url):
  global count
  global rolling_hash_set

  # Make a GET request to the specified URL
  try:
    response = requests.get(url)
    rolling_hash_set.add(url)
  except Exception as e:
    print(f'Error: {e}')
    return

  # Parse the HTML content of the page
  soup = BeautifulSoup(response.text, 'html.parser')

  # Extract the page title and body content
  title = soup.title.string if soup.title else ''
  body = soup.body.text if soup.body else ''

  # Store the page in the database
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute('''
    CREATE TABLE IF NOT EXISTS webpage (
      url TEXT NOT NULL,
      title TEXT,
      body TEXT
    )
  ''')
  c.execute('INSERT INTO webpage (url, title, body) VALUES (?, ?, ?)', (url, title, body))
  conn.commit()
  conn.close()

  # Find all the links on the page
  links = soup.find_all('a')
  
  # Follow the links and crawl to the next web page, to avoid deadlocks a rolling hash set is used
  # to keep track of visited URL
  for link in links:
    next_url = link.get('href')
    if next_url not in rolling_hash_set:
      crawl(next_url)

# Start the crawl at a specific URL
crawl('https://www.nbcnews.com')
