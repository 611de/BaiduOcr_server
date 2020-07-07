import threading

from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import json
import requests
import base64
import webbrowser

app = Flask(__name__,static_folder="./dist/static",template_folder="./dist")
# CORS(app, supports_credentials=True)

@app.route('/', methods=['post','get'])
def index():
    return render_template('index.html')


# 请求图片的编码，相当于代理服务器，加上跨域的响应头
# 只有一个请求
@app.route('/general_ocr', methods=['post'])
def general_ocr():
    print('执行general_ocr()函数，处理通用识别')
    # 接受请求，分离请求体
    data = request.get_data()  # data类型是bytes
    print(type(data))
    # print(data)
    data = json.loads(data)  # 转化为json
    token = data["access_token"]  # 提取数据
    image = data["image"]
    print(token, image)
    # 向百度发出请求
    # r = requests.get("http://www.baidu.com") # 测试  https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic
    # print(r) # 测试
    send_data = {"image": image}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = requests.post("https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic", params='access_token=' + token,
                      data=send_data,headers=headers)
    print(r)
    print(r.text)
    print(r.content)
    print(r.json())
    # 接受响应
    # 加上跨域响应头，返回

    return r.json(),200,{"Access-Control-Allow-Origin":"*","Access-Control-Allow-Method":"*","Access-Control-Allow-Headers":"*"}# 响应体，状态码，响应头


if __name__ == '__main__':
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # # 二进制方式打开图片文件
    # f = open(r'C:\Users\611的\Pictures\无标题.png', 'rb')
    # img = base64.b64encode(f.read())
    # print(img)
    # params = {"image":img}
    # access_token = '24.0d1db53aa4337d74ec6632d11d354ffc.2592000.1588002642.282335-18012314'
    # request_url = request_url + "?access_token=" + access_token
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    # response = requests.post(request_url, data=params, headers=headers)
    # if response:
    #     print (response.json())
    url = "http://127.0.0.1:5000"
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    app.run(debug=False,host='::',port=5000) # ipv6可以访问，ipv4也可以访问

