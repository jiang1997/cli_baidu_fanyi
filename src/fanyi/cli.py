from fanyi.BaiDuFanYi import BaiDuFanYi
import argparse
import pprint

def IsChinese(str):
    for ch in str:
        if '\u4e00' <= ch <= '\u9fa5':
            return True
    return False

def CustomPrint(tmp, src, prefix=''):
    if 'attrs' not in tmp:
        if not tmp['IsList']:
            src = [src]
        for i in src:
            if 'title' in tmp:
                prefix += ' '
                print(tmp['title'])

            print(f'{prefix}{i}')
    else:    
        # prefix = prefix + ' '
        items = src
        if not tmp['IsList']:
            items = [src]            
        for i in items:
            for cur_attr in tmp['attrs']:
                cur_tmp = tmp['template'][cur_attr]
                # print(i)
                if cur_attr in i:
                    CustomPrint(cur_tmp, i[cur_attr], prefix)
        # print('\n')


def parse_args():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add an argument
    # parser.add_argument('--word', type=bool, default=)
    # parser.add_argument('--word', type=str, required=True)
    parser.add_argument('word', type=str)

    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-e', '--en', action='store_true')
    # group.add_argument('-z', '--zh', action='store_true')
    
    # Parse the argument
    args = parser.parse_args()
    return args

def cli():
    args = parse_args()
    f = 'en'
    t = 'zh'
    if IsChinese(args.word):
        f, t = t, f

    words = args.word
    mydict = BaiDuFanYi()
    res = mydict.translate(words, f, t)
    # pprint.pprint(res.json()['dict_result']['simple_means'])
    # print(res.json()['trans_result']['data'][0]['dst'])
    # pprint.pprint(res.json()['dict_result']['simple_means']['symbols'])
    
    if 'dict_result' not in res.json():
        print('nothing found!')
        return

    parts_meansTmp = {'name': 'parts-means', 'IsList': False}
    parts_partTmp = {'name': 'parts-part', 'IsList': False}
    partsTmp = {'name': 'parts', 'IsList': True, 'attrs': ['part', 'means'], 'template': {'means': parts_meansTmp, 'part': parts_partTmp}}

    ph_amTmp = {'name': 'am', 'IsList': False, 'title': 'am'}
    ph_enTmp = {'name': 'en', 'IsList': False, 'title': 'en'}

    symbolTmp = {'name': 'symbol', 'IsList': False, 'attrs': ['parts', 'ph_am', 'ph_en'], 'template': {'ph_am': ph_amTmp, 'ph_en': ph_enTmp, 'parts': partsTmp}}

    # pprint.pprint(res.json()['dict_result']['simple_means']['symbols'])

    # CustomPrint(partsTmp, res.json()['dict_result']['simple_means']['symbols'][0]['parts'])
    CustomPrint(symbolTmp, res.json()['dict_result']['simple_means']['symbols'][0])


    

if __name__ == '__main__':
    cli()
