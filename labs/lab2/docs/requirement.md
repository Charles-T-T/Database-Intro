# 实验二  DBMS软件安装及数据定义语句

## 一、实验目的

掌握常见DBMS软件安装及使用方法；

尝试简单的SQL定义语句。

## 二、实验内容和要求

实验内容：

1. 安装常见的DBMS软件，包括但不限于OpenGauss，MySQL，金仓数据库等。查阅帮助，了解其基本的使用方法。

   > 说明：机房电脑已经预装金仓数据库，若想尝试金仓数据库安装，可以使用自己的电脑。若希望安装OpenGauss，可以参考文件“在ECS上安装部署openGauss数据库指导手册”。

2. 在DBMS软件尝试教材例3.1、3.5、3.6和3.7。观察运行的结果。
3. 修改表的定义如下：
   - 学生的性别只能是男或女。
   - 学生出生年月必须是2020之前。
   - 学生学号必须以’20’开头。
   - 课程开课学期必须是四个数字加字母S或F，如‘2023F’, ‘2023S’。
   - 在学生表增加一列，email，并根据email地址格式要求增加约束条件。

## 三、实验重点和难点

实验重点：安装使用DBMS软件。