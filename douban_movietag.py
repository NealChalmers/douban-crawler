import time
import requests
import re
import xlwt

from urllib import request
from bs4 import BeautifulSoup


#以下是电影标签页的爬取参数

urls = []       #电影链接
year = 2016     #要爬取的年份
pages = 3      #爬取的电影页数，每页20部

#以下是电影详情页属性的爬取参数

movie_title = []            #电影名字
movie_country = []          #国家
movie_director = []         #导演
movie_screenWriter = []     #编剧
movie_actor = []            #主演
movie_type = []             #类型
movie_language = []         #语言
movie_date = []             #上映时间
movie_time= []              #电影时长
movie_name = []             #又名

#以下是电影详情页评分的爬取参数

comment = []          #短评数量
vote = []                  #评分人数


#网页爬取配置参数
cookie_str = 'Cookie: ll="108303"; bid=VCwqhdGykZc; __yadk_uid=WlU2z5PfT7ayM2AUFMlUVm6XHaxwoUsx; _vwo_uuid_v2=D0CA41EDEED1A0C639F0837D53C6F56A7|731b88fd10c962f37b53e476cad040b8; __utmc=30149280; __utmc=223695111; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18705; ue="1274184982@qq.com"; __utma=30149280.1927612880.1539001446.1541743879.1541750881.23; __utmz=30149280.1541750881.23.8.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword; dbcl2="187059995:etWky9gmE6A"; ck=S3Xi; __utmb=30149280.3.10.1541750881; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1541750915%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.656272146.1539001446.1541743879.1541750915.22; __utmb=223695111.0.10.1541750915; __utmz=223695111.1541750915.22.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=cb1300d538aa9452.1537752921.24.1541751703.1541743879.'



for c in range(pages):              #查看URL发现第一个是0，选3页看看用range(3)
    url=r'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags={}&start={}'.format(year,c*20)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page=requests.get(url=url,headers=headers).json()
    #print (page)                 #把打印出的page格式化，可以看出page是一个字典，其键'data'的值page['data']是一个列表
    time.sleep(1)
    for r in range(20):              #每次加载是20条，字典、列表、字符串的索引都是从0开始的，所以用range(20)；注意，网站标签，是从1开始的
        print('movie {} in page {} is searching'.format(r, c))
        list=page['data']
        #print (list)
        dict=list[r]                 #之后我们发现，列表每个索引的值又是一个字典
        #print (dict)
        #title = dict['title']
        #rate = dict['rate']
        #casts=dict['casts']          #字典dict[casts]的值又是一个列表
        #print (casts)
        url=dict['url']
        time.sleep(1)
        #print ('片名：{}\n评分：{}\n主演：{}\n地址：{}'.format(title,rate,'，'.join(casts),url))

        response_link = request.Request(url)
        response_link.add_header('cookie', cookie_str)
        response_link.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
        content_link = request.urlopen(response_link).read().decode('utf-8', 'ignore')
        bs1 = BeautifulSoup(content_link, 'lxml')
        title = bs1.title

        if (title):
            movie_title.append(title.text.strip().split('/')[0])
        else:
            movie_title.append('')
        country_namePat = '制片国家/地区:</span> (.*?)<br/>'
        country_name = re.compile(country_namePat).findall(content_link)  # 国家
        if (country_name):
            movie_country.append(country_name[0])
        else:
            movie_country.append('')
        director_name = bs1.find('span', class_='attrs')  # 导演
        if (director_name):
            movie_director.append(director_name.get_text())
        else:
            movie_director.append('')
        screenWriter_name = bs1.find_all('span', class_='attrs')  # 编剧
        if (screenWriter_name):
            movie_screenWriter.append(screenWriter_name[len(screenWriter_name) - 2].get_text())
        else:
            movie_screenWriter.append('')
        actor_name = bs1.find_all('span', class_='attrs')  # 主演
        if (actor_name):
            movie_actor.append(actor_name[len(actor_name) - 1].get_text())
        else:
            movie_actor.append('')
        type_name = bs1.find('span', property="v:genre")  # 类型名字
        if (type_name):
            movie_type.append(type_name.get_text())
        else:
            movie_type.append('')
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
        comment_name = re.compile(comment_namePat).findall(content_link)   #短评数量
        if(comment_name):
            comment.append(comment_name)
        else:
            comment.append("")
        vote_namePat = '>(\d*)</span>人评价</a>'
        vote_name = re.compile(vote_namePat).findall(content_link)   #评分人数
        if(vote_name):
            vote.append(vote_name)
        else:
            vote.append("")


f = xlwt.Workbook()
sheet1 = f.add_sheet('豆瓣电影详情', cell_overwrite_ok=True)
title_text = ['电影名', '国家', '导演', '编剧', '主演', '类型', '语言', '上映时间', '电影时长', '又名', '短评数量', '评分人数']
for i in range(0, len(title_text)):
    sheet1.write(0, i, title_text[i])
for q in range(0, len(movie_title)):
    sheet1.write(q + 1, 0, movie_title[q])
for y in range(0, len(movie_country)):
    sheet1.write(y + 1, 1, movie_country[y])
for w in range(0, len(movie_director)):
    sheet1.write(w + 1, 2, movie_director[w])
for e in range(0, len(movie_screenWriter)):
    sheet1.write(e + 1, 3, movie_screenWriter[e])
for r in range(0, len(movie_actor)):
    sheet1.write(r + 1, 4, movie_actor[r])
for t in range(0, len(movie_type)):
    sheet1.write(t + 1, 5, movie_type[t])
for u in range(0, len(movie_language)):
    sheet1.write(u + 1, 6, movie_language[u])
for i in range(0, len(movie_date)):
    sheet1.write(i + 1, 7, movie_date[i])
for o in range(0, len(movie_time)):
    sheet1.write(o + 1, 8, movie_time[o])
for p in range(0, len(movie_name)):
    sheet1.write(p + 1, 9, movie_name[p])
for x in range(0, len(comment)):
    sheet1.write(x + 1, 10, comment[x])
for z in range(0, len(vote)):
    sheet1.write(z + 1, 11, vote[z])

f.save('D:/douban_{}.xlsx'.format(year))