<!--
 * @Date: 2021-03-26 21:21:27
 * @LastEditors: LIULIJING
 * @LastEditTime: 2021-07-25 00:56:43
-->
# MODIS Scrapy 爬虫

## 使用前配置需求

+ 修改 `cfg.py`完成配置，[登录网站](https://urs.earthdata.nasa.gov/login)可能需要科学上网，确认**代理端口**，默认端口为`7890`  

+ 修改 `cfg.py`中的`FILES_STORE`以修改存储路径，注意 `Windows` 系统使用反斜杠`\`表示路径，并且注意使用双反斜杠`\\`转义

+ 注意：可以在用户目录下(Windows系统的 `C:\\用户\[默认用户]\.netrc`)配置用户密码，复制如下内容(网站为`urs.earthdata.nasa.gov`，尽量不要修改)，注意修改`USERNAME`、`PASSWORD`

```
machine urs.earthdata.nasa.gov                                              
login [USERNAME]
password [PASSWORD]
```

+ 目前经过测试的数据中心包括`NSIDC`, `LAADS`, `LPDAAC`，其中`LPDAAC`可能所有资源需要科学上网，可以在`pipeline.py`的`Request`中设置`meta={'proxy': 'PROXY_HERE'}`

+ **[RC]支持拼接转投裁剪一步完成** 使用`gdal`可输出`GTiff`格式文件，`cfg.py`中`turn_on_stitch_and_reproject`为`Yes`，按照注释提示修改配置选项即可。尚未在`Windows`系统进行测试，欢迎在[#issues](https://github.com/stjimreal/Modis_Scrapy/issues)上提出问题。

> ⚠️ 目前仅支持使用已经处理好的栅格数据作为`裁剪选区`、`转投影`、`重采样`(分别对应`bounding_box`，`coordination descriptions`，`resolution`参数)的掩膜条件，尚未支持矢量数据及描述文件完成配置。您可以使用[HEG工具](https://wiki.earthdata.nasa.gov/display/DAS/HEG%3A++HDF-EOS+to+GeoTIFF+Conversion+Tool)生成您的目标`tif`影像，并用于掩膜数据

## 使用需要安装

+ `python3`运行环境，同样可以使用`Anaconda`环境

+ 安装`Scrapy`依赖环境，`pip install -r requirements.txt`

+ 运行`main.py`

## 如果遇到问题欢迎在 [#issue](https://github.com/stjimreal/Modis_Scrapy/issues) 中提出！
