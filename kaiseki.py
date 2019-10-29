# coding: utf-8
import sys
import MeCab

m = MeCab.Tagger ("-Ochasen")
x=m.parse ("北斗の拳の作者は誰ですか")
print(x)

