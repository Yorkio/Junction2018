import gensim
from enum import Enum
from nltk.tokenize import word_tokenize

class Actions(Enum):
    NONE = 0
    SHOW_GLASSES = 1
    SHOW_HAT = 2
    WAR_PER = 3
    TIME_SHIP = 4
    Y = 5
    N = 6
    GREET = 7
    EXIT = 8
    INP_CH = 9


reply = {
    Actions.NONE:["I do not understand you. Please try one more time.",
                  "My memory is overloaded. Try again."],
    Actions.SHOW_GLASSES:["Check this out!",
                          "This one is awesome! I already have four pairs.",
                          "I think you have to check this!","Let's try this one.",
                          "Can you do me a favor? Check this out!"],

    Actions.SHOW_HAT:["Check this out!",
                      "This one is awesome! I already have four pairs.",
                      "I think you have to check this!","Let's try this one.",
                      "Can you do me a favor? Check this out!"],

    Actions.WAR_PER:["""Our product is warranted against defects in materials
                     and workmanship for a period of ONE (1) YEAR from the date
                     of original retail purchase"""],

    Actions.TIME_SHIP:["""The shipping method time starts when the item ships.
    Your order will be delivered within 2-3 business days."""],

    Actions.Y:["""Got you.""",
               """Yep! Finally!""",
               """*Trombone sounds* Sure!""",
               """Yes, yes, yes!"""],

    Actions.N:["""I can try something else.""",
               """So.. It's okay if you say 'No'""","""No. no. no."""],

    Actions.GREET:["""Greetings!""","""Hi! Everything is good, right?""",
                   """Hey! What's up?""","""Hello! How it's going?""",
                   """Hi! Is there anything I can help you with?"""],

    Actions.EXIT:["See you soon!"]}


docs = ['',
        'I want glasses',
        'I want to buy glasses',
        'Sell me glasses',
        'I want to buy hat',
        'Show me cap',
        'Show me hat',
        'Expected date of arrival?',
        'When to expect shipment?',
        'Warranty period?',
        'How long is warranty?',
        'Yes',
        'No',
        'Hello',
        'Hi',
        'Yo',
        'Quit',
        'Exit',
        'change input method',
        'end for today',
        'hey',
        "i'm done"]


dict2act = {docs[0]: Actions.NONE,
            docs[1]: Actions.SHOW_GLASSES,
            docs[2]: Actions.SHOW_GLASSES,
            docs[3]: Actions.SHOW_GLASSES,
            docs[4]: Actions.SHOW_HAT,
            docs[5]: Actions.SHOW_HAT,
            docs[6]: Actions.SHOW_HAT,
            docs[7]: Actions.TIME_SHIP,
            docs[8]: Actions.TIME_SHIP,
            docs[9]: Actions.WAR_PER,
            docs[10]: Actions.WAR_PER,
            docs[11]: Actions.Y,
            docs[12]: Actions.N,
            docs[13]: Actions.GREET,
            docs[14]: Actions.GREET,
            docs[15]: Actions.GREET,
            docs[16]: Actions.EXIT,
            docs[17]: Actions.EXIT,
            docs[18]: Actions.INP_CH,
            docs[19]: Actions.EXIT,
            docs[20]: Actions.GREET,
            docs[21]: Actions.EXIT}

def find_action(inp_query):
    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in docs]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('',tf_idf[corpus],
                                          num_features=len(dictionary))
    query_doc = [w.lower() for w in word_tokenize(inp_query)]
    #print(query_doc)
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    #print(sims[query_doc_tf_idf])
    best_score = 0
    action = Actions.NONE
    for i, score in enumerate(sims[query_doc_tf_idf]):
        if score > best_score:
            best_score = score
            action = dict2act[docs[i]]
    #print(action)
    return sims[query_doc_tf_idf], action

def main():
    inp_query = input()
    find_action(inp_query)


if __name__ == '__main__':
    main()
