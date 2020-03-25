# -*- coding: utf-8 -*-

import sqlite3
import re
from k2h import kata2hira
from furigana import deduce_furigana_known_reading
from jmdict2pos import jmdict2pos
from kanjinumbers import is_numbers, get_number_reading
from gramdata import special_conjforms, special_words, special_meanings, verb_connections

def compare_pos(pos1, pos2, strict):
    if strict:
        result = pos1[0] == pos2[0] and        pos1[1] == pos2[1] and        pos1[2] == pos2[2] and        pos1[3] == pos2[3] and        pos1[4] == pos2[4]
    else:
        result = pos1[0] == pos2[0]
    return result

from os.path import commonprefix

def split_based_on_common_prefix(s1, s2):
    prefix = commonprefix([s1, s2])
    prefixlen = len(prefix)
    suffix1 = s1[prefixlen:]
    suffix2 = s2[prefixlen:]
    return (prefix, suffix1, suffix2)

def remove_suffix(s, suffixlen):
    if suffixlen == 0:
        return s
    else:
        return s[:-suffixlen]

def get_reading_lemma(writing, writinglemma, reading):
    (prefix, suffix1, suffix2) = split_based_on_common_prefix(writing, writinglemma)
    readingprefix = remove_suffix(reading, len(suffix1))
    return readingprefix + suffix2


# if we can get a match on the written form and the reading, prefer that
def get_possible_entries(cursor, origform, reading):
    seqs = dict()
    if reading != origform:
        cursor.execute('select definings.seq, definings.freq from definings, readings on definings.seq = readings.seq where defining = ? and reading = ?', (origform, reading))
        seqs = dict([(row[0], row[1]) for row in cursor.fetchall()])
    if not seqs:
        cursor.execute('select seq, freq from readings where reading = ?', (kata2hira(origform),))
        seqs = dict([(row[0], row[1]) for row in cursor.fetchall()])
    return seqs


paren_match_re = re.compile("\s*\([^)]+\)")

def remove_paren(s):
    return paren_match_re.sub("", s)

def get_glosses(cursor, writing, reading, pos, strict=True):
    seqs = get_possible_entries(cursor, writing, reading)
    glosses = []
    seqs = dict(seqs)
    for special_word in special_words:
        if special_word in seqs:
            del seqs[special_word]
    for (seq, freqs) in sorted(seqs.items(), key=lambda elem:elem[0]):
        cursor.execute('select gloss, misc, pos from senses where seq = ?', (seq,))
        senses = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
        lastposs = None
        newsfreq = [int(elem[2:]) for elem in freqs.split("\t") if elem[:2] == "nf"]
        for (gloss, misc, poss) in senses:
            if poss == "":
                poss = lastposs
            lastposs = poss
            sortkey = 200
            if newsfreq:
                sortkey = newsfreq[0]
            if "ichi1" in freqs.split("\t"):
                sortkey = 0
            if u"rude or X-rated term (not displayed in educational software)" in misc.split("\t"):
                sortkey = 99999
            dictpos = [jmdict2pos.get(jmdictpos) for jmdictpos in poss.split("\t")]
            filtereddictpos = [pos1 for pos1 in dictpos if pos1 and compare_pos(pos1.split(","), pos, strict)]
            if not strict and not filtereddictpos:
                filtereddictpos = [pos1 for pos1 in dictpos if pos1 == u"exp"]
            gloss = "\t".join([remove_paren(word) for word in gloss.split("\t")])
            if filtereddictpos:
                glosses.append((sortkey, gloss))
    glosses = sorted(glosses, key=lambda elem:elem[0])
    return [gloss[1] for gloss in glosses]

def is_counter(elem):
    (pos,subclass1,subclass2,subclass3,conjform) = elem["pos"]
    return (pos,subclass1,subclass2) == (u'名詞', u'接尾', u'助数詞')

def get_combined_glosses(cursor, elems):
    last_successful_glosses = []
    last_successful_surface = u""
    last_successful_reading = u""
    last_successful_length = 0
    for length in range(2,len(elems)+1):
        tryelems = elems[0:length]
        surface = "".join([elem["surface"] for elem in tryelems])
        if is_numbers(tryelems) or (is_numbers(tryelems[:-1]) and is_counter(tryelems[-1])):
            if is_numbers(tryelems):
                numbers = tryelems
                counter = {"surface":None,"reading":None}
                counter_gloss = []
            else:
                numbers = tryelems[:-1]
                counter = tryelems[-1]
                counter_gloss = get_glosses(cursor, counter["surface"], counter["reading"], counter["pos"], strict=True)
            
            last_successful_length = length
            (reading, surface, number) = get_number_reading("".join([elem["surface"] for elem in numbers]), counter["surface"], counter["reading"], counter_gloss)
            if reading == None:
                # get_number_reading failed
                reading = u""
            last_successful_surface = surface
            last_successful_reading = ("preformatted", reading, surface)
            last_successful_glosses = [unicode(number)]
            if not reading:
                last_successful_glosses = []
            continue
        if any(["reading" not in elem for elem in tryelems]):
            break
        reading = "".join([elem["reading"] for elem in tryelems])
        glosses = get_glosses(cursor, surface, reading, tryelems[-1]["pos"], strict=False)
        if glosses:
            last_successful_length = length
            last_successful_glosses = glosses
            last_successful_surface = surface
            last_successful_reading = reading
    return (last_successful_surface, last_successful_surface, last_successful_reading, last_successful_glosses, last_successful_length)

def get_nouns(elems):
    nouns = []
    for elem in elems:
        if elem["pos"][0] == u"名詞":
            nouns.append(elem)
        else:
            break
    return nouns

def find_verb_connection(pos, conjtype, next_word_origform, next_word_pos, surface):
    if conjtype == u"基本形":
        return None
    key = (pos, conjtype, next_word_origform, next_word_pos)
    connection = verb_connections.get(key)
    if not connection:
        if conjtype == u"て" and next_word_pos[0] == u"名詞":
            pass
        else:
            pass
    else:
        pass
    return connection

def processelem(elem, arg, cursor):
    reading = elem.get("reading")
    origform = elem["origform"]
    conjtype = elem["conjtype"]
    reading_lemma = elem.get("reading_lemma")
    (pos,subclass1,subclass2,subclass3,conjform) = elem["pos"]
    surface = elem["surface"]
    conjfunc = []

    noglosses = elem["conjform"] in special_conjforms
    glosses = []
    if pos in [u"名詞", u"接頭詞"]:
        # noun or prefix
        nouns = get_nouns(arg)
        if nouns:
            (combined_surface, combined_origform, combined_reading, combined_glosses, nconsumed) = get_combined_glosses(cursor, [elem] + nouns)
            if combined_glosses:
                conjform = arg[nconsumed-1]["conjform"]
                conjtype = arg[nconsumed-1]["conjtype"]
                del arg[0:nconsumed-1]
                surface = combined_surface
                reading = combined_reading
                reading_lemma = combined_reading
                glosses = combined_glosses
                origform = combined_origform
    elif ((pos == u"動詞" and subclass1 == u"自立") or (pos == u"形容詞" and subclass1 == u"自立")) and arg and reading:
        # conjugable morpheme token and there are more tokens after
        verbfunction = None
        while arg:
            next_word = arg[0]
            verbfunction = find_verb_connection(pos, conjtype, next_word["origform"], next_word["pos"], surface)
            if verbfunction:
                pos = next_word["pos"][0]
                conjform = next_word["conjform"]
                conjtype = next_word["conjtype"]
                if verbfunction == u"て":
                    conjtype = u"て"
                    explanation = u""
                else:
                    explanation = verbfunction
                conjfunc.append({"explanation":explanation, "origform": next_word["origform"]})
                surface = surface + next_word["surface"]
                reading = reading + next_word.get("reading", "")
                del arg[0]
                if next_word["origform"] in [u"、", u"。"]:
                    break
            else:
                break
    if not glosses and is_numbers([elem]):
        (number_reading, number_surface, number_gloss) = get_number_reading(elem["surface"], None, None, [])
        if number_reading == None:
            # get_number_reading failed
            number_reading = u""
        reading = ("preformatted", number_reading, number_surface)
        glosses = [number_gloss]
    if reading:
        if not glosses:
            glosses = get_glosses(cursor, origform, reading_lemma, elem["pos"])
        if not glosses:
            glosses = get_glosses(cursor, origform, reading_lemma, elem["pos"], strict=False)
    if noglosses:
        glosses = []
    return glosses, conjfunc, surface, reading, reading_lemma, conjtype, origform

def gettext(arg, resourcedir):
    conn = sqlite3.connect(resourcedir + "/lib/JMDict.sqlite")
    cursor = conn.cursor()
    
    chunks = []

    # add features as separate members
    for elem in arg:
        features = elem["feature"].split(",")
        if len(features) == 9:
            (pos,subclass1,subclass2,subclass3,conjform,conjtype,origform,reading,pronunciation) = features
            elem["pos"] = (pos,subclass1,subclass2,subclass3,conjform)
            elem["conjform"] = conjform
            elem["conjtype"] = conjtype
            elem["origform"] = origform
            elem["reading"] = kata2hira(reading)
            elem["pronunciation"] = pronunciation
        elif len(features) == 7:
            (pos,subclass1,subclass2,subclass3,conjform,conjtype,origform) = features
            elem["pos"] = (pos,subclass1,subclass2,subclass3,conjform)
            elem["conjform"] = conjform
            elem["conjtype"] = conjtype
            elem["origform"] = origform
        else:
            raise Exception("cannot process: " + elem)

    # add reading lemma
    for elem in arg:
        if "reading" in elem:
            elem["reading_lemma"] = get_reading_lemma(elem["surface"], elem["origform"], elem["reading"])


    try:
        while True:
            elem = arg.pop(0)
            (pos,subclass1,subclass2,subclass3,conjform) = elem["pos"]

            # default values
            glosses, conjfunc, surface, reading, reading_lemma, conjtype, origform = ([], [], elem["surface"], elem.get("reading"), elem.get("reading_lemma"), elem["conjtype"], elem["origform"])

            if pos == u"BOS/EOS":
                continue
            elif pos == u"助詞":
                pass
            elif pos not in [u"名詞", u"動詞", u"形容詞", u"副詞", u"接頭詞", u"接続詞"]:
                pass
            elif (origform, elem["pos"]) in special_meanings:
                glosses = special_meanings[(origform, elem["pos"])]
            else:
                glosses, conjfunc, surface, reading, reading_lemma, conjtype, origform = processelem(elem, arg, cursor)

            if reading:
                if isinstance(reading, tuple) and reading[0] == "preformatted":
                    combinedreadings = reading[1]
                    combinedwritings = reading[2]
                    combinedreadingslemma = reading[1]
                    combinedwritingslemma = reading[2]
                else:
                    deducedfurigana = deduce_furigana_known_reading(cursor, reading, surface)
                    combinedreadings = u"\t".join([e[0] for e in deducedfurigana])
                    combinedwritings = u"\t".join([e[1] for e in deducedfurigana])
                    deducedfuriganalemma = deduce_furigana_known_reading(cursor, reading_lemma, origform)
                    combinedreadingslemma = u"\t".join([e[0] for e in deducedfuriganalemma])
                    combinedwritingslemma = u"\t".join([e[1] for e in deducedfuriganalemma])
            else:
                combinedreadings = u""
                combinedwritings = surface
                combinedreadingslemma = u""
                combinedwritingslemma = origform

            if glosses:
                firstgloss = glosses[0].split("\t")[0]
                glosses.insert(0, firstgloss)

            chunks.append((combinedreadings, combinedwritings, glosses, pos, (combinedreadingslemma, combinedwritingslemma), conjtype, conjfunc))
    except IndexError:
        pass

    return chunks


# pos,subclass1,subclass2,subclass3,conjform,conjtype,origform,reading,pronunciation
