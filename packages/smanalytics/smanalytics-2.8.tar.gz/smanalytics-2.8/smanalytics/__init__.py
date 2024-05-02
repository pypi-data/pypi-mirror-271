from .main import analytics


"""
SM Analytics  for Social Media
=====

Provides
  1. An array object of arbitrary homogeneous items
  2. Fast mathematical operations over arrays
  3. Linear Algebra, Fourier Transforms, Random Number Generation

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`the NumPy homepage <https://numpy.org>`_.

-----------------------------------

## 2. New
```
## 1. New 
# Importing pandas library

import pandas as pd

# Loading the CSV file into a DataFrame

df=pd.read_csv('/content/export-youtube-comments (1).csv')

# Displaying the first 10 rows of the DataFrame

df.head(10)

# Getting information about the DataFrame

df.info()

# Displaying the column names of the DataFrame

df.columns

# Dropping specified columns from the DataFrame

cols_to_drop = ['Date', 'Like Count', 'Channel ID of user',
       'Link to Channel', 'Link to Profile Picture', 'Video ID', 'Comment ID',
       'Comment parent ID', 'Link to comment']
df = df.drop(columns=cols_to_drop)


# Extracting the first comment from the DataFrame

df.head(10)

# Printing the extracted comment

text=(df['Comment'].iloc[0])

print(text)

# Removing exclamation marks from the extracted comment

text = text.replace('!', " ")

# Printing the comment after removing exclamation marks

print(text)

# Removing '@' symbol from the 'Name' column

df['Name'] = df['Name'].str.replace('@', '')

# Displaying the first few rows of the DataFrame after removing '@' symbol from the 'Name' column

df.head()

df.to_csv("newOutputCSV.csv")
print("New data was exported!")
```
-----------------------------------

## 3. Expo data analysis

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#to ignore warnings
import warnings
from IPython.display import display
warnings.filterwarnings('ignore')
data = pd.read_csv('/content/used_cars_data.csv')
#display(data.shape())
display(data.head())
display(data.tail())
data.info()
display(data.nunique())
display(data.isnull().sum())

# Remove S.No. column from data
data = data.drop(['S.No.'], axis = 1)
data.info()


#Feature Engineering
from datetime import date
date.today().year
data['Car_Age']=date.today().year-data['Year']
data.head()

#split name column into brand and model name
data['Brand'] = data.Name.str.split().str.get(0)
data['Model'] = data.Name.str.split().str.get(1) + data.Name.str.split().str.get(2)
data[['Name','Brand','Model']]
print(data.Brand.unique())
print(data.Brand.nunique())
searchfor = ['Isuzu','ISUZU','Mini','Land']
data[data.Brand.str.contains('|'.join(searchfor))].head(5)
data["Brand"].replace({"ISUZU": "Isuzu", "Mini": "Mini Cooper","Land":"Land Rover"}, inplace=True)


#describe() function gives all statistics summary of data

data.describe().T

#Before we do EDA, lets separate Numerical and categorical variables for easy analysis
cat_cols=data.select_dtypes(include=['object']).columns
num_cols = data.select_dtypes(include=np.number).columns.tolist()
print("Categorical Variables:")
print(cat_cols)
print("Numerical Variables:")
print(num_cols)



#Univariate Analysis

#plots for continuous variables

for col in num_cols:
    print(col)
    print('Skew :', round(data[col].skew(), 2))
    plt.figure(figsize = (15, 4))
    plt.subplot(1, 2, 1)
    data[col].hist(grid=False)
    plt.ylabel('count')
    plt.subplot(1, 2, 2)
    sns.boxplot(x=data[col])
    plt.show()



#categorical variables are being visualized using a count plot

fig, axes = plt.subplots(3, 2, figsize = (18, 18))
fig.suptitle('Bar plot for all categorical variables in the dataset')
sns.countplot(ax = axes[0, 0], x = 'Fuel_Type', data = data, color = 'blue',
              order = data['Fuel_Type'].value_counts().index);
sns.countplot(ax = axes[0, 1], x = 'Transmission', data = data, color = 'blue',
              order = data['Transmission'].value_counts().index);
sns.countplot(ax = axes[1, 0], x = 'Owner_Type', data = data, color = 'blue',
              order = data['Owner_Type'].value_counts().index);
sns.countplot(ax = axes[1, 1], x = 'Location', data = data, color = 'blue',
              order = data['Location'].value_counts().index);
sns.countplot(ax = axes[2, 0], x = 'Brand', data = data, color = 'blue',
              order = data['Brand'].head(20).value_counts().index);
sns.countplot(ax = axes[2, 1], x = 'Model', data = data, color = 'blue',
              order = data['Model'].head(20).value_counts().index);
axes[1][1].tick_params(labelrotation=45);
axes[2][0].tick_params(labelrotation=90);
axes[2][1].tick_params(labelrotation=90);



# Function for log transformation of the column
def log_transform(data,col):
    for colname in col:
        if (data[colname] == 1.0).all():
            data[colname + '_log'] = np.log(data[colname]+1)
        else:
            data[colname + '_log'] = np.log(data[colname])
    data.info()
log_transform(data,['Kilometers_Driven','Price'])
#Log transformation of the feature 'Kilometers_Driven'
sns.distplot(data["Kilometers_Driven_log"], axlabel="Kilometers_Driven_log");




#Bivariate Analysis
plt.figure(figsize=(13,17))
sns.pairplot(data=data.drop(['Kilometers_Driven','Price'],axis=1))
plt.show()



#A bar plot can be used to show the relationship between Categorical variables and continuous variables
fig, axarr = plt.subplots(4, 2, figsize=(12, 18))
data.groupby('Location')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[0][0], fontsize=12)
axarr[0][0].set_title("Location Vs Price", fontsize=18)
data.groupby('Transmission')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[0][1], fontsize=12)
axarr[0][1].set_title("Transmission Vs Price", fontsize=18)
data.groupby('Fuel_Type')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[1][0], fontsize=12)
axarr[1][0].set_title("Fuel_Type Vs Price", fontsize=18)
data.groupby('Owner_Type')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[1][1], fontsize=12)
axarr[1][1].set_title("Owner_Type Vs Price", fontsize=18)
data.groupby('Brand')['Price_log'].mean().sort_values(ascending=False).head(10).plot.bar(ax=axarr[2][0], fontsize=12)
axarr[2][0].set_title("Brand Vs Price", fontsize=18)
data.groupby('Model')['Price_log'].mean().sort_values(ascending=False).head(10).plot.bar(ax=axarr[2][1], fontsize=12)
axarr[2][1].set_title("Model Vs Price", fontsize=18)
data.groupby('Seats')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[3][0], fontsize=12)
axarr[3][0].set_title("Seats Vs Price", fontsize=18)
data.groupby('Car_Age')['Price_log'].mean().sort_values(ascending=False).plot.bar(ax=axarr[3][1], fontsize=12)
axarr[3][1].set_title("Car_Age Vs Price", fontsize=18)
plt.subplots_adjust(hspace=1.0)
plt.subplots_adjust(wspace=.5)
sns.despine()


```

-----------------------------------

## 4. Semantic data analysis

```
# Social Media Analytics
## Practical No. 5
### Implementation of Content Based Social Media Analytics.
### 1. Implement Sentiment Analysis on collected social media data.
### 2. Trend analysis using Google Trends

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from textblob import TextBlob
from wordcloud import WordCloud
from IPython.display import display

# Read Preprocessed CSV File
text_df = pd.read_csv('/content/preprocess_CNBC.csv')
text_df.info()
display(text_df.head(10))

# Define Polarity
def polarity(Tweet):
    return TextBlob(Tweet).sentiment.polarity

# Apply polarity
text_df['polarity'] = text_df['Tweet'].apply(polarity)
display(text_df.head(10))

# Define Sentiment
def sentiment(label):
    if label <0:
        return "Negative"
    elif label ==0:
        return "Neutral"
    elif label>0:
        return "Positive"

# Apply Sentiments
text_df['sentiment'] = text_df['polarity'].apply(sentiment)
text_df = text_df.drop(['Unnamed: 0.1'], axis=1)
text_df = text_df.drop(['Unnamed: 0'], axis=1)
display(text_df)

# Save data with sentiments in new file
text_df.to_csv('/content/tweet.csv')

# Plot Sentiments
sns.countplot(x='sentiment', data = text_df)
fig = plt.figure(figsize=(5,5))
fig = plt.figure(figsize=(7,7))
colors = ("yellowgreen", "gold", "red")
wp = {'linewidth':2, 'edgecolor':"black"}
tags = text_df['sentiment'].value_counts()
explode = (0.1,0.1,0.1)
tags.plot(kind='pie', autopct='%1.1f%%', shadow=True, colors = colors, startangle=90, wedgeprops = wp, explode = explode, label='')
plt.title('Distribution of sentiments')
plt.show()

# Find Positive Tweets
pos_tweets = text_df[text_df.sentiment == 'Positive']
pos_tweets = pos_tweets.sort_values(['polarity'], ascending= False)
display(pos_tweets.head())
Tweet = ' '.join([word for word in pos_tweets['Tweet']])

# Display Wordcloud for positive tweets
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(Tweet)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in positive tweets', fontsize=19)
plt.show()

# Find Negative Tweets
neg_tweets = text_df[text_df.sentiment == 'Negative']
neg_tweets = neg_tweets.sort_values(['polarity'], ascending= False)
display(neg_tweets.head())
Tweet = ' '.join([word for word in neg_tweets['Tweet']])

# Display Wordcloud for negative tweets
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(Tweet)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in negative tweets', fontsize=19)
plt.show()

# Find neutral Tweets
neutral_tweets = text_df[text_df.sentiment == 'Neutral']
neutral_tweets = neutral_tweets.sort_values(['polarity'], ascending= False)
display(neutral_tweets.head())
Tweet = ' '.join([word for word in neutral_tweets['Tweet']])

# Display Wordcloud for neutral tweets
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(Tweet)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in neutral tweets', fontsize=19)
plt.show()

```

-----------------------------------

## 5. structure Based Social Media Analytics Facebook Network Analysis using Networks

```
import pandas as pd
import networkx as nx
from IPython.display import display

# Read the CSV file into a DataFrame
df = pd.read_csv("/content/pseudo_facebook.csv")

# Display the first few rows of the DataFrame
display(df.head())


# Load edge list
fb_graph = nx.from_pandas_edgelist(df, source="dob_year", target="gender")

# Check the type of fb_graph
type(fb_graph)


# Display all nodes in the graph
display(fb_graph.nodes())
print("_________________________________________________________________________")
# Display all edges in the graph
display(fb_graph.edges())


# Add a new node and edge to the graph
fb_graph.add_edge("female", "2022")

# Display nodes and edges again after adding the new node
display(fb_graph.nodes())
print("____________________________________________________________________________________________________________________________________________________________________________________")
display(fb_graph.edges())


import matplotlib.pyplot as plt

# Create a new undirected graph from the existing fb_graph
G = nx.Graph(fb_graph)

# Set the figure size
plt.figure(figsize=(12, 8))

# Draw the Facebook friends network with a different layout (e.g., spring layout)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', edge_color='gray', font_size=10)

# Show the plot
plt.show()


import matplotlib.pyplot as plt

# Create a new undirected graph from the existing fb_graph
G = nx.Graph(fb_graph)

# Set the figure size
plt.figure(figsize=(12, 8))

# Draw the Facebook friends network with a different layout (e.g., spring layout)
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', edge_color='gray', font_size=10)

# Show the plot
plt.show()

import matplotlib.pyplot as plt

# Create a new undirected graph from the existing fb_graph
G = nx.Graph(fb_graph)

# Set the figure size
plt.figure(figsize=(12, 8))

# Draw the Facebook friends network with a different layout (e.g., spring layout)
pos = nx.shell_layout(G)
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', edge_color='gray', font_size=10)

# Show the plot
plt.show()

import matplotlib.pyplot as plt

# Create a new undirected graph from the existing fb_graph
G = nx.Graph(fb_graph)

# Set the figure size
plt.figure(figsize=(12, 8))

# Draw the Facebook friends network with a different layout (e.g., spring layout)
pos = nx.spiral_layout(G)
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', edge_color='gray', font_size=10)

# Show the plot
plt.show()
```

-----------------------------------

## 8. Youtube  analysis

```
# Social Media Analytics
## <font color="red"> Practical No. 10
### Implementation of scrapping Top-level YouTube Video Review/Comments using YouTube Google API and having Sentiment Analysis for Improvement in Business Model.

# Requirements
import requests
video_id = "JyJd111Ym7U"
api_key = "AIzaSyA7OeUdnm6P6XXrngx8a4wbAnpRAY8I2sg"

# Retrieve video information
video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
video_info_response = requests.get(video_info_url)
video_info_data = video_info_response.json()
video_info_data

# Retrieve video comments
comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}"
comments_response= requests.get(comments_url)
comments_data = comments_response.json()
comments_data

# Extract the carnents
comments = [item["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for item in comments_data["items"]]
print(comments)

from textblob import TextBlob

# Apply Sentiments on extracted comments
def get_comment_sentiment(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

# Print Comments with Sentiments
comment_list = []
sentiment_list = []
for comment in comments:
    sentiment = get_comment_sentiment(comment)
    comment_list.append(comment)
    sentiment_list.append(sentiment)
    print(f"{comment}: {sentiment}")

import pandas as pd
# Create Dataframe of extracted Comments
sentiment_df = pd.DataFrame({"Comments": comment_list,"Sentiment": sentiment_list})
sentiment_df.head(15)

# Convert to .CSV File
sentiment_df.to_csv("end_file.csv")
print("Saved file YouTube_Comments_Sentiment.csv")
```

-----------------------------------

Start IPython and import `numpy` usually under the alias ``np``: `import
numpy as np`.  Then, directly past or use the ``%cpaste`` magic to paste
examples into the shell.  To see which functions are available in `numpy`,
type ``np.<TAB>`` (where ``<TAB>`` refers to the TAB key), or use
``np.*cos*?<ENTER>`` (where ``<ENTER>`` refers to the ENTER key) to narrow
down the list.  To view the docstring for a function, use
``np.cos?<ENTER>`` (to view the docstring) and ``np.cos??<ENTER>`` (to view
the source code).

Copies vs. in-place operation
-----------------------------
Most of the functions in `numpy` return a copy of the array argument
(e.g., `np.sort`).  In-place versions of these functions are often
available as array methods, i.e. ``x = np.array([1,2,3]); x.sort()``.
Exceptions to this rule are documented.

"""