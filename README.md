# 西安电子科技大学晨午晚检自动填报工具

本代码参考 https://github.com/HPShark/xdu_chenwuwanjian.git 和 https://github.com/abadfox233/ncov 的作品。感谢大佬们的无私奉献。本代码仅供学术交流。

## 项目依赖

* python >= 3
* requests 库
## 使用方法
### 安装requests库

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

### 编写 data/config.json 配置文件，格式如下

> python 字典的语法, '//'以后为注释。各个参数与选项皆已列出,每一项都是必填字段
```python
{
    "stuNum" : "123456789", // 学号
    "passWord" : "12345678", // 密码
    "Location" : "1",  // 校区，1：北校区，其他：南校区
    "ServerToken" : "" // server酱的token，用于消息提醒，非必填
}
```
server酱问题：使用server酱进行通知，先前往[server酱官网](http://sc.ftqq.com/)进行申请与绑定，得到一个server酱的Token，将此Token替换config.json里的token

### 配合腾讯云函数使用（免费）

没有云服务器的情况下，可以使用腾讯云函数。

1. 配置好config.json内的参数，运行`python3 index.py`命令。**这一步是为了获取cookies.txt，如果云函数中的cookies失效了，重新上传一次cookies.txt即可。**

2. 打开[腾讯云函数](https://console.cloud.tencent.com/scf/index?rid=1)，注册认证后，进入控制台，点击左边的层，然后点新建，名称随意，然后点击上传zip，选择项目中的`层文件.zip`上传，然后选择运行环境`python3.6`，然后点击确定，耐心等待一下，上传依赖包需要花费的时间比较长 

3. ![image-20200727162912337](https://github.com/cunzao/ncov/raw/master/img/image-20200727162912337.png)

4. 点左边的函数服务，新建云函数，名称随意，运行环境选择`python3.6`，创建方式选择空白函数，然后点击下一步 

   ![image-20200727163011638](https://github.com/cunzao/ncov/raw/master/img/image-20200727163011638.png)

5. 修改`执行方法`为：`index.index`，提交方法选择上传本地压缩包，把本地的/data，/utils，index.py打包上传，在点击下面的高级设置，设置内存为64M，超时时间为`30秒`，添加层为刚刚新建的函数依赖层，然后点击完成

   ![image-20200727163222470](https://github.com/cunzao/ncov/raw/master/img/image-20200727163222470.png)

6. 进入新建好的云函数，左边点击触发管理，点击创建触发器，名称随意，触发周期选择自定义，然后配置cron表达式。下面的表达式表示每天八点零五分，十三点零五分和十八点零五分执行

   ```
   0 5 8,13,18 * * * *
   ```

7. 然后就可以测试云函数了，绿色代表云函数执行成功，红色代表云函数执行失败（失败的原因大部分是由于依赖造成的）。如遇到问题，请仔细查看日志，欢迎推pull request。

8. enjoy it!



### 服务器使用

由自己的服务器的时候可以使用这个方法

配置好配置文件后运行

```bash
python3 index.py
```

至于如何后台运行请百度一下？