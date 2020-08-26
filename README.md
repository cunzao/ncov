# 西安电子科技大学晨午晚检自动填报工具

本代码参考[HPShark/xdu_chenwuwanjian.git](https://github.com/HPShark/xdu_chenwuwanjian)和[abadfox233/ncov](https://github.com/abadfox233/ncov), [cunzao/ncov](https://github.com/cunzao/ncov)的作品。感谢大佬们的无私奉献。本代码仅供学术交流。

2020-08-26 更新日志：

1. 更人性化的设计：程序启动时立即上报一次。

2. 新增了随机初始化上报的时刻的功能。

3. 上报失败时，自动尝试重新上报(最大次数3次)；新增了每次上报后的冷却(cd)时间为180秒。

4. 除了南北校区外，新增了在校外的地点选择(出差模式)。

## 项目依赖

* python >= 3
* requests 库

## 使用方法

### Step 1 环境配置：安装requests库

Linux系统：

```bash
pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Windows系统：

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 2 运行

```bash
python3 index.py
```

### 编写 data/config.json 配置文件，格式如下

> python 字典的语法, '//'以后为注释。各个参数与选项皆已列出,每一项都是必填字段
```python
{
    "stuNum" : "123456789",   // 学号or工号
    "passWord" : "12345678",  // 密码
    "Location" : "1",         // 校区，1：北校区，0：南校区，其他：在校外
    "ServerToken" : ""        // server酱的token，用于消息提醒，非必填
}
```
server酱问题：使用server酱进行通知，先前往[server酱官网](http://sc.ftqq.com/)进行申请与绑定，得到一个server酱的Token，将此Token替换config.json里的token

### 配合腾讯云函数使用（免费）

没有云服务器的情况下，可以使用腾讯云函数。

1. 打开[腾讯云函数](https://console.cloud.tencent.com/scf/index?rid=1)，注册认证后，进入控制台，点击左边的层，然后点新建，名称随意，然后点击上传zip，选择项目中的`层文件.zip`上传，然后选择运行环境`python3.6`，然后点击确定，耐心等待一下，上传依赖包需要花费的时间比较长 

2. ![image-20200727162912337](./img/image-20200727162912337.png)

3. 点左边的函数服务，新建云函数，名称随意，运行环境选择`python3.6`，创建方式选择空白函数，然后点击下一步 

   ![image-20200727163011638](./img/image-20200727163011638.png)

4. 修改`执行方法`为：`index.index`，提交方法选择上传本地压缩包，把本地的/data，/utils，index.py打包上传，在点击下面的高级设置，设置内存为64M，超时时间为`30秒`，添加层为刚刚新建的函数依赖层，然后点击完成

   ![image-20200727163222470](./img/image-20200727163222470.png)

5. 进入新建好的云函数，左边点击触发管理，点击创建触发器，名称随意，触发周期选择自定义，然后配置cron表达式。下面的表达式表示每天八点半，十三点半和十八点半执行

   ```
   0 30 8,13,18 * * * *
   ```

6. 然后就可以测试云函数了，绿色代表云函数执行成功，红色代表云函数执行失败（失败的原因大部分是由于依赖造成的）。如遇到问题，请仔细查看日志，欢迎提ISSUE

7. enjoy it!

### 服务器使用

由自己的服务器的时候可以使用这个方法

配置好配置文件后运行

```bash
python3 index.py
```

至于如何后台运行请[百度一下](http://www.baidu.com/)？
