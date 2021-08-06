from .BaiDuFanYi import BaiDuFanYi
import argparse
import pprint


def parse_args():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add an argument
    # parser.add_argument('--word', type=bool, default=)
    # parser.add_argument('--word', type=str, required=True)
    parser.add_argument('word', type=str)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--en', action='store_true')
    group.add_argument('-z', '--zh', action='store_true')
    
    # Parse the argument
    args = parser.parse_args()
    return args

def cli():
    args = parse_args()
    f = 'en'
    t = 'zh'
    if args.zh:
        f, t = t, f

    # print(args.word)
    words = args.word
    mydict = BaiDuFanYi()
    res = mydict.translate(words, f, t)
    # pprint.pprint(res.json()['dict_result']['simple_means'])
    # print(res.json()['trans_result']['data'][0]['dst'])
    pprint.pprint(res.json()['dict_result']['simple_means']['symbols'])

if __name__ == '__main__':
    cli()