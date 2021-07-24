<!--
 * @Date: 2021-03-26 21:21:27
 * @LastEditors: LIULIJING
 * @LastEditTime: 2021-07-24 22:06:42
-->
# MODIS NSIDC 冰雪数据集 Scrapy 爬虫

## 使用前配置需求

+ 修改 `cfg.py`完成配置，登录网站(https://urs.earthdata.nasa.gov/login)可能需要科学上网，确认登录端口，默认端口为`7890`  

+ 修改 `cfg.py`中的`FILES_STORE`以修改存储路径，注意 `Windows` 系统使用反斜杠`\`表示路径，并且注意使用双反斜杠`\\`转义

+ 注意：可以在用户目录下(Windows系统的 `C:\\用户\[默认用户]\.netrc`)配置用户密码，复制如下内容(网站为`urs.earthdata.nasa.gov`，尽量不要修改)，注意修改`USERNAME`、`PASSWORD`

```
machine urs.earthdata.nasa.gov                                              
login [USERNAME]
password [PASSWORD]
```

## 使用需要安装

+ `python3`运行环境，同样可以使用`Anaconda`环境

+ 安装`Scrapy`依赖环境，`pip install -r requirements.txt`

+ 运行`main.py`