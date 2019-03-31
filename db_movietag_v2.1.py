import time
import requests
import re
import xlwt
import random
import urllib.error
# import http.cookiejar

from urllib import request
from bs4 import BeautifulSoup

# 以下是电影标签页的爬取参数
urls = []  # 电影链接
year = 2006  # 要爬取的年份
pages_start = 0  # 爬取的电影页数，每页20部
pages_end = 25

# 以下是电影详情页属性的爬取参数
movie_id = []  # 电影id
movie_title = []  # 电影名字
movie_country = []  # 国家
movie_director = []  # 导演
director_id = []  # 导演 id
movie_screenWriter = []  # 编剧
screenWriter_id = []  # 编剧id
movie_actor = []  # 主演
actor_id = []  # 主演 id
movie_type = []  # 类型
movie_language = []  # 语言
movie_date = []  # 上映时间
movie_time = []  # 电影时长
movie_name = []  # 又名

# 以下是电影详情页评分的爬取参数
comment = []  # 短评数量
vote = []  # 评分人数
rating = []  # 电影评分
stars5 = []  # 五星比例
stars4 = []  # 四星比例
stars3 = []  # 三星比例
stars2 = []  # 二星比例
stars1 = []  # 一星比例


# 网页爬取配置参数
# cookie_str = http.cookiejar.MozillaCookieJar()
# cookie_str.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# cookie_str = 'Cookie: ll="108303"; bid=VCwqhdGykZc; __yadk_uid=WlU2z5PfT7ayM2AUFMlUVm6XHaxwoUsx; _vwo_uuid_v2=D0CA41EDEED1A0C639F0837D53C6F56A7|731b88fd10c962f37b53e476cad040b8; __utmc=30149280; __utmc=223695111; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18705; ue="1274184982@qq.com"; __utma=30149280.1927612880.1539001446.1541743879.1541750881.23; __utmz=30149280.1541750881.23.8.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword; dbcl2="187059995:etWky9gmE6A"; ck=S3Xi; __utmb=30149280.3.10.1541750881; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1541750915%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.656272146.1539001446.1541743879.1541750915.22; __utmb=223695111.0.10.1541750915; __utmz=223695111.1541750915.22.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=cb1300d538aa9452.1537752921.24.1541751703.1541743879.'

def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = UserAgent
    return headers


for c in range(pages_start, pages_end):  # 查看URL发现第一个是0，选3页看看用range(3)
    url = r'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影,{}&start={}'.format(year, c * 20)
    headers = getheaders()
    headers = {'User-Agent': headers}
    page = requests.get(url=url, headers=headers).json()
    # print (page)                 #把打印出的page格式化，可以看出page是一个字典，其键'data'的值page['data']是一个列表

    pidx = [0] * 20
    for i in range(20):
        pidx[i] = i
    random.shuffle(pidx)

    for r in pidx:  # 每次加载是20条，字典、列表、字符串的索引都是从0开始的，所以用range(20)；注意，网站标签，是从1开始的
        print('movie {} in page {} is searching'.format(r, c))
        list = page['data']
        # print (list)
        dict = list[r]  # 之后我们发现，列表每个索引的值又是一个字典
        # print (dict)
        # title = dict['title']
        # rate = dict['rate']
        # casts=dict['casts']          #字典dict[casts]的值又是一个列表
        # print (casts)
        url = dict['url']
        time.sleep(0.2 + random.random() * 0.8)
        # print ('片名：{}\n评分：{}\n主演：{}\n地址：{}'.format(title,rate,'，'.join(casts),url))
        try:
            response_link = request.Request(url)
            # response_link.add_header('cookie', cookie_str)
            # response_link.add_header('User-Agent',
            #                         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

            proxies = [  # 代理IP池
                '116.209.55.73:9999',
                '110.52.235.129:9999',
                '114.88.53.19:53281',
                '111.160.236.84:39692',
                '222.92.112.69:8080',
                '171.37.153.55:9797',
                '116.209.54.228:9999',
                '110.52.235.101:9999',
                '116.209.57.20:9999'
            ]
            pro_ip = random.choice(proxies)
            proxy = {'http': proxies}
            # 创建ProxyHandler
            proxy_support = request.ProxyHandler(proxy)
            # 创建Opener
            opener = request.build_opener(proxy_support)
            # 添加User Angent
            opener.addheaders = [('User-Agent', getheaders())]
            # 安装OPener
            request.install_opener(opener)
            content_link = request.urlopen(response_link).read().decode('utf-8', 'ignore')
        except urllib.error.URLError:
            continue
        movie_id.append(re.compile("(\d{5}\d*)").findall(url))  # 电影 ID
        bs1 = BeautifulSoup(content_link, 'lxml')
        title = bs1.title
        if (title):
            movie_title.append(title.text.strip().split('/')[0])
        else:
            movie_title.append('')
        movie_rating = bs1.find('strong', property='v:average')  # 评分
        if (movie_rating):
            rating.append(movie_rating.get_text())
        country_namePat = '制片国家/地区:</span> (.*?)<br/>'
        country_name = re.compile(country_namePat).findall(content_link)  # 国家
        if (country_name):
            movie_country.append(country_name)
        else:
            movie_country.append('')
        attrs_name = bs1.find_all('span', class_='attrs')  # 导演
        if (len(attrs_name) > 0):
            movie_director.append(attrs_name[0].get_text())
            director_id.append(re.compile("(\d{5}\d*)").findall(str(attrs_name[0])))
        else:
            movie_director.append('')
            director_id.append('')
        if (len(attrs_name) > 1):
            movie_screenWriter.append(attrs_name[1].get_text())
            screenWriter_id.append(re.compile("(\d{5}\d*)").findall(str(attrs_name[1])))
        else:
            movie_screenWriter.append('')
            screenWriter_id.append('')
        if (len(attrs_name) > 2):  # 主演
            movie_actor.append(attrs_name[2].get_text())
            actor_id.append(re.compile("(\d{5}\d*)").findall(str(attrs_name[2])))
        else:
            movie_actor.append('')
            actor_id.append('')
        type_name = bs1.find_all('span', property="v:genre")  # 类型
        temp_name = []
        for t in range(len(type_name)):
            temp_name.append(type_name[t].get_text())
        movie_type.append(temp_name)
        language_namePat = '语言:</span> (.*?)<br/>'
        language_name = re.compile(language_namePat).findall(content_link)  # 语言
        if (language_name):
            movie_language.append(language_name[0])
        else:
            movie_language.append('')
        date_name = bs1.find('span', property="v:initialReleaseDate")  # 开播时间
        if (date_name):
            movie_date.append(date_name.get_text())
        else:
            movie_date.append('')
        movies_time = bs1.find('span', property="v:runtime")  # 片长
        if (movies_time):
            movie_time.append(movies_time.get_text())
        else:
            movie_time.append('')
        name_namePat = '又名:</span> (.*?)<br/>'
        list = re.compile(name_namePat).findall(content_link)  # 又名
        if (list):
            movie_name.append(list[0])  # 列表不是空的说明电影有别名
        else:
            movie_name.append("")  # 没有的话用空字符串占个位置
        comment_namePat = '更多短评(\d*)条</a>'
        comment_name = re.compile(comment_namePat).findall(content_link)  # 短评数量
        if (comment_name):
            comment.append(comment_name)
        else:
            comment.append("")
        vote_name = bs1.find('span', property="v:votes")  # 评分人数
        if (vote_name):
            vote.append(vote_name.get_text())
        else:
            vote.append("")
        stars = bs1.find_all('span', class_="rating_per")  # 评分比例
        if (len(stars) != 0):
            stars5.append(stars[0].get_text())
            stars4.append(stars[1].get_text())
            stars3.append(stars[2].get_text())
            stars2.append(stars[3].get_text())
            stars1.append(stars[4].get_text())
        else:
            stars5.append('')
            stars4.append('')
            stars3.append('')
            stars2.append('')
            stars1.append('')

    time.sleep(1)

f = xlwt.Workbook()
sheet1 = f.add_sheet('豆瓣电影详情', cell_overwrite_ok=True)
title_text = ['电影ID', '电影名', '国家1', '国家2', '导演1', '导演1 ID', '导演2', '导演2 ID', '编剧1', '编剧1 ID', '编剧2', '编剧2 ID',
              '类型1', '类型2', '类型3', '语言1', '语言2', '上映时间', '电影时长', '又名', '短评数量', '评分人数', '电影评分',
              '五星比例', '四星比例', '三星比例', '两星比例', '一星比例', '主演1', '主演1 ID', '主演2', '主演2 ID',
              '主演3', '主演3 ID', '主演4', '主演4 ID', '主演5', '主演5 ID']
for i in range(len(title_text)):
    sheet1.write(0, i, title_text[i])
for d in range(len(movie_id)):
    sheet1.write(d + 1, 0, movie_id[d])
for q in range(len(movie_title)):
    sheet1.write(q + 1, 1, movie_title[q])
for y in range(len(movie_country)):
    temp_country = movie_country[y][0].split(' / ')
    sheet1.write(y + 1, 2, temp_country[0])
    if (len(temp_country) > 1):
        sheet1.write(y + 1, 3, temp_country[1])
for w in range(len(movie_director)):
    temp_director = movie_director[w].split(' / ')
    sheet1.write(w + 1, 4, temp_director[0])
    if (len(temp_director) > 1):
        sheet1.write(w + 1, 6, temp_director[1])
for i in range(len(director_id)):  # 导演 ID
    temp_id = director_id[i]
    if len(temp_id) > 0:
        sheet1.write(i + 1, 5, temp_id[0])
    if len(temp_id) > 1:
        sheet1.write(i + 1, 7, temp_id[1])
for e in range(len(movie_screenWriter)):
    temp_screenWriter = movie_screenWriter[e].split(' / ')
    sheet1.write(e + 1, 8, temp_screenWriter[0])
    if len(temp_screenWriter) > 1:
        sheet1.write(e + 1, 10, temp_screenWriter[1])
for i in range(len(screenWriter_id)):  # 编剧 ID
    temp_id = screenWriter_id[i]
    if len(temp_id) > 0:
        sheet1.write(i + 1, 9, temp_id[0])
    if len(temp_id) > 1:
        sheet1.write(i + 1, 11, temp_id[1])
for t in range(len(movie_type)):  # 类型
    for r in range(len(movie_type[t])):
        if r > 2:
            break
        sheet1.write(t + 1, 12 + r, movie_type[t][r])
for u in range(len(movie_language)):
    temp_language = movie_language[u].split(' / ')
    sheet1.write(u + 1, 15, temp_language[0])
    if (len(temp_language) > 1):
        sheet1.write(u + 1, 16, temp_language[1])
for i in range(len(movie_date)):
    sheet1.write(i + 1, 17, movie_date[i])
for o in range(len(movie_time)):
    sheet1.write(o + 1, 18, movie_time[o])
for p in range(len(movie_name)):
    sheet1.write(p + 1, 19, movie_name[p])
for x in range(len(comment)):
    sheet1.write(x + 1, 20, comment[x])
for z in range(len(vote)):
    sheet1.write(z + 1, 21, vote[z])
for c in range(len(rating)):
    sheet1.write(c + 1, 22, rating[c])
for s1 in range(len(stars1)):
    sheet1.write(s1 + 1, 23, stars5[s1])  # 评分比例
for s2 in range(len(stars2)):
    sheet1.write(s2 + 1, 24, stars4[s2])
for s3 in range(len(stars3)):
    sheet1.write(s3 + 1, 25, stars3[s3])
for s4 in range(len(stars4)):
    sheet1.write(s4 + 1, 26, stars2[s4])
for s5 in range(len(stars5)):
    sheet1.write(s5 + 1, 27, stars1[s5])

for r in range(len(movie_actor)):
    temp_actor = movie_actor[r].split(' / ')
    if (len(actor_id) > r):
        temp_id = actor_id[r]
    else:
        temp_id = ''
    ind = 5
    if (len(temp_actor) < 5):
        ind = len(temp_actor)

    for s in range(ind):
        sheet1.write(r + 1, 28 + s * 2, temp_actor[s])  # 主演
        if (len(temp_id) > s):
            id = temp_id[s]
        else:
            id = ''
        sheet1.write(r + 1, 29 + s * 2, id)  # 主演 ID

f.save('D:/douban_{}.xlsx'.format(year))
