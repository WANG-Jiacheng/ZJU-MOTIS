"""
这个模块中的方法和类用于给用户调用
"""
from Entities.Course import Course
from Entities.WishList import WishList as _WishList
from Entities.ClassTable import ClassTable
from Entities.Time import ClassTime
from selectClass import selectClass
from Entities.Strategy import Strategy
import network as _network
import data as _data

class WishList(_WishList):
    def __init__(self):
        super().__init__()

    def append(self, courseCode: str) -> Course:
        course = _data.getCourseFromCourseCode(courseCode)
        return super().append(course)


def init():
    _network.updateCoursesJson()
    _data.loadCourseData()

# 时间常量
# 第一节课，上午第一节课
First = ClassTime([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                  [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)])
# 第二节课，上午第二节课
Second = ClassTime([(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)],
                   [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)])
Third = ClassTime([(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)],
                    [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)])
Fourth = ClassTime([(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)],
                    [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)])
# 第五节课，上午最后一节课
Fifth = ClassTime([(1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)],
                    [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)])
# 第六节课，下午第一节课
Sixth = ClassTime([(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
                    [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)])
Seventh = ClassTime([(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)],
                    [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)])
Eighth = ClassTime([(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8)],
                    [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8)])
Ninth = ClassTime([(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9)],
                    [(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9)])
# 第十节课，下午最后一节课
Tenth = ClassTime([(1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10)],
                    [(1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10)])
# 第十一节课，晚上第一节课
Eleventh = ClassTime([(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11)],
                    [(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11)])
Twelfth = ClassTime([(1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12)],
                    [(1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12)])
# 第十三节课，晚上最后一节课
Thirteenth = ClassTime([(1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13)],
                    [(1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13)])
# 早八
MorningEight = First
# 晚课
Night = Eleventh + Twelfth + Thirteenth
Monday = ClassTime([(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13)],
                   [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13)])
Tuesday = ClassTime([(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13)],
                    [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13)])
Wednesday = ClassTime([(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13)],
                      [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13)])
Thursday = ClassTime([(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13)],
                        [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13)])
Friday = ClassTime([(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13)],
                    [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13)])
Saturday = ClassTime([(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13)],
                      [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13)])
Sunday = ClassTime([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)],
                    [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)])


