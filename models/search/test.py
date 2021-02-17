# To add a new cell, type '# %%'
# %%

# To add a new markdown cell, type '# %% [markdown]'
# %%
import json
from pymongo import MongoClient
import pymongo
import uuid
import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen
from IPython import get_ipython

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# %%
# Specify the url parameters

base_url = "http://libgen.rs"
base_url1 = "http://libgen.is"

params = {
    "res": 100,
    "req": "docker",
    "view": "detailed",
    "column": "def",
    "sort": 'def',
    "sortmode": "ASC",
    "page": 1
}

url = f"{base_url}/search.php?&res={params['res']}&req={params['req']}&phrase=1&view={params['view']}&column={params['column']}&sort={params['sort']}&sortmode={params['sortmode']}&page={params['page']}"

#url1 = "http://libgen.rs/search.php?&res=100&req=docker&phrase=1&view=detailed&column=def&sort=def&sortmode=ASC&page=1"


# %%
response = {
    "errors": {
        "error_code": "",
        "error_desc": ""
    },
    "records": ""

}


# %%
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')


# %%


# %%
text = soup.get_text()
# print(text)


# %%
tables = soup.find_all("table", rules="cols")


# %%
# test the parser by getting web page title
try:
    title = soup.title
    title.get_text()
except Error:
    response['errors']['error_code'] = 503
    response['errors']['error_desc'] = "Service temporarily unavailable"
    exit()

if len(tables) == 0:
    response['errors']['error_code'] = 403
    response['errors']['error_desc'] = "No books found, search for another book"
    exit()

else:
    books = []
    tables = soup.find_all("table", rules="cols")
    for table in tables:
        try:
            books.append(get_book_data(table))
        except IndexError:
            pass

    response["records"] = books


# %%
def get_book_data(table):
    book = {
        "ID": "",
        "Title": "",
        "Authors": "",
        "Language": "",
        "Publisher": "",
        "Year": "",
        "ISBN": "",
        "Edition": "",
        "No_of_Pages": "",
        "Size": "",
        "Extension": "",
        "Image_Url": "",
        "Quick_Download_Url": ""}

    # Get Book ID
    book["ID"] = str(uuid.uuid4())

    # Get Book Title
    data = str(table.find_all('td')[3])
    book['Title'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Author
    data = str(table.find_all('td')[6])
    book['Authors'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Publisher
    data = str(table.find_all('td')[12])
    book['Publisher'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Year
    data = str(table.find_all('td')[16])
    book['Year'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Edition
    data = str(table.find_all('td')[18])
    book['Edition'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Language
    data = str(table.find_all('td')[20])
    book['Language'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Pages
    data = str(table.find_all('td')[22])
    book['No_of_Pages'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book ISBN
    data = str(table.find_all('td')[24])
    book['ISBN'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Size
    data = str(table.find_all('td')[32])
    book['Size'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book Extension
    data = str(table.find_all('td')[34])
    book['Extension'] = BeautifulSoup(data, "lxml").get_text()

    # Get Book url
    data = table.find_all('img')[0]
    book['Image_Url'] = f"{base_url}{data.attrs['src']}"

    # Get Book QUick download url
    data = table.find_all('a')[0]
    book["Quick_Download_Url"] = f"{base_url}{data.attrs['href']}"

    return book


# %%


# %%
books[99]


# %%
table_data = []
for data in tables:
    table_data.append(data)
    print(data.find_all('tr'))


# %%
tables[2]


# %%
table_data = []


for data in tables:
    str_cells = str(data.find_all('td'))
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    print(cleantext)


# %%
df = pd.DataFrame(list_data)
df

# %% [markdown]
# Now that our data is in tables, just like you would have in an excel sheet, we need to clean it up, including also extracting the table headers and putting it in the right place.
#
# Since we need to separate the data at the comma (,) to get the details of each column into seperate columns, we can use the split function in pandas to split the data.
# %% [markdown]
# We can now bring in the headers for the table by using our soup to find all the table headers.

# %%
headers = soup.find_all('th')


# %%
all_header = []
col_str = str(headers)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)

# %% [markdown]
# Then we convert the headers into a dataframe, split it using "," also then make it the header for our data table

# %%
df2 = pd.DataFrame(all_header)
df2.head()


# %%
df3 = df2[0].str.split(',', expand=True)
df3.head()

# %% [markdown]
# Then we also split the main data table at the comma point

# %%
df1 = df[0].str.split(',', expand=True)
df1

# %% [markdown]
# We then append both tables, by using concat or we could also use append i.e.df3.append(df1)

# %%
frames = [df3, df1]
df4 = pd.concat(frames)
df4.head(10)

# %% [markdown]
# We can then proceed to clean up the contents of the header and body using str.replace which is similar to find and replace in excel

# %%
df4.iloc[0] = df4.iloc[0].str.replace("\n", "")


# %%
df4[0] = df4[0].str.replace("[", "")


# %%
df4[3] = df4[3].str.replace("]", "")


# %%
df4.head()

# %% [markdown]
# Now that the data is a little cleaner, we can set the first row as the header of our table

# %%
df5 = df4.rename(columns=df4.iloc[0])
df5.head()

# %% [markdown]
# Then we can drop the rows in index 0 and 1 as we dont need them anymore

# %%
df7 = df5.drop(df5.index[0:1])
df7.head()

# %% [markdown]
# At this stage, we have succssfully parsed the data from the website, and imported the contents to a dataframe table. we can easily export this to a csv or excel file by using the pd.to_csv(r"filepath/doc name.csv").
# %% [markdown]
# ### What Next?
#
# What i intend to achieve however goes beyond just parsing the data into a csv file. I noticed that Abokifx does not provide historical information on black market exchange rates to the public, and the information available on the website is only for a couple of weeks, which is really not helpful if you inted to do some predictive or forecasting analysis on BDC rates. So I decided to create a cloud atlas storage in MongoDB to hold the data. This will ensure that everytime I run this notbook (a two-weeks scheduled refresh on ML studio) I get the latest information from the website and retain the historical data for as long as I want. I usually favor working with NO SQL databses because I love working with JSON and I particularly like MongoDB. You can create a free atlas databse here https://www.mongodb.com/cloud/atlas
# %% [markdown]
# To work with MongoDB, i use a package called pymongo and, while this process stores the data on an atlas cluster, I have provided code on how you can store it on your local drive, provided you have MongoDB installed

# %%

# connect to localhost
#client = MongoClient('mongodb://localhost:27017/')
# db=client['aboki_fx']
#collection = db['bdc_rates']

# connect to atlas cluster
client = pymongo.MongoClient(
    "mongodb+srv://abokifx_user:abokifx_user@stephencluster-ifq4j.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client['aboki_fx']
collection = db['bdc_rates']

# %% [markdown]
# To work with No SQL databses, we have to convert the dataframe to json using the json package

# %%
data_json = json.loads(df7.to_json(orient='records'))
# db['aboki_fx'].remove() --don' remove previous data
db['bdc_rates'].insert(data_json)

# %% [markdown]
# ### Retreiving the data from the atlas storage
# %% [markdown]
# In case you need to retrieve this data you can easily connect to the databas and then call the data by using the code below

# %%
documents = []
for doc in collection.find():
    if doc not in documents:
        documents.append(doc)

abokifx = pd.DataFrame(documents)


# %%
documents


# %%
# dropping duplicates incase we have saved data on a particular day twice
abokifx.drop_duplicates(
    subset=[abokifx.columns[1]], keep='first', inplace=True)


# %%
abokifx


# %%


# %%
