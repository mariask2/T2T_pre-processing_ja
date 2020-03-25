# -*- coding: utf-8 -*-

import re

digits = {
    u"０":0,
    u"0":0,
    u"１":1,
    u"1":1,
    u"２":2,
    u"2":2,
    u"３":3,
    u"3":3,
    u"４":4,
    u"4":4,
    u"５":5,
    u"5":5,
    u"６":6,
    u"6":6,
    u"７":7,
    u"7":7,
    u"８":8,
    u"8":8,
    u"９":9,
    u"9":9,
    u"一":1,
    u"二":2,
    u"三":3,
    u"四":4,
    u"五":5,
    u"六":6,
    u"七":7,
    u"八":8,
    u"九":9,
    u"十":10,
    u"百":100,
    u"千":1000,
    u"万":10000,
    u"億":100000000,
}

def is_numbers(elems):
    types = set()
    for elem in elems:
        (pos,subclass1,subclass2,subclass3,conjform) = elem["pos"]
        if (pos,subclass1) != (u'名詞', u'数'):
            return None
        if elem["surface"][0] in digits:
            types.add("arabic/kanji")
    return types


def normalize_digit(digit):
    return digits.get(digit)

kanji_digits = {
    1:u"一",
    2:u"二",
    3:u"三",
    4:u"四",
    5:u"五",
    6:u"六",
    7:u"七",
    8:u"八",
    9:u"九",
    }

def number_pronunciation_parts(number):
    if number >= 1000000000000L:
        return None
    if number < 1:
        return u"０"
    parts = []
    while number:
        if number >= 100000000L:
            parts = parts + number_pronunciation_parts(number / 100000000L)
            parts.append(u"億")
            number = number % 100000000L
        elif number >= 10000L:
            parts = parts + number_pronunciation_parts(number / 10000L)
            parts.append(u"万")
            number = number % 10000L
        elif number >= 1000L:
            digit = number / 1000L
            if digit > 1:
                parts.append(kanji_digits[digit])
            parts.append(u"千")
            number = number % 1000L
        elif number >= 100L:
            digit = number / 100L
            if digit > 1:
                parts.append(kanji_digits[digit])
            parts.append(u"百")
            number = number % 100L
        elif number >= 10L:
            digit = number / 10L
            if digit > 1:
                parts.append(kanji_digits[digit])
            parts.append(u"十")
            number = number % 10L
        else:
            parts.append(kanji_digits[number])
            number = 0
    return parts

kanji_digits_pronunciation = {
    u"０":u"ぜろ",
    u"一":u"いち",
    u"二":u"に",
    u"三":u"さん",
    u"四":u"よん",
    u"五":u"ご",
    u"六":u"ろく",
    u"七":u"なな",
    u"八":u"はち",
    u"九":u"きゅう",
    u"十":u"じゅう",
    u"百":u"ひゃく",
    u"千":u"せん",
    u"万":u"まん",
    u"億":u"おく",
    }

kanji_digits_pronunciation_exceptions = {
    u"三百" : (u"さん", u"びゃく"),
    u"六百" : (u"ろっ", u"ぴゃく"),
    u"八百" : (u"はっ", u"ぴゃく"),
    u"三千" : (u"さん", u"ぜん"),
    u"八千" : (u"はっ", u"せん"),
    }

def pronounce_number(number, counterreadingdict):
    pronunciations = []
    lastkanji = None
    for kanji in reversed(number):
        if counterreadingdict and not pronunciations:
            pronunciation = counterreadingdict[kanji][0]
        elif lastkanji and kanji+lastkanji in kanji_digits_pronunciation_exceptions:
            (pronunciation, prevpronunciation) = kanji_digits_pronunciation_exceptions[kanji+lastkanji]
            pronunciations[0] = prevpronunciation
        else:
            pronunciation = kanji_digits_pronunciation[kanji]
        pronunciations.insert(0, pronunciation)
        lastkanji = kanji
    return pronunciations

plain_digits_string_re = re.compile("^[0-9]+$")

def is_plain_digits_string(s):
    return plain_digits_string_re.match(s)

def partitionlist(l, separator):
    if separator not in l:
        return (l, [], [])
    index = l.index(separator)
    return (l[:index], l[index], l[index+1:])

def digits_to_number(digits):
    (okuleft,oku,okuright) = partitionlist(digits, 100000000L)
    if oku:
        if okuleft:
            left = digits_to_number(okuleft)
        else:
            left = 1
        return left * 100000000L + digits_to_number(okuright)
    (manleft,man,manright) = partitionlist(digits, 10000L)
    if man:
        if manleft:
            left = digits_to_number(manleft)
        else:
            left = 1
        return left * 10000L + digits_to_number(manright)
    acc = 0
    value = 0
    for digit in digits:
        if digit < 10:
            value = value * 10 + digit
        else:
            if value:
                acc += value * digit
            else:
                acc += digit
            value = 0
    acc += value
    return acc

basic_exceptions = {
    u"は": {
        u"一": u"いっぱ",
        u"三": u"さんば",
        u"六": u"ろっぱ",
        u"八": u"はっぱ",
        u"十": u"じっぱ",
    },    
    u"た": {
        u"一": u"いった",
        u"八": u"はった",
        u"十": u"じった",
    },    
    u"さ": {
        u"一": u"いっさ",
        u"八": u"はっさ",
        u"十": u"じっさ",
    },    
    u"か": {
        u"一": u"いっか",
        u"六": u"ろっか",
        u"八": u"はっか",
        u"十": u"じっか",
    },
}

# $o = ordinal suffix
# $n = the number (automatically prepended if not present)
# | = separates irregular pluralization; first = 0, last = high numbers
# (s) = pluralization suffix, in this case "s"

counters = {
    u"円":(u"えん", [
        (u"四", u"よ", None),
        (u"九", u"く", None),
    ], u"yen"),
    u"本":(u"ほん", [
        (u"一", u"いっ", u"ぽん"),
        (u"三", None, u"ぼん"),
        (u"六", u"ろっ", u"ぽん"),
        (u"八", u"はっ", u"ぽん"),
        (u"十", u"じっ", u"ぽん"), #multiple pronunciations
    ]),
    u"冊":(u"さつ", []),
    u"枚":(u"まい", [(u"七", u"しち", None),]),
    u"杯":(u"はい", []),

    u"台":(u"だい", []),
    u"階":(u"かい", [(u"三", None, u"がい"),], u"$n$o floor"),
    u"個":(u"こ", [
        (u"一", u"いっ", None),
        (u"六", u"ろっ", None),
        (u"八", u"はっ", None),
        (u"十", u"じっ", None),
        ]),
    u"畳":(u"じょう", [], u"mat"),
    u"匹":(u"ひき", [
        (u"一", u"いっ", u"ぴき"),
        (u"三", None, u"びき"),
        (u"六", u"ろっ", u"ぴき"),
        (u"七", u"しち", None),
        (u"八", u"はっ", u"ぴき"),
        (u"十", u"じっ", u"ぴき"), #multiple pronunciations
        ]),
    u"羽":(u"わ", [(u"七", u"しち", None),]),
    u"頭":(u"とう", [
        (u"一", u"いっ", None),
        (u"八", u"はっ", None),
        (u"十", u"じっ", None),
        ]),
    u"人":(u"にん", [
        (u"一", u"ひと", u"り"),
        (u"二", u"ふた", u"り"),
        (u"四", u"よ", None),
        (u"七", u"しち", None),
        ], u"person(s)"),
    u"度":(u"ど", [(u"七", u"しち", None),], u"degrees|time/degree|times/degrees|times/degrees|degrees"),
    u"回":(u"かい", [(u"七", u"しち", None),], u"time(s)"),
    u"番":(u"ばん", [(u"九", u"く", None),], u"$n$o"),
    u"号":(u"ごう", [(u"七", u"しち", None),(u"九", u"く", None),], u"number $n"),
    u"秒":(u"びょう", [(u"九", u"く", None),], u"second(s)"),
    u"分":(u"ふん", [
        (u"一", u"いっ", u"ぷん"),
        (u"三", None, u"ぷん"),
        (u"四", None, u"ぶん"),
        (u"六", u"ろっ", u"ぷん"),
        (u"八", u"はっ", u"ぷん"),
        (u"十", u"じっ", u"ぷん"),
        ], u"minute(s)"),
    u"時":(u"じ", [(u"四", u"よ", None),(u"七", u"しち", None),(u"九", u"く", None),], u"o'clock"),
    u"時間":(u"じかん", [(u"四", u"よ", None),(u"七", u"しち", None),(u"九", u"く", None),], u"hour(s)"),
    u"週":(u"しゅう", [
        (u"一", u"いっ", None),
        (u"八", u"はっ", None),
        (u"十", u"じっ", None),
        ], u"week $n"),
    u"週間":(u"しゅうかん", [
        (u"一", u"いっ", None),
        (u"八", u"はっ", None),
        (u"十", u"じっ", None),
        ], u"$n week(s)"),
    u"年":(u"ねん", [(u"四", u"よ", None),(u"七", u"しち", None),(u"九", u"く", None),], u"year $n"),
    u"年度":(u"ねんど", [(u"四", u"よ", None),(u"七", u"しち", None),(u"九", u"く", None),], u"year $n"),
    u"歳":(u"さい", [], u"year(s) old"),
    u"丁目":(u"ちょうめ", [], u"block $n"),
    }

def ordinal_suffix(number):
    lastdigit = number % 10
    if number % 100 in range(11,20):
        return "th"
    elif lastdigit == 1:
        return "st"
    elif lastdigit == 2:
        return "nd"
    elif lastdigit == 3:
        return "rd"
    else:
        return "th"

paren_match_re = re.compile("\(([^)]+)\)")

def handle_plural_parens(rule, number):
    if u"|" in rule:
        rules = rule.split("|")
        if number > len(rules) - 2:
            return rules[-1]
        else:
            return rules[number]
    if number == 1:
        return paren_match_re.sub("", rule)
    else:
        return paren_match_re.sub(r'\1', rule)

def get_counter_meaning(rule, number):
    if not rule:
        return unicode(number)
    rule = handle_plural_parens(rule, number)
    if u"$n" not in rule:
        rule = u"%(n)d " + rule
    rule = rule.replace(u"$n", u"%(n)d")
    rule = rule.replace(u"$o", u"%(o)s")   
    return rule % {"n":number, "o":ordinal_suffix(number)}

def get_counter_reading(counter, default_counter_reading):
    if counter in counters:
        if len(counters[counter]) == 3:
            (reading, exceptions, meaning) = counters[counter]
        else:
            (reading, exceptions) = counters[counter]
            meaning = None
    else:
        reading = default_counter_reading
        exceptions = []
        meaning = None
        
    exceptiondict = {}
    for (digit, pronunciation) in kanji_digits_pronunciation.items():
        exceptiondict[digit] = (pronunciation, reading)
    if reading[0] in basic_exceptions:
        basic_exception = basic_exceptions[reading[0]]
        for (digit, pronunciation) in basic_exception.items():
            exceptiondict[digit] = (pronunciation[:-1], pronunciation[-1] + reading[1:])
    for (digit, digitpronunciation, counterpronuncation) in exceptions:
        exceptiondict[digit] = (digitpronunciation or kanji_digits_pronunciation[digit],
                                counterpronuncation or reading)
    return (exceptiondict, meaning)

def get_number_reading(surface, counter, default_counter_reading, counter_gloss):
    if surface == u"．" and not counter:
        return (u"てん", surface, u"point")
    digits = [normalize_digit(digit) for digit in surface]
    if None in digits:
        return (None, surface, surface)
    number = digits_to_number(digits)

    parts = number_pronunciation_parts(number)
    meaning = unicode(number)
    if not parts:
        return (None, surface, meaning)

    if counter:
        (counterreadingdict, counter_meaning_rule) = get_counter_reading(counter, default_counter_reading)
        if counter_meaning_rule:
            meaning = get_counter_meaning(counter_meaning_rule, number)
        elif counter_gloss:
            meaning = unicode(number) + u" " + counter_gloss[0]
        else:
            meaning = unicode(number)
        pronunciation = pronounce_number(parts, counterreadingdict)
        counterreading = counterreadingdict[parts[-1]][1]
    else:
        pronunciation = pronounce_number(parts, None)
    
    reading = "".join(pronunciation)
    if counter:
        reading = reading + u"\t" + counterreading
        surface = surface + u"\t" + counter
    return (reading, surface, meaning)

if __name__ == '__main__':
    testcases = [
        (u"１",u"いち",1),
        (u"２十１",u"にじゅういち",21),
        (u"３百２十１",u"さんびゃくにじゅういち",321),
        (u"４千３百２十１",u"よんせんさんびゃくにじゅういち",4321),
        (u"５万４千３百２十１",u"ごまんよんせんさんびゃくにじゅういち",54321),
        (u"６十５万４千３百２十１",u"ろくじゅうごまんよんせんさんびゃくにじゅういち",654321),
        (u"７百６十５万４千３百２十１",u"ななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",7654321),
        (u"８千７百６十５万４千３百２十１",u"はっせんななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",87654321),
        (u"９億８千７百６十５万４千３百２十１",u"きゅうおくはっせんななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",987654321),
        (u"一",u"いち",1),
        (u"二十一",u"にじゅういち",21),
        (u"三百二十一",u"さんびゃくにじゅういち",321),
        (u"四千三百二十一",u"よんせんさんびゃくにじゅういち",4321),
        (u"五万四千三百二十一",u"ごまんよんせんさんびゃくにじゅういち",54321),
        (u"六十五万四千三百二十一",u"ろくじゅうごまんよんせんさんびゃくにじゅういち",654321),
        (u"七百六十五万四千三百二十一",u"ななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",7654321),
        (u"八千七百六十五万四千三百二十一",u"はっせんななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",87654321),
        (u"九億八千七百六十五万四千三百二十一",u"きゅうおくはっせんななひゃくろくじゅうごまんよんせんさんびゃくにじゅういち",987654321),
        (u"９百万", u"きゅうひゃくまん", 9000000),
        (u"５百億３百２万３千",u"ごひゃくおくさんびゃくにまんさんぜん",50003023000),
        (u"４億２百",u"よんおくにひゃく",400000200),
        (u"千億",u"せんおく",100000000000),
        (u"百万",u"ひゃくまん",1000000),
        (u"千万",u"せんまん",10000000),
        (u"１０２３４",u"いちまんにひゃくさんじゅうよん",10234),
        (u"２４５６",u"にせんよんひゃくごじゅうろく",2456),
        (u"２３５９０７５８９２３",u"にひゃくさんじゅうごおくきゅうせんななじゅうごまんはっせんきゅうひゃくにじゅうさん",23590758923),
        (u"４４",u"よんじゅうよん",44),
        (u"１０",u"じゅう",10),
        (u"９",u"きゅう",9),
        (u"２３２",u"にひゃくさんじゅうに",232),
        (u"１００",u"ひゃく",100),
        (u"１３９",u"ひゃくさんじゅうきゅう",139),
        (u"１１１",u"ひゃくじゅういち",111),
        (u"百万",u"円",u"ひゃくまん\tえん",1000000),
        (u"四",u"円",u"よ\tえん",4),
        (u"九",u"円",u"く\tえん",9),
        (u"321",u"本",u"さんびゃくにじゅういっ\tぽん",321),
        (u"1",u"本",u"いっ\tぽん",1),
        (u"2",u"本",u"に\tほん",2),
        (u"1",u"冊",u"いっ\tさつ",1),
        (u"7",u"枚",u"しち\tまい",7),
        (u"一",u"杯",u"いっ\tぱい",1),
        (u"三",u"杯",u"さん\tばい",3),
        ]

    for testcase in testcases:
        if len(testcase) == 3:
            (surface, correct_reading, correct_number) = testcase
            counter = None
        else:
            (surface, counter, correct_reading, correct_number) = testcase
        (reading, newsurface, number) = get_number_reading(surface, counter, u"なになに")
        if reading != correct_reading:
            print newsurface.encode("utf8"),reading.encode("utf8"),"!=",correct_reading.encode("utf8")
        if number != unicode(correct_number):
            print newsurface.encode("utf8"),number.encode("utf8"),"!=",correct_number

    for counter in counters.keys():
        for digit in u"一二三四五六七八九十":
            (reading, newsurface, number) = get_number_reading(digit, counter, u"なになに")
            print reading.encode("utf8"), newsurface.encode("utf8"), number.encode("utf8")
        print
