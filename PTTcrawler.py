
import urllib.request as req
import bs4
import csv
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

isContinue = True
isFind = False
page = 0


def GetData(url, postDate, userAgent):
    global page
    page += 1
    print("finding page"+str(page)+"...")

    # create request object including Request Headers to pretend browser
    request = req.Request(url, headers={
        "cookie": "over18=1",
        "User-Agent": userAgent})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # parse html
    soup = bs4.BeautifulSoup(data, "html.parser")  # parse html format by bs4
    titles = soup.find_all("div", class_="title")  # find title class
    file = open("data.txt", "a", encoding="utf-8")

    for title in titles:
        if title.a != None:  # exclude those posts have been deleted
            date = soup.find("div", class_="date")
            newdate = date.text.replace(" ", "")
            if newdate == str(postDate):  # judge post date
                print(title.a.string)
                global isFind
                isFind = True
            # store to txt
                file.write(str(title.a.string))
                # # put data into csv
                # with open("data3.csv", "a", newline='') as csvfile:
                #     writer = csv.writer(csvfile, delimiter=' ')
                #     writer.writerow(str(title.a.string))
            else:
                if isFind == True:
                    global isContinue
                    isContinue = False
    file.close()

    nextLink = soup.find("a", string="‹ 上頁")  # catch url of last page
    # print(nextLink["href"])
    if isContinue == True:
        return nextLink["href"]
    else:
        return None


def create_cloudword():
    with open('resource/stopword.txt', 'r', encoding='utf-8') as file:  # customized illegal word
        stops = file.read().split('\n')

    text_from_file_with_apath = open(
        'data.txt', encoding='utf8').read()  # data

    breakword = jieba.cut(
        text_from_file_with_apath, cut_all=False)  # default hyphenation

    final_words = []  # legal word

    for word in breakword:
        if word not in stops:
            final_words.append(word)

    wl_space_split = " ".join(final_words)

    font_path = 'resource/irohamaru-Regular.ttf'  # font

    abel_mask = np.array(Image.open("resource/heart.jpg"))  # image outline

    my_wordcloud = WordCloud(background_color='white', mask=abel_mask,
                             font_path=font_path).generate(wl_space_split)  # create wordcloud
    plt.figure(figsize=(10, 10))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    # catch pages
    userAgent = input("please input user agent of browser\n")
    postDate = input("please input post date ex.4/13\n")
    boardName = input("please input board name ex.Gossiping\n")
    data_path = "./data.txt"
    if os.path.isfile(data_path):
        file = open(data_path, 'w')
        file.close()
    PageURL = 'https://www.ptt.cc/bbs/'+boardName+'/index.html'
    # finding all posts of assigned date
    while isContinue == True and GetData(PageURL, postDate, userAgent) != None:
        PageURL = 'https://www.ptt.cc'+GetData(PageURL, postDate, userAgent)

    create_cloudword()

    # count = 0
    # while count < 5:
    #     PageURL = 'https://www.ptt.cc'+GetData(PageURL, postDate,userAgent)
    #     count+=1
