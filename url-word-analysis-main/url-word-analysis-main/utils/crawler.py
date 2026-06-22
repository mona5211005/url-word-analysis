import requests
from bs4 import BeautifulSoup
import re
from .config import DEFAULT_HEADERS

def fetch_text_from_url(url: str) -> str:
    try:
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=30,
            verify=False,
            allow_redirects=True
        )

        if response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding or 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        text = '\n'.join([p.get_text(strip=True) for p in soup.find_all('p')])
        if not text:
            text = soup.get_text(strip=True)

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)
        return text.strip()

    except requests.exceptions.Timeout:
        raise Exception(f"请求超时：URL访问时间超过30秒")
    except requests.exceptions.ConnectionError:
        raise Exception(f"连接错误：无法连接到目标服务器")
    except requests.exceptions.SSLError:
        raise Exception(f"SSL错误：建议使用HTTP协议URL")
    except Exception as e:
        raise Exception(f"抓取失败：{str(e)}")