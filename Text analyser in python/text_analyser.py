import nltk
nltk.download([  "names", "stopwords","vader_lexicon","punkt","wordnet",'omw-1.4', 'maxent_ne_chunker','words'])
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

"""
This whole file works as the procesing of text
"""

#Text analysis

#open text file in read mode
text_file = open("read.txt", "r", encoding='utf-8')
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()
 

#Read the data
text = data

print('Hello! I will help you to understand the logic of your article (should be teh only one in the reas.txt file, in the same folder')


#Sentence tokenization
sentences = nltk.sent_tokenize(text)
#print(sentences)
#Print the number of sentences
print("")
print("You wrote", len(sentences), 'sentences')

#Word tokenization
words = nltk.word_tokenize(text)
#print(words)

#Print the number of words
print("")
print("You wrote", len(words), 'words')

print('Thsi means that ypur wrote', len(words)/len(sentences), 'words per sentence on average')



#determine most common words in each sentence
def most_common_words(text, n):
    words = nltk.tokenize.word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stopwords.words('english')]
    fdist = nltk.FreqDist(words)
    return fdist.most_common(n)

print("")
print('The 5 most common words in your text are:')
print(most_common_words(text, 5))

"""
for i in range(len(sentences)):
    print('Sentence', i+1, ':', sentences[i])
    print('Most common words:', most_common_words(sentences[i], 5))
    print()
"""



#Remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
filtered_words = [w for w in words if not w in stop_words]
#print(filtered_words)



#Stemming
#Stemming is the process of reducing inflected (or sometimes derived) words to their stem, base or root form—generally a written word form.
from nltk.stem import PorterStemmer
ps = PorterStemmer()
stemmed_words = [ps.stem(w) for w in filtered_words]
#print(stemmed_words)
print("")
print("Stemmming is the process of reducing inflected (or sometimes derived) words to their stem, base or root form—generally a written word form.")
print("")
#Determine the most common frequent stemmed words
fdist = nltk.FreqDist(stemmed_words)
print("Your most common stemmed words are:")
print(fdist.most_common(10))



#Lemmatization
#Lemmatization is the process of grouping together the different inflected forms of a word so they can be analysed as a single item.
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(w) for w in filtered_words]
#print(lemmatized_words)

#Determine the most common frequent lemmatized words
fdist = nltk.FreqDist(lemmatized_words)
#print(fdist.most_common(10))

print('')
print('Lemmatization is the process of grouping together the different inflected forms of a word so they can be analysed as a single item.')
print('')
print("Your most common lemmatized words are:")
print(fdist.most_common(10))

#Part of speech tagging
#Part of speech tagging is the process of marking up a word in a text as corresponding to a particular part of speech, based on both its definition and its context.
tagged_words = nltk.pos_tag(lemmatized_words)
print('')
#print('Speech tagging is the process of marking up a word in a text as corresponding to a particular part of speech, based on both its definition and its context.')
#print('')
#print('Your tagged words are:')
#print(tagged_words)

#Named entity recognition
#Named entity recognition is the process of detecting and classifying key information (entities) in text into pre-defined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.
namedEnt = nltk.ne_chunk(tagged_words)
#print(namedEnt)
#print('')
#print('Named entity recognition is the process of detecting and classifying key information (entities) in text into pre-defined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.')
#print('')
#print('Your named entities are:')
#print(namedEnt)



#Sentiment analysis
#Sentiment analysis is the process of determining whether a piece of writing is positive, negative or neutral.
print('')
print('Sentiment analysis is the process of determining whether a piece of writing is positive, negative or neutral.')
print('')
print('The values you can get are compound (meaning the overall sentiment), neg (meaning the negative sentiment), neu (meaning the neutral sentiment) and pos (meaning the positive sentiment).')
print('The values go from 0 to 1, where 0 is the lowest and 1 is the highest.')
#print('Your sentiment analysis is for each sentence is:')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
#for sentence in sentences:
 #   print(sentence)
  #  ss = sid.polarity_scores(sentence)
   # for k in sorted(ss):
    #    print('{0}: {1}, '.format(k, ss[k]), end='')
    #print()
print('')
print('Your sentiment analysis is for the whole text is:')
ss = sid.polarity_scores(text)
for k in sorted(ss):
    print('{0}: {1}, '.format(k, ss[k]), end='')
print()


#Text summarization
#Text summarization is the process of shortening a text document with software, in order to create a summary with the major points of the original document.
print('')
print('Text summarization is the process of shortening a text document with software, in order to create a summary with the major points of the original document.')
print('Make sure your text summary makes sese to the ain points you wanted to talk about in your text')
print('If it dosent make sense reconsider your text and try again')
print('')
def read_article(file_name):
    file = open(file_name,"r",encoding='utf-8')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def generate_summary(file_name, top_n=5):
    """
    file_name: the path to the text file
    top_n: the number of sentences the summary should contain
    """


    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top ranked_sentence order are ", ranked_sentence)
    print('')    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    print("Summarize Text: ", ". ".join(summarize_text))

# Let's begin
generate_summary( "read.txt", 2)


print('')
print('Ohhh, its time to see some plots!')
print('They shoudl help you to see what is your text trying to say')
print('')
print('Your word cloud is:')
#plot the word cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

print('')
print('Your frequency distribution plot is:')
#plot the frequency distribution withot stopwords
fdist = nltk.FreqDist(filtered_words)
for i in fdist:
    if i in ['et','al','al.','et.','(',')','[',']','{','}','–','—','/','\\','|',"'",'*','&','^','%','$','#','@','!','~','`','\'','\"','<','>','?','.',',',';',':','_','0','1','2','3','4','5','6','7','8','9']:
        fdist.pop(i)
fdist.plot(30,cumulative=False)
plt.show()


print('')
print('Yeiii we are done!')
print('I hope you enjoyed this program and it helped you to understand your NS assignemnets better, and you get the general logic of your text')

print('')

"""

Tri tree

class Node:


    def __init__(self, character):
        #Transforms the character into a node
        self.character = character
        #The children are stored in a dictionary
        self.children = {}
        #as in the overview the color of the node determins if it's the end of the word
        #Black - Not the end of the word
        #Yellow = end of the word
        self.color = "Black"
        self.rep = 0
        #raise NotImplementedError()
        
class Trie:
  
    
    def __init__(self, word_list):
       t of strings to be inserted into the trie upon creation.

        #Need to create an empty node for the root
        self.root = Node("")
        #Deals with an empty word to avoid errors
        self.root.color = "Yellow"
        #Beacuse The code creates objects we can just change the attribute of the root
        #to easily deal with especial cases
        #treats the root as it's own word
        #To identify a word regardless of the case avoiding case problem
        self.word_list = [word.lower() for word in word_list]
        #Assumes the imput will be a list of words
        #pass each word from the list to be inserted
        for word in self.word_list:
            self.insert(word)
        #raise NotImplementedError()
    
    def insert(self, word):
    
        #marks the current node
        current_node = self.root
        #cheacks each character of the word
        for character in word:
            #If the character is not already one of the childre it creates the node
            if character not in current_node.children:
                #pass the character as a child node of the current character
                current_node.children[character] = Node(character)
            #If it was already in itonly opdate current node
            current_node = current_node.children[character]
        #marks the final node of the word as the end of the word/ chnage color
        current_node.color = "Yellow"
        current_node.rep += 1
        #raise NotImplementedError()
        
    def lookup(self, word):
insert('Prague') should lead to trie.lookup('prague') = True
        
        #avaoiding problems with the case of the word
        #making teh case consistent with the word_list
        word = word.lower()
        #starts looking at the root
        current_node = self.root
        #checks each character of the word
        for character in word:
            #return found if it's not a children
            if character not in current_node.children:
                return False
            #updates the current node
            current_node = current_node.children[character]
            #print("current_node",current_node.color)
        #Checks the color of the last node to determine if teh wrd exists
        #If the last character yellow return True
        if current_node.color == "Yellow":
            return True
        #If black return false 
        #Even if the word is a prifix of another it was never added as a full word
        else:
            return False
        #raise NotImplementedError()


    def alphabetical_list(self):
   
        #Given the structure of the code (requiring an input not necesary to count for non children)
        
        first_letters = [ i for i in self.root.children]
        #first_letters.sort()
        #print(first_letters)
        lst = []
        max_rep = []
    
        #for i in range(len(first_letters)):
                
        def preorder_traversal(node, start, end):
                
        #determind if it's the end of the word
            if node.color == "Yellow":
                #appends the firts letter with teh end
                lst.append(start + end)
                    
                 #transverse thru the tree
            for letter in node.children:
                #holds the end of the word to be updated on each iteration
                hold = end
                #updates the end of the word appending the new letter
                #varaible need to be created tomantain the order of letters
                hold += letter
                #print(hold)
                #creates the child node, to perform the recurssion
                child = node.children[letter]
                #call the function to iterate thru the tree
                preorder_traversal(child, start, hold)
                
        for i in first_letters:
            #print(i)
            preorder_traversal(self.root.children[i], i, "")
            
        lst.sort()
        return lst
        
        
       # raise NotImplementedError()
    
    def k_most_common(self, k):
  
        #Even when it appears as repeated to the albaethical list, this code has the new implementation of 
        #the counting of the word to avoid disturbing the othre
        
        #Given the structure of the code (requiring an input not necesary to count for non children)
        
        first_letters = [ i for i in self.root.children]
        #first_letters.sort()
        #print(first_letters)
        lst = []
        max_rep = []
    
        #for i in range(len(first_letters)):
                
        def preorder_traversal(node, start, end):
                
        #determind if it's the end of the word
            if node.color == "Yellow":
                #Only difference is that the counting of the word is also present
                lst.append([start + end, node.rep])
                    
                 #transverse thru the tree
            for letter in node.children:
                #holds the end of the word to be updated on each iteration
                hold = end
                #updates the end of the word appending the new letter
                #varaible need to be created tomantain the order of letters
                hold += letter
                #print(hold)
                #creates the child node, to perform the recurssion
                child = node.children[letter]
                #call the function to iterate thru the tree
                preorder_traversal(child, start, hold)
                
        for i in first_letters:
            #print(i)
            preorder_traversal(self.root.children[i], i, "")
        
        
        #sorts the list first in desending number numerically
        #and then alphabetically solving the duplicate value problem
        lst.sort(key=lambda x: (-x[1], x[0]))
            
        #Append the first number of elements
        #already sorted
        for i in range(k):
             max_rep.append(lst[i])
            
                
        #transforms into a tuple to match the requirmenets
        final = [tuple(i) for i in max_rep]

        return final

#function to split text into word
def split_text_into_words(text):
    words = []
    for word in text.split():
        words.append(word)
    return words

#function to remove stop words
def remove_stop_words(words):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words

#function to remove punctuation
def remove_punctuation(words):
    punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''
    words = [word for word in words if word not in punctuations]
    return words

#function to remove special characters
def remove_special_characters(words):
    special_characters = '''!()-[]"\,<>./?@#$%^&*_~'''
    words = [word for word in words if word not in special_characters]
    return words

#function to remove numbers
def remove_numbers(words):
    words = [word for word in words if not word.isdigit()]
    return words

#function to remove whitespaces
def remove_whitespaces(words):
    words = [word for word in words if word.strip()]
    return words

#function to remove empty strings
def remove_empty_strings(words):
    words = [word for word in words if word]
    return words

#function to remove words with length less than 3
def remove_words_with_length_less_than_3(words):
    words = [word for word in words if len(word) > 2]
    return words

#Functions remove the same thing as above
speech_full = get(f"https://www.gutenberg.org/files/84/84-0.txt").text
just_text = ''.join(c for c in speech_full if c not in bad_chars)
without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in just_text)
just_words = [word for word in without_newlines.split(" ") if word != ""]
    
trie = Trie(just_words)
print(" ")
#assert the most common words
print("")

"""
