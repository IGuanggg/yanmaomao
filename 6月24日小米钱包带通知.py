# 百度搜索小米账号，抓包即可
# cron "30 10 * * *" script-path=xiaomi/小米钱包.py, tag=小米钱包
# 适用: 青龙面板

import os
import time
import random
import requests
import urllib3
from datetime import datetime
from typing import Optional, Dict, Any, Union
import json
# from notify import send


# 生成 0-15 的随机分钟延迟
# delay_minutes = random.randint(0, 15)
# print(f"随机延迟 {delay_minutes} 分钟")
# time.sleep(delay_minutes * 60)  # 转换为秒并延迟


# import sendNotify
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RnlRequest:
    def __init__(self, cookies: Union[str, dict]):
        self.session = requests.Session()
        self._base_headers = {
            'Host': 'm.jr.airstarfinance.net',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 14; zh-CN; M2012K11AC Build/UKQ1.230804.001; AppBundle/com.mipay.wallet; AppVersionName/6.89.1.5275.2323; AppVersionCode/20577595; MiuiVersion/stable-V816.0.13.0.UMNCNXM; DeviceId/alioth; NetworkType/WIFI; mix_version; WebViewVersion/118.0.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36 XiaoMi/MiuiBrowser/4.3',
        }
        self.update_cookies(cookies)

    def request(
            self,
            method: str,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Union[Dict[str, Any], str, bytes]] = None,
            json: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Optional[Dict[str, Any]]:
        headers = {**self._base_headers, **kwargs.pop('headers', {})}
        try:
            resp = self.session.request(
                verify=False,
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                **kwargs
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[Request Error] {e}")
            return None
        except ValueError as e:
            print(f"[JSON Parse Error] {e}")
            return None

    def update_cookies(self, cookies: Union[str, dict]) -> None:
        if cookies:
            if isinstance(cookies, str):
                dict_cookies = self._parse_cookies(cookies)
            else:
                dict_cookies = cookies
            self.session.cookies.update(dict_cookies)
            self._base_headers['Cookie'] = self.dict_cookie_to_string(dict_cookies)

    @staticmethod
    def _parse_cookies(cookies_str: str) -> Dict[str, str]:
        return dict(
            item.strip().split('=', 1)
            for item in cookies_str.split(';')
            if '=' in item
        )

    @staticmethod
    def dict_cookie_to_string(cookie_dict):
        cookie_list = []
        for key, value in cookie_dict.items():
            cookie_list.append(f"{key}={value}")
        return "; ".join(cookie_list)

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[Dict[str, Any]]:
        return self.request('GET', url, params=params, **kwargs)

    def post(self, url: str, data: Optional[Union[Dict[str, Any], str, bytes]] = None,
             json: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[Dict[str, Any]]:
        return self.request('POST', url, data=data, json=json, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class RNL:
    def __init__(self, c):
        self.t_id = None
        self.options = {
            "task_list": True,
            "complete_task": True,
            "receive_award": True,
            "task_item": True,
            "UserJoin": True,
        }
        self.activity_code = '2211-videoWelfare'
        self.rr = RnlRequest(c)
        self.current_user_id = None  # 存储当前处理的用户ID
        self.total_days = "未知"
        self.today_records = []
        self.error_info = ""

    def get_task_list(self):
        data = {
            'activityCode': self.activity_code,
        }
        try:
            response = self.rr.post(
                'https://m.jr.airstarfinance.net/mp/api/generalActivity/getTaskList',
                data=data,
            )
            if response and response['code'] != 0:
                self.error_info = f"获取任务列表失败：{response}"
                print(self.error_info)
                return None
            target_tasks = []
            for task in response['value']['taskInfoList']:
                if '浏览组浏览任务' in task['taskName']:
                    target_tasks.append(task)
            return target_tasks
        except Exception as e:
            self.error_info = f'获取任务列表失败：{e}'
            print(self.error_info)
            return None

    def get_task(self, task_code):
        try:
            data = {
                'activityCode': self.activity_code,
                'taskCode': task_code,
                'jrairstar_ph': '98lj8puDf9Tu/WwcyMpVyQ==',
            }
            response = self.rr.post(
                'https://m.jr.airstarfinance.net/mp/api/generalActivity/getTask',
                data=data,
            )
            if response and response['code'] != 0:
                self.error_info = f'获取任务信息失败：{response}'
                print(self.error_info)
                return None
            return response['value']['taskInfo']['userTaskId']
        except Exception as e:
            self.error_info = f'获取任务信息失败：{e}'
            print(self.error_info)
            return None

    def complete_task(self, task_id, t_id, brows_click_urlId):
        try:
            response = self.rr.get(
                f'https://m.jr.airstarfinance.net/mp/api/generalActivity/completeTask?activityCode={self.activity_code}&app=com.mipay.wallet&isNfcPhone=true&channel=mipay_indexicon_TVcard&deviceType=2&system=1&visitEnvironment=2&userExtra=%7B%22platformType%22:1,%22com.miui.player%22:%224.27.0.4%22,%22com.miui.video%22:%22v2024090290(MiVideo-UN)%22,%22com.mipay.wallet%22:%226.83.0.5175.2256%22%7D&taskId={task_id}&browsTaskId={t_id}&browsClickUrlId={brows_click_urlId}&clickEntryType=undefined&festivalStatus=0',
            )
            if response and response['code'] != 0:
                self.error_info = f'完成任务失败：{response}'
                print(self.error_info)
                return None
            return response['value']
        except Exception as e:
            self.error_info = f'完成任务失败：{e}'
            print(self.error_info)
            return None

    def receive_award(self, user_task_id):
        try:
            response = self.rr.get(
                f'https://m.jr.airstarfinance.net/mp/api/generalActivity/luckDraw?imei=&device=manet&appLimit=%7B%22com.qiyi.video%22:false,%22com.youku.phone%22:true,%22com.tencent.qqlive%22:true,%22com.hunantv.imgo.activity%22:true,%22com.cmcc.cmvideo%22:false,%22com.sankuai.meituan%22:true,%22com.anjuke.android.app%22:false,%22com.tal.abctimelibrary%22:false,%22com.lianjia.beike%22:false,%22com.kmxs.reader%22:true,%22com.jd.jrapp%22:false,%22com.smile.gifmaker%22:true,%22com.kuaishou.nebula%22:false%7D&activityCode={self.activity_code}&userTaskId={user_task_id}&app=com.mipay.wallet&isNfcPhone=true&channel=mipay_indexicon_TVcard&deviceType=2&system=1&visitEnvironment=2&userExtra=%7B%22platformType%22:1,%22com.miui.player%22:%224.27.0.4%22,%22com.miui.video%22:%22v2024090290(MiVideo-UN)%22,%22com.mipay.wallet%22:%226.83.0.5175.2256%22%7D'
            )
            if response and response['code'] != 0:
                self.error_info = f'领取奖励失败：{response}'
                print(self.error_info)
        except Exception as e:
            self.error_info = f'领取奖励失败：{e}'
            print(self.error_info)

    def queryUserJoinListAndQueryUserGoldRichSum(self):
        try:
            total_res = self.rr.get(
                'https://m.jr.airstarfinance.net/mp/api/generalActivity/queryUserGoldRichSum?app=com.mipay.wallet&deviceType=2&system=1&visitEnvironment=2&userExtra={"platformType":1,"com.miui.player":"4.27.0.4","com.miui.video":"v2024090290(MiVideo-UN)","com.mipay.wallet":"6.83.0.5175.2256"}&activityCode=2211-videoWelfare')
            if not total_res or total_res['code'] != 0:
                self.error_info = f'获取兑换视频天数失败：{total_res}'
                print(self.error_info)
                return False
            self.total_days = f"{int(total_res['value']) / 100:.2f}天" if total_res else "未知"

            response = self.rr.get(
                f'https://m.jr.airstarfinance.net/mp/api/generalActivity/queryUserJoinList?&userExtra=%7B%22platformType%22:1,%22com.miui.player%22:%224.27.0.4%22,%22com.miui.video%22:%22v2024090290(MiVideo-UN)%22,%22com.mipay.wallet%22:%226.83.0.5175.2256%22%7D&activityCode={self.activity_code}&pageNum=1&pageSize=20',
            )
            if not response or response['code'] != 0:
                self.error_info = f'查询任务完成记录失败：{response}'
                print(self.error_info)
                return False

            history_list = response['value']['data']
            current_date = datetime.now().strftime("%Y-%m-%d")

            # 清空记录
            self.today_records = []

            for a in history_list:
                record_time = a['createTime']
                record_date = record_time[:10]
                if record_date == current_date:
                    self.today_records.append({
                        'createTime': record_time,
                        'value': a['value']
                    })

            return True
        except Exception as e:
            self.error_info = f'获取任务记录失败：{e}'
            print(self.error_info)
            return False

    def main(self):
        if not self.queryUserJoinListAndQueryUserGoldRichSum():
            return False
        for i in range(2):
            # 获取任务列表
            tasks = self.get_task_list()
            if not tasks:
                return False

            task = tasks[0]
            try:
                t_id = task['generalActivityUrlInfo']['id']
                self.t_id = t_id
            except:
                t_id = self.t_id
            task_id = task['taskId']
            task_code = task['taskCode']
            brows_click_url_id = task['generalActivityUrlInfo']['browsClickUrlId']

            time.sleep(13)

            # 完成任务
            user_task_id = self.complete_task(
                t_id=t_id,
                task_id=task_id,
                brows_click_urlId=brows_click_url_id,
            )

            time.sleep(2)

            # 获取任务数据
            if not user_task_id:
                user_task_id = self.get_task(task_code=task_code)
                time.sleep(2)

            # 领取奖励
            self.receive_award(
                user_task_id=user_task_id
            )

            time.sleep(2)

        # 重新获取最新记录
        self.queryUserJoinListAndQueryUserGoldRichSum()
        return True


def get_xiaomi_cookies(pass_token, user_id):
    session = requests.Session()
    login_url = 'https://account.xiaomi.com/pass/serviceLogin?callback=https%3A%2F%2Fapi.jr.airstarfinance.net%2Fsts%3Fsign%3D1dbHuyAmee0NAZ2xsRw5vhdVQQ8%253D%26followup%3Dhttps%253A%252F%252Fm.jr.airstarfinance.net%252Fmp%252Fapi%252Flogin%253Ffrom%253Dmipay_indexicon_TVcard%2526deepLinkEnable%253Dfalse%2526requestUrl%253Dhttps%25253A%25252F%25252Fm.jr.airstarfinance.net%25252Fmp%25252Factivity%25252FvideoActivity%25253Ffrom%25253Dmipay_indexicon_TVcard%252526_noDarkMode%25253Dtrue%252526_transparentNaviBar%25253Dtrue%252526cUserId%25253Dusyxgr5xjumiQLUoAKTOgvi858Q%252526_statusBarHeight%25253D137&sid=jrairstar&_group=DEFAULT&_snsNone=true&_loginType=ticket'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'cookie': f'passToken={pass_token}; userId={user_id};'
    }

    try:
        session.get(url=login_url, headers=headers, verify=False)
        cookies = session.cookies.get_dict()
        return f"cUserId={cookies.get('cUserId')};jrairstar_serviceToken={cookies.get('serviceToken')}"
    except Exception as e:
        error_msg = f"获取Cookie失败: {e}"
        print(error_msg)
        return None, error_msg


def generate_notification(account_id, rnl_instance,us):
    """生成格式化的通知消息"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    msg = f"""
【账号信息】

✨ 账号：{us} ID:{account_id}
📊 当前兑换视频天数：{rnl_instance.total_days}

📅 {current_date} 任务记录
{"-" * 40}"""

    for record in rnl_instance.today_records:
        record_time = record["createTime"]
        days = int(record["value"]) / 100
        msg += f"""
⏰ {record_time}
🎁 领到视频会员，+{days:.2f}天"""

    if rnl_instance.error_info:
        msg += f"""
⚠️ 执行异常：{rnl_instance.error_info}"""

    msg += f"""
{"=" * 40}"""

    return msg


if __name__ == "__main__":
    # 多账号配置区 ##################################
    try:
        with open("xiaomiconfig.json", "r", encoding="utf-8") as f:
            ORIGINAL_COOKIES = json.load(f)
        assert isinstance(ORIGINAL_COOKIES, list), "配置文件格式错误，应为账号字典列表"
    except Exception as e:
        print(f"读取xiaomiconfig.json失败: {e}")
        exit(1)
    # 结束配置 ######################################

    # 构建完整通知消息
    full_notification = "📺【小米钱包任务执行结果】\n"

    cookie_list = []
    if len(ORIGINAL_COOKIES) == 0:
        print("没有账号")
        exit(1)
    for account in ORIGINAL_COOKIES:
        data = account.get('data', {})
        us = data.get('us')
        owner_id = account.get('owner_id')
        user_id = data.get('userId')
        pass_token = data.get('passToken')
        security_token = data.get('securityToken')
        print(f"\n>>>>>>>>>> 正在处理账号 {us}id{user_id} <<<<<<<<<<")

        # 获取Cookie - 兼容原函数返回值
        cookie_result = get_xiaomi_cookies(pass_token, user_id)

        # 处理返回结果
        if isinstance(cookie_result, tuple):
            new_cookie, error = cookie_result
        else:
            new_cookie = cookie_result
            error = None

        # 创建RNL实例并设置当前用户ID
        rnl = RNL(new_cookie)
        rnl.current_user_id = user_id

        if error:
            rnl.error_info = error
        else:
            print(f"账号 {us} Cookie获取成功")
            cookie_list.append(new_cookie)

            # 执行主程序
            try:
                rnl.main()
            except Exception as e:
                rnl.error_info = f"执行异常: {str(e)}"
                print(rnl.error_info)

        # 生成当前账号的通知消息并添加到完整通知中
        account_notification = generate_notification(user_id, rnl,us)
        full_notification += account_notification

        # ========== 写入最新日志到data.log ==========
        try:
            with open("xiaomiconfig.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            for acc in config:
                data2 = acc.get("data", {})
                if data2.get("us") == us and acc.get("owner_id") == owner_id:
                    if "data" not in acc or not isinstance(acc["data"], dict):
                        acc["data"] = {}
                    acc["data"]["log"] = account_notification.strip()
                    break
            with open("xiaomiconfig.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"写入日志到data.log失败: {e}")

    # 添加汇总信息
    full_notification += f"""
📊 执行汇总：
✅ 成功账号数：{len(cookie_list)}
⚠️ 失败账号数：{len(ORIGINAL_COOKIES) - len(cookie_list)}
"""

    # 打印最终通知消息
    print(full_notification)

    # 此处可添加实际的消息推送代码
    # send("小米钱包任务推送", full_notification)
