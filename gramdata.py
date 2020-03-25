# -*- coding: utf-8 -*-

special_conjforms = [u"サ変・スル"]
special_words = set([1296400])
special_meanings = {
    (u"いる", (u"動詞",u"非自立",u"*",u"*",u"一段")):[],
    (u"れる", (u"動詞",u"接尾",u"*",u"*",u"一段")):["passive"],
    }

verb_connections = {
    (u'動詞', u'未然形', u'ない', (u'助動詞', u'*', u'*', u'*', u'特殊・ナイ')) : u"negation",
    (u'動詞', u'未然形', u'ぬ', (u'助動詞', u'*', u'*', u'*', u'特殊・ヌ')) : u"negation",
    (u'動詞', u'連用タ接続', u'た', (u'助動詞', u'*', u'*', u'*', u'特殊・タ')) : u"past tense",
    (u'動詞', u'連用形', u'た', (u'助動詞', u'*', u'*', u'*', u'特殊・タ')) : u"past tense",
    (u'動詞', u'連用形', u'て', (u'助詞', u'接続助詞', u'*', u'*', u'*')) : u"て",
    (u'動詞', u'連用タ接続', u'て', (u'助詞', u'接続助詞', u'*', u'*', u'*')) : u"て",
    (u'動詞', u'連用形', u'、', (u'記号', u'読点', u'*', u'*', u'*')) : u"phrase end",
    (u'動詞', u'未然形', u'れる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"passive/potential",
    (u'動詞', u'未然形', u'られる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"passive/potential",
    (u'動詞', u'未然レル接続', u'れる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"passive/potential",

    (u'動詞', u'未然形', u'せる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"causative",
    (u'動詞', u'未然形', u'させる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"causative",
    (u'動詞', u'未然レル接続', u'せる', (u'動詞', u'接尾', u'*', u'*', u'一段')) : u"causative",

    (u'助詞', u'て', u'いる', (u'動詞', u'非自立', u'*', u'*', u'一段')) : u"progressive/resultant state",
    (u'助詞', u'て', u'くる', (u'動詞', u'非自立', u'*', u'*', u'カ変・クル')) : u"くる",
    (u'助詞', u'て', u'から', (u'助詞', u'格助詞', u'一般', u'*', u'*')) : u"after",

    (u'形容詞', u'ガル接続', u'さ', (u'名詞', u'接尾', u'特殊', u'*', u'*')) : u"concrete nominalization",
    (u'形容詞', u'連用テ接続', u'て', (u'助詞', u'接続助詞', u'*', u'*', u'*')) : u"て",


    (u'動詞', u'連用形', u'ます', (u'助動詞', u'*', u'*', u'*', u'特殊・マス')) : u"politeness",
    (u'助動詞', u'連用形', u'た', (u'助動詞', u'*', u'*', u'*', u'特殊・タ')) : u"past tense",
    (u'動詞', u'連用形', u'たい', (u'助動詞', u'*', u'*', u'*', u'特殊・タイ')) : u"desire",
    (u'動詞', u'連用タ接続', u'で', (u'助詞', u'接続助詞', u'*', u'*', u'*')) : u"て",
    (u'助動詞', u'連用テ接続', u'ない', (u'助動詞', u'*', u'*', u'*', u'特殊・ナイ')) : u"negation",
    (u'助動詞', u'未然形', u'ん', (u'助動詞', u'*', u'*', u'*', u'不変化型')) : u"negation",
    (u'助動詞', u'連用タ接続', u'た', (u'助動詞', u'*', u'*', u'*', u'特殊・タ')) : u"past tense",

    (u'動詞', u'連用形', u'に', (u'助詞', u'格助詞', u'一般', u'*', u'*')) : u"purpose",
    (u'助動詞', u'仮定形', u'ば', (u'助詞', u'接続助詞', u'*', u'*', u'*')) : u"hypothetical conditional",
    (u'助詞', u'て', u'くれる', (u'動詞', u'非自立', u'*', u'*', u'一段・クレル')) : u"for the benefit of me",
    (u'助詞', u'*', u'なる', (u'動詞', u'非自立', u'*', u'*', u'五段・ラ行')) : u"become",
    }