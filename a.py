import requests.sessions
import re
import execjs

import argparse

class BaiDuFanYi():

    def __init__(self):
        self.homeUrl = "https://fanyi.baidu.com/"
        self.transUrl = "https://fanyi.baidu.com/v2transapi"
        self.headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        self.gtk = None
        self.token = None
        self.s = requests.Session()
        self.get_params()
        self.get_params()

    def get_sign(self, query_string):
        JS_CODE = """
        function a(r, o) {

        for (var t = 0; t < o.length - 2; t += 3) {

        var a = o.charAt(t + 2);

        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),

        a = "+" === o.charAt(t + 1) ? r >>> a: r << a,

        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a

        }

        return r

        }

        var C = null;

        var token = function(r, _gtk) {

        var o = r.length;

        o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));

        var t = void 0,

        t = null !== C ? C: (C = _gtk || "") || "";

        for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {

        var m = r.charCodeAt(g);

        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)

        }

        for (var S = h,

        u = "+-a^+6",

        l = "+-3^+b+-f",

        s = 0; s < d.length; s++) S += d[s],

        S = a(S, u);

        return S = a(S, l),

        S ^= i,

        0 > S && (S = (2147483647 & S) + 2147483648),

        S %= 1e6,

        S.toString() + "." + (S ^ h)

        }

        """

        return execjs.compile(JS_CODE).call('token', query_string, self.gtk)

    def get_params(self):
        r = self.s.get(self.homeUrl, headers=self.headers)
        self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        self.token = re.findall(r"token: '(.*?)',", r.text)[0]

    def translate(self, query_string):
        sign = self.get_sign(query_string)
        data = {
        'from': 'en',
        'to': 'zh',
        'query': query_string,
        'simple_means_flag': 3,
        'sign': sign,
        'token': self.token,
        }

        res = self.s.post(url=self.transUrl, data=data, headers=self.headers)
        # print(res.text)
        print(res.json()['dict_result']['simple_means'])
        return res.json()['trans_result']['data'][0]['dst']
def main():
    words = input("请输入原文: ")
    mydict = BaiDuFanYi()
    print(f"翻译结果是： {mydict.translate(words)}")    

if __name__ == '__main__':
    main()

