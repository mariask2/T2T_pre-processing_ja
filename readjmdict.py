#!/usr/bin/python

from xml.etree.ElementTree import ElementTree
import sqlite3
import sys
from k2h import kata2hira

conn = sqlite3.connect("lib/JMDict.sqlite")

c = conn.cursor()
c.execute("create table definings (seq integer, defining text, truekanji integer, notes text, freq text)")
c.execute("create table readings (seq integer, reading text, freq text, restr text)")
c.execute("create table senses (seq integer, pos text, misc text, gloss text, lang text)")

c.execute("create index senseseq on senses (seq)")
c.execute("create index reading on readings (reading)")
c.execute("create index readingseq on readings (seq)")
c.execute("create index defining on definings (defining)")
c.execute("create index definingseq on definings (seq)")
c.execute("create index glosses on senses(gloss)")

tree = ElementTree()
jmdict = tree.parse(sys.argv[1])

entries = jmdict.getiterator("entry")
nentries = 0
for entry in entries:
    nentries += 1
    if nentries % 10000 == 0:
        print nentries
    seq = entry.find("ent_seq").text
    writings = list(entry.getiterator("k_ele"))
    readings = list(entry.getiterator("r_ele"))
    senses = list(entry.getiterator("sense"))
    for writing in writings:
        kebs = list(writing.getiterator("keb"))
        ke_inf = [p.text for p in list(writing.getiterator("ke_inf"))]
        ke_pri = [p.text for p in list(writing.getiterator("ke_pri"))]
        for keb in kebs:
            c.execute("insert into definings (seq, defining, truekanji, notes, freq) values (?, ?, ?, ?, ?)", (seq, keb.text, 1, "\t".join(ke_inf), "\t".join(ke_pri)))
    for reading in readings:
        rebs = list(reading.getiterator("reb"))
        if len(rebs) != 1:
            print seq, len(rebs)
        re_pri = [p.text for p in list(reading.getiterator("re_pri"))]
        re_restr = [p.text for p in list(reading.getiterator("re_restr"))]
        reb = rebs[0]
        if not writings:
            re_restr = [reb.text]
        c.execute("insert into readings (seq, reading, freq, restr) values (?, ?, ?, ?)", (seq, kata2hira(reb.text), "\t".join(re_pri), "\t".join(re_restr)))
        if not writings:
            c.execute("insert into definings (seq, defining, truekanji, freq) values (?, ?, ?, ?)", (seq, reb.text, 0, "\t".join(re_pri)))
    for sense in senses:
        pos = [p.text for p in list(sense.getiterator("pos"))]
        misc = [p.text for p in list(sense.getiterator("misc"))]
        glosses = [gloss.text for gloss in list(sense.getiterator("gloss")) if gloss.get("{http://www.w3.org/XML/1998/namespace}lang", default="eng") == "eng"]
        if glosses:
            c.execute("insert into senses (seq, pos, misc, gloss, lang) values (?, ?, ?, ?, ?)", (seq, "\t".join(pos), "\t".join(misc), "\t".join(glosses), "eng"))
            pos = []
            misc = []
    conn.commit()
