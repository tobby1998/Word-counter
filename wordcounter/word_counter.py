import sys,re,collections,nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

set(stopwords.words('german'))
stoppwords = stopwords.words('german')
stoppwords.extend(['%'])
print (stoppwords)

# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")
# split corpus with certain symbol
pat_split = r'(?:[?!.:])'




#import re
#pattern = r'(?:[?!.:])'
#test_text = 'b,b.b/b;b\'b`b[b]b<b>b?b:b"b{b}b~b!b@b#b$b%b^b&b(b)b-b=b_b+b，b。b、b；bb'
#result_list = re.split(pattern, test_text)
#print(result_list)


lmtzr = WordNetLemmatizer()

def check_charset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(4)
        charset = chardet.detect(data)['encoding']
    return charset

def get_words(file):  
    with open (file, encoding="utf-8") as f:  
        words_box=[]
        counter = 0;
        pat = re.compile(r'[^a-zA-Z \']+')
        for line in f:                           
            #if re.match(r'[a-zA-Z]*',line): 
            #    words_box.extend(line.strip().strip('\'\"\.,').lower().split())
            # words_box.extend(pat.sub(' ', line).strip().lower().split())
            words_box.extend(merge(nltk.sent_tokenize(line,language='german')))
            print ("line: ",counter)
            counter = counter +1
        
    return collections.Counter(words_box)  

#1 去除符号 nltk.sent_tokenize(line,language='german')

#2 sentencs tokenized_sent = nltk.tokenize.word_tokenize(sentences,language='german')
    
#3 tag tags = tagger.tag_sent(tokenized_sent)
    


    
def merge(sentences):
    from HanTa import HanoverTagger as ht
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    new_words = []
    for sentence in sentences:
        tokenized_sent = nltk.tokenize.word_tokenize(sentence,language='german')
        words_tags = tagger.tag_sent(tokenized_sent)
        for word in words_tags:
            if word[2][0] in ['N','A','V'] and word[1].lower() not in stoppwords:
                new_words.append((word[1],word[2]))
    return new_words

#    for word in words:
#        if word:
#            tag = nltk.pos_tag(word_tokenize(word,language='german')) # tag is like [('bigger', 'JJR')]
#            pos = wntag(tag[0][1])
#            if word.lower() in stopwords.words():
#                word=[]
#            elif pos:
#                lemmatized_word = lmtzr.lemmatize(word, pos) #Englisch geht nicht, muss es geändert werden. um das zu schaffen muss man sätzerweise tokenisieren.
#                new_words.append(lemmatized_word) # https://textmining.wp.hs-hannover.de/Preprocessing.html
#            else:
#                new_words.append(word)
#    return new_words


def wntag(pttag):
    if pttag in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    elif pttag in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif pttag in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif pttag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    return None


def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text


def append_ext(words):
    new_words = []
    for item in words:
        element, count = item
        tag = element[1] # tag is like [('bigger', 'JJR')]
        word = element[0]
        new_words.append((word, count, tag))
    return new_words

def write_to_file(words, file='results.txt'):
    f = open(file, 'w', encoding="utf-8")
    for item in words:
        for field in item:
            f.write(str(field)+',')
        f.write('\n')


if __name__=='__main__':
    book = "sophiesworld_1_to_2.txt"
    print ("counting...")
    words = get_words(book)
    print ("counting process is finished") 
    print ("writing file...")
    write_to_file(append_ext(words.most_common()))
    
