# lab.py


import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def extract_book_links(text):
    soup = bs4.BeautifulSoup(text, features='lxml')
    links = []
    for article in soup.find_all('article', class_='product_pod'):
        rating_info = article.find('p', class_='star-rating')['class']
        rating = rating_info[1] if len(rating_info) > 1 else None
        if rating in ['Four', 'Five']:  
            price_info = article.find('p', class_='price_color').get_text()
            price = float(price_info.strip('Â£'))  
            if price < 50.0:  
                link = article.find('h3').find('a')['href']
                links.append(link)  
    return links

def get_product_info(text, categories):
    soup = bs4.BeautifulSoup(text, features='lxml')
    category = soup.find('ul', class_='breadcrumb').find_all('a')
    book_cat = category[-1].get_text()
    if book_cat in categories:
        product = {}
        product['UPC'] = soup.find('th', text='UPC').find_next_sibling('td').get_text()
        product['Product Type'] = soup.find('th', text='Product Type').find_next_sibling('td').get_text()
        product['Price (excl. tax)'] = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').get_text()
        product['Price (incl. tax)'] = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').get_text()
        product['Tax'] = soup.find('th', text='Tax').find_next_sibling('td').get_text()
        product['Availability'] = soup.find('th', text='Availability').find_next_sibling('td').get_text().strip()
        product['Number of reviews'] = int(soup.find('th', text='Number of reviews').find_next_sibling('td').get_text())
        product['Category'] = book_cat
        product['Rating'] = soup.find('p', class_='star-rating')['class'][1]
        product['Description'] = soup.find('meta', attrs={'name': 'description'})['content']
        product['Title'] = soup.find('h1').get_text()
        return product
    else:
        return None

def scrape_books(k, categories):
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    books = []
    for page in range(1, k+1):
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            book_links = extract_book_links(html_content)
            for link in book_links:
                book_url = f'http://books.toscrape.com/catalogue/{link}'
                book_response = requests.get(book_url)
                if book_response.status_code == 200:
                    book_html_content = book_response.content
                    book_info = get_product_info(book_html_content, categories)
                    if book_info:
                        books.append(book_info)
    return pd.DataFrame(books)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def stock_history(ticker, year, month):
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-28" if month == 2 else f"{year}-{month:02d}-30" if month in [4, 6, 9, 11] else f"{year}-{month:02d}-31"
    
    api = '9OLew5GiIPP7NIbeHNm6b7Pwzs6UekUL'
    
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start}&to={end}&apikey={api}'
    
    response = requests.get(url)
    
    data = response.json()
        
    if 'historical' in data:
        historical_data = data['historical']
    
    df = pd.DataFrame(historical_data)
    
    df_final = df.drop(columns = ['adjClose','unadjustedVolume'])
    
    return df_final

def stock_stats(history):
    first = history.iloc[-1]['open']
    last = history.iloc[0]['close']
    percent_change = ((last - first) / first) * 100
    percent_str = f"{percent_change:+.2f}%"
    
    history['average_price'] = (history['high'] + history['low']) / 2
    history['transaction_volume'] = history['average_price'] * history['volume']
    total_volume = history['transaction_volume'].sum() / 1e9
    volume_str = f"{total_volume:.2f}B"
    
    return (percent_str, volume_str)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def fetch_item(item_id):
    url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
    response = requests.get(url)
    return response.json()

def dfs_comments(comment_ids):
    comments = []
    
    def dfs(comment_id):
        comment = fetch_item(comment_id)
        if comment is None or comment.get('dead'):
            return
        comments.append({
            'id': comment['id'],
            'by': comment.get('by', '[deleted]'),
            'text': comment.get('text', '[deleted]'),
            'parent': comment['parent'],
            'time': pd.to_datetime(comment['time'], unit='s')
        })
        if 'kids' in comment:
            for kid_id in comment['kids']:
                dfs(kid_id)
    
    for comment_id in comment_ids:
        dfs(comment_id)
    
    return comments

def get_comments(storyid):
    story = fetch_item(storyid)
    if story is None or 'kids' not in story:
        return pd.DataFrame(columns=['id', 'by', 'text', 'parent', 'time'])
    
    comments = dfs_comments(story['kids'])
    
    df = pd.DataFrame(comments)
    
    return df
