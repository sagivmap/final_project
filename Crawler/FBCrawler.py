from bs4 import BeautifulSoup
import requests

# log in page url
url = "https://m.facebook.com/login.php"
s = requests.session()

# log in data
post_data = {
    'email': 'yourEmail@gmail.com',
    'pass': 'yourPass',
}

r = s.post(url, data=post_data,  allow_redirects=False)

r = s.get('https://www.facebook.com/ENTER_REACHABLE_PATH_FROM_YOUR_ACCOUNT', cookies=r.cookies, allow_redirects=False)

# beautiful soup init
soup = BeautifulSoup(r.text)
# print what achieved
print (soup.prettify())