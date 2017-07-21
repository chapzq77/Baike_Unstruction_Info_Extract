# encoding:utf-8
import urllib2
from lxml import etree
import re
import json

"""
抽取百科的半结构化的属性，存在字典中，并且写在json文件中。
整合三种百科的抽取代码。。。
"""

xx = u"[\u4e00-\u9fa50-9]+"
pattern = re.compile(xx)

def baike_extract(url,name):
    if "http://baike.baidu.com" in url:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        html = etree.HTML(html.decode('utf8', 'ignore'))
        property_name_list =[]
        property_value_list =[]
        property = dict()
        if html.xpath('//div[@class="basic-info cmn-clearfix"]/dl'):
            for t in html.xpath('//div[@class="basic-info cmn-clearfix"]/dl'):
                for dt in t.xpath('./dt[@class="basicInfo-item name"]'):
                    property_name = ''.join(pattern.findall(''.join(dt.xpath('./text()'))))
                    property_name_list.append(property_name)
                for dd in t.xpath('./dd[@class="basicInfo-item value"]'):
                    property_value = (''.join(dd.xpath('.//text()')).replace("\n",""))
                    property_value_list.append(property_value)
        for i in range(len(property_value_list)):
            property.setdefault(property_name_list[i],property_value_list[i])
        jsobj = json.dumps(property)
        file_name = open('baike.json','w')
        file_name.write(jsobj)
        file_name.close()

        for i,j in property.iteritems():
            print i.encode('utf-8'),j.encode('utf-8')

    elif "http://www.baike.com/" in url:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        html = etree.HTML(html.decode('utf8', 'ignore'))
        #存储属性名的列表
        #property_name_list =[]
        #存储属性名对应的属性值
        #property_value_list =[]
        property = dict()
        if html.xpath('//div[@class="module zoom"]'):
            for tr in html.xpath('//div[@class="module zoom"]//tr'):
                for td in tr.xpath('./td'):
                    property_name = ''.join(''.join(td.xpath('./strong//text()')))
                    property_name =property_name[0:-1]
                    #print property_name.encode('utf-8')
                    property_value = ''.join(''.join(td.xpath('./span//text()')).split())
                    #print property_name,property_value
                    if property_name or property_value != '':
                        property.setdefault(property_name,property_value)
        jsobj = json.dumps(property)
        file_name = open('hudongbaike.json','w')
        file_name.write(jsobj)
        file_name.close()
        for i,j in property.iteritems():
            print i,j

    elif 'http://baike.sogou.com/' in url:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        html = etree.HTML(html.decode('utf8', 'ignore'))
        #存放属性键值对
        property = dict()
        if html.xpath('//table[@class="abstract_tbl"]'):
            for td in html.xpath('//table[@class="abstract_tbl"]//td[@class="abstract_list_wrap"]'):
                for tr in td.xpath('.//tr'):
                    property_name =''.join( ''.join(tr.xpath('./th//text()')).split())
                    property_value = ''.join(''.join(tr.xpath('./td//text()')).split())
                    property.setdefault(property_name,property_value)
                    #print property_name,property_value
        jsobj = json.dumps(property)
        file_name = open('sofoubaike.json','w')
        file_name.write(jsobj)
        file_name.close()
        for i,j in property.iteritems():
            print i,j
    else:
        return None


if __name__ == '__main__':
    url="http://baike.baidu.com/item/%E6%9D%8E%E5%A8%9C/5285"
    name=u"李静"
    baike_extract(url, name)
