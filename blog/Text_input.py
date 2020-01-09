# coding: utf-8
import MeCab
import sys
import re
import csv
import unicodedata

class Text_check:

    def __init__(self, input_text):
        self.input_text = input_text

    def input_check1(self):
        text =self.input_text
        if not (text.endswith('。'+'\n') == True) or (text.endswith('。'+'\r\n') == True):
            text = text + "。"
            for i in text:
                let = unicodedata.east_asian_width(i)
                if let == 'H' or let == 'Na':
                    print("半角文字が含まれています。")
                    print("すべて全角で記入してください。")
                    break
        return text

def main():
    input_text=input("敬語に変換したい文章＞＞")
    Ti = Text_check(input_text) #文の整形
    input_text = Ti.input_check1()

    print(input_text)
if __name__ == '__main__':
    main()
    #input_text.encode('utf-8)
