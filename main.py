# -*- encoding:utf-8 -*-

# 题目：网站访问日志分析
# 需求：
# 统计本日志文件的总pv、uv
# 列出全天每小时的pv、uv数
# 列出top 10 uv的IP地址，以及每个ip的pv点击数
# 列出top 10 访问量最多的页面及每个页面的访问量
# 列出访问来源的设备列表及每个设备的访问量

import re
import time, datetime
import sys
import collections


# 计算当天每个时间的时间戳
def per_hour_timestamp(num):
    if len(str(num)) != 2:
        num = '0' + str(num)
    if int(num) < 24:
        i = str(num) + ":00:00"
        now_data = datetime.date.today()
        t_struct = str(now_data) + i  # 字符串
        t_tuple = time.strptime(t_struct, "%Y-%m-%d%H:%M:%S")  # 转成时间的元组形式
        t = time.mktime(t_tuple)  # 转成时间戳
    elif int(num) == 24:
        i = "00:00:00"
        now_data = datetime.date.today() + datetime.timedelta(days=+1) # 第二天
        t_struct = str(now_data) + i  # 字符串
        t_tuple = time.strptime(t_struct, "%Y-%m-%d%H:%M:%S")  # 转成时间的元组形式
        t = time.mktime(t_tuple)  # 转成时间戳
    else:
        print("input num range 00-24")
        sys.exit(2)
    return t

# 把当天日志的时间变成时间戳
def str_to_timestamp(num):
    num = str(num)
    now_data = datetime.date.today()
    t_struct = str(now_data) + num  # 字符串
    t_tuple = time.strptime(t_struct, "%Y-%m-%d%H:%M:%S")  # 转成时间的元组形式
    t = time.mktime(t_tuple)  # 转成时间戳
    return t

def show_pv():
    f =  open('网站访问日志.txt','r',encoding='utf-8')
    count = len(f.readlines())
    f.close()
    print('pv：' + str(count))
    return count
def show_uv():
    log_ips = []
    f =  open('网站访问日志.txt','r',encoding='utf-8')
    for i in f:
        i = i.split(' ')[0]
        # i = re.match(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+',i)
        i = re.search(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+',i)
        try:
            i = i.group()
            log_ips.append(i)  # 获取ip存在列表上
        except:
            pass
    print('uv：' + str(len(set(log_ips))))  # 去重计数个数
    f.close()


def list_pv_and_uv_per_hour():
    log_times = []
    log_ips = []
    f = open('网站访问日志.txt','r',encoding='utf-8')
    for i in f:
        i = i.split(' ')
        log_time = re.search(r'[0-9]{2}:[0-9]{2}:[0-9]{2}$', i[3])
        log_ip = re.search(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+', i[0])
        try:
            log_time = log_time.group()
            log_ip = log_ip.group()
            log_times.append(log_time)  # 获取log_times存在列表上
            log_ips.append(log_ip)  # 获取ip存在列表上
        except:
            pass
    f.close()
    for num in range(24): # 循环时间段，按时间段要判断
        tmp_time = []
        tmp_ip = []
        for j in range(len(log_times)): # 循环列表
            if per_hour_timestamp(num) < str_to_timestamp(log_times[j]) < per_hour_timestamp(num + 1):
                tmp_time.append(log_times[j])  # 按时间存储
                tmp_ip.append(log_ips[j])       # 按时间对应的ip存储
        print("在 %s~%s 时间段PV量为：%s ip为：%s uv为：%s"
              %
              (str(num),str(num + 1),str(len(tmp_time)),str(list(tmp_ip)),str(len(set(tmp_ip)))))

def list_uv_top_10_ip():
    log_ips = []
    f = open('网站访问日志.txt', 'r', encoding='utf-8')
    for i in f:
        i = i.split(' ')[0]
        # i = re.match(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+',i)
        i = re.search(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+', i)
        try:
            i = i.group()
            log_ips.append(i)  # 获取ip存在列表上
        except:
            pass
    f.close()
    log_ips_dist = {}
    print("每个ip的pv点击数如下：")
    for i in set(log_ips):
        print("ip: %s, pv点击数：%s" % (i, log_ips.count(i)))  # 计数每个ip的个数
        log_ips_dist.setdefault(i, log_ips.count(i))  # 增加字典
    log_ips_dist = collections.Counter(log_ips_dist).most_common() # 字典按value排列，返回tuple类型的二级list
    print("top 10 uv的IP地址如下：")
    for num  in range(10):
        print(log_ips_dist[num][0])


def list_page_pv_top_10():
    print("每个页面的访问量如下：")
    log_ips = []
    f = open('网站访问日志.txt', 'r', encoding='utf-8')
    for i in f:
        i = i.split(' ')[6]
        try:
            log_ips.append(i)  # 获取ip存在列表上
        except:
            pass
    f.close()
    log_ips_dist = {}
    for i in set(log_ips):
        print("页面: %s, 该页面的访问量：%s" % (i, log_ips.count(i)))  # 计数每个ip的个数
        log_ips_dist.setdefault(i, log_ips.count(i))  # 增加字典
    log_ips_dist = collections.Counter(log_ips_dist).most_common() # 字典按value排列，返回tuple类型的二级list
    print("top 10 的页面如下：")
    for num  in range(10):
        print(log_ips_dist[num][0])


def list_ip_pc():
    log_ips = []
    log_pc = []
    print("访问来源的设备列表如下：")
    f =  open('网站访问日志.txt','r',encoding='utf-8')
    for i in f:
        j = i.split('"')[5]
        i = i.split(' ')[0]

        # i = re.match(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+',i)
        i = re.search(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+',i)

        try:
            i = i.group()
            log_ips.append(i)  # 获取ip存在列表上
            log_pc.append(j)
            print(str(i) + ' ' + str(j))
        except:
            pass
    f.close()

    print("每个设备的访问量如下：")
    for i in set(log_pc):
        print("设备: %s, 该设备的访问量：%s" % (i, log_pc.count(i)))  # 计数每个ip的个数
if __name__ == '__main__':
    show_pv()
    show_uv()
    list_pv_and_uv_per_hour()
    list_uv_top_10_ip()
    list_page_pv_top_10()
    list_ip_pc()
