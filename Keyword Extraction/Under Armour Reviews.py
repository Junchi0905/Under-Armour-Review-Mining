#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import nltk
from nltk.util import bigrams 
from nltk.tokenize import word_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
ps = PorterStemmer()
stopwords_english = set(stopwords.words('english'))
import os


# In[16]:


os.chdir('C:\\Users\\junch\\Desktop\\Basil Lab')


# In[17]:


keywords=['price','expensive','cheap','prices','discount','discounts','money','pricey','priced','paid','pay','paying','$','%',
          'overpriced','affordable','Price','Expensive','Cheap','Prices','Discount','Discounts','Money','Pricey','Priced',
          'Paid','Pay','Paying','$','Overpriced','Affordable']


# In[18]:


keywords_=['checkout','Checkout','Staff','staff','Employees','employees','Associates','associate','worker','Worker','service'
           ,'Service','manager','Manager','people','cashier']


# In[19]:


sentiment=pd.DataFrame()


# In[20]:


sid = SentimentIntensityAnalyzer()
for file in os.scandir('csvs'):
    reviews=pd.read_csv(file)
    reviews.drop(['num_reviews','review_data','loc_type','avg_review','name_only','user_href','ID'],axis=1,inplace=True)
    reviews.dropna(axis=0,subset=['text'],inplace=True)
    text = reviews['text']
    #text = str(text.encode('utf-8'))
    for sentence in text:
        for i in keywords:
            if i in sentence:
                ss = sid.polarity_scores(sentence)
                sentiment = sentiment.append({'Address': reviews['name_of_loc'][0],
                                  'Review':sentence,
                                  'Sentiment Score':ss['compound'],
                                    'Review Number':int(len(reviews)),
                                    'lat':reviews['lat'][0],
                                    'long':reviews['long'][0]
                                             
                                             }, ignore_index=True)

                break


# In[21]:


sentiment


# In[22]:


sentiment_gb=sentiment.groupby(['Address']).mean()
sentiment_gb


# In[11]:


sentiment_gb.to_csv('Sentiment Under Armour.csv',index=True)


# In[ ]:





# In[ ]:





# In[12]:


corpus=sentiment['Review']
corpus = corpus.str.split()
corpus = corpus.apply(lambda x: [re.sub(r'[^a-zA-Z]', "",y.lower()) for y in x])
corpus = corpus.apply(lambda x: [ps.stem(y) for y in x])
corpus = corpus.apply(lambda x: [' '.join(x)])
corpus = pd.Series(corpus).astype(str)


# In[13]:


vectorizer = CountVectorizer(stop_words='english', min_df=int(5), max_df=0.9, ngram_range=(1, 1))
tfidf = vectorizer.fit_transform(corpus)

transformer = TfidfTransformer()
transformed_weights = transformer.fit_transform(tfidf)
weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'term_CN': vectorizer.get_feature_names(), 'weight': weights})
weights=weights_df.sort_values(by='weight', ascending=False).reset_index(drop=True)[:40]


# In[14]:


weights


# In[ ]:





# # TF-IDF

# In[33]:


All_review=pd.DataFrame(columns=['Address','Review','lat','long'])


# In[34]:


for file in os.scandir('csvs'):
    reviews=pd.read_csv(file)
    reviews.drop(['num_reviews','review_data','loc_type','avg_review','name_of_loc','name_only','user_href','ID'],axis=1,inplace=True)
    reviews.dropna(axis=0,subset=['text'],inplace=True)
    text = reviews['text']
    #text = str(text.encode('utf-8'))
    for sentence in text:
        All_review = All_review.append({'Address': reviews['address_only'][0],
                                  'Review':sentence,
                                    'lat':reviews['lat'][0],
                                    'long':reviews['long'][0]
                                             }, ignore_index=True)
        
        
        


# In[24]:


corpus = All_review['Review']
corpus = corpus.str.split()
corpus = corpus.apply(lambda x: [re.sub(r'[^a-zA-Z]', "",y.lower()) for y in x])
corpus = corpus.apply(lambda x: [ps.stem(y) for y in x])
corpus = corpus.apply(lambda x: [' '.join(x)])
corpus = pd.Series(corpus).astype(str)


# In[25]:


vectorizer = CountVectorizer(stop_words='english', min_df=int(5), max_df=0.9, ngram_range=(1, 1))
tfidf = vectorizer.fit_transform(corpus)

transformer = TfidfTransformer()
transformed_weights = transformer.fit_transform(tfidf)
weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'term_CN': vectorizer.get_feature_names(), 'weight': weights})
weights=weights_df.sort_values(by='weight', ascending=False).reset_index(drop=True)[:40]


# In[26]:


weights


# # LDA(Latent Dirichlet Allocation)

# In[35]:


df_review = All_review['Review'].tolist()


# In[36]:


df_review


# In[39]:


from gensim import corpora
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in df_review] 

dictionary_review = corpora.Dictionary(doc_clean)


# In[41]:


import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary_review.doc2bow(doc) for doc in doc_clean]


# In[75]:


# Running and Trainign LDA model on the document term matrix.
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=15, id2word = dictionary_review, passes=50)


# In[76]:


print(ldamodel.print_topics(num_topics=15, num_words=3))


# # LSA(Latent Semantic Analysis)
# 

# In[49]:


reindexed_data = All_review['Review']
reindexed_data.index = All_review.index


# In[50]:


from sklearn.feature_extraction.text import CountVectorizer

small_count_vectorizer = CountVectorizer(stop_words='english', max_features=400)
small_text_sample = reindexed_data.as_matrix()

#display(small_text_sample_CN)
small_document_term_matrix = small_count_vectorizer.fit_transform(small_text_sample)


# In[51]:


from sklearn.decomposition import TruncatedSVD

n_topics = 8

lsa_model = TruncatedSVD(n_components=n_topics)
lsa_topic_matrix = lsa_model.fit_transform(small_document_term_matrix)


# In[52]:


from collections import Counter
# Define helper functions
def get_keys(topic_matrix):
    '''returns an integer list of predicted topic categories for a given topic matrix'''
    keys = []
    for i in range(topic_matrix.shape[0]):
        keys.append(topic_matrix[i].argmax())
    return keys

def keys_to_counts(keys):
    '''returns a tuple of topic categories and their accompanying magnitudes for a given list of keys'''
    count_pairs = sorted(Counter(keys).items())
    categories = [pair[0] for pair in count_pairs]
    counts = [pair[1] for pair in count_pairs]
    return (categories, counts)


# In[53]:


lsa_keys = get_keys(lsa_topic_matrix)
lsa_categories, lsa_counts = keys_to_counts(lsa_keys)


# In[59]:


def get_top_n_words(n, keys, document_term_matrix, count_vectorizer):
    '''returns a list of n_topic strings, where each string contains the n most common 
        words in a predicted category, in order'''
    categories, counts = keys_to_counts(keys)
    top_word_indices = []
    for topic in categories:
        temp_vector_sum = 0
        for i in range(len(keys)):
            if keys[i] == topic:
                temp_vector_sum += document_term_matrix[i]
        temp_vector_sum = temp_vector_sum.toarray()
        top_n_word_indices = np.flip(np.argsort(temp_vector_sum)[0][-n:],0)
        top_word_indices.append(top_n_word_indices)   
    top_words = []
    for topic in top_word_indices:
        topic_words = []
        for index in topic:
            temp_word_vector = np.zeros((1,document_term_matrix.shape[1]))
            temp_word_vector[:,index] = 1
            the_word = count_vectorizer.inverse_transform(temp_word_vector)[0][0]
            topic_words.append(the_word.encode('ascii').decode('utf-8'))
        top_words.append(" ".join(topic_words))
    return top_words, categories


# In[62]:


import numpy as np
top_n_words_lsa, topic_n = get_top_n_words(3, lsa_keys, small_document_term_matrix, small_count_vectorizer)

for i in range(len(topic_n)):
    print("Topic {}: ".format(topic_n[i]), top_n_words_lsa[i])


# In[64]:


import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

get_ipython().run_line_magic('matplotlib', 'inline')
top_3_words, topic_3= get_top_n_words(3, lsa_keys, small_document_term_matrix, small_count_vectorizer)
labels = ['Topic {}: \n'.format(topic_3[i]) + top_3_words[i] for i in range(len(topic_n))]

fig, ax = plt.subplots(figsize=(16,8))
ax.bar(list(i for i in range(len(lsa_categories))), lsa_counts)
ax.set_xticks(list(i for i in range(len(lsa_categories))))
ax.set_xticklabels(labels)
ax.set_title('LSA Topic Category Counts')


# # Textrank

# In[65]:


from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

class TextRank4Keyword():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    
    def set_stopwords(self, stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break
        
        
    def analyze(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""
        
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Pare text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight


# In[66]:


tr_review = All_review['Review']
comment_words = ' '
for sentence in tr_review:
    comment_words = comment_words + sentence + ' '


# In[67]:


tr4w = TextRank4Keyword()
tr4w.analyze(comment_words, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
tr4w.get_keywords(10)


# In[68]:


tr4w.get_keywords(20)


# # Word Cloud

# In[70]:


from wordcloud import WordCloud, STOPWORDS 


# In[73]:



corpus = All_review['Review']
comment_words = ' '
stopwords = set(STOPWORDS) 
  
# iterate through the csv file 
for title in corpus[:]: 
      
    # typecaste each val to string 
    title = str(title) 
  
    # split the value 
    tokens = title.split() 
      
    # Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
          
    for words in tokens: 
        comment_words = comment_words + words + ' '

        
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 30).generate(comment_words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 


# # Information Extraction

# In[27]:


import en_core_web_sm
import spacy
nlp = spacy.load('en_core_web_sm')


# In[28]:


doc_persons = {}
doc_locations = {}
doc_organs = {}


# In[29]:


for rev in All_review['Review']:
    content = nlp(rev)
    for word in content.ents:
        text = word.text.strip()
        if word.label_ == 'PERSON':
            if text in doc_persons.keys():
                doc_persons[text] += 1
            else:
                doc_persons[text] = 1
        elif word.label_ == 'LOC' or word.label_ == 'GPE':
            if text in doc_locations.keys():
                doc_locations[text] += 1
            else:
                doc_locations[text] = 1
        elif word.label_ == 'ORG':
            if text in doc_organs.keys():
                doc_organs[text] += 1
            else:
                doc_organs[text] = 1 


# In[30]:


persons=sorted(doc_persons.items(), key=lambda item:item[1],reverse=True)
locations=sorted(doc_locations.items(), key=lambda item:item[1],reverse=True)
organs=sorted(doc_organs.items(), key=lambda item:item[1],reverse=True)


# In[31]:


persons[:20]


# In[32]:


locations[:20]


# In[33]:


organs[:20]

