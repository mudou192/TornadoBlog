# TornadoBlog
16年1月写的

当时看了点Tornado源码(现在都忘的差不多了)，想练练手，加上刚买了VPS，除了上下google放在那感觉浪费，就花了几个周末自己做了一个博客玩玩。

功能比较简单，模板是网上找的，然后自己改了改。评论用的是多说，编辑器用的是CK-Editor配置了语法高亮及图片上传，数据库Mysql（Mysql只保存了博客关系，内容保存在本地，其实应该全保存在数据库的，这样移植也方便些）

自己用了一年，中间修改过三次

- 第一次被SQL注入
- 第二次添加设置页面
- 第三次添加保密/开放功能（产生一个BUG，当数据库中的文件在本地不存在会导致其他页面不能正常访问，很好改，取文件的时候判断下就行）

第三次还没改完，就换了Wordpress,前端不好，加上本来就是做着玩的，就当个Demo看看，跟 Wordpress 比占用资源挺少的——10M+（Wordpress都在200M以上）

个人博客:[http://zahuodian.me/](http://zahuodian.me/)

![image1](http://zahuodian.me/wp-content/uploads/2017/02/954de83f-7435-441c-8de5-7f8c7c83a2c3.jpg)

![image2](http://zahuodian.me/wp-content/uploads/2017/02/c7ddee27-665a-4b87-b225-e0ce569c284e.jpg)

![image3](http://zahuodian.me/wp-content/uploads/2017/02/dba5debf-5dd7-4578-b4b2-2a4218ba59ff.jpg)
