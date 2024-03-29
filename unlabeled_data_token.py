import argparse
from nltk.tokenize import word_tokenize
import re 
import unidecode

def tokenize(inputFile, outputFile, max_word, max_char):
    with open(outputFile, mode='w', encoding='utf8') as out_f:
        input_f = open(inputFile, mode='r', encoding='utf8')
        for text in input_f.readlines():
            text = text.strip()
            text = re.sub(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', "url", text)
            text = text.strip("\n\r    \xa0")
            text = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+' , '', text)
            text = unidecode.unidecode(text) ## convert accented text to unaccented text

            if text == "": continue
            words = word_tokenize(text)
            if len(words) > max_word: continue

            too_long_char = False
            for word in words:
                char_len = len(word)
                if char_len > max_char:
                    too_long_char = True
                    break
            if too_long_char: continue

            for word in words:
                line = word + '\t' + "o" + '\n'
                out_f.write(line)
            out_f.write('\n')
            out_f.flush()
        input_f.close()
    return 

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--unlabeled_file', default='sample.lap')
    argparser.add_argument('--max_word', default=50, type=int, help='max word num')
    argparser.add_argument('--max_char', default=15, type=int, help='max char num')

    args, extra_args = argparser.parse_known_args()
    tokenize(args.unlabeled_file, args.unlabeled_file + ".tok", args.max_word, args.max_char)
    print("OK")