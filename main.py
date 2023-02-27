import it_core_news_sm
import en_core_web_sm
import fr_core_news_sm
import de_core_news_sm
import nltk
import time
import spacy

# initialize the english pos tagger
nlp_en = spacy.cli.download("en_core_web_sm")
nlp_en = en_core_web_sm.load()

# initialize the italian pos tagger
nlp_it = spacy.cli.download("it_core_news_sm")
nlp_it = it_core_news_sm.load()

# initialize the french pos tagger
nlp_fr = spacy.cli.download("fr_core_news_sm")
nlp_fr = fr_core_news_sm.load()

# initialize the german pos tagger
nlp_gr = spacy.cli.download("de_core_news_sm")
nlp_gr = de_core_news_sm.load()


# this function does the pos tagging of a given language and calls the simplifier function
def simple_pos_tagger(text, input_language):
    if input_language == 'english':
        tagged = nlp_en(text)
    elif input_language == 'italian':
        tagged = nlp_it(text)
    elif input_language == 'german':
        tagged = nlp_gr(text)
    elif input_language == 'french':
        tagged = nlp_fr(text)

    simplified_tagged = [(token.text, get_simple_tag(token.pos_)) for token in tagged]
    return simplified_tagged


# this function generalize tags that are too specific for the Contex Free Grammar
def get_simple_tag(tag):
    if tag == 'PROPN':  # proper nouns into nouns
        return 'NOUN'
    elif tag == 'AUX':  # auxiliary verbs into verbs
        return 'VERB'
    elif tag == 'CCONJ':  # complex conjunctions into normal conjunctions
        return 'CONJ'
    else:
        return tag  # if doesn't need simplification return the normal tag


# defining the context free grammar with the rule stated in the assignment page on moodle
# english-german grammar
grammar_one = nltk.CFG.fromstring("""
    S -> NP VP | NP VP Punct
    NP -> Det Adj NP | Noun | Noun NP | NP Noun | Adj NP | Det NP | NP PP | NP Conj NP | PP NP | PP Det Noun
    VP -> Verb VP | Verb | Verb Adj | Verb Adv | Verb NP | Verb NP PP | Verb NP Adv |Verb Adv NP | Verb Adj Adv NP | Verb Adj Adv | Verb Adv Adj | VP Conj VP | Verb PP | Verb Det Adv NP
    PP -> Prep NP | Prep
    Det -> 'DET'
    Noun -> 'NOUN'
    Adj -> 'ADJ'
    Verb -> 'VERB'
    Conj -> 'CONJ'
    Adv -> 'ADV'
    Prep -> 'ADP'
    Punct -> 'PUNCT'
""")

# italian-french grammar
grammar_two = nltk.CFG.fromstring("""
    S -> NP VP | NP VP Punct
    NP -> Det NP Adj | Noun | Noun NP | NP Noun | NP Adj | Det NP | NP PP | NP Conj NP | PP NP | PP Det Noun
    VP -> Verb VP | Verb | Verb Adj | Verb Adv | Verb NP | Verb NP Adv | Verb Adv NP | Verb Adv Adj | Verb Adj Adv | Verb Adj Adv NP | VP Conj VP | Verb PP | Verb Det Adv NP
    PP -> Prep NP | Prep
    Det -> 'DET'
    Noun -> 'NOUN'
    Adj -> 'ADJ'
    Verb -> 'VERB'
    Conj -> 'CONJ'
    Adv -> 'ADV'
    Prep -> 'ADP'
    Punct -> 'PUNCT'
""")

# infinite loop to analyze multiple sentences
while 1:

    # delay to avoid mixups in the console logs
    time.sleep(1)

    # we get in input the sentence
    print("Please write a sentence in one of this language: english, italian, french or german")
    input_text = input("Sentence: ")

    # we get in input the language of the sentence
    # a language identification function could be use but with short sentences accuracy is low
    # this problem could be resolved with an ML algorithm
    print("In which language is the sentence? (english,italian,german,french)")
    input_lang = input("Language: ")

    # we loop until a correct language is typed
    while input_lang not in ['english', 'italian', 'german', 'french']:
        print("Please chose one of the following: (english,italian,german,french)")
        input_lang = input("Language: ")

    # we call the pos-tagging and simplifying function on the sentence in input
    tagged_phrase = simple_pos_tagger(input_text, input_lang)
    print(tagged_phrase)

    # we separate the tags from the words
    tags_list = [tag for word, tag in tagged_phrase]
    # print(tags_list)

    # we count the adverbs to limit them to one as stated in the assignment
    adv_number = 0
    for tag in tags_list:
        if tag == 'ADV':
            adv_number = adv_number + 1

    # we check if there are pronouns and more than one adverb
    if 'PRON' not in tags_list:
        if adv_number > 1:
            print("Only one adverb is admitted")
        else:
            # we call the correct grammar for the given language
            # german and english should have an identical grammar structure
            # italian and french have very similar structures
            if input_lang == 'english' or input_lang == 'german':
                parser = nltk.ChartParser(grammar_one)
            elif input_lang == 'italian' or input_lang == 'french':
                parser = nltk.ChartParser(grammar_two)

            # we generate the possible trees stopping at the first available one
            for tree in parser.parse(tags_list):
                tree.pretty_print()
                break

    # inform the user pronouns aren't allowed
    else:
        print("Pronouns aren't accepted")
