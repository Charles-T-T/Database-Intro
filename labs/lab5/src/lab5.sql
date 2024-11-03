-- 1. 安全性实验
-- 1.1 教材实验
-- 创建用户
CREATE USER 'U1'@'localhost';
CREATE USER 'U2'@'localhost';
CREATE USER 'U3'@'localhost';
CREATE USER 'U4'@'localhost';

-- 把查询Student表的权限授给用户U1
GRANT SELECT
ON Student
TO 'U1'@'localhost';

-- 把对Student表和Course表的全部操作权限授予用户U2和U3
GRANT ALL PRIVILEGES
ON Student
TO 'U2'@'localhost', 'U3'@'localhost';
GRANT ALL PRIVILEGES
ON Course
TO 'U2'@'localhost', 'U3'@'localhost';

-- 把对表SC的查询权限授予所有用户
GRANT SELECT
ON SC
TO 'U1'@'localhost', 'U2'@'localhost', 'U3'@'localhost', 'U4'@'localhost';

-- 把查询Student表和修改学生学号的权限授予用户U4
GRANT SELECT, UPDATE(Sno)
ON Student
TO 'U4'@'localhost';

-- 把对表SC的INSERT权限授予U5用户，并允许将此授权再授予其他用户
CREATE USER 'U5'@'localhost';
GRANT INSERT 
ON SC
TO 'U5'@'localhost'
WITH GRANT OPTION;

-- 用户U5将对表SC的INSERT权限授予用户U6（允许再授权）
-- mysql -u root -p
-- CREATE USER 'U6'@'localhost';
-- exit
-- mysql -u U5
GRANT INSERT
ON SC
TO 'U6'@'localhost'
WITH GRANT OPTION;

-- 同样，U6还可以将此权限继续授予U7
-- mysql -u root -p
-- CREATE USER 'U7'@'localhost';
-- exit
-- mysql -u U6
GRANT INSERT
ON SC   
TO U7@localhost;

-- 把用户U4修改学生学号的权限收回
-- root
REVOKE UPDATE(Sno)
ON TABLE Student
FROM U4@localhost;

-- 收回所有用户对表SC的查询权限
REVOKE SELECT
ON SC
FROM 'U1'@'localhost', 'U2'@'localhost', 'U3'@'localhost', 'U4'@'localhost';

-- 把用户U5对SC表的INSERT权限收回
REVOKE INSERT
ON TABLE SC
FROM U5@localhost;

-- 创建角色R1，使用GRANT语句，
-- 使R1拥有Student表的SELECT, UPDATE, INSERT权限
CREATE ROLE R1@localhost;
GRANT SELECT, UPDATE, INSERT
ON TABLE Student
TO R1@localhost;

-- 将角色R1授予U1、U2、U3
GRANT R1@localhost
TO U1@localhost, U2@localhost, U3@localhost;

-- 一次性通过R1来收回U1的这三个权限
REVOKE R1@localhost
FROM U1@localhost;

-- 给角色R1添加新的权限
GRANT DELETE
ON Student
TO R1@localhost;

-- 减少角色R1的权限
REVOKE SELECT
ON Student
FROM R1@localhost;

DROP USER
U1@localhost,
U2@localhost,
U3@localhost,
U4@localhost,
U5@localhost,
U6@localhost,
U7@localhost;
DROP ROLE R1@localhost;


-- 1.2 在DBMS上尝试下面的实验，并分析原因：
-- A、B、C为用户。
-- x为某权限，比如在某表上的select（select on student)
CREATE USER
A@localhost,
B@localhost,
C@localhost;

-- root
GRANT SELECT
ON Student
TO A@localhost
WITH GRANT OPTION;

-- A
GRANT SELECT
ON Student
TO B@localhost
WITH GRANT OPTION;

-- B
GRANT SELECT
ON Student
TO C@localhost;

-- 收回B的x
-- A
REVOKE SELECT
ON Student
FROM B@localhost;

-- root
GRANT SELECT
ON Student
TO C@localhost;

-- 收回C的x
REVOKE SELECT
ON Student
FROM C@localhost;


-- 2. 触发器实验

-- 首先，在orders表中，插入一列，TotalPrice，
-- 含义为该订单的总价。
-- use northwind
ALTER TABLE orders
ADD COLUMN TotalPrice DECIMAL(15, 2);

-- 使用Update语句为每个订单填入总价。
UPDATE orders o
SET o.TotalPrice = (
    SELECT SUM(od.Quantity * od.UnitPrice * (1 - od.Discount))
    FROM `order details` od
    WHERE od.OrderID = o.OrderID
);

-- 2.1 在order_details表上定义一个UPDATE触发器，
-- 当修改订单明细（quantity, discount）时，
-- 自动修改订单Orders的TotalPrice，以保持数据一致性。
DELIMITER $$

CREATE TRIGGER update_totalprice
AFTER UPDATE ON `order details`
FOR EACH ROW
BEGIN
    UPDATE Orders o
    SET o.TotalPrice = (
        SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount))
        FROM `Order Details` od
        WHERE od.OrderID = o.OrderID
    )
    WHERE o.OrderID = NEW.OrderID;
END$$

DELIMITER ;


-- 2.2 在order_details表上定义一个INSERT触发器，
-- 当增加一项订单明细时，自动修改订单Orders的TotalPrice，
-- 以保持数据一致性。假设增加订单明细项时，对应订单已经存在。
DELIMITER $$

CREATE TRIGGER update_totalprice_2
AFTER INSERT ON `order details`
FOR EACH ROW
BEGIN
    UPDATE Orders o
    SET o.TotalPrice = (
        SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount))
        FROM `Order Details` od
        WHERE od.OrderID = o.OrderID
    )
    WHERE o.OrderID = NEW.OrderID;
END$$

DELIMITER ;


-- 增加订单明细
INSERT INTO `order details` 
(OrderID, ProductID, UnitPrice, Quantity, Discount) VALUES
(10248, 51, 42.4000, 9, 0.1);


-- 查询某个数据库中的触发器
SELECT 
    TRIGGER_NAME, 
    EVENT_MANIPULATION AS Event, 
    EVENT_OBJECT_TABLE AS TableName, 
    ACTION_TIMING AS Timing, 
    ACTION_STATEMENT AS Statement 
FROM 
    information_schema.TRIGGERS 
WHERE 
    TRIGGER_SCHEMA = 'northwind';
