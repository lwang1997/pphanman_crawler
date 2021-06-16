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
    comics = {
        comic.select(".comic-name")[0].string: full_url(comic.a.attrs.get("href"))
        for comic in comics
    }
    return comics


def get_chapters(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, features="lxml")
    chapters = soup.select(".chapter-item")
    chapters = {c.a.string: full_url(c.a.attrs.get("href")) for c in chapters}
    return chapters


def download_chapter(name, url):
    def is_chapter_completed():
        mark = name + "/mark"
        if not os.path.exists(name):
            os.mkdir(name)
            open(mark, "w")
            return False
        return not os.path.exists(mark)

    if is_chapter_completed():
        return

    os.chdir(name)

    print("  chapter: " + name)
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="lxml")
        images = soup.select(".comic-page")
        images = {
            image.img.attrs.get("alt"): image.img.attrs.get("src") for image in images
        }
        for alt, src in images.items():
            print("    " + alt)
            img = requests.get(src, headers=HEADERS)
            with open(alt, "wb") as f:
                f.write(img.content)
        os.remove("mark")
    except Exception as e:
        print(e)

    os.chdir("..")


def download(name, url):
    print("comic: " + name)
    if not os.path.exists(name):
        os.mkdir(name)
    chapters = get_chapters(url)
    os.chdir(name)
    for cname, curl in chapters.items():
        download_chapter(cname, curl)


if __name__ == "__main__":
    comics = get_ascension()
    for name, url in comics.items():
        download(name, url)
