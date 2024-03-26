import os
import csv
import httpx
from dataclasses import asdict, fields
from selectolax.parser import HTMLParser
from headlineGenerator.logging import logger
from headlineGenerator.entity import Content, DataScraperConfig


def get_html(url, **kwargs):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}
    timeout = httpx.Timeout(connect=None, read=None, write=5, pool=5)
    # page keyword is used for getting news from a specific page
    if kwargs.get("page"):
        resp = httpx.get(url + f"page/{kwargs.get('page')}/", headers=headers, timeout=timeout, follow_redirects=True)
    else:
        resp = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)

    html = HTMLParser(resp.text)
    # handle when page number is exceeded
    if html.css_first("title").text() == "Page not found | AIT LIVE":
        logger.info(f"No results found while requesting URL {resp.url}. Page Limit Exceeded")
        return False

    return html


def extract_text(html, selector):
    try:
        return html.css_first(selector).text(strip=True)
    except AttributeError:
        return None
    except Exception as e:
        raise e


def extract_attribute(html, selector, attribute):
    try:
        return html.css_first(selector).attributes[attribute]
    except AttributeError:
        return None
    except Exception as e:
        raise e


def get_page_url(html: HTMLParser):
    blog_contents = html.css("div.blog-content div.block-inner div[data-pid]")

    for content in blog_contents:
        yield content.css_first("h4.entry-title a").attributes["href"]


def get_page_content(html: HTMLParser, url: str):
    content = Content(
        headline=extract_text(html, "h1.s-title"),
        last_update=extract_attribute(html, "time.updated-date", "datetime"),
        writer=extract_text(html, "span.meta-el.meta-custom.meta-bold"),
        editor=extract_text(html, "div[itemprop=articleBody] p:nth-last-of-type(2) strong"),
        summary=extract_text(html, "div[itemprop=articleBody] p strong"),
        main_story=" ".join(
            [node.text() for node in html.css("div[itemprop=articleBody] p:not(:has(strong))")]).strip(),
        page_url=url
    )

    return asdict(content)


def export_to_csv(contents: list, path: str):
    field_names = [field.name for field in fields(Content)]
    with open(path, "w") as file:
        writer = csv.DictWriter(file, field_names)
        writer.writeheader()
        writer.writerows(contents)


class DataScraper:
    def __init__(self, config: DataScraperConfig):
        self.config = config

    def scrape_data(self):
        for category in self.config.categories:
            contents = []
            data_count = 1

            logger.info(f"'>>> {category.upper()} CATEGORY'")

            for i in range(1, self.config.max_pages):
                logger.info(f"Scraping page {i}/{self.config.max_pages}")
                url = self.config.source_url + category + "/"
                html = get_html(url, page=i)
                if html is False:
                    break
                content_urls = get_page_url(html)

                for content_url in content_urls:
                    content_html = get_html(content_url)
                    logger.info(f"#{data_count} ==> {content_html.css_first('title').text()}")
                    content = get_page_content(content_html, content_url)
                    contents.append(content)
                    data_count += 1
                    logger.info("-" * 200)

            save_path = os.path.join(self.config.save_dir, f"{category}_contents.csv")
            export_to_csv(contents, save_path)
            logger.info(f"{category.upper()} CONTENTS SAVED TO CSV SUCCESSFULLY.")
