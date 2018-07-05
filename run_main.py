# -*- coding: GB2312 -*-
#from typing import Any, Union

from bs4 import BeautifulSoup
import requests


def spider_secondinnerurl(secondurl):  # �ڵڶ�������ҳ��ִ�еĲ���
    response = requests.get(secondurl)
    response.encoding = "GB2312"
    soup = BeautifulSoup(response.text, 'lxml')
    t = soup.find(text=(u'¥������')).parent
    response = requests.get(t.get('href'))
    response.encoding = "GB2312"
    soup = BeautifulSoup(response.text, 'lxml')
    prices = soup.find_all(name='em')  # �۸�
    wuyeleibies = soup.find_all(name='div', attrs={"class": "list-right"})  # ��ҵ���
    jianzhuleibies = soup.select(
        'div.clearfix.cqnx_512 > p')  # soup.find_all(name='span', attrs={"class": "bulid-type"}) # �������
    kaifashangs = soup.select('div.list-right-text > a')  # ������
    tels = soup.select('div.list-right.c00')  # ��ѯ�绰
    for price, wuyeleibie, jianzhuleibie, kaifashang, tel in zip(prices, wuyeleibies, jianzhuleibies, kaifashangs,
                                                                 tels):
        data3 = {  # �����ֵ�
            'price': price.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),  # ��ȷ��
            'wuyeleibie': wuyeleibie.get('title').strip().replace("\t", "").replace(" ", "").replace("\n", ""),
            'jianzhuleibie': jianzhuleibie.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),
            'kaifashang': kaifashang.get_text(),
            'tel': tel.get_text()
            # 'zlhx' : zlhx.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),
            # 'address' : address.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "")
        }
        print(data3["price"] + '|' + data3["wuyeleibie"] + '|' + data3['jianzhuleibie'] + '|' + data3[
            'kaifashang'] + '|' + data3['tel'])  # �����Զ����ʽ������SQL���


# url='http://cangmashanguojilvyoudujiaqu.fang.com/'
# spider_secondinnerurl(url)


def spider_outer(firsturl):  # �����б�ҳ��ִ�еĲ���
    response = requests.get(firsturl)
    response.encoding = "GB2312"
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.nlcd_name > a')  # ����
    hrefs = soup.select('div.nlcd_name > a')  # ��һ������ҳ���ַ
    adds = soup.select('div.address > a')  # ��ַ
    imgs = soup.find_all('img', width='168')  # Ч��ͼ����
    zlhxs = soup.select('div.house_type.clearfix')  # ��������
    labels = soup.find_all(name='span', attrs={"class": "inSale"}) + soup.find_all(name='span',
                                                                                   attrs={"class": "forSale"})
    for title, href, add, img, zlhx, label in zip(titles, hrefs, adds, imgs, zlhxs, labels):
        addyoukuohaoweizhi = add.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "").index(']')
        add.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "")[0:addyoukuohaoweizhi + 1]
        # try:
        #    yujiweizhi = housetype.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "").index('Ԥ��')
        #    housetypestr = housetype.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "")[0:yujiweizhi + 1]
        # except :
        #    housetypestr = housetype.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),  # ��ȷ��
        data1 = {  # �����ֵ�
            'title': title.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),  # ��ȷ��
            'href': href.get('href'),  # ��ȷ��
            'add': add.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", "").replace("��", "")[
                   0:addyoukuohaoweizhi + 1] + add.get("title").replace("��", "")[addyoukuohaoweizhi - 1:],  # ��ȷ��
            'img': img.get('src'),
            'zlhx': zlhx.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),
            'label': label.get_text()
        }
        print(
            data1["title"] + "|" + data1["href"] + '|' + data1["add"] + '|' + data1["img"] + '|' + data1['zlhx'] + '|' +
            data1['label'] + '|')  # �����Զ����ʽ������SQL���
        spider_secondinnerurl(data1["href"])


for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
          '20']:
    spider_outer('http://newhouse.qd.fang.com/house/s/a77-b9' + i + '/')
