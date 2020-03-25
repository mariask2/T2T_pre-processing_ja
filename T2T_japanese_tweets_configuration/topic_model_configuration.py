import os
from html.parser import HTMLParser

# An import that should function both locally and when running an a remote server
try:
    from environment_configuration import *
except:
    from topics2themes.environment_configuration import *

if RUN_LOCALLY:
    from topic_model_constants import *
    from word2vec_term_similarity import *

else:
    from topics2themes.topic_model_constants import *
    from topics2themes.word2vec_term_similarity import *

"""
Nr of topics to retrieve
"""
NUMBER_OF_TOPICS = 15


"""
Nr of words to display for each topic
"""
NR_OF_TOP_WORDS = 10

"""
Nr of most typical document to retrieve for each topic
"""

NR_OF_TOP_DOCUMENTS = 20

"""
Number of runs to check the stability of the retrieved topics.
Only topics that occur in all NUMBER_OF_RUNS runs will be
considered valid
"""
NUMBER_OF_RUNS = 100


"""
Mininimum overlap of retrieved terms to considered the retrieved topic as
the same topic of a another one
"""
OVERLAP_CUT_OFF = 0.7


"""
Whether to use pre-processing (collocation detection and synonym clustering)
"""
PRE_PROCESS = True

"""
Mininimum occurrence in the corpus for a term to be included in the topic modelling
"""
MIN_DOCUMENT_FREQUENCY = 1

"""
Maximum occurrence in the corpus for a term to be included in the topic modelling
"""
MAX_DOCUMENT_FREQUENCY = 0.95

"""
Search path to the vector space
"""


SPACE_FOR_PATH = "latest-ja-word2vec-gensim-model/word2vec.gensim.model"

VECTOR_LENGTH = 50

GENSIM_FORMAT = True

MAX_DIST_FOR_CLUSTERING = 0.55

"""
    Whether to remove document duplicates (and near-duplicates) in the data.
    Recommended to do that, otherwise there is a risk that the topic modelling algorithm will find
    these as topics
    """

REMOVE_DUPLICATES = False

"""
    If two documents have a series of MIN_NGRAM_LENGTH_FOR_DUPLICATE tokens that are identical, these
    documents are then cosidered as duplicates, and the longest one of these two documents is removed
    """
MIN_NGRAM_LENGTH_FOR_DUPLICATE = 15

"""
The stop word file of user-defined stopiwords to use (Scikit learn stop words are also used)
"""

STOP_WORD_FILE = "japanese-stopwords_extended.txt"

MAX_NR_OF_FEATURES = 10000

"""
The directories in which data is to be found. The data is to be in files with the ".txt" extension
in these directories. For each directory, there should also be a stance-label and a color associated with
the data
"""

DATA_LABEL_LIST = [{DATA_LABEL : "Pos", DIRECTORY_NAME : "pos", LABEL_COLOR : GREEN },\
                   {DATA_LABEL : "Non", DIRECTORY_NAME : "neu", LABEL_COLOR : "#ccad00"},\
                   {DATA_LABEL : "Neg", DIRECTORY_NAME : "neg", LABEL_COLOR : RED}]



TOPIC_MODEL_ALGORITHM = NMF_NAME


class JaHTMLParserLemma(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_rt = False
        self.acc_str = ""
    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "lemma":
                self.acc_str = self.acc_str + " " + attr[1]


def remove_non_text(html_str):
    parser = JaHTMLParserLemma()
    parser.feed(html_str)
    return parser.acc_str


def get_readings_from_html(html_str):
    parser = JaHTMLParser()
    parser.feed(html_str)
    return parser.acc_str

class JaHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_rb = False
        self.acc_str = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == "rb":
            self.inside_rb = True
    
    def handle_endtag(self, tag):
        if tag == "rb":
            self.inside_rb = False
    
    def handle_data(self, data):
        if self.inside_rb:
            self.acc_str = self.acc_str + " " + data


CLEANING_METHOD = get_readings_from_html

emo_dic = {'344': ['negative'], '346': ['negative'], '340': ['negative', 'positive'], '341': ['negative'], '343': ['negative'], '810': ['negative'], '811': ['excitement'], '812': ['positive'], '813': ['negative', 'sadness', 'soc_neg', 'negative', 'negative', 'negative'], '349': ['positive'], '719': ['positive', 'positive', 'positive'], '717': ['positive', 'negative'], '716': ['positive'], '714': ['negative'], '712': ['negative', 'sadness', 'negative', 'negative', 'negative', 'negative'], '711': ['positive'], '911': ['positive'], '298': ['negative'], '291': ['positive', 'positive'], '593': ['positive', 'negative'], '592': ['positive'], '198': ['positive'], '597': ['positive'], '599': ['negative'], '191': ['positive'], '192': ['positive'], '273': ['negative'], '278': ['negative'], '525': ['negative'], '526': ['negative', 'negative'], '449': ['positive'], '446': ['negative'], '109': ['positive'], '100': ['positive'], '902': ['negative'], '39': ['positive', 'positive'], '905': ['negative'], '31': ['positive'], '30': ['positive', 'positive', 'positive'], '37': ['positive'], '36': ['positive', 'positive'], '438': ['positive'], '646': ['negative'], '434': ['positive', 'positive'], '432': ['negative'], '433': ['negative'], '431': ['positive'], '753': ['positive'], '339': ['positive'], '338': ['positive'], '334': ['negative', 'positive'], '331': ['positive'], '330': ['positive'], '332': ['excitement'], '745': ['negative', 'positive'], '856': ['positive', 'positive'], '857': ['positive'], '850': ['positive', 'positive', 'positive', 'positive'], '851': ['negative', 'negative'], '98': ['negative'], '95': ['joy', 'soc_pos', 'positive', 'positive', 'positive'], '742': ['sadness', 'soc_neg', 'negative', 'negative', 'negative'], '743': ['negative', 'positive', 'positive'], '558': ['positive', 'positive'], '749': ['negative'], '557': ['negative'], '550': ['positive', 'positive'], '238': ['negative'], '147': ['negative'], '143': ['negative', 'positive', 'negative', 'positive'], '141': ['negative'], '613': ['joy', 'soc_pos', 'positive', 'positive', 'positive'], '611': ['positive', 'negative', 'negative', 'negative'], '615': ['positive'], '948': ['negative'], '947': ['dislike', 'negative', 'negative', 'negative'], '944': ['positive', 'positive'], '945': ['positive'], '942': ['positive'], '940': ['negative'], '687': ['negative', 'negative'], '680': ['positive', 'positive', 'positive'], '683': ['positive', 'negative'], '130': ['negative', 'positive'], '137': ['negative'], '135': ['negative'], '490': ['negative', 'negative'], '492': ['negative'], '25': ['positive'], '27': ['positive'], '22': ['positive'], '23': ['positive'], '29': ['positive', 'positive', 'positive', 'positive'], '405': ['positive', 'positive', 'negative'], '403': ['joy', 'soc_pos', 'positive', 'positive', 'positive'], '401': ['positive'], '931': ['negative'], '935': ['negative'], '408': ['negative'], '379': ['negative'], '825': ['positive', 'positive', 'positive', 'joy', 'soc_pos', 'positive', 'positive', 'positive'], '370': ['positive'], '373': ['negative'], '372': ['positive'], '821': ['positive'], '820': ['positive'], '377': ['negative'], '706': ['negative'], '700': ['negative', 'negative'], '393': ['positive', 'positive', 'positive'], '392': ['positive', 'positive'], '88': ['positive'], '89': ['negative', 'negative', 'negative', 'negative'], '394': ['positive', 'positive', 'positive'], '82': ['negative'], '86': ['negative'], '87': ['positive'], '84': ['negative'], '796': ['positive', 'positive', 'negative'], '790': ['negative'], '799': ['negative', 'positive', 'positive'], '584': ['negative'], '585': ['soc_neg'], '245': ['negative'], '247': ['negative'], '246': ['positive'], '240': ['positive', 'negative'], '243': ['joy', 'positive', 'positive'], '925': ['positive', 'positive'], '519': ['negative'], '511': ['positive'], '513': ['negative', 'joy', 'positive', 'positive'], '512': ['positive', 'positive'], '515': ['negative', 'negative'], '458': ['negative'], '622': ['positive', 'positive', 'soc_neg'], '451': ['negative'], '452': ['positive'], '628': ['negative'], '456': ['positive'], '174': ['positive'], '171': ['positive'], '656': ['positive', 'negative'], '183': ['joy', 'soc_pos', 'positive', 'positive', 'positive', 'negative', 'positive', 'negative'], '654': ['negative'], '186': ['negative', 'positive'], '187': ['negative'], '184': ['positive'], '659': ['dislike', 'negative', 'negative'], '11': ['positive'], '10': ['positive', 'positive', 'positive'], '13': ['negative'], '15': ['negative'], '14': ['positive'], '16': ['negative'], '861': ['positive'], '18': ['negative'], '867': ['negative'], '882': ['positive'], '881': ['positive'], '887': ['excitement'], '886': ['negative'], '752': ['dislike', 'soc_neg', 'negative', 'negative'], '889': ['positive', 'positive'], '929': ['negative'], '320': ['negative', 'negative'], '321': ['negative'], '324': ['positive', 'positive'], '329': ['positive'], '201': ['negative'], '774': ['positive', 'positive'], '777': ['positive', 'positive'], '772': ['positive'], '208': ['positive', 'positive'], '778': ['positive'], '75': ['negative'], '74': ['negative', 'negative'], '73': ['negative'], '70': ['negative'], '79': ['positive'], '78': ['positive'], '669': ['positive', 'positive'], '667': ['negative'], '665': ['negative'], '663': ['positive'], '662': ['negative'], '661': ['negative'], '660': ['positive', 'positive'], '695': ['positive'], '698': ['soc_neg'], '542': ['negative'], '543': ['negative'], '547': ['positive'], '544': ['positive'], '545': ['positive', 'positive', 'positive', 'positive'], '68': ['positive', 'negative', 'positive'], '120': ['positive'], '121': ['negative'], '123': ['negative'], '127': ['positive'], '128': ['positive'], '129': ['like', 'soc_pos', 'positive', 'positive'], '414': ['negative'], '415': ['positive'], '416': ['negative'], '417': ['negative'], '412': ['negative'], '413': ['positive', 'negative'], '920': ['positive', 'negative', 'negative'], '419': ['negative'], '926': ['positive'], '319': ['positive'], '318': ['positive'], '313': ['negative'], '312': ['positive'], '832': ['positive', 'positive'], '3': ['negative'], '364': ['negative'], '365': ['negative'], '362': ['positive', 'positive', 'positive', 'positive'], '363': ['negative'], '360': ['positive', 'negative'], '381': ['positive', 'positive'], '386': ['positive', 'positive', 'positive', 'sadness', 'soc_neg', 'negative', 'negative', 'negative'], '784': ['positive'], '787': ['positive'], '780': ['negative', 'positive'], '782': ['positive', 'positive'], '783': ['positive'], '579': ['negative'], '570': ['negative', 'soc_pos', 'positive', 'positive'], '577': ['negative'], '576': ['soc_neg'], '574': ['soc_neg'], '65': ['positive', 'negative'], '66': ['negative', 'dislike', 'soc_neg', 'negative', 'negative'], '67': ['negative', 'negative'], '252': ['positive'], '69': ['positive'], '250': ['positive'], '254': ['positive'], '154': ['soc_pos', 'positive', 'positive'], '730': ['positive', 'negative'], '733': ['negative'], '735': ['negative'], '737': ['negative'], '736': ['positive'], '739': ['positive'], '507': ['positive', 'negative'], '502': ['positive', 'positive'], '500': ['positive'], '501': ['positive'], '630': ['negative', 'negative'], '633': ['negative'], '468': ['negative'], '465': ['dislike', 'negative', 'negative'], '639': ['positive'], '467': ['positive', 'positive'], '461': ['positive'], '463': ['negative'], '462': ['negative'], '168': ['negative'], '169': ['negative'], '164': ['positive'], '165': ['positive', 'positive', 'positive'], '167': ['negative'], '162': ['positive'], '163': ['positive', 'positive'], '878': ['positive'], '879': ['positive'], '873': ['positive'], '871': ['positive'], '9': ['positive'], '892': ['negative'], '893': ['positive', 'negative'], '895': ['positive', 'positive'], '897': ['negative'], '899': ['negative'], '356': ['positive', 'negative', 'soc_neg', 'positive'], '808': ['excitement', 'positive'], '352': ['positive', 'negative', 'positive'], '802': ['positive', 'positive'], '805': ['soc_neg'], '769': ['negative'], '762': ['positive'], '763': ['positive', 'positive'], '766': ['positive', 'positive'], '218': ['soc_neg'], '4': ['positive'], '281': ['positive', 'negative'], '283': ['positive'], '285': ['positive'], '287': ['positive'], '679': ['positive'], '675': ['positive'], '676': ['positive'], '677': ['negative', 'negative'], '671': ['soc_pos', 'soc_neg'], '673': ['positive', 'positive'], '263': ['positive', 'negative'], '262': ['negative'], '261': ['negative'], '266': ['negative'], '269': ['negative', 'negative'], '50': ['positive', 'positive', 'negative'], '52': ['positive', 'negative', 'negative'], '537': ['negative', 'negative'], '533': ['positive'], '200': ['positive'], '114': ['positive'], '116': ['positive'], '915': ['positive'], '914': ['positive', 'sadness', 'soc_neg', 'negative', 'negative'], '917': ['negative'], '916': ['sadness', 'soc_neg', 'negative', 'negative', 'negative'], '425': ['negative'], '424': ['positive'], '309': ['negative'], '300': ['positive'], '371': ['positive'], '847': ['joy', 'soc_pos', 'positive', 'positive', 'positive'], '846': ['soc_neg', 'soc_neg'], '843': ['negative'], '842': ['positive'], '823': ['positive', 'positive', 'positive'], '568': ['negative'], '569': ['positive'], '751': ['soc_pos'], '757': ['positive', 'positive'], '756': ['negative'], '561': ['negative'], '759': ['negative'], '564': ['negative'], '565': ['negative'], '227': ['negative'], '223': ['negative'], '727': ['positive'], '720': ['joy', 'soc_pos', 'positive', 'positive', 'positive', 'positive'], '721': ['negative', 'positive'], '728': ['positive', 'negative'], '605': ['negative'], '601': ['positive'], '600': ['negative'], '603': ['negative', 'negative'], '609': ['positive'], '48': ['positive'], '951': ['negative'], '950': ['negative'], '44': ['positive'], '45': ['positive'], '41': ['positive'], '488': ['negative'], '483': ['negative'], '481': ['positive'], '480': ['soc_pos', 'positive', 'positive'], '472': ['positive'], '473': ['negative', 'negative', 'negative', 'negative'], '477': ['negative', 'positive'], '474': ['negative'], '478': ['positive', 'positive', 'negative'], '479': ['negative', 'negative', 'negative']}

def get_emotions(doc_id):
    id = doc_id.split("/")[-1].replace(".txt", "")
    if id in emo_dic:
        return list(set(emo_dic[id]))
    else:
        return []

ADDITIONAL_LABELS_METHOD = get_emotions
SHOW_ARGUMENTATION = False

WORDS_NOT_TO_INCLUDE_IN_CLUSTERING_FILE = "not_cluster.txt"





