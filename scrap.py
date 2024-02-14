from bs4 import BeautifulSoup

import cloudscraper
import json, pandas


def open_url(url):
    with cloudscraper.create_scraper() as scraper:
        html = scraper.get(url).text
    return html

def parse_yt(html):
    soup = BeautifulSoup(html,"html.parser")
    parse_json = soup.find_all("script",{"type":"application/ld+json"})[1]
    parse_json = parse_json.text
    parse_json = json.loads(parse_json)
    embedUrl = parse_json["embedUrl"]
    return embedUrl

def main(url):
    result = dict()
    
    html = open_url(url)
    embedUrl = parse_yt(html)

    result["website_url"] = url
    result["youtube_video_url"] = embedUrl

    return result

def save_excel(list_of_dict):
    df = pandas.DataFrame(list_of_dict)
    df.to_excel("youtube_embed.xlsx",index=False)


if __name__=="__main__":
    list_urls = ["https://eightify.app/summary/personal-development-and-self-improvement/cultivating-intelligence-a-guide-by-italo-marsili",
           "https://eightify.app/summary/technology-and-gadgets/avoid-turning-off-your-firestick-every-night-here-s-why",
           "https://eightify.app/summary/fitness-and-nutrition/10-sugar-hacks-for-guilt-free-indulgence"]
    result = []    
    for url in list_urls:
        result.append(main(url))

    save_excel(result)
    
