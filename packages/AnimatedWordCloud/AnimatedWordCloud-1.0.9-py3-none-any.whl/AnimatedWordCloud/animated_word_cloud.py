from .preprocessing import prep
from .wsWordObj_monthly import *
from .wsWordObj import *
sys.path.append('./framework/')
from .framework.framework import main


class animated_word_cloud():
    def __init__(self, text, time, date_format, max_words, freq, ngram, stopwords, skip):
        self.text = text
        self.time = time
        self.date_format = date_format
        self.max_words = max_words
        self.freq = freq
        self.ngram = ngram
        self.stopwords = stopwords
        self.skip = skip

        text = text.dropna()

        output = prep(text_prep=text, time=time, date_format=date_format, max_words = max_words, ngram=ngram, freq=freq, stopwords=stopwords, skip=skip)
        output.to_csv("matrix.csv", index=False, encoding="utf8")
        print("Data matrix created ...")

        if freq == "Y":
            from .WordSwarm import WordSwarm
            main(WordSwarm, sys.argv[1:])
                
        elif freq == "M":
            from .WordSwarm_monthly import WordSwarm
            main(WordSwarm, sys.argv[1:])

        else:
            print(""""Incorrect frequency specification Use "Y" or "M" """)