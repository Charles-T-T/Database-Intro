import pandas as pd
from prettytable import PrettyTable
import os
import sys
import time
from datetime import datetime


def df_to_table(df: pd.DataFrame):
    """ 将pd.dataframe转化为PrettyTable中更好展示的表格 """
    table = PrettyTable()
    table.field_names = df.columns
    for row in df.itertuples(index=False):
        table.add_row(row)
    return table


def clear_screen():
    """ 清屏 """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def input_legal_int(require: str, min_v: int, max_v: int) -> int:
    """ 从用户输入中获取合法操作数(int类型) """
    while True:
        try:
            value = int(input(require))
            if min_v <= value <= max_v:
                return value
            else:
                print(f"输入有误，请输入一个{min_v}到{max_v}之间的整数！")
        except ValueError:
            print(f"输入有误，请输入一个{min_v}到{max_v}之间的整数！")


class GoodsManager:
    """ 管理库存的类
        主要数据包括商品目录页和进销记录页
    """

    def __init__(self, goods_path: str, stock_path: str) -> None:
        """ 初始化
            读取商品目录和进销记录文件
            并以pd.dateframe的形式存储
        """
        self.goods_df = pd.read_excel(goods_path)
        self.stock_df = pd.read_excel(stock_path)
        self.stock_df['操作时间'] = pd.to_datetime(self.stock_df['操作时间']).dt.date

    # 库存管理
    op = {
        1: "进货",
        -1: "销售"
    }

    MIN_ID = 100001  # 商品最小编号
    MAX_ID = 200000  # 商品最大编号
    MAX_STOCK = 10000  # 单件商品最大库存

    def show_all_goods(self):
        """ 展示所有商品目录 """
        print(df_to_table(self.goods_df))

    def show_goods_list(self):
        """ 按类别组织商品目录并展示 """
        print("商品目录")
        groups = self.goods_df.groupby('类别')  # TODO 列名检查
        for kind, group in groups:
            print(kind)
            group.sort_values(by='库存量', ascending=False, inplace=True)
            print(df_to_table(group))
            print()

    def show_goods_by_kind(self, kind: str):
        """ 按类别查看商品 """
        df = self.goods_df
        group = df[df['类别'] == kind].sort_values(by='库存量', ascending=False)
        if group.empty:
            print("抱歉，该商品类别不存在！")
            print("当前商品目录中的商品类别有：", df['类别'].unique())
        else:
            print(df_to_table(group))

    def delete_by_id(self, id: int): 
        """ 按商品编号从目录中删除商品 """
        df = self.goods_df
        if id not in df['商品编号'].values:
            print("该商品编号不存在！")
        else:
            df.drop(df[df['商品编号'] == id].index, inplace=True)

    def update_stock(self, id: int, change: int):
        """ 更新目录中的商品库存量 """
        df = self.goods_df
        df.loc[df['商品编号'] == id, '库存量'] += change

    def add_new_goods(self, id: int, name: str, kind: str, count: int):
        """ 向目录中添加新商品 """
        df = self.goods_df
        df.loc[len(df)] = [id, name, kind, count]

    def show_all_record(self):
        """ 打印所有进销记录（默认按时间） """
        print(df_to_table(self.stock_df))

    def record_stock(
            self,
            id: int, name: str, type: int,
            person: str, time: datetime.date, count: int):
        """ 录入进销记录 """
        df1 = self.stock_df
        df1.loc[len(df1)] = [id, name, self.op[type], person, time, count]

    def show_main_menu(self):  
        """ 主菜单 """
        print("----------------------")
        print("    商城库存管理系统   ")
        print("----------------------")
        print(" 1. 商品目录查看")
        print(" 2. 记录库存变动")
        print(" 3. 从目录中删除商品")
        print(" 4. 按类别查看商品")
        print(" 5. 进销记录查询")
        print(" 6. 销量汇总")
        print(" 0. 退出系统")
        print("----------------------")

        choice = input_legal_int("> 请选择要进行的操作(0-6): ", 0, 6)
        clear_screen()
        match choice:
            case 0:
                print("> 欢迎下次使用，再见！")
                sys.exit()
            case 1:
                self.func1()
            case 2:
                self.func2()
            case 3:
                self.func3()
            case 4:
                self.func4()
            case 5:
                self.func5()
            case 6:
                self.func6()
            case _:
                print("still developing...")
                time.sleep(0.5)
                clear_screen()
        input("> 按回车键继续...")

    def func1(self):
        """ 功能1-商品目录查看 """
        clear_screen()
        self.show_goods_list()

    def func2(self):
        """ 功能2-记录库存变动 """
        clear_screen()
        # todo 错误情况判断
        df = self.goods_df
        id = input_legal_int("> 请输入商品编号：", self.MIN_ID, self.MAX_ID)
        if id not in df['商品编号'].values:
            print("该商品编号不存在，是否作为新商品添加？")
            choice = input_legal_int("> (1:是，继续添加; 0:否，返回主菜单): ", 0, 1)
            if choice == 0:
                return
            name = input("> 请输入商品名称：")
            kind = input("> 请输入商品类别名: ")
            print("新商品默认操作类型为“进货”，已自动记录")
            type = 1
        else:
            name = df.loc[df['商品编号'] == id, '商品名称'].iloc[0]
            kind = df.loc[df['商品编号'] == id, '类别'].iloc[0]
            type = input_legal_int("> 请选择操作类型(1:进货, 2:销售): ", 1, 2)
        person = input("> 请输入操作人姓名：")
        count = input_legal_int("> 请输入操作数量：", 0, self.MAX_STOCK)
        time = datetime.now().date()  # 自动记录操作日期

        if id in df['商品编号'].values:
            if type == 2 and count > df.loc[df['商品编号'] == id, '库存量'].iloc[0]:
                print("库存量不足！")
                return
            self.update_stock(id, type * count)
        else:
            self.add_new_goods(id, name, kind, count)

        self.record_stock(id, name, 3 - 2 * type, person, time, count)

    def func3(self):
        """ 功能3-从目录中删除商品 """
        id = input_legal_int("> 请输入待删除商品的编号: ", self.MIN_ID, self.MAX_ID)
        self.delete_by_id(id)

    def func4(self):
        """ 功能4-按类别查询商品 """
        kind = input("> 请输入要查看的商品类型：")
        self.show_goods_by_kind(kind)

    def func5(self):
        """ 功能5-进销记录查询 """
        choice = input_legal_int("> 请选择查询方式(1:所有记录, 2:某一商品的记录): ", 1, 2)
        if choice == 1:
            self.show_all_record()
            return

        df = self.stock_df
        while True:
            id = input_legal_int("> 请输入待查询商品的编号：", self.MIN_ID, self.MAX_ID)
            if id not in df['商品编号'].values:
                print("抱歉，该商品编号不存在！")
            else:
                target = df.loc[df["商品编号"] == id]
                break

        type = input_legal_int("> 请输入要查询的记录类型(1:进货, 2:销售, 3:全部): ", 1, 3)
        if type != 3:
            target = target.loc[target['操作类型'] == self.op[3 - 2 * type]]

        time_choice = input_legal_int("> 是否要限定时间范围(1:是, 0:否): ", 0, 1)
        if time_choice == 1:
            print("请输入要查询的时间范围")
            print("起点：")
            y = input_legal_int("> 年：", 2000, datetime.now().date().year)
            m = input_legal_int("> 月：", 1, 12)
            d = input_legal_int("> 日：", 1, 31)
            start_date = datetime(y, m, d).date()

            print("终点：")
            y = input_legal_int("> 年：", 2000, datetime.now().date().year)
            m = input_legal_int("> 月：", 1, 12)
            d = input_legal_int("> 日：", 1, 31)
            end_date = datetime(y, m, d).date()

            # target = target.reset_index(drop=True)  # 重置索引
            target = target.loc[(target['操作时间'] >= start_date)
                                & (target["操作时间"] <= end_date)]

        person_choice = input_legal_int("> 是否要限定操作人(1:是, 0:否): ", 0, 1)
        if person_choice == 1:
            person = input("> 请输入要查询的操作人姓名：")
            target = target.loc[target['操作人'] == person]

        if target.empty:
            print("抱歉，查询结果为空！")
        else:
            print(df_to_table(target))

    def func6(self):
        """ 功能6-销量汇总（一定时间内的全部/某类/某个商品） """
        df1 = self.goods_df
        df2 = self.stock_df
        target = df2.loc[df2['操作类型'] == "销售"]

        choice = input_legal_int(
            "> 请选择销量汇总方式(1:全部商品, 2:按商品类别, 3:按商品编号): ", 1, 3)
        match choice:
            case 1:
                pass
            case 2:
                kinds = df1['类别'].unique()
                while True:
                    kind = input("> 请输入商品类别：")
                    if kind in kinds:
                        target_id_lst = df1[df1["类别"] == kind]['商品编号'].tolist()
                        break
                    else:
                        print("抱歉，该商品类别不存在！")
                        print("当前商品目录中的商品类别有：", kinds)
                target = target[target['商品编号'].isin(target_id_lst)]
            case 3:
                while True:
                    id = input_legal_int(
                        "> 请输入商品编号：", self.MIN_ID, self.MAX_ID)
                    if id not in df1['商品编号'].values:
                        print("抱歉，该商品编号不存在！")
                    else:
                        break
                target = target.loc[target["商品编号"] == id]

        time_choice = input_legal_int("> 是否要限定时间范围(1:是, 0:否): ", 0, 1)
        if time_choice == 1:
            print("请输入要查询的时间范围")
            print("起点：")
            y = input_legal_int("> 年：", 2000, datetime.now().date().year)
            m = input_legal_int("> 月：", 1, 12)
            d = input_legal_int("> 日：", 1, 31)
            start_date = datetime(y, m, d).date()

            print("终点：")
            y = input_legal_int("> 年：", 2000, datetime.now().date().year)
            m = input_legal_int("> 月：", 1, 12)
            d = input_legal_int("> 日：", 1, 31)
            end_date = datetime(y, m, d).date()

            # target = target.reset_index(drop=True)  # 重置索引
            target = target.loc[(target['操作时间'] >= start_date)
                                & (target["操作时间"] <= end_date)]

        print("总销量为：", target['操作数量'].sum())


def main():
    manager = GoodsManager("../data/goods.xlsx", "../data/new_stock.xlsx")
    while 1:
        clear_screen()
        manager.show_main_menu()


if __name__ == "__main__":
    main()