import requests
from bs4 import BeautifulSoup as bs
import PyPDF2
import re

def extract_links(URLs):
    session = requests.Session()
    session.headers['User-Agent']
    my_headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    extracted_content = []
    for url in URLs:
        try:
            if(url.endswith('.pdf')):
                extracted_content.append(scrape_pdf(url))
                continue
            result = session.get(url, headers=my_headers, verify=False, timeout=3)
            doc = bs(result.content, "html.parser")
            contents = doc.find_all("p")
            for content in contents:
                extracted_content.append(content.text)
        except:
            pass
    return extracted_content # list of strings

def scrape_pdf(url):
    session = requests.Session()
    my_headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36",
        "Accept": "application/pdf"
    }
    result = session.get(url, headers=my_headers, verify=False, timeout=3)
    with open("./temp.pdf", "wb") as f:
        f.write(result.content)
    extracted_texts = []
    with open("./temp.pdf", "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted_texts.append(page.extract_text())
    extracted_text = " ".join(extracted_texts)
    return extracted_text # string

if __name__ == "__main__":
    import ast
    query = "['https://arxiv.org/pdf/2303.00747.pdf']"
    param = ast.literal_eval(query)
    response = extract_links(param)
    print("Extracted content:\n", response)