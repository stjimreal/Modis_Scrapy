<!--
 * @Date: 2021-03-26 21:21:27
 * @LastEditors: LIULIJING
 * @LastEditTime: 2021-07-22 23:27:34
-->
# MODIS NSIDC 冰雪数据集 Scrapy 爬虫

## 使用前配置需求

修改 `configuration.json`完成配置，登录网站(https://urs.earthdata.nasa.gov/login)可能需要科学上网，确认登录端口，默认端口为`7890`  

修改 `settings.py`中的`FILES_STORE`以修改存储路径，注意 `Windows` 系统使用反斜杠`\`表示路径，并且注意使用双反斜杠`\\`转义(目前尚未实现在`configuration.json`当中直接配置保存路径)

## 使用需要安装

+ `python3`运行环境，同样可以使用`Anaconda`环境

+ 安装`Scrapy`依赖环境，`pip install -r requirements.txt`

+ 运行`main.py`