# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import analyze
import os
import json

import dictionary_configuration

def is_negative(text):
    labels = label_dictionary.get(text, [])
    return "negative" in labels or "soc_neg" in labels

def is_positive(text):
    labels = label_dictionary.get(text, [])
    return "positive" in labels or "soc_pos" in labels

def printchunks(chunks, sentence_nr):
    acc_str = ""
    
    for chunk in chunks:
        combinedreadings = chunk[0]
        combinedwritings = chunk[1]
        glosses = chunk[2]
        pos = chunk[3]
        (combinedreadingslemma, combinedwritingslemma) = chunk[4]
        conjtype = chunk[5]
        conjfunc = chunk[6]
        if glosses:
            gloss = glosses[0]
        else:
            gloss = u""

        lemma_without_digit = u"".join([e for e in combinedwritingslemma.split("\t") if not e.isdigit()])

        display_text = combinedwritings.replace("\t", "").strip()
        
        # Check if in emotion lexicons
        emotion_add = None
        if display_text in label_dictionary:
            emotion_add = display_text
        elif u"な" not in display_text and lemma_without_digit in label_dictionary:
            emotion_add = lemma_without_digit

        if emotion_add:
            for label in label_dictionary[emotion_add]:
                emotion_dict.setdefault(str(sentence_nr), []).append(label)

        # Check if in sentiment lexicon
        if is_positive(display_text) or (u"な" not in display_text and is_positive(lemma_without_digit)):
            display_text = POS_START + display_text + POS_END
        elif is_negative(display_text) or (u"な" not in display_text and is_negative(lemma_without_digit)):
            display_text = NEG_START + display_text + NEG_END

        start_ruby = '<span class = "jp_lemma" lemma = "' + lemma_without_digit + '" title = "' + "|".join(glosses[1:]).replace("\t", ", ") + '"> ' + '<ruby>'

        start_marker_added = False
        acc_str = acc_str + start_ruby
        readings = combinedreadings.replace("\t","").strip()
        if readings == "":
            readings = "."
        if readings != ".":
            readings = '| ' + readings + ' |'
        acc_str = acc_str + '<ruby><rb>' + display_text + '</rb>'
        acc_str = acc_str + '<rt class = "furigana">' + readings + '</rt></ruby>'
        if gloss.strip() != "":
            gloss = "| " + gloss.strip() + " |"
        end_ruby = '<rt class="gloss">' + gloss + '</rt></ruby></span>'
        acc_str = acc_str + end_ruby
        
            
    acc_str = '<span class = "jp">' + acc_str + '</span>'
    output_file = os.path.join("testdata/output/neu", str(sentence_nr) + ".txt")
    print_to = open(output_file, "w")
    print_to.write(acc_str.encode("utf-8"))
    print_to.close()


NEG_START = "<negative>"
NEG_END = "</negative>"
POS_START = "<positive>"
POS_END = "</positive>"

label_dictionary = {}

def read_label_dictionary(dict_name, label):
    f = open(dict_name)
    content = f.read().decode("utf-8")
    saved_dict = json.loads(content)
    if type(saved_dict) is dict:
        words = saved_dict.keys()
    elif type(saved_dict) is list:
        words = saved_dict
    else:
        raise ValueError("unknown type")
    for word in words:
        label_dictionary.setdefault(word, []).append(label)


try:
    label_dictionary_files = dictionary_configuration.label_dictionary_files
except AttributeError:
    label_dictionary_files = []

for filename, label in label_dictionary_files:
    read_label_dictionary(filename, label)

#File for saving emotions
emotion_dict = {}
emotion_file = open("testdata/output/emotions.json", "w")

data = []
sentence_nr = 0

for row in open(sys.argv[1]):
    row = row.decode("utf-8", errors='ignore').rstrip("\n").split("\t")
    if len(row) == 11:
        data.append({"surface":row[0], "feature": ",".join(row[1:10])})
    elif len(row) == 9:
        data.append({"surface":row[0], "feature": ",".join(row[1:8])})
    elif len(row) == 2:
        data.append({"surface":row[0], "feature": row[1]})
    elif len(row) == 1:
        assert(row[0] == "EOS")
        sentence_nr = sentence_nr + 1
        printchunks(analyze.gettext(data, "."), sentence_nr)
        data = []
    else:
        print >>sys.stderr, "unknown row length", row

assert(data == [])

emotion_file.write(str(emotion_dict))

emotion_file.flush()
emotion_file.close()
