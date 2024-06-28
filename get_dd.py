from undetected_playwright.sync_api import sync_playwright
import sys
import json
from time import sleep

def get_dd_cookie(url, proxy=None):
    browser = None
    used_user_agent = None
    datadome_cookie = None
    try:
        with sync_playwright() as p:
            args = ["--disable-blink-features=AutomationControlled"]
            
            if proxy:
                proxy_parts = proxy.split(':')
                if len(proxy_parts) == 4:
                    proxy_address = f"{proxy_parts[0]}:{proxy_parts[1]}"
                    proxy_username = proxy_parts[2]
                    proxy_password = proxy_parts[3]
                    context_options = {
                        'proxy': {
                            'server': f"http://{proxy_address}",
                            'username': proxy_username,
                            'password': proxy_password
                        }
                    }
                else:
                    raise ValueError("Proxy format should be 'ip:port:username:password'")
            else:
                context_options = {}
            # Specify the path to the Chromium executable
            browser = p.chromium.launch(args=args, headless=False, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
            context = browser.new_context(**context_options)
            page = context.new_page()
            used_user_agent = page.evaluate("navigator.userAgent")
            page.goto(url)
            cookies = context.cookies()
            datadome_cookie = next((cookie for cookie in cookies if cookie['name'] == 'datadome'), None)

            browser.close()
    except Exception as e:
        print(f"Error during Playwright execution: {e}", file=sys.stderr)
        if browser:
            try:
                browser.close()
            except Exception as e:
                print(f"Error while closing the browser: {e}", file=sys.stderr)

    result = {
        "code": 200,
        "cookie": datadome_cookie,
        "agent": used_user_agent,
        "url": url
    }

    formatted_result = json.dumps(result, indent=4)
    
    with open('response.txt', 'w') as file:
        file.write(formatted_result)
    
    print(formatted_result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python get_dd.py <url> [proxy]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    proxy = sys.argv[2] if len(sys.argv) > 2 else None
    get_dd_cookie(url, proxy)
