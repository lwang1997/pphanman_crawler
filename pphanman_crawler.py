#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2021-06-15 22:41
import requests
import os
from bs4 import BeautifulSoup

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}


def full_url(url):
    return "https://pphanman.com/" + url


def get_ascension():
    url = "https://pphanman.com/custom/ascension"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, features="lxml")
    comics = soup.select(".rank-item")
    return {
        comic.select(".comic-name")[0].string: full_url(comic.a.attrs.get("href"))
        for comic in comics
    }


def get_chapters(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, features="lxml")
    chapters = soup.select(".chapter-item")
    return {c.a.string: full_url(c.a.attrs.get("href")) for c in chapters}


def download_chapter(comic_name, chapter_name, chapter_url):
    mark = os.path.join(top_dir, comic_name, chapter_name, "mark")

    def is_chapter_completed():
        chapter_dir = os.path.join(top_dir, comic_name, chapter_name)
        if not os.path.exists(chapter_dir):
            os.mkdir(chapter_dir)
            open(mark, "w")
            return False
        return not os.path.exists(mark)

    if is_chapter_completed():
        return

    print("  chapter: " + chapter_name)
    try:
        response = requests.get(chapter_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="lxml")
        images = soup.select(".comic-page")
        images = {
            image.img.attrs.get("alt"): image.img.attrs.get("src") for image in images
        }
        for alt, src in images.items():
            print("    " + alt)
            img = requests.get(src, headers=HEADERS)
            with open(os.path.join(top_dir, comic_name, chapter_name, alt), "wb") as f:
                f.write(img.content)
        os.remove(mark)
    except Exception as e:
        print(e)


def download(comic_name, comic_url):
    print("comic: " + comic_name)
    comic_dir = os.path.join(top_dir, comic_name)
    os.path.exists(comic_dir) or os.mkdir(comic_dir)
    chapters = get_chapters(comic_url)
    for chapter_name, chapter_url in chapters.items():
        download_chapter(comic_name, chapter_name, chapter_url)


if __name__ == "__main__":
    comics = get_ascension()
    top_dir = os.getcwd()
    for comic_name, comic_url in comics.items():
        download(comic_name, comic_url)
