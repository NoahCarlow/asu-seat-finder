import requests
import random
from bs4 import BeautifulSoup as bs

def proxy_generator():
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies

def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}
    return session

if __name__ == "__main__":
    proxies = proxy_generator()

    for i in range(50):
        s = get_session(proxies)
        try:
            print("Request page with IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
            print(s)
            break
        except Exception as e:
            continue