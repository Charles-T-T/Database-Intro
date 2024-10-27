UPDATE student
SET GPA = (
    SELECT SUM(sc.grade * course.ccredit) / SUM(course.ccredit)
    FROM sc
    JOIN course ON sc.cno = course.cno
    WHERE sc.sno = student.sno
    GROUP BY sc.sno
);

INSERT INTO sc(sno, cno, grade, semester, teachingclass) VALUES
('20180306', '81006', '81', '20211', '81006-01'),
('20180306', '81007', '85', '20211', '81007-01'),
('20180306', '81001', '83', '20211', '81001-01'),
('20180306', '81005', '77', '20211', '81005-01'),
('20180307', '81002', '90', '20212', '81002-02'),
('20180307', '81003', '88', '20212', '81003-02'),
('20221530', '81007', '84', '20242', '81007-02'),
('20221530', '81008', '80', '20242', '81008-02'),
('20221530', '81006', '87', '20242', '81006-02');


DELETE FROM sc
WHERE sno = '20221530';

INSERT INTO sc(sno, cno, semester, teachingclass) VALUES
('20180306', '81003', '20211', '81003-01');

DELETE FROM sc
WHERE grade IS NULL;

DELETE FROM sc
WHERE sno IN (
    SELECT sno
    FROM student
    WHERE smajor = '计算机科学与技术'
);

CREATE VIEW sGPA AS
SELECT sno, sname, GPA
FROM student;

SELECT GPA
FROM sGPA
WHERE sname = '张立';

INSERT INTO sGPA(sno, sname, GPA) VALUES
('20241020', '刘香菜', 99.00);