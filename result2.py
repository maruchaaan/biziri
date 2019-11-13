from natto import MeCab
import sys

mc = MeCab()
 
text = "アルバイト・パート本社は明治４２年創業、大阪中央郵便局内に職員食堂として開業。以後順調に業績を延ばし、全国２０ケ所に営業所を開設している。"
 
print(mc.parse(text))

