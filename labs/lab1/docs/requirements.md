# 实验一  基于文件系统的“商城库存管理”应用系统

## 一、实验目的
掌握使用文件系统存取数据的基本原理；  
理解文件系统中表达数据间关联的基本方法。

## 二、实验内容和要求

### 实验内容：
使用C/C++，Java，Python等高级编程语言，基于文件系统实现简单的“商城库存管理”应用。需要实现的应用功能包括：

- 商品目录查看：
实现一个查看商品目录的功能，要求商品按类别进行组织和展示。

- 库存管理（进货与销售）：
实现进货和销售功能，支持根据商品编号增减库存。每条进货或销售记录应包括以下信息：商品编号、商品名称、操作类型（进货或销售）、操作人、操作时间和操作数量。

- 商品删除：
实现删除指定编号商品的功能，删除后保留该商品的进货和销售记录。

- 按类别浏览与库存排序：
实现按类别浏览商品功能，支持查看某类别下的所有商品，并按库存量多少排序展示。

- 进销记录查询：
针对某一商品，实现进货和销售记录的查询功能，支持按时间范围或操作人进行检索。

- 销量汇总：
实现销量汇总功能，能够查询在一定时间范围内全部商品或某类商品的总销量。

### 其他要求：  

1. 检查录入数据的正确性，比如时间格式，库存数量等。  
2. 允许使用AI来辅助编程，但必须独立完成。代码会进行软件查重，重复率过高需要合理解释。  

数据集由学生根据系统需求自行设计和生成。数据集应包含必要的商品信息、进销记录等内容，以确保系统功能的正常实现

## 三、实验重点和难点
实验重点：使用文件系统实现数据的增、删、查等操作。  
实验难点：选择合适的数据结构实现数据的存取管理。  