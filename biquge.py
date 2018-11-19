import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import time

baseUrl = 'http://www.xbiquge.la/'
novelSearchUrl = baseUrl + 'xiaoshuodaquan/'
deleteString = '亲,点击进去,给个好评呗,分数越高更新越快,据说给新笔趣阁打满分的最后都找到了漂亮的老婆哦!' \
               '手机站全新改版升级地址：http://m.xbiquge.la，数据和书签与电脑站同步，无广告清新阅读！'
replceString = '    '
charSet = 'utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
}


def search_novel(novelName):
    searchResponse = requests.get(novelSearchUrl, headers=headers)
    searchResponse.encoding = charSet
    novelLists = {}
    searchSoup = BeautifulSoup(searchResponse.text, 'lxml')
    for novelList in searchSoup.select('.novellist li a'):
        novelLists.setdefault(novelList.text, novelList.attrs['href'])
    # print(novelLists)
    return detail_novel(novelName, novelLists.get(novelName, "无"))


def download_novel(novelName, detailUrls, chapters, method):
    if not os.path.exists(novelName):
        os.mkdir(novelName)
        print('创建文件夹 %s' % novelName)
    else:
        print('文件夹 %s 已存在' % novelName)
    print('文件夹路径为 %s' % os.getcwd() + "\\" + novelName)
    s = requests.session()
    for index, detailUrl in enumerate(detailUrls):
        chapterResponse = s.get(detailUrl, headers=headers)
        chapterResponse.encoding = charSet
        chapterSoup = BeautifulSoup(chapterResponse.text, 'lxml')
        chapter = re.sub(deleteString, "", chapterSoup.select('#content')[0].text)
        chapter = re.sub(replceString, "    \r\n", chapter)
        if method == '1':
            with open(novelName + "\\" + chapters[index] + ".txt", 'w+', encoding='utf-8') as f:
                f.write(chapter)
        elif method == '2':
            with open(novelName + "\\" + novelName + ".txt", 'a+', encoding='utf-8') as f:
                f.write(chapters[index] + '\n')
                f.write(chapter + 3 * '\n')
        show_progress(index + 1, len(detailUrls))


def show_progress(index, total):
    sys.stdout.write('\r')
    sys.stdout.write("%.2f%% |%s" % (float(index / total) * 100, (int(float(index / total) * 20)) * '#'))
    sys.stdout.flush()
    if index == total:
        print('\n' + 'finish!')
    if (index % 100) == 0:
        time.sleep(3)


def detail_novel(novelName, detailUrl):
    if detailUrl == '无':
        print('找不到小说: %s' % novelName)
        sys.exit(0)
    else:
        downloadOrNot = input('已找到小说: %s ,是否开始下载？输入是(下载)  其他(结束) ： \n' % novelName)
        if downloadOrNot == '是':
            method = input('选择分章节下载(输入 1),或整本下载(输入 2) 其他(结束)  \n')
            detailResponse = requests.get(detailUrl, headers=headers)
            detailResponse.encoding = charSet
            detailSoup = BeautifulSoup(detailResponse.text, 'lxml')
            chapterContent = detailSoup.find_all(name='dl')[0]
            detailUrls = []
            chapters = []
            content1 = re.compile('<dd><a href="(.*?)">(.*?)</a></dd>')
            results = re.findall(content1, str(chapterContent))
            for result in results:
                detailUrls.append(baseUrl + result[0])
                chapters.append(result[1])
            download_novel(novelName, detailUrls, chapters, method)
        else:
            sys.exit(0)


# html = requests.get(url, headers=headers)
# html.encoding = 'utf-8'
# detailUrls = []
# chapters = []
# soup = BeautifulSoup(html.text, 'lxml')
# dl = soup.find_all(name='dl')[0]
# name = soup.find(name="h1").text
# if not os.path.exists(name):
#     os.mkdir(name)
#     print('创建文件夹 %s' % name)
# else:
#     print('文件夹 %s 已存在' % name)
# content1 = re.compile('<dd><a href="(.*?)">(.*?)</a></dd>')
# results = re.findall(content1, str(dl))
# for result in results:
#     detailUrls.append(result[0])
#     chapters.append(result[1])
#     detail = requests.get('http://www.xbiquge.la/' + result[0], headers=headers)
#     detail.encoding = 'utf-8'
#     detailSoup = BeautifulSoup(detail.text, 'lxml')
#     detailContent = detailSoup.select('#content')[0].text
#     with open(name + '\\' + result[1] + '.txt', 'w', encoding='utf-8') as f:
#         f.write(detailContent)

if __name__ == '__main__':
    novelName = input("请输入您想查找的小说：")
    search_novel(novelName)

# search_novel('牧神记')
