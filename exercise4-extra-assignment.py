import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from gensim import corpora, models
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

# Load Alice's Adventures in Wonderland text from gutenberg corpus
nltk.download('gutenberg')
alice_raw = gutenberg.raw('carroll-alice.txt')

# Tokenize the text
alice_tokens = word_tokenize(alice_raw)

# Prepare the data for the LDA model
dictionary = corpora.Dictionary([alice_tokens])
corpus = [dictionary.doc2bow(text) for text in [alice_tokens]]

# Train the LDA model
lda_model = models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# Visualize topics using pyLDAvis
vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis_data)
