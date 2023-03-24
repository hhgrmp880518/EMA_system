# EMA System
這是由 EMA 團隊開發的數學詳解影音動畫生成系統。

## 環境安裝
### VScode
> [下載 VScode 1.76](https://code.visualstudio.com/Download) 或更高版本

### Python
> [下載 Python 3.7](https://www.python.org/downloads) 或更高版本

### Node.js
> [下載 Node.js 6.0.0](https://nodejs.org/zh-tw/download) 或更高版本

### FFmpeg
> [下載 FFmpeg](https://www.wikihow.com/Install-FFmpeg-on-Windows)

### MiKTeX
> [下載 MiKTeX](https://miktex.org/download)

## 函式庫安裝

### Python
* Manim
```sh
$ pip install manim #v0.17.2
$ pip install PyExecJS
```
* LINE Bot
```sh
$ pip install requests
$ pip install flask
$ pip install line-bot-sdk
```

### Node.js

```sh
$ npm install mathsteps
```

## 檔案結構
EMA System 對於檔案路徑極為敏感，請遵守以下檔案結構：
> ⚠️請將 `static` 新增到 `EMA_system` 之下
>
> ⚠️請將 `config.ini` 新增到 `EMA_system` 之下

```sh
/EMA_system
|—— EMA.py
    .
    .
    .
|—— static
   |—— <user_id>.mp4
   |—— <user_id>.png
|—— config.ini
```

### _`config.ini`_

存放 LINE Bot 敏感資訊

檔案需要添加以下內容：
> ⚠️請將 `<your access token>`, `<your secret>`, `<your webhook url>` 替換為您個人的資訊
```sh
[line-bot]
channel_access_token = <your access token> 
channel_secret = <your secret>
webhook_url = <your webhook url>
```

### _`static`_
空白資料夾