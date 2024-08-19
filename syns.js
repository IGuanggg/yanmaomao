
/*
------------------------------------------
@Description: 所有女生小程序
------------------------------------------
变量名wawo
变量值 https://7.wawo.cc/api/  域名Headers请求头里面的authorization 去掉bearer  多账号&或换行或新建同名变量
[Script]
http-response

[MITM]
hostname = 

*/

const $ = new Env("所有女生会员中心");
let ckName = `wawo`;
let userCookie = checkEnv(
    ($.isNode() ? process.env[ckName] : $.getdata(ckName)) || ""
);
const notify = $.isNode() ? require("./sendNotify") : "";

!(async () => {
    console.log(
        `==================================================\n 脚本执行 - 北京时间(UTC+8): ${new Date(
            new Date().getTime() +
            new Date().getTimezoneOffset() * 60 * 1000 +
            8 * 60 * 60 * 1000
).toLocaleString()} \n==================================================`
);
    //console.log(userCookie)
    if (!userCookie?.length) return console.log(`没有找到CK哦`);
    let index = 1;
    let strSplitor = "#";

    for (let user of userCookie) {
        $.log(`\n🚀 user:【${index}】 start work\n`);
        index++
        $.token = user
        $.ckStatus = true;
        await getPoints()
        await signInInfo()
    }

    await $.sendMsg($.logs.join("\n"));
})()
    .catch((e) => console.log(e))
    .finally(() => $.done());
async function getPoints() {
    const config =
    {
        url: 'https://7.wawo.cc/api/score/wx/score/queryAmount',
        headers: {
            "content-type": "application/json",
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'bearer ' + $.token,
            'content-type': 'application/json',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'xweb_xhr': '1',
            "referer": `https://servicewechat.com/wx7d1403fe84339669/1038/page-frame.html`,
            "user-agent": `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555`

        }
    }
    let { data: result } = await Request(config)

    if (result?.code == "000") {
        $.log(`账号当前积分[${result.data}]`)
    } else {
        $.log(`账号积分查询失败[${result.message}]`)
    }
}
async function signInInfo() {
    const config =
    {
        url: 'https://7.wawo.cc/api/activity/wx/task/sign/signMsg',
        method: "POST",
        headers: {
            "content-type": "application/json",
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'bearer ' + $.token,
            'content-type': 'application/json',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'xweb_xhr': '1',
            "referer": `https://servicewechat.com/wx7d1403fe84339669/1038/page-frame.html`,
            "user-agent": `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555`

        },
        data: JSON.stringify({
            "cardNo": "411886986591633408"
        })
    }
    let { data: result } = await Request(config)

    if (result?.code == "000") {
        if (result.data.signed !== 1) {
            $.log(`未签到 ===> 签到ing`)
            await signIn()
        } else {
            $.log(`已签到 ===> 跳过签到`)
        }
    } else {
        $.log(`获取签到信息失败[${result.message}]`)
    }
}
async function signIn() {
    const config =
    {
        url: 'https://7.wawo.cc/api/activity/wx/task/sign/signIn',
        method: "POST",
        headers: {
            "content-type": "application/json",
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'bearer ' + $.token,
            'content-type': 'application/json',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'xweb_xhr': '1',
            "referer": `https://servicewechat.com/wx7d1403fe84339669/1038/page-frame.html`,
            "user-agent": `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555`

        },
        data: JSON.stringify({})
    }
    let { data: result } = await Request(config)

    if (result?.code == "000") {
        $.log(`签到成功`)
    } else {
        $.log(`签到失败[${result.message}]`)
    }
}

async function done(taskId) {
    const config =
    {
        url: 'https://7.wawo.cc/api/operate/wx/rewards/task/done?taskId=' + taskId,
        method: "POST",

        headers: {
            "content-type": "application/json",
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'bearer ' + $.token,
            'content-type': 'application/json',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'xweb_xhr': '1',
            "referer": `https://servicewechat.com/wx7d1403fe84339669/1038/page-frame.html`,
            "user-agent": `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555`

        },
        data: JSON.stringify({ "taskId": taskId })
    }
    let { data: result } = await Request(config)

    if (result?.code == "000") {
        $.log(`任务成功`)
    } else {
        $.log(`任务失败[${result.message}]`)
    }
}


function checkEnv(userCookie) {
    const envSplitor = ["&", "\n"];
    //console.log(userCookie);
    let userList = userCookie
        .split(envSplitor.find((o) => userCookie.includes(o)) || "&")
        .filter((n) => n);
    console.log(`共找到${userList.length}个账号`);
    return userList;
}
// prettier-ignore
function Env(t, s) { return new (class { constructor(t, s) { this.name = t; this.logs = []; this.logSeparator = "\n"; this.startTime = new Date().getTime(); Object.assign(this, s); this.log("", `\ud83d\udd14${this.name},\u5f00\u59cb!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } queryStr(options) { return Object.entries(options).map(([key, value]) => `${key}=${typeof value === "object" ? JSON.stringify(value) : value}`).join("&") } getURLParams(url) { const params = {}; const queryString = url.split("?")[1]; if (queryString) { const paramPairs = queryString.split("&"); paramPairs.forEach((pair) => { const [key, value] = pair.split("="); params[key] = value }) } return params } isJSONString(str) { try { return JSON.parse(str) && typeof JSON.parse(str) === "object" } catch (e) { return false } } isJson(obj) { var isjson = typeof obj == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length; return isjson } async sendMsg(message) { if (!message) return; if (this.isNode()) { await notify.sendNotify(this.name, message) } else { this.msg(this.name, "", message) } } randomNumber(length) { const characters = "0123456789"; return Array.from({ length }, () => characters[Math.floor(Math.random() * characters.length)]).join("") } randomString(length) { const characters = "abcdefghijklmnopqrstuvwxyz0123456789"; return Array.from({ length }, () => characters[Math.floor(Math.random() * characters.length)]).join("") } uuid() { return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) { var r = (Math.random() * 16) | 0, v = c == "x" ? r : (r & 0x3) | 0x8; return v.toString(16) }) } time(t) { let s = { "M+": new Date().getMonth() + 1, "d+": new Date().getDate(), "H+": new Date().getHours(), "m+": new Date().getMinutes(), "s+": new Date().getSeconds(), "q+": Math.floor((new Date().getMonth() + 3) / 3), S: new Date().getMilliseconds(), }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (new Date().getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in s) { new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? s[e] : ("00" + s[e]).substr(("" + s[e]).length))) } return t } msg(title = t, subtitle = "", body = "", options) { const formatOptions = (options) => { if (!options) { return options } else if (typeof options === "string") { if (this.isQuanX()) { return { "open-url": options } } else { return undefined } } else if (typeof options === "object" && (options["open-url"] || options["media-url"])) { if (this.isQuanX()) { return options } else { return undefined } } else { return undefined } }; if (!this.isMute) { if (this.isQuanX()) { $notify(title, subtitle, body, formatOptions(options)) } } let logs = ["", "==============📣系统通知📣=============="]; logs.push(title); subtitle ? logs.push(subtitle) : ""; body ? logs.push(body) : ""; console.log(logs.join("\n")); this.logs = this.logs.concat(logs) } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, s) { const e = !this.isQuanX(); e ? this.log("", `\u2757\ufe0f${this.name},\u9519\u8bef!`, t.stack) : this.log("", `\u2757\ufe0f${this.name},\u9519\u8bef!`, t) } wait(t) { return new Promise((s) => setTimeout(s, t)) } done(t = {}) { const s = new Date().getTime(), e = (s - this.startTime) / 1e3; this.log("", `\ud83d\udd14${this.name},\u7ed3\u675f!\ud83d\udd5b ${e}\u79d2`); this.log(); if (this.isNode()) { process.exit(1) } if (this.isQuanX()) { $done(t) } } })(t, s) }

async function Request(options) {
    if ($.isNode()) {
        const axios = require("axios");
        Request = async (options) => {
            try {
                return await axios.request(options);
            } catch (error) {
                return error && error.error ? error.error : "请求失败";
            }
        };
    }
    if ($.isQuanX()) {
        Request = async (options) => {
            try {
                return await $task.fetch(options);
            } catch (error) {
                return error && error.error ? error.error : "请求失败";
            }
        };
    }
    return await Request(options);
}
