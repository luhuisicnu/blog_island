<pre>
项目：blog_island  #博客岛
简介：多人使用的博客平台

开发环境：
操作系统:CentOS 6.5
语言:python 2.6.6
数据库:mysql 5.6
框架:flask/bootstrap/Jinja2/sqlalchemy

本项目大致包含几个模块:
1，登录认证
    注册、登录、修改账户
2，权限管理
    多权限&多角色&多用户，并提供页面的权限和角色授予方式，以及账户禁用
3，内容审核
    对用户产生的任何自定义信息，内容管理员均具有禁用启用的便捷页面操作方式，但无权对其进行修改
4，博客管理
    项目的主要模块，引用了ckeditor页面编辑器
5，评论和关注
    互动模块，利用ORM数据模型管理其复杂关系
</pre>

