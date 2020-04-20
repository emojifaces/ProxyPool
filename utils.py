import requests

def get_page(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    response = requests.get(url,headers=header)
    response.encoding = response.apparent_encoding
    return response.text

if __name__ == '__main__':
    result = get_page('http://www.66ip.cn/')
    print(result)