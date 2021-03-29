# REAPER 社区机器人应答匹配

*reabot.csv* 文件是用于社区（QQ 群：243473647）自助应答机器人 **Reabot** 的关键词匹配字典。

- 建议使用文本编辑工具（例如 Atom，Notepad++ 等）来编辑字典。
- 不建议使用 WPS Office 编辑，因为 Ryusa 发现打开之后全是乱码。

## 目录构成

### faq.csv

其实下载 *.csv* 文件看一下格式就会知道如何编辑啦。

无论是单行还是多行内容，answer 列都应用英文双引号`"`将多行内容包括起来。

在英文双引号里的内容若需要换行，直接换行即可，**不需要加\n**。

### img

img 文件夹为存放图片的目录，

## faq.csv 用法

- name

  为匹配的关键词，目前为完全匹配。

- desc

  为该类目的描述，一般为解决问题的简介。

- answer

  为答案，默认是字符串，分行直接换行即可。

  图片需要使用[CQ码](https://docs.nonebot.dev/glossary.html#cq-%E7%A0%81)。

## 词条贡献者

<a href="https://github.com/REAPER-CN/reabot.REAPER-CN/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=REAPER-CN/reabot.REAPER-CN" />
</a>