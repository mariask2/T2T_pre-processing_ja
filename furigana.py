#!/usr/bin/python
# -*- coding: utf-8 -*-

from k2h import kata2hira, voice_first_char, maru_first_char, godan_dict2cont

def append_to_all_strings(strings, chars):
    result = set([])
    for s in strings:
        for c in chars:
            dotindex = c.find(".")
            if dotindex != -1:
                origc = c
                extrac = c[dotindex+1:dotindex+2]
                contextrac = godan_dict2cont(extrac)
                c = c[0:dotindex]
                extrastring = c+extrac
                extrastring = extrastring.replace("-", "")
                result.add(s+extrastring+".")
                if contextrac:
                    extrastring = c+contextrac
                    extrastring = extrastring.replace("-", "")
                    result.add(s+extrastring+".")
            c = c.replace("-", "")
            result.add(s+c+".")
    return result

specialkanji = {
    u"涔":(u"シン", u""),
    u"Ａ":(u"", u"えー"),
    u"Ｂ":(u"", u"びー"),
    u"Ｃ":(u"", u"しー"),
    u"Ｄ":(u"", u"でぃー"),
    u"Ｅ":(u"", u"いー"),
    u"Ｆ":(u"", u"えふ"),
    u"Ｇ":(u"", u"じー"),
    u"Ｈ":(u"", u"えっち"),
    u"Ｉ":(u"", u"あい"),
    u"Ｊ":(u"", u"じぇー"),
    u"Ｋ":(u"", u"けー"),
    u"Ｌ":(u"", u"える"),
    u"Ｍ":(u"", u"えむ"),
    u"Ｎ":(u"", u"えぬ"),
    u"Ｏ":(u"", u"おー"),
    u"Ｐ":(u"", u"ぴー"),
    u"Ｑ":(u"", u"きゅー"),
    u"Ｒ":(u"", u"あーる"),
    u"Ｓ":(u"", u"えす"),
    u"Ｔ":(u"", u"てぃー"),
    u"Ｕ":(u"", u"ゆー"),
    u"Ｖ":(u"", u"びー ぶい ゔい"),
    u"Ｗ":(u"", u"だぶりゅー　だぶる"),
    u"Ｘ":(u"", u"えっくす"),
    u"Ｙ":(u"", u"わい"),
    u"Ｚ":(u"", u"ぜっと"),
    u"１":(u"イチ", u""),
    u"３":(u"サン", u""),
    }

extrareadings = {
    u"日":u"に にっ",
    u"文":u"も",
    u"八":u"はっ",
    u"石":u"せっ",
    u"時":u"と",
    }

def prune_impossible(strings, reading):
    return [s for s in strings if reading.startswith(s.replace(".", ""))]

def generate_all_readings(cursor, writing, reading):
    result = set([""])
    previous = None
    history = []
    for c in writing:
        chars = set([])
        if c == u"々":
            if not previous:
                # Kanji repetition sign used, but the previous character was not a kanji
                return set([""])
            kanji = previous
        elif c in specialkanji:
            kanji = specialkanji[c]
        else:
            cursor.execute('select onyomi,kunyomi from kanji where kanji = ?', (c,))
            kanji = cursor.fetchone()
        previous = kanji
        if kanji:
            (onyomis, kunyomis) = kanji
            if onyomis:
                for onyomi in onyomis.split(" "):
                    onyomi = kata2hira(onyomi).replace("-", "")
                    chars.add(onyomi)
                    voiced = voice_first_char(onyomi)
                    if voiced:
                        chars.add(voiced)
                    maruchar = maru_first_char(onyomi)
                    if maruchar:
                        chars.add(maruchar)
                    if len(onyomi) > 1 and (onyomi.endswith(u"つ") or onyomi.endswith(u"く")):
                        chars.add(onyomi[0:-1] + u"っ")
            if kunyomis:
                for kunyomi in kunyomis.split(" "):
                    kunyomi = kunyomi.replace("-", "")
                    chars.add(kunyomi)
                    voiced = voice_first_char(kunyomi)
                    if voiced:
                        chars.add(voiced)
                    maruchar = maru_first_char(kunyomi)
                    if maruchar:
                        chars.add(maruchar)
        else:
            chars.add(kata2hira(c))
        if c in extrareadings:
            for extrareading in extrareadings[c].split(" "):
                chars.add(extrareading)
        lastresult = result
        result = append_to_all_strings(result, chars)
        history.append(result)
        result = prune_impossible(result, reading)
        if len(result) == 0:
            return set()
    
    return result

def fill_empty_forward(l):
    newl = []
    old = ''
    for e in l:
        if e:
            newl.append(e)
            old = e
        else:
            newl.append(old)
    return newl

special_words = [
    (u"為替", u"かわせ"),
    (u"相撲", u"すもう"),
    (u"時計", u"とけい"),
    (u"１０", u"じっ"),
    (u"眼鏡", u"めがね"),
    (u"田舎", u"いなか"),
    (u"切手", u"きって"),
    (u"部屋", u"へや"),
    (u"心地", u"ここち"),
    (u"勝手", u"かって"),
    (u"ＲＡＭ", u"らむ"),
    (u"風邪", u"かぜ"),
    (u"天皇", u"てんのう"),
    (u"大和", u"やまと"),
    (u"切符", u"きっぷ"),
    (u"取締", u"とりしまり"),
    (u"海老", u"えび"),
    (u"太刀", u"たち"),
    (u"気質", u"かたぎ"),
    (u"日和", u"ひより"),
    (u"可愛", u"かわい"),
    (u"下手", u"へた"),
    (u"蕎麦", u"そば"),
    (u"神楽", u"かぐら"),
    (u"今日", u"きょう"),
    (u"昨日", u"きのう"),
    (u"奈良", u"なら"),
]

special_words_and_voiced = special_words + [(w, voice_first_char(r)) for (w, r) in special_words if voice_first_char(r)]

def try_split_word(cursor, writing, reading):
    for (spec_writing, spec_reading) in special_words_and_voiced:
        (w1,w2,w3) = writing.partition(spec_writing)
        (r1,r2,r3) = reading.partition(spec_reading)
        if w2 and r2:
            part1 = [s for s in generate_all_readings(cursor, w1, r1) if s.replace(".", "") == r1]
            part2 = r2 + u"." + u"%." * (len(w2) - 1)
            part3 = [s for s in generate_all_readings(cursor, w3, r3) if s.replace(".", "") == r3]
            if part1 and part3:
                suggestions = []
                for e1 in part1:
                    for e3 in part3:
                        suggestions.append(e1+part2+e3)
                return suggestions
    return []

def compact_furigana(acc, val):
    (f, k) = val
    if f == "%":
        (prevf, prevk) = acc[-1]
        return acc[0:-1] + [(prevf, prevk + k)]
    if len(acc):
        (prevf, prevk) = acc[-1]
        if prevf == "" and f == "":
            return acc[0:-1] + [("", prevk + k)]
    return acc + [(f, k)]

def get_suggestions(cursor, writing, reading):
    all_readings = generate_all_readings(cursor, writing, reading)
    these_suggestions = [s for s in all_readings if s.replace(".", "") == reading]
    if not these_suggestions:
        these_suggestions = try_split_word(cursor, writing, reading)
    return these_suggestions

def suggestion_to_furigana(suggestion, writing):
    parts = suggestion.split(".")[0:-1]
    furigana = list(zip(parts, list(writing)))
    furigana = [(f if kata2hira(k) != f else "" ,k) for (f,k) in furigana]
    cfurigana = reduce(compact_furigana, furigana, [])
    if furigana != cfurigana:
        furigana = cfurigana
    return furigana

def deduce_furigana_known_reading(cursor, reading, writing):
    suggestions = get_suggestions(cursor, writing, reading)
    if len(suggestions) == 1:
        return suggestion_to_furigana(suggestions[0], writing)
    else:
        return [(reading, writing)]

def deduce_furigana(cursor, seq):
    cursor.execute('select reading from readings where seq = ?', (seq,))
    readings = [row[0] for row in cursor.fetchall()]
    cursor.execute('select misc from senses where seq = ?', (seq,))
    senses_misc = [row[0] for row in cursor.fetchall()]
    senses_misc = fill_empty_forward(senses_misc)
    senses_misc_uk = set(["word usually written using kana alone" in misc.split("\t") for misc in senses_misc])
    cursor.execute('select defining from definings where seq = ?', (seq,))
    (writing,) = cursor.fetchone()
    suggestions = []
    if senses_misc_uk == set([True]):
        return [(readings[0], writing)]
    for reading in readings:
        these_suggestions = get_suggestion(cursor, writing, reading)
        if these_suggestions:
            suggestions = these_suggestions
            break

    if len(suggestions) > 1:
        print seq, writing.encode("utf8"), ",".join(readings).encode("utf8"), "suggestions:", "\n".join(suggestions).encode("utf8")
        return [(readings[0], writing)]
    elif len(suggestions) == 0:
        print seq, writing.encode("utf8"), ",".join(readings).encode("utf8"), "no suggestions", senses_misc
        return [(readings[0], writing)]
    else:
        suggestion = suggestions[0]
        return suggestion_to_furigana(suggestion)
