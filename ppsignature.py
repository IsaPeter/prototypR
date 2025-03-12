import sys
from argparse import ArgumentParser
import requests
import re
import urllib3
urllib3.disable_warnings()

# Implemented from: https://blog.s1r1us.ninja/research/PP


gadget_db = [
   (r"(String\(\w+\)\.split\(\/&\|;\/\)\,\s*function\()","Purl (jQuery-URL-Parser) Prototype Pollution"),
   (r"(\/\(\[\^\\\[\\\]\]\+\)\|\(\\\[\\\]\)\/g\s*)","CanJS deparam Prototype Pollution"),
   (r"(\.substr\(0,\s*\w+\s*-\s*1\)\.match\(\/\(\[\^\\\]\\?\[\]\+\|\(\\B\)\(\?\=\\\]\)\)\/g\))","MooTools More Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(\/\\\.\(\.\+\)\?\/\)\[1\])","jquery.parseParams.js Prototype Pollution"),
   (r"(\$\.each\(\s*\w+\.replace\(\s*\/\\\+\/g\s*,\s*['\"] ['\"]\s*\)\.split\(\s*['\"]&['\"]\s*\))","jQuery BBQ (deparam) Prototype Pollution"),
   (r"(\s*\/\\\[\/\.test\(\s*\w+\[0\]\s*\)\s*&&\s*\/\\\]\$\/\.test\(\s*\w+\[\s*\w+\s*\]\s*\)\s*)","deparam Prototype Pollution"),
   (r"(['\"]\[\]['\"]\s*===\s*\w+\s*\?\s*\w+\.push\(\w+\)\s*:\s*\w+\[\w+\]\s*=\s*\w+)","deparam Prototype Pollution"),
   (r"((\w+)\s*=\s*decodeURIComponent[\w+;,\s\(\)\.\{=\[\]'\"-\/\?}]+\b(\w+)\s*=\s*\3\[\2\]\s*=\s*\3\[\2\]\s*\|\|\s*\{\})","backbone-query-parameters 2 Prototype Pollution"),
   (r"(\w+\s*=\s*\/\\\[\(\[\^\\\]\]\*\)\]\/g)","V4Fire Core Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(\/\\\&\(amp\\\;\)\?\/\))","jQuery Sparkle Prototype Pollution"),
   (r"(\/\^\(\[\^\[\]\+\??\)\(\\\[\.\*\\\]\)\?\$\/\.exec\(\s*\w+\s*\))","jQuery query-object Prototype Pollution"),
   (r"(\.match\(\/\(\^\[\^\[\]\+\)\(\\\[\.\*\\\]\$\)\?\/\))","queryToObject Prototype Pollution"),
   (r"(\?\s*decodeURIComponent\(\s*\w+\.substr\(\s*\w+\s*\+\s*1\)\)\s*:\s*['\"]['\"])","getJsonFromUrl Prototype Pollution"),
   (r"(\w+\.replace\(\s*['\"]\[\]['\"]\s*,\s*['\"]\[['\"]\.concat\()","Unknown lib_0 Prototype Pollution"),
   (r"(\w+\s*=\s*\/\(\\w\+\)\\\[\(\\d\+\)\\\]\/)","component/querystring Prototype Pollution"),
   (r"(\(\w+\s*=\s*\w+\.exec\(\w+\)\)\s*\?\s*\(\s*\w+\[\w+\[1\]\]\s*=\s*\w+\[\w+\[1\]\]\s*\|\|\s*\[\])","component/querystring #2 Prototype Pollution"),
   (r"(\/\(\.\*\)\\\[\(\[\^\\\]\]\*\)\\\]\$\/\.exec\(\w+\))","YUI 3 querystring-parse Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(\/\\\.\(\.\+\)\?\/\)\[1\])","jquery.parseParams.js Prototype Pollution"),
   (r"(\w+\s*=\s*\/\\\[\?\(\[\^\\\]\[\]\+\)\\\]\?\/g)","flow.js Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\(\w+\[1\]\.slice\(\w+\s*\+\s*1,\s*\w+\[1\]\.indexOf\(['\"]\]['\"],\s*\w+\)\)\))","wishpond decodeQueryString Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.slice\(0,\s*\w+\.indexOf\(['\"]\\x?0?0['\"]\)\))","PHP.js parse_str Prototype Pollution"),
   (r"(\"\[\]\"\s*===\s*\w+\.substring\(\w+\.length\s*-\s*2\)[\s\?\)\(]*(?:\w+\[)?\w+\s*=\s*\w+\.substring\(0,\s*\w+\.length\s*-\s*2\))","Unknown lib_1 Prototype Pollution"),
   (r"(\w+\.match\(\/\(\^\[\^\\\[\]\+\)\(\\\[\.\*\\\]\$\)\?\/\))","Unknown lib_2 Prototype Pollution"),
   (r"(\(\[\^\\\\\[\^\\\\\]\]\+\)\(\(\\\\\[\(\^\\\\\[\^\\\\\]\)\\\\\]\)\*\))","Unknown lib_3 Prototype Pollution"),
   (r"(['\"]-1['\"]\s*==\s*\w+\[1\]\.indexOf\(['\"]\[['\"]\))","inbound setUrlParams Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(['\"]\.['\"]\)\s*[;,]\s*\w+\s*=\s*\w+\.pop\(\)\s*[;,]\s*\w+\s*=\s*\w+\.reduce\()","Unknown lib_4 Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(\/\\\]\\\[\?\|\\\[\/\)[\w\s=\(\;\,<\-]*\w+\.indexOf\(['\"]\[['\"]\))","Old mithril.js Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.split\(['\"]\.['\"]\)[\s;,\w]+=\s*\w+\.pop\(\)[!\s;,\w]+\(\w+\.length\))","builder.io QueryString.deepen Prototype Pollution"),
   (r"(\w+\s*=\s*\w+\.indexOf\(['\"]\]['\"],\s*\w+\)[\s\w;,]+=\s*decodeURIComponent\(\w+\.substring\(\w+\s*\+\s*1)","Unknown lib_5 Prototype Pollution"),
   (r"(\w+\.replace\(['\"]\]['\"],\s*['\"]['\"]\)[\w\s;,\(]+\.search\(\/\[\\\.\\\[\]\/\))","arg.js Prototype Pollution"),
   (r"(\/\^\(\[\$a-zA-z_\]\[\$a-zA-z0-9\]\*\)\\\[\(\[\$a-zA-z0-9\]\*\)\\\]\$\/)","R.js Prototype Pollution"),
   (r"(\/\^\(\\w\+\)\\\[\(\\w\+\)\?\\\]\(\\\[\\\]\)\?\/)","davis.js Prototype Pollution"),
   (r"(\.match\(\/\^\[\\\[\\\]\]\*\(\[\^\\\[\\\]\]\+\)\\\]\*\(\.\*\)\/\))","SoundCloud SDK decodeParams Prototype Pollution"),
   (r"((\w+)\s*=\s*\w+\.split\(['\"]\.['\"]\)[\w+;,\s\(\)\.\{=\[\]'\"<]+\b(\w+)\s*=\s*\2\[\w+\][\w+;,\s\(\)\.\{=\[\]'\"<\-!\|&]+(\w+)\[\3\]\s*=\s*\{\}[\w+;,\s\(\)\.\{=\[\]'\"<\-!\|&]+\b\4\s*=\s*\4\[\3\])","Unknown lib_7 Prototype Pollution"),
]








def read_file_data(path):
    with open(path) as f:
        data = f.read()
    return data

def download_file(url):
    resp = requests.get(url, verify=False, allow_redirects=True)
    return resp.text
    
def read_url_list(path):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def analyze_js(js_data):
    for regex,name in gadget_db:
        match =  re.findall(regex,js_data, re.I|re.M)
        if match:
            print(f"[*] Potentially Vulnerable JS found! ({name})")

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-f","--file", dest="file", metavar="", help="File to be analyze")
    parser.add_argument("-u", "--url", dest="url", metavar="", help="Set URL to be analyze")
    parser.add_argument("-ul", "--url-list", dest="url_list", metavar="", help="Set URL list")
    parser.add_argument("--stdin", dest="stdin", action="store_true", help="Set input from stdin")

    return parser.parse_args()
def main():
    args = parse_arguments()

    if args.file:
        file_data = read_file_data(args.file)
        analyze_js(file_data)

    if args.url:
        js_file = download_file(args.url)
        analyze_js(js_file)

    if args.url_list:
        url_list = read_url_list(args.url_list)
        for url in url_list:
            js_file = download_file(url)
            analyze_js(js_file)


    if args.stdin:
        for line in sys.stdin.buffer:
            try:
                decoded_line = line.decode("utf-8") 
            except UnicodeDecodeError:
                decoded_line = line.decode("latin-1", errors="replace") 
            print(decoded_line)
            js_data = download_file(decoded_line)
            print(js_data)
            if js_data:
                analyze_js(js_data)



if __name__ == '__main__':
    main()