# import the necessary libraries
import re
import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# download the necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# read the text file
text = gutenberg.raw('melville-moby_dick.txt')

# filter the whole punctuations in the text
text = re.sub(r'[^\w\s]', '', text)

tokens = word_tokenize(text)

stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

pos_tags = pos_tag(filtered_tokens)

pos_counts = Counter([tag for tag, _ in pos_tags])
top_5_pos = pos_counts.most_common(5)
print("Top 5 Parts of Speech and their frequencies:")
for pos, count in top_5_pos:
    print(f"{pos}: {count}")

# Lemmatization: convert words to their root forms using pos-tagged tokens
lemmatizer = WordNetLemmatizer()
top_tokens = nltk.FreqDist(filtered_tokens).most_common(20)
lemmatized_tokens = [(token, lemmatizer.lemmatize(token)) for token, _ in top_tokens]
print("Top 20 tokens and their lemmas:")
for token, lemma in lemmatized_tokens:
    print(f"{token}: {lemma}")

# Plotting frequency distribution: plot a bar chart to visualize the frequency of top 20
plt.figure(figsize=(10, 6))
plt.bar([pos for pos, _ in pos_counts.most_common(20)], [count for _, count in pos_counts.most_common(20)])
plt.xticks(rotation=45)  # rotate x-axis labels by 45 degrees
plt.title("Frequency Distribution of Parts of Speech")  # add title
plt.xlabel("Parts of Speech")  # add x-axis label
plt.ylabel("Frequency")  # add y-axis label
plt.show()

# Sentiment Analysis
sid = SentimentIntensityAnalyzer()

# score the sentiment of the text
sentiment_scores = sid.polarity_scores(text)
average_sentiment_score = sum(sentiment_scores.values()) / len(sentiment_scores)

# judge the sentiment of the text
if average_sentiment_score > 0.05:
    print("The overall text sentiment is positive.")
else:
    print("The overall text sentiment is negative.")

# print the average sentiment score
print(f"The average sentiment score is {average_sentiment_score:.2f}.")