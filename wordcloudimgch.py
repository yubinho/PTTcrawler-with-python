import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

with open('D:/python/final/wordcloud/stopword.txt', 'r', encoding='utf-8') as file:  # 自定義停用詞典
    stops = file.read().split('\n')

text_from_file_with_apath = open(
    'D:/python/final/data4.txt', encoding='utf8').read()  # 選擇要製作的txt

breakword = jieba.cut(
    text_from_file_with_apath, cut_all=False)  # 預設模式斷詞

final_words = []  # 用來放非停用詞的句子

for word in breakword:
    if word not in stops:  # 不是停用字
        final_words.append(word)

wl_space_split = " ".join(final_words)

font_path = 'D:/python/final/wordcloud/irohamaru-Regular.ttf'  # 引入中文字型

abel_mask = np.array(Image.open("D:/python/final/wordcloud/heart.jpg"))  # 選擇外觀

my_wordcloud = WordCloud(background_color='white', mask=abel_mask,
                         font_path=font_path).generate(wl_space_split)  # (背景,外觀,字型,斷詞方式)
plt.figure(figsize=(10, 10))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

# my_wordcloud.to_file('D:/python/final/wordcloud/newWordCloud.png')
