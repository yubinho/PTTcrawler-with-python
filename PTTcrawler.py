import urllib.request as req
import bs4
import csv


def GetData(url, postDate):
    # create request object including Request Headers to pretend browser
    request = req.Request(url, headers={
        "cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # parse html
    soup = bs4.BeautifulSoup(data, "html.parser")  # parse html format by bs4
    titles = soup.find_all("div", class_="title")  # find title class
    file = open("./wordtext/data4.txt", "w", encoding="utf-8")
    for title in titles:
        if title.a != None:  # exclude those posts have been deleted
            date = soup.find("div", class_="date")
            newdate = date.text
            newdate = newdate.replace(" ", "")
            if newdate == str(postDate):  # judge post date
                print(title.a.string)
            # store to txt
                file.write(str(title.a.string))
                # # put data into csv
                # with open("data3.csv", "a", newline='') as csvfile:
                #     writer = csv.writer(csvfile, delimiter=' ')
                #     writer.writerow(str(title.a.string))
    file.close()
    # 抓取上一頁的連結
    nextLink = soup.find("a", string="‹ 上頁")  # catch url of last page
    # print(nextLink["href"])
    return nextLink["href"]


# catch pages
postDate = input("please input post date ex.4/13\n")
boardName = input("please input post date ex.Gossiping\n")
PageURL = 'https://www.ptt.cc/bbs/'+boardName+'/index.html'
#PageURL = 'https://www.ptt.cc/bbs/Gossiping/index.html'
count = 0
while count < 10:  # finding page setting
    PageURL = 'https://www.ptt.cc'+GetData(PageURL, postDate)
    count += 1
