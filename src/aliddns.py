from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import requests
from urllib.request import urlopen
from flask import Flask, request
import json
import os

ipv4_flag = 1  # 是否开启ipv4 ddns解析,1为开启，0为关闭
ipv6_flag = 0  # 是否开启ipv6 ddns解析,1为开启，0为关闭
accessKeyId = os.getenv("ACCESSKEYID")  # 将accessKeyId改成自己的accessKeyId
accessSecret = os.getenv("ACCESSSECRET")  # 将accessSecret改成自己的accessSecret
domain = os.getenv("DOMAIN")  # 你的主域名
name_ipv4 = os.getenv("NAME_IPV4")  # 要进行ipv4 ddns解析的主机记录，即前缀
name_ipv6 = os.getenv("NAME_IPV6")  # 要进行ipv6 ddns解析的主机记录，即前缀 [此处对应的是阿里云解析中的 主机记录 应填写 www 或 @ 等。填写www解析后的域名为www.xxx.com；填写@解析后为主域名xxx.com]

client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
app = Flask(__name__)


@app.route('/updateV4')
def updateV4():
    ip = request.args.get('ip')
    update_ipv4(ip)
    print(f'IP update success! ip: {ip}')
    return 'done'


@app.route('/updateV6')
def updateV6():
    ip = request.args.get('ip')
    update_ipv6(ip)
    print(f'IP update success! ip: {ip}')
    return 'done'


def update(RecordId, RR, Type, Value):  # 修改域名解析记录
    from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)


def add(DomainName, RR, Type, Value):  # 添加新的域名解析记录
    from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(DomainName)
    request.set_RR(RR)  # https://blog.zeruns.tech
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)


def update_ipv4(ipv4: str):
    if ipv4_flag == 1:
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_SubDomain(name_ipv4 + '.' + domain)
        request.set_Type("A")
        response = client.do_action_with_exception(request)  # 获取域名解析记录列表
        domain_list = json.loads(response)  # 将返回的JSON数据转化为Python能识别的

        # ip = urlopen('https://api-ipv4.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv4地址
        # ipv4 = str(ip, encoding='utf-8')
        # print("获取到IPv4地址：%s" % ipv4)

        if domain_list['TotalCount'] == 0:
            add(domain, name_ipv4, "A", ipv4)
            print("新建域名解析成功")
        elif domain_list['TotalCount'] == 1:
            if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv4.strip():
                update(domain_list['DomainRecords']['Record'][0]['RecordId'], name_ipv4, "A", ipv4)
                print("修改域名解析成功")
            else:  # https://blog.zeruns.tech
                print("IPv4地址没变")
        elif domain_list['TotalCount'] > 1:
            from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest

            request = DeleteSubDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domain)  # https://blog.zeruns.tech
            request.set_RR(name_ipv4)
            request.set_Type("A")
            response = client.do_action_with_exception(request)
            add(domain, name_ipv4, "A", ipv4)
            print("修改域名解析成功")


# print("本程序版权属于zeruns，博客：https://blog.zeruns.tech")

def update_ipv6(ipv6: str):
    if ipv6_flag == 1:
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_SubDomain(name_ipv6 + '.' + domain)
        request.set_Type("AAAA")
        response = client.do_action_with_exception(request)  # 获取域名解析记录列表
        domain_list = json.loads(response)  # 将返回的JSON数据转化为Python能识别的

        # ip = urlopen('https://api-ipv6.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv6地址
        # ipv6 = str(ip, encoding='utf-8')
        # print("获取到IPv6地址：%s" % ipv6)

        if domain_list['TotalCount'] == 0:
            add(domain, name_ipv6, "AAAA", ipv6)
            print("新建域名解析成功")
        elif domain_list['TotalCount'] == 1:
            if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv6.strip():
                update(domain_list['DomainRecords']['Record'][0]['RecordId'], name_ipv6, "AAAA", ipv6)
                print("修改域名解析成功")
            else:  # https://blog.zeruns.tech
                print("IPv6地址没变")
        elif domain_list['TotalCount'] > 1:
            from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest

            request = DeleteSubDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domain)
            request.set_RR(name_ipv6)  # https://blog.zeruns.tech
            request.set_Type("AAAA")
            response = client.do_action_with_exception(request)
            add(domain, name_ipv6, "AAAA", ipv6)
            print("修改域名解析成功")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
