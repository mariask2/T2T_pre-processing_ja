# -*- coding: utf-8 -*-

import string

kata = u'アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヲンッャュョァィゥェォヴ'
hira = u'あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをんっゃゅょぁぃぅぇぉゔ'
trans = dict((ord(c1), ord(c2)) for c1,c2 in zip(kata,hira))

unvoiced = u'かきくけこさしすせそたちつてとはひふへほ'
voiced =   u'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
voicetrans = dict((ord(c1), ord(c2)) for c1,c2 in zip(unvoiced,voiced))

notmaru = u'はひふへほ'
maru    = u'ぱぴぷぺぽ'
marutrans = dict((ord(c1), ord(c2)) for c1,c2 in zip(notmaru,maru))

godanverbdict = u'うくぐすつぬぶむる'
godanverbcont = u'いきぎしちにびみり'
godantranscont = dict((ord(c1), ord(c2)) for c1,c2 in zip(godanverbdict,godanverbcont))

def kata2hira(s):
    return s.translate(trans)

def voice_first_char(s):
    first = s[0]
    if not first in unvoiced:
        return None
    return first.translate(voicetrans) + s[1:]

def maru_first_char(s):
    first = s[0]
    if not first in notmaru:
        return None
    return first.translate(marutrans) + s[1:]

def godan_dict2cont(s):
    if not s in godanverbdict:
        return None
    return s.translate(godantranscont)

def iskana(c):
    return (c in kata) or (c in hira)
