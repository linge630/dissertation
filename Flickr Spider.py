import os
import csv
import json
import flickrapi
import urllib.request


def downloadpic(pic_url, pic_name, pic_extend):
    file_path = "//Users/qpple/Desktop/Dissertation/flickrSpider/0627/0629"
    sep = '.'
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        filename = '{}{}{}{}{}'.format(file_path, os.sep, pic_name, sep, pic_extend)
        print(filename + '开始下载')
        urllib.request.urlretrieve(pic_url, filename=filename)
        print(filename + '下载完成')
    except IOError as e:
        print("IOError", e)
    except Exception as e:
        print("Exception", e)


def writetocsv(info):
    with open("//Users/qpple/Desktop/Dissertation/flickrSpider/0627/newpicinfo0629.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for pic in info:
            writer.writerow(pic)
    #print('csv 写入完成')


def walkdata(bboxlist, totalnum):
    index = 1
    target_list = [12, 13, 17, 18]
    for index_bbox, bbox in enumerate(bboxlist):
        if index_bbox not in target_list:
            continue
        photonum = 0
        try:
            photos = flickr.walk(bbox=bbox, accuracy=16,
                                 content_type=1, per_page=100,
                                 extras='url_c')
        except Exception as e:
            print(e)

        picinfo = []
        for i, photo in enumerate(photos):
            newline = []
            try:
                picid = photo.get('id')
                url = photo.get('url_c')
                picname = photo.get('id')
                
                text = json.loads(flickr.photos.getInfo(photo_id=picid, format='json'))
                favorites = json.loads(flickr.photos.getFavorites(photo_id=picid, format='json'))
                
                owner = photo.get('owner')
                photolist = json.loads(flickr.people.getPublicPhotos(user_id=owner, format='json'))
                totalphotos = photolist['photos']['total']
                
                newline.append(picid)
                newline.append(owner)
                newline.append(totalphotos)
                newline.append(len(favorites['photo']['person']))
                newline.append(text['photo']['comments']['_content'])
                newline.append(text['photo']['location']['latitude'])
                newline.append(text['photo']['location']['longitude'])
                newline.append(text['photo']['dates']['taken'])
                tags = []
                for tag in text['photo']['tags']['tag']:
                    tags.append(tag['raw'])
                newline.append('-'.join(tags))
                picinfo.append(newline)
                
                downloadpic(url, picname, url.split('.')[-1])
                photonum += 1
                
                if i >= totalnum:
                    break
            except Exception as e:
                #print(e)
                continue
        print("地块" + str(index) + "共抓取" + str(photonum))
        index += 1

        writetocsv(picinfo)


# 必需的认证信息
api_key = '0d9b223318564736600bca26b5803737'
api_secret = '4ed777205f0bfeed'
# 最多抓取的数量
total_num = 3000
flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
# 测试地块
testBbox = '116.3433108,39.8643448,116.4833276,39.9708536'
# 生成地块坐标bbox
lon = ['116.203294', '116.2733024', '116.3433108',
       '116.4133192', '116.48833276', '116.553336']
lat = ['39.757836', '39.8110904', '39.8643448',
       '39.9175992', '39.9708536', '40.024108']
bboxList = []
for i in range(6):
    if i == 5:
        continue
    for j in range(6):
        if j == 5:
            continue
        temp = []
        temp.append(lon[j])
        temp.append(lat[i])
        temp.append(lon[j + 1])
        temp.append(lat[i + 1])
        bboxList.append(','.join(temp))
with open("//Users/qpple/Desktop/Dissertation/flickrSpider/0627/newpicinfo0629.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['picid', 'owner_id', 'totalphotos', 'favorites', 'comments', 'lat', 'lon', 'taken', 'tags']
    writer.writerow(header)
walkdata(bboxList, total_num)




