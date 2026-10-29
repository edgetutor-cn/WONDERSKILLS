# -*- coding: utf-8 -*-
"""开启/查询 WONDERSKILLS 仓库 GitHub Pages（运行时从 .git/config 读取 token，不回显）。"""
import configparser, json, urllib.request, urllib.error, os

cp = configparser.ConfigParser()
cp.read('.git/config')
url = cp.get('remote "origin"', 'url')
# https://<token>@github.com/edgetutor-cn/WONDERSKILLS.git
token = url.split('https://', 1)[1].split('@', 1)[0]
repo = url.split('github.com/', 1)[1].replace('.git', '')

API = f'https://api.github.com/repos/{repo}/pages'
HDR = {'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
       'User-Agent': 'wonderskills-deploy'}

def req(method, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API, data=data, method=method, headers=HDR)
    try:
        resp = urllib.request.urlopen(r)
        return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

# 先尝试开启（已开启会返回 409）
st, txt = req('POST', {"source": {"branch": "master", "path": "/"}})
print('POST pages status:', st)
# 查询状态
st2, txt2 = req('GET')
print('GET pages status:', st2)
try:
    j = json.loads(txt2)
    print('pages status field:', j.get('status'), '| url:', j.get('html_url'))
except Exception:
    print('GET body:', txt2[:200])
