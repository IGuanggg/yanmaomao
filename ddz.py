#   --------------------------------注释&变量区--------------------------------
#   微信入口： https://168721367-1257141735.cos-website.ap-nanjing.myqcloud.com/index.html?pid=143331
#   注册后开始抓包，点击开始阅读，排除.qq.com结尾的抓包，找GET类型的请求，复制里面的cookie，全都复制保存下来
#   cokkie样例 user_openid=？？？; uid=？？; PHPSESSID=？？？
#   变量名：s_ddz    变量名值的格式：备注#cookie#提现金额（元）#wxpusher的apptoken#主题id#提现支付宝名字#支付宝账号
#   支持多号,多号之间用换行符(回车键)
#   提现功能不再可用，请自行提现。。。
#   const $ = new Env('点点赚');
#   cron 40 8,10,12,14,16,18,20 * * *

import hashlib
import json
import math
import os
import time
import requests
import random
import re
from urllib.parse import quote, urlparse, parse_qs
import urllib3
from urllib.parse import parse_qs, urlsplit
requests.packages.urllib3.disable_warnings()

def push(appToken, topicId, title, link, text, type):
    """
    推送文章到微信

    Args:
    - appToken (str): 应用令牌
    - topicId (str): 主题ID
    - title (str): 文章标题
    - link (str): 文章链接
    - text (str): 文章内容
    - type (int): 内容类型

    Returns:
    - bool: 推送成功与否
    """

    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "阅读过检测",
        "contentType": 2,
        "topicIds": [topicId],
        "url": link,
    }
    #print(datapust)
    urlpush = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = requests.post(
            url=urlpush, json=datapust, verify=False
        )
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，，要黑号了！",p.json())
            return False
    except:
        print("❌ 推送文章到微信失败，，要黑号了！",p.json())
        return False


def ts():
    """
    获取当前时间戳（毫秒级）

    Returns:
    - str: 当前时间戳（毫秒级），以字符串形式返回
    """
    return str(int(time.time())) + "000"



class Main:
    def __init__(self, cg):
        self.code = ""
        self.wxcode = ""
        self.uid = ""
        self.web_url = ""
        self.wx_cloud = cg['wx_cloud']
        self.cookie = cg["cookie"]
        self.txbz = cg["txbz"]
        self.topicId = cg["topicId"]
        self.appToken = cg["appToken"]
        self.aliAccount = cg["aliAccount"]
        self.aliName = cg["aliName"]
        self.name = cg["name"]
        self.domnainHost = ""
        self.wxid = cg['wxid']

    def gold(self):
        """
        获取金币信息

        Returns:
        - bool: 获取信息成功返回True，否则返回False
        """
        try:
            value = ""
            headers={
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23013RK75C Build/TKQ1.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5419 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie":f"{self.cookie}",
            }
            
            r = requests.get(
                f"http://{self.domnainHost}/index/mob/tixian.html",
                headers = headers,
                verify=False,
            )
            r2 = requests.get(
                f"http://{self.domnainHost}/index/mob/index.html",
                headers = headers,
                verify=False,
            )
            htmlText = r.text
            htmlText2 = r2.text
            #print(htmlText2)
            pattern = r'<div class="b1">可兑换：<span>(\d+\.\d+)米</span></div>'
            pattern2 = r'<div class="b2">今日还可兑换<span>(\d+)</span>次</div>'
            pattern3 = r'<div[^>]*>可兑换(\d+(?:\.\d+)?)米<\/div>'
            matches3 = re.findall(pattern3, htmlText2)
            matches = re.findall(pattern, htmlText)
            matches2 = re.findall(pattern2, htmlText)
            #print(htmlText)
            if matches:
                value = matches[0]
                print(f"账号[{self.name}]余额：{value}元,剩余提现次数：{matches2[0]}")
            else:
                value = matches3[0]
                print(f"账号[{self.name}]余额：{value}元")
            return value
        except Exception as e:
            print("出错，重试。。")
            time.sleep(1)
            self.gold()



    def getKey(self):
        """
        获取code和阅读参数

        Returns:
        - tuple: 包含code和请求头信息的元组，格式为 (code, headers)
        """
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23013RK75C Build/TKQ1.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5419 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": f"http://{self.domnainHost}/index/mob/index.html",
            "Cookie": f"{self.cookie}",
        }

        res = requests.get(
            f"http://{self.domnainHost}/index/mob/get_read_qr.html",
            headers=headers,
            verify=False,
        ) 

        try:
            # 删除反斜杠
            json_data_no_slash = res.text.replace('\\', '')

            # 提取 web_url 参数中的 URL 部分
            pattern = r'web_url":"(http:\/\/[^ ]+)'
            match = re.search(pattern, json_data_no_slash)
            web_url = match.group(1)
            #print("提取到的 web_url:", web_url)

            # 使用 urlparse 解析 URL
            parsed_url = urlparse(web_url)
            self.web_url = parsed_url.netloc
            self.code = parsed_url.query
            self.uid = re.search(r'uid=(\d+)', self.cookie).group(1)
            #print(self.web_url,self.uid,self.code)
        except ConnectionError as e:
            print(f"账号[{self.name}]获取阅读参数失败重试...")
            time.sleep(1)
            self.getKey()
        except Exception as e:
            print(f"账号[{self.name}]获取阅读参数失败!返回：",res.text)
            return
        
        if self.web_url == "":
            print(f"账号[{self.name}]获取阅读参数失败，返回：{res.text}")
            return False
        else:
            print(f"账号[{self.name}] 阅读准备成功✅，阅读参数为：{self.code}")
            #print(self.web_url,self.code,self.uid)
            return True

    

    def read(self):
        """
        阅读文章

        Returns:
        - bool: True 表示阅读成功，False 表示阅读失败
        """
         
        self.getKey()
        if self.web_url == "":
            print(f"账号[{self.name}]获取阅读参数失败!停止阅读")
            return
        while True:
            data = {
                "code":self.code,
                "uid":self.uid
            }
            headers={
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23013RK75C Build/TKQ1.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5419 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": f"{self.cookie}",
                "Referer": f"http://{self.web_url}/?{self.code}",
                "Origin" : f"http://{self.web_url}"
            }

            while True:
                try:
                  
                    res = requests.post(
                        f"http://{self.web_url}/index/index/get_article.html",
                        headers=headers,
                        data=data,
                        timeout=60,
                        verify=False,
                    )
                    result = res.json()
                    if res.text == "" or "code" not in res.text:
                        print("疑似台子接口出错，重试。。。")
                        #print(res.text)
                        time.sleep(10)
                        continue
                    else:
                        break
                except:
                    print("疑似台子接口出错，重试。。。")
                    #print(res.text)
                    time.sleep(10)
                    continue
            #print(res.text)
            #print(res.json()["code"])
            if res.text and res.json()["code"] == 1:
                result = res.json()
            else:
                print(f"账号[{self.name}]获取文章链接失败：{res.text}")
                return

            if result.get("code") == 1:
                wechatPostLink = result['data']['info']['link']
                rid = result['data']['info']['rid']
                try:
                    type = result['data']['info']['type']
                except:
                    type = ""
                #print(rid)
                
                print (f"账号[{self.name}] 获取文章链接成功 ✅")
                sleepTime = random.randint(10,15)
                
                if ( type != ""):
                    print(f"⚠️账号[{self.name}]出现检测文章!\n{wechatPostLink}")
                    sleepTime = random.randint(30, 40)
                    print(f"⚠️ 账号[{self.name}]检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。")
                    push(
                        self.appToken,
                        self.topicId,
                        "点点赞阅读过检测",
                        wechatPostLink,
                        f"账号[{self.name}]正在等待过检测，等待时间：{sleepTime}秒！",
                        "xyyyd",
                    )
                else:
                    sleepTime = random.randint(6,7)
                    print(f"模拟读{sleepTime}秒...")
                    
                time.sleep(sleepTime)
                
                data2 = {
                "rid":rid,
                "time_is_gou":1
                }
                
                while True:
                    try:
                        r = requests.post(
                            f"http://{self.web_url}/index/index/auth_record.html",
                            headers=headers,
                            data=data2,
                            timeout=60,
                            verify=False,
                        )
                        result = r.json()
                        if r.text == "" or "code" not in r.text:
                            print("疑似台子接口出错，重试。。。")
                            #print(r.text)
                            time.sleep(10)
                            continue
                        else:
                            break
                    except:
                        print("疑似台子接口出错，重试。。。")
                        time.sleep(10)
                        continue
                #print(r)
                #print(r.text)
                result2 = r.json()
                if r.text and result2:
                    try:
                        if result2["code"] == 1:
                            print(f"✅ 提交成功！当前进度：{result2['txt']}")
                            print("-"*49)
                        elif result2["code"] == 3:
                            print(f"✅ 文章阅读完毕！结算中...")
                            data3 = {
                                "code":self.code
                            }
                            r = requests.post(
                                f"http://{self.web_url}/index/index/read_result.html",
                                headers=headers,
                                timeout=60,
                                data=data3
                            )
                            result3 = r.json()
                            if result3['code'] == 1:
                                print("✅ 结算成功！")
                            else:
                                print("❌ 结算失败！",result3)
                            break
                        else:
                            print(f"❌ 提交失败：{result2.get('msg')}")
                            #break
                    except Exception as e:
                        print(f"❌ 提交异常：{result2.get('msg')}")
                        break
                else:
                    print(f"❌ 账号[{self.name}]阅读文章失败：{r.text}")
                    break
            else:
                print(f"⚠️ 账号[{self.name}]阅读出错：{res.text}")
                time.sleep(1.5) 

    def withdraw(self):
        """
        提现金币

        Args:
        - self: 类实例本身

        Returns:
        - bool: 提现是否成功
        """
        # 取code
        try:
            data = { 
                "Appid": "wxc95b4c8b462b9b86",
                "Url": "",
                "Wxid": self.wxid
            }
            #print(self.wxid)
            r = requests.post(f"{self.wx_cloud}/VXAPI/Tools/ThirdAppGrant",json=data).json()
            #print(r)
            if r["Success"]:
                print(f"账户[{self.name}]获取code成功✅ :",r['Data'])
                self.wxcode = r['Data']
            else:
                print(f"账户[{self.name}]获取code失败❌ :",r['Message'])
                return False
        except Exception as e:
            if ConnectionError in str(e):
                print(f"账户[{self.name}]获取code失败!无法连接云端❌ ",)
                return False

        gold = float(self.gold())
        coin = gold*10000
        #print(coin)
        if gold < float(self.txbz):
            print(f"账号[{self.name}]没有达到提现标准")
            return False
        
        print(f"账号[{self.name}]本次提现金额：{gold}元")
        if gold:
            name = quote(self.aliName)
            account = quote(self.aliAccount)
            u1 = f"http://{self.domnainHost}/index/mob/fa_tx.html"
            p1 = f"code={self.wxcode}&money={self.txbz}&kou_credit={coin}&tx_type=2&ali_name={name}&ali_account={account}"
            r = requests.post(
                u1,
                data=p1,
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f"{self.cookie}",
                    "Host": f"{self.domnainHost}",
                    "Origin": f"http://{self.domnainHost}",
                    "Proxy-Connection": "keep-alive",
                    "Referer": f"http://{self.domnainHost}/index/mob/fa_tx.html",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23013RK75C Build/TKQ1.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5419 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
                    "X-Requested-With": "XMLHttpRequest",
                },
                verify=False,
            )
            try:
                res = r.json()
                if res['code'] == "1":
                    print(f"✅ 账号[{self.name}]提现成功")
                else:
                    print(f"账号[{self.name}]提现失败：", r.text)
            except Exception as e:
                print(f"账号[{self.name}]提现失败：", r.text)    

    def init(self):
        """
        初始化账号信息

        Args:
        - self: 类实例本身

        Returns:
        - bool: 初始化是否成功
        """
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23013RK75C Build/TKQ1.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5419 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": f"{self.cookie}",
        }
        try:
            r = requests.get(
                "http://sx.shuxiangby.cn/index/mob/auth2.html?cos=1&pid=139715&code=061XYHll2xob7d4lrbml23bJZB1XYHlM&state=STATE",
                verify=False,
            )

            if r.history:
                for resp in r.history:
                    url = resp.headers["Location"]
                    self.domnainHost = urlparse(url).hostname
                            
            #print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")

            for i in range(3):
                r = requests.get(
                    f"http://{self.domnainHost}/index/mob/index.html",
                    headers = headers,
                    verify=False,
                )
             
                if r.history:
                    for resp in r.history:
                        if "open.weixin.qq.com" in resp.headers["Location"]:
                            print(f"账号[{self.name}] Cookie已过期!")
                            return False

            return True
        except ConnectionError as e:
            print("获取信息失败，重试...")
            time.sleep(1)
            self.run()
        except Exception as e:
            print(f"账号[{self.name}]初始化失败,请检查你的ck")
            return False

    def run(self):
        """
        运行任务流程

        Args:
        - self: 类实例本身

        Returns:
        - None
        """
        if self.init():  # 初始化账号信息
            self.read()  # 开始阅读文章
            #if use_tx:
            #    self.withdraw()  # 进行提现操作    




if __name__ == "__main__":
    # 从环境变量中获取账号信息
    accounts = os.getenv("s_ddz")
    wx_cloud = os.getenv("wx_cloud")
    use_tx = False
    wx_list = ""
    #if os.getenv("wx_list") and os.getenv("wx_cloud"):
    #    wx_list = os.getenv("wx_list").split('\n')[0].split('#')[1]
    #    print(f"🚀启用提现功能，提取{wx_list}的code参数！")
    #    use_tx = True
    #else:
    #    print("⚠️无ipad过检云端参数，关闭提现功能")


    inviteUrl = "http://u5a.cn/28ClC"

    if accounts is None:
        # 如果账号信息未配置，则打印提示信息并展示邀请链接
        print("未找到环境变量！")
    else:
        # 如果账号信息已配置，则解析账号信息并执行任务
        accounts_list = os.environ.get("s_ddz").split("\n")
        num_of_accounts = len(accounts_list)
        # 打印账号数量和邀请链接
        print(f"⚠️提示：获取到 {num_of_accounts} 个账号⚠️\n最新入口：{inviteUrl}")
        print("-" * 50)
        for i, account in enumerate(accounts_list, start=1):
            values = account.split("#")
            cg = {
                "name": values[0]+"]"+"["+str(i),
                "cookie": values[1],
                "txbz": values[2],
                "appToken": values[3],
                "topicId": values[4],
                "aliName": values[5],
                "aliAccount": values[6],
                "wxid": wx_list,
                "wx_cloud": wx_cloud
            }
            a = Main(cg)
            a.init()
            a.gold()

        for i, account in enumerate(accounts_list, start=1):
            print("*" * 49)
            print(f"账号[{account.split('#')[0]}][{i}]开始执行任务 >>>")

            # 解析账号信息
            values = account.split("#")
            cg = {
                "name": values[0]+"]"+"["+str(i),
                "cookie": values[1],
                "txbz": values[2],
                "appToken": values[3],
                "topicId": values[4],
                "aliName": values[5],
                "aliAccount": values[6],
                "wxid": wx_list,
                "wx_cloud": wx_cloud
            }

            try:
                # 实例化并执行任务
                if (cg["appToken"].startswith("AT_") == False) or (cg["topicId"].isdigit() == False):
                    print(f"账号[{account.split('#')[0]}][{i}] wxpush 配置错误！")
                    continue
                api = Main(cg)
                api.run()
            except Exception as e:
                print(f"账号[{account.split('#')[0]}][{i}] 出错啦:",e)
                continue
            print(f"账号[{account.split('#')[0]}][{i}]执行任务完毕！")
