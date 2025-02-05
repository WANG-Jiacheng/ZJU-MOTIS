# MOTIS
MOTIS: Multi-criteria Optimization Tool for Intelligent Scheduling

![icon](.\icon.png)

[TOC]


## 简介

MOTIS是一个适用于浙江大学学生的选课辅助系统。

它能够帮你找出符合你意愿的最佳课表。



## 注意
您需要通过Python代码来描述你对课程的需求。

如果你擅长Python，那么你可以在阅读完下面文档之后自己书写代码来描述你的选课意愿。

**如果你不会写或者不擅长写Python代码**，**没关系**，下面提供了一种很简单的方法让您使用这个程序而不用自己写代码。



## 代码教程

下面介绍的是程序的一些代码。你可以选择跳过这部分。但是如果你想自己写代码来描述选课愿望，那么你需要阅读下面的文档。

### 一个简单的示例

```python
wish_list.append("MATH1136G").withPriority(10).avoidTeacher("朱静芬").withStrategy(Strategy(hot=0, normal=1, cold=2))

wish_list.append("MATH1138F").withPriority(9)

wish_list.append("ME1103F").withPriority(9)

wish_list.append("MARX1002G").withPriority(8).withTeacherFactor(2.0)

wish_list.append("EDU2001G").withPriority(6).preferredTeacher("沈莉萍").goodTeacher("程春")

wish_list.append("PHIL0902G").withPriority(6)

wish_list.append("PPAE1100G").withPriority(5).expectClassAt(Eleventh)

wish_list.append("PPAE0065G").withPriority(4).avoidClassAt(MorningEight + First + Second + Third + Fourth + Fifth)
```

这就是最终您需要书写的代码。接下来我会对其语法进行描述。

### 愿望清单对象wish_list

这个工具提供了一个对象，叫做**wish_list**。这是一个愿望清单对象，您可以向其中添加想要的课程。

```python
wish_list.append(courseCode: str) -> Course
```
通过这个语句向wish_list中添加课程。比如，wish_list.append("MATH1136G")就是向wish_list中添加一个课程代码为MATH1136G的课程（微积分（甲）II ）。

这个函数的输入参数是一个字符串，表示课程的代码。

这个方法的返回值是课程代码对应的课程的Course对象。Course对象是一个课程对象，我们稍后介绍他。

下面是wish_list的部分源代码:

```python
class _WishList:
    def __init__(self):
        self.wishes : List[Course] = []
        self.max_priority = -1

    def append(self, course) -> Course:
        self.wishes.append(course)
        return course

class WishList(_WishList):
    def __init__(self):
        super().__init__()

    def append(self, courseCode: str) -> Course:
        course = _data.getCourseFromCourseCode(courseCode)  # 通过课程代码获取课程对象
        return super().append(course)
```

### 课程类Course与需求描述

代码中通过Course对象来描述对这门课的需求。程序支持的对课程需求的包括课程的优先级(priority)，课程的时间(time)，课程的教师(teacher)，志愿选择策略(strategy)，以及用户认为教师、时间、选上概率这三个因素对课程的重要性(factor)。
接下来我会详细介绍这些需求的含义与如何使用Course对象来描述这些需求。

#### 课程类Course

源代码中提供了一个类，叫做Course。我们称其实例为课程对象(Course对象)。

我们可以通过Course对象的方法来描述我们对这一门课程的需求。

#### 优先级

priority是一个非负整数，表示课程的优先级。优先级越高，说明这门课程越重要。选课算法执行时，会优先处理优先级高的课程。
如果用户说一门课比另一门课更重要，那么我们可以通过设置这门课的优先级来描述这个需求。
我们可以通过Course对象的这个方法来设置课程的优先级：

```python
withPriority(self, priority: int) -> Course
```

这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置优先级。
比如，下面的代码就是设置course的优先级为10：

```python
course.withPriority(10)		# course是一个Course对象
```

#### 志愿选择策略

strategy用于描述选课时选择志愿的策略，是一个Strategy对象。

我们知道，一个学生一门课可以选择最多三个志愿，一个志愿对应一个教学班。

一般来说，我们选课的时候会选择三个志愿，分别是第一志愿、第二志愿和第三志愿。其中第一志愿是比较热门的教学班，第二志愿和第三志愿是比较冷门的教学班。这样可以提高选课成功的概率。

当然这个策略是可以调整的，我们可以通过Strategy对象来描述我们的志愿选择策略。

Strategy对象的构造函数如下：

```python
Strategy(hot: int, normal: int, cold: int)
```

hot表示选几个热门教学班，normal表示选几个普通教学班，cold表示选几个冷门教学班。这三个数字的和必须等于3，即使这门课只有两个教学班。在调用时建议显式写出hot,normal,cold这三个参数的名字，从而提高代码可读性。

cold越多，对应越保守的策略，选上的概率越高。hot越多，对应越激进、大胆的策略，选上的概率越低。

默认的策略是Strategy(hot=1, normal=2, cold=0)。如果用户不设置策略，那么就采用默认的策略。

我们可以通过Course对象的这个方法来设置课程的选课策略：

```python
withStrategy(self, strategy: Strategy) -> Course
```

这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置选课策略。

#### 设置教师/时间/选上概率三个因素的重要性

如何评价一门课是好还是坏？可以从教师、时间、选上概率三个角度评分。程序的底层为你完成了评分的工作。现在你需要做的就是设置这三者的权值。

teacherFactor表示用户认为教师对课程的重要性，是一个非负实数。这个值越大，表示用户认为教师对课程的重要性越高。

同理还有timeFactor和possibilityFactor，分别表示用户认为时间和选上概率对课程的重要性。

teacherFactor越大，选课结果就会偏向选好老师的课。timeFactor越大，选课结果就会偏向选上课时间合适的课。possibilityFactor越大，选课结果就会偏向选上概率高的课。

当然，这三个值是相对的。同时增大这三个值不会选出老师也好、时间也好、选上概率又大的课。
teacherFactor的默认值是1.0，timeFactor的默认值是1.0，possibilityFactor的默认值是3.0。
我们可以通过Course对象的下面三个方法来设置这三个因素的重要性：

```python
withTeacherFactor(self, teacherFactor: float) -> Course
withTimeFactor(self, timeFactor: float) -> Course
withPossibilityFactor(self, possibilityFactor: float) -> Course
```

这三个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置这三个因素的重要性。

#### 设置教师偏好

程序内部会通过査老师的教师评分为老师评分。然而用户可能有一些其他的考量。这时用户可以显式地指定他认为哪些老师好，哪些老师相对没那么好。**这里设置的教师偏好反映的是用户个人的主观偏好。**

此外，这里用户也可以描述一定要上哪些老师的课或者一定不要上哪些老师的课。
我们可以通过Course对象的如下方法来描述这些需求：

```python
onlyChooseFromTheseTeachers(self, *teacherName) # 表示只选这些老师的课。
preferredTeacher(self, *teacherName) # 表示这些老师的课是很好的。用户很想上这个老师的课。
goodTeacher(self, *teacherName) # 表示这些老师的课是好的。用户比较想上这个老师的课
normalTeacher(self, *teacherName) # 表示这些老师的课是普通的。用户对这个课程的老师没有特别的要求。
badTeacher(self, *teacherName) # 表示这些老师的课是不好的。用户不想上这个老师的课。
avoidTeacher(self, *teacherName) # 表示这些老师的课是很不好的。用户一定不要上这个老师的课。
```

这些方法的参数是一个或多个字符串，表示老师的名字。比如，下面的代码表示只选张三和李四的课。

```python
course.onlyChooseFromTheseTeachers("张三", "李四")
```

这些方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置教师偏好。

**注意！用户应该提供完整的老师的名字，而不是提供“王老师”之类的描述**

#### 设置时间偏好

程序内使用ClassTime对象来描述上课时间。所以我们必须先学习ClassTime类的知识。

##### ClassTime对象

ClassTime对象用于描述课程的上课时间。他的部分源代码如下：

```python
class ClassTime:
    def __init__(self, firstHalfTimeList: List[Tuple[int, int]], secondHalfTimeList: List[Tuple[int, int]]):
        """
        上课时间
        :param firstHalfTimeList: 上半学期的课程时间 [(周几, 第几节课), ...]
        :param secondHalfTimeList: 下半学期的课程时间 [(周几, 第几节课), ...]
        """
        self.firstHalfTimeList = firstHalfTimeList
        self.secondHalfTimeList = secondHalfTimeList
```
想要描述一段上课时间，需要分上/下半学期来描述。ClassTime构造函数的第一个参数描述了上半学期的课程时间，第二个参数描述了下半学期的课程时间。

其参数格式为：

```python
[(周几, 第几节课), ...]
```

这里提供几个例子:

```python
ClassTime([(1, 1), (1, 2), (3, 5)], [])
# 表示的时间是：上半学期的周一的第一节课、周一的第二节课、周三的第五节课。

ClassTime([(2, 1), (2, 2), (2, 3)], [(2, 1), (2, 2), (2, 3)])
# 表示的时间是：上半学期的周二的第一到第三节课；下半学期的周二的第一到第三节课。
```

一周有七天，一天13节课。所以元组内第一个参数的范围是1-7, 第二个参数范围是1-13。

值得注意的是，这个工具为我们提供了一些定义好的ClassTime对象，比如晚课、早八、周一的课，这是比较常用的。共有以下几种：
```python
First   # 第一节课，上午第一节课
Second  # 第二节课，上午第二节课
Third
Fourth
Fifth   # 第五节课，上午最后一节课
Sixth   # 第六节课，下午第一节课
Seventh
Eighth
Ninth
Tenth   # 第十节课，下午最后一节课
Eleventh    # 第十一节课，晚上第一节课
Twelfth
Thirteenth  # 第十三节课，晚上最后一节课
MorningEight    # 早八，等价于第一节课
Night   # 晚课，等价于第十一节课、第十二节课、第十三节课
Monday  # 周一的课
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday  # 周日的课
```

其部分源代码如下：

```python
First = ClassTime([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                  [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)])
Sunday = ClassTime([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)],
                    [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)])
```

ClassTime对象可以通过+运算符来组合。比如，下面的表达式表示所有的周六周日的课和上午的前两节课。

```python
First + Second + Saturday + Sunday
```

##### 设置时间偏好

我们可以通过以下Course对象的方法设置时间偏好：

```python
expectClassAt(self, classTime: ClassTime) -> Course # 设置期待的课程的上课时间
avoidClassAt(self, classTime: ClassTime) -> Course  # 设置不希望的课程的上课时间
```

一个例子：

```python
course.expectClassAt(Tuesday + Wednsday + Thursday + Friday).avoidClassAt(MorningEight)
```


下面是Course对象的部分源代码：
```python
class Course:
    def __init__(self, ...):
        self.priority = 0       # 选课优先级。数字越大，优先级越高。非负整数
        self.strategy = Strategy(*STRATEGY_DEFAULT) # 默认选课策略

        self.teacherGroup = [[], [], [], []]
        self.requiredTeachers = []
        self.avoidedTeachers = []
    
        self.expectedTimeList : List[ClassTime] = []  # 期望上课时间
        self.avoidTimeList : List[ClassTime] = [] # 避免上课时间
    
        self.teacherFactor = 1.0  # 教师因素权重
        self.timeFactor = 1.0    # 时间因素权重
        self.possibilityFactor = 3.0    # 选上的概率的权重


    def withPriority(self, priority: int):
        if priority < 0 or not isinstance(priority, int):
            raise ValueError(
                "Priority must be a non-negative integer!"
            )
        self.priority = priority
        return self
    
    def withStrategy(self, strategy: Strategy):
        self.strategy = strategy
        return self
    
    def onlyChooseFromTheseTeachers(self, *teacherName):
        self.autoTeacherGroup = False
        self.requiredTeachers.extend(teacherName)
        return self
    
    def preferredTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[0].extend(teacherName)
        return self
    
    def goodTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[1].extend(teacherName)
        return self
    
    def normalTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[2].extend(teacherName)
        return self
    
    def badTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[3].extend(teacherName)
        return self
    
    def avoidTeacher(self, *teacherName):
        self.avoidedTeachers.extend(teacherName)
        return self
    
    def expectClassAt(self, classTime: ClassTime):
        self.expectedTimeList.append(classTime)
        return self
    
    def avoidClassAt(self, classTime: ClassTime):
        self.avoidTimeList.append(classTime)
        return self
    
    def withTeacherFactor(self, factor: float):
        self.teacherFactor = factor
        return self
    
    def withTimeFactor(self, factor: float):
        self.timeFactor = factor
        return self
    
    def withPossibilityFactor(self, factor: float):
        self.possibilityFactor = factor
        return self
```
### 示例

以下是几个添加愿望课程并描述的例子:

```python
wish_list.append("MATH1136G").withPriority(10).withStrategy(Strategy(hot=1, normal=1, cold=1)).onlyChooseFromTheseTeachers("张三", "李四").expectClassAt(Night)
# 这表示我希望选MATH1136G这门课，优先级为10，选课策略是三个志愿选一个热门教学班，一个普通教学班，一个冷门教学班。只选张三和李四的课。希望这门课在上晚上的课上。

wish_list.append("MARX1002G").withPriority(8).preferredTeacher("王五").goodTeacher("赵六", "周七").avoidTeacher("张八").avoidClassAt(ClassTime([(2, 1), (2, 2), (2, 3)], [(2, 1), (2, 2), (2, 3)])
# 这表示我希望选MARX1002G这门课，优先级为8，很喜欢王五老师的课，也比较喜欢赵六和周七老师的课，不喜欢张八老师的课。希望这门课在上半学期的周二的第一到第三节课，下半学期的周二的第一到第三节课上课。

wish_list.append("CSCI1001G").withPriority(5).withTeacherFactor(2.0).withTimeFactor(1.0).withPossibilityFactor(3.0)
# 这表示我希望选CSCI1001G这门课，优先级为5，我认为教师对这门课的重要性是时间的两倍，选上的概率的三倍。
```

接下来是一个完整的例子：
用户的需求是：

```
我要选MATH1136G这门课，这门课最重要，优先级是10，我想上朱静芬老师的课的课，这门课可以选的大胆一点。
我要选PHY1001G这门课，优先级为9。
我要选MATH1138F这门课，优先级为9
我要选ME1002F这门课，优先级为7
我要选CS1241G这门课，优先级为7
我要选PPAE1100G这门课，优先级为5，这门课最好在晚上第一节课上课。
我要选PPAE0065G这门课，优先级为4，这门课不要在早上上课。
我要选BEFS0402G这门课，优先级为3
我要选ME1103F这门课，优先级为9
我要选MARX1002G这门课，这门课比ME1103F相对不那么重要，但也挺重要的，这门课最好要选个好一些的老师
我要选EDU2001G这门课，优先级为6，最好能上沈莉萍老师的课，程春老师的也不错。
我要选PHIL0902G这门课，优先级为6
```


对应的代码为：

```python
# 1. MATH1136G，优先级为10，想上朱静芬老师的课，选课策略保守
wish_list.append("MATH1136G").withPriority(10).preferredTeacher("朱静芬").withStrategy(Strategy(hot=2, normal=1, cold=0))

# 2. PHY1001G，优先级为9
wish_list.append("PHY1001G").withPriority(9)

# 3. MATH1138F，优先级为9
wish_list.append("MATH1138F").withPriority(9)

# 4. ME1103F，优先级为9
wish_list.append("ME1103F").withPriority(9)

# 5. MARX1002G，优先级为8，最好选个好老师
wish_list.append("MARX1002G").withPriority(8).withTeacherFactor(2.0)

# 6. ME1002F，优先级为7
wish_list.append("ME1002F").withPriority(7)

# 7. CS1241G，优先级为7
wish_list.append("CS1241G").withPriority(7)

# 8. EDU2001G，优先级为6，最好能上沈莉萍老师的课，程春老师的也不错
wish_list.append("EDU2001G").withPriority(6).preferredTeacher("沈莉萍").goodTeacher("程春")

# 9. PHIL0902G，优先级为6
wish_list.append("PHIL0902G").withPriority(6)

# 10. PPAE1100G，优先级为5，最好在晚上第一节课上课
wish_list.append("PPAE1100G").withPriority(5).expectClassAt(Eleventh)

# 11. PPAE0065G，优先级为4，不要在早上上课
wish_list.append("PPAE0065G").withPriority(4).avoidClassAt(First + Second + Third + Fourth + Fifth)

# 12. BEFS0402G，优先级为3
wish_list.append("BEFS0402G").withPriority(3)
```

## 使用方法

打开MOTIS.exe（或者UI.py），先在右上角输入学号和密码并登录，才能执行后续操作。

首次使用时，要点击右下角按钮“更新课程信息”。这执行了本地课程库与ZDBK的同步。

在左侧代码输入框输入代码(**不会写代码？没关系往后看**)，然后点击右下角按钮开始选课。

如果关闭了选课结果窗口，也可以按右下角按钮重新展示。

### 自己写代码描述选课需求

如题，自己写代码。这里推荐在IDE中写完复制到代码输入框中。不要再代码输入框中写代码。

### 把你的需求告诉AI，让AI帮你生成代码

先看一张效果图：

![AI](.\AI.png)

如果你不会写代码或者没看懂我的文档，没关系。

你可以把下面的prompt喂给AI，让他帮你写。如果一整个prompt太长，可以在合适的地方断开，分段喂给AI。

经过测试，deepseek和通义千问都可以完成代码编写任务。其他AI我没测o(\*￣︶￣\*)o。

**不要完全信赖AI写的代码，如果可以，请自己审查一遍**
*!!!!!*

prompt如下：

````
你好，我是一个浙江大学的大学本科生。我现在正在进行选课。
我有一个工具，只要我通过Python代码描述我对各个课程的需求，它就可以帮我选择出最适合我的课程。
我想请您帮我书写Python代码来描述我的需求。下面是开发者对这个工具所需要的代码的介绍。请您牢牢记住开发者下面给你对工具的介绍。你要有联想能力和推理能力。

这个工具提供了一个对象，叫做**wish_list**。这是一个愿望清单对象，用户可以向其中添加想要的课程。
我们可以通过

```python
wish_list.append(courseCode: str)
```
向wish_list中添加课程。

这个函数的输入参数是一个字符串，表示课程的代码。比如，wish_list.append("MATH1136G")就是向wish_list中添加一个代码为MATH1136G的课程。
这个方法的返回值是一个Course对象。Course对象是一个课程对象，我们稍后介绍他。
下面是wish_list的源代码:

```python
class _WishList:
    def __init__(self):
        self.wishes : List[Course] = []
        self.max_priority = -1

    def append(self, course) -> Course:
        self.wishes.append(course)
        return course

class WishList(_WishList):
    def __init__(self):
        super().__init__()

    def append(self, courseCode: str) -> Course:
        course = _data.getCourseFromCourseCode(courseCode)  # 通过课程代码获取课程对象
        return super().append(course)
```

这个工具还提供了一个类，叫做Course。我们称其实例为课程对象(Course对象)，我们可以通过Course对象来描述我们对课程的需求。
这些需求包括课程的优先级(priority)，课程的时间(time)，课程的教师(teacher)，选课的策略(strategy)，用户认为教师、时间、选上概率这三个因素对课程的重要性(factor)。
我们可以通过Course对象的方法来描述这些需求。
接下来我会详细介绍这些需求的含义与如何使用Course对象来描述这些需求。

priority是一个非负整数，表示课程的优先级。优先级越高，说明这门课程越重要。选课算法执行时，会优先处理优先级高的课程。
如果用户说一门课比另一门课更重要，那么我们可以通过设置这门课的优先级来描述这个需求。
我们可以通过Course对象的withPriority(self, priority: int)方法来设置课程的优先级。这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置优先级。
比如，course.withPriority(10)就是设置course的优先级为10。

strategy表示选课的策略，是一个Strategy对象。这用于描述选课时选择志愿的策略。
一个学生一门课可以选择最多三个志愿，一个志愿对应一个教学班。
一般来说，我们选课的时候会选择三个志愿，分别是第一志愿、第二志愿和第三志愿。其中第一志愿是比较热门的教学班，第二志愿和第三志愿是比较冷门的教学班。这样可以提高选课成功的概率。
当然这个策略是可以调整的，我们可以通过Strategy对象来描述我们的选课策略。
Strategy对象的构造函数是Strategy(hot: int, normal: int, cold: int)。在调用时必须显式写出hot,normal,cold这三个参数的名字。
hot表示选几个热门教学班，normal表示选几个普通教学班，cold表示选几个冷门教学班。
这三个数字的和必须等于3，表示我们一共选择了三个志愿！这三个数字的和必须等于3！！这三个数字的和必须等于3！！！
举个例子，如果用户告诉你他想选个普通的班，那么你可以设置normal为3，hot和cold都为0。或者normal为2，hot为0，cold为1。具体如何，你可以自己推断，也可以向用户询问更多信息。
但是一定要记住，hot、normal、cold的和必须等于3！！！
cold越多，对应越保守的策略，选上的概率越高。hot越多，对应越激进、大胆的策略，选上的概率越低。
默认的策略是Strategy(hot=1, normal=2, cold=0)。如果用户不设置策略，那么就采用默认的策略。
我们可以通过Course对象的withStrategy(self, strategy: Strategy)方法来设置课程的选课策略。这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置选课策略。

teacherFactor表示用户认为教师对课程的重要性。是一个非负实数，表示用户认为教师对课程的重要性。这个值越大，表示用户认为教师对课程的重要性越高。
同理还有timeFactor和possibilityFactor，分别表示用户认为时间和选上概率对课程的重要性。
teacherFactor越大，选课结果就会偏向选好老师的课。timeFactor越大，选课结果就会偏向选上课时间合适的课。possibilityFactor越大，选课结果就会偏向选上概率高的课。
当然，这三个值是相对的。相等地增大这三个值没有意义。
teacherFactor的默认值是1.0，timeFactor的默认值是1.0，possibilityFactor的默认值是3.0。
我们可以通过Course对象的withTeacherFactor(self, teacherFactor: float)、withTimeFactor(self, timeFactor: float)、withPossibilityFactor(self, possibilityFactor: float)方法来设置这三个因素的重要性。
这三个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置这三个因素的重要性。

teacher是上课教师。用户可以描述自己觉得哪个老师好，哪个老师不好。也可以描述一定要上哪些老师的课或者一定不要上哪些老师的课。
我们可以通过Course对象的方法来描述这些需求。
onlyChooseFromTheseTeachers(self, *teacherName) 表示只选这些老师的课。
preferredTeacher(self, *teacherName) 表示这些老师的课是很好的。用户很想上这个老师的课。
goodTeacher(self, *teacherName) 表示这些老师的课是好的。用户比较想上这个老师的课
normalTeacher(self, *teacherName) 表示这些老师的课是普通的。用户对这个课程的老师没有特别的要求。
badTeacher(self, *teacherName) 表示这些老师的课是不好的。用户不想上这个老师的课。
avoidTeacher(self, *teacherName) 表示这些老师的课是很不好的。用户一定不要上这个老师的课。
这些方法的参数是一个或多个字符串，表示老师的名字。比如，course.onlyChooseFromTheseTeachers("张三", "李四")表示只选张三和李四的课。
注意！用户应该给你提供完整的老师的名字，而不是只给你姓或名。如果用户只给你姓或名，你应该向用户询问，以获取完整的老师名字。或者你可以拒绝输出。

time表示课程上课的时间，是一个ClassTime对象。
ClassTime对象用于描述课程的上课时间。他的源代码如下：
```python
class ClassTime:
    def __init__(self, firstHalfTimeList: List[Tuple[int, int]], secondHalfTimeList: List[Tuple[int, int]]):
        """
        上课时间
        :param firstHalfTimeList: 上半学期的课表 [(周几, 第几节课), ...]
        :param secondHalfTimeList: 下半学期的课表 [(周几, 第几节课), ...]
        """
        self.firstHalfTimeList = firstHalfTimeList
        self.secondHalfTimeList = secondHalfTimeList
```
例如，
ClassTime([(1, 1), (1, 2), (3, 5)], [])表示的时间是：上半学期的周一的第一节课、周一的第二节课、周三的第五节课。
ClassTime([(2, 1), (2, 2), (2, 3)], [(2, 1), (2, 2), (2, 3)])表示的时间是：上半学期的周二的第一到第三节课；下半学期的周二的第一到第三节课。
一天有13节课，分别是1-13节课。上午的课是1-5节课，下午的课是6-10节课，晚上的课是11-13节课。
我们可以通过Course对象的expectClassAt(self, classTime: ClassTime)方法来设置期待的课程的上课时间。这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置期待的上课时间。
我们可以通过Course对象的avoidClassAt(self, classTime: ClassTime)方法来设置不希望的课程的上课时间。这个方法会返回这个Course对象，所以我们可以通过链式调用的方式来设置不希望的上课时间。
值得注意的是，这个工具为我们提供了一些定义好的ClassTime对象，比如晚课、早八、周一的课，这是比较常用的。共有以下几种：
First   # 第一节课，上午第一节课
Second  # 第二节课，上午第二节课
Third
Fourth
Fifth   # 第五节课，上午最后一节课
Sixth   # 第六节课，下午第一节课
Seventh
Eighth
Ninth
Tenth   # 第十节课，下午最后一节课
Eleventh    # 第十一节课，晚上第一节课
Twelfth
Thirteenth  # 第十三节课，晚上最后一节课
MorningEight    # 早八，等价于第一节课
Night   # 晚课，等价于第十一节课、第十二节课、第十三节课
Monday  # 周一的课
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday  # 周日的课
其部分源代码如下：
```python
First = ClassTime([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                  [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)])
Sunday = ClassTime([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)],
                    [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)])
```
可以使用avoidClassAt(First)来表示不希望选上午第一节的课。
ClassTime对象可以通过+运算符来组合。比如，First + Second + Saturday + Sunday表示所有的周六周日的课和上午的前两节课。


下面是Course对象的部分源代码：
```python
class Course:
    def __init__(self, ...):
        self.priority = 0       # 选课优先级。数字越大，优先级越高。非负整数
        self.strategy = Strategy(*STRATEGY_DEFAULT) # 默认选课策略

        self.teacherGroup = [[], [], [], []]
        self.requiredTeachers = []
        self.avoidedTeachers = []
    
        self.expectedTimeList : List[ClassTime] = []  # 期望上课时间
        self.avoidTimeList : List[ClassTime] = [] # 避免上课时间
    
        self.teacherFactor = 1.0  # 教师因素权重
        self.timeFactor = 1.0    # 时间因素权重
        self.possibilityFactor = 3.0    # 选上的概率的权重


    def withPriority(self, priority: int):
        if priority < 0 or not isinstance(priority, int):
            raise ValueError(
                "Priority must be a non-negative integer!"
            )
        self.priority = priority
        return self
    
    def withStrategy(self, strategy: Strategy):
        self.strategy = strategy
        return self
    
    def onlyChooseFromTheseTeachers(self, *teacherName):
        self.autoTeacherGroup = False
        self.requiredTeachers.extend(teacherName)
        return self
    
    def preferredTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[0].extend(teacherName)
        return self
    
    def goodTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[1].extend(teacherName)
        return self
    
    def normalTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[2].extend(teacherName)
        return self
    
    def badTeacher(self, *teacherName):
        self.autoTeacherGroup = False
        self.teacherGroup[3].extend(teacherName)
        return self
    
    def avoidTeacher(self, *teacherName):
        self.avoidedTeachers.extend(teacherName)
        return self
    
    def expectClassAt(self, classTime: ClassTime):
        self.expectedTimeList.append(classTime)
        return self
    
    def avoidClassAt(self, classTime: ClassTime):
        self.avoidTimeList.append(classTime)
        return self
    
    def withTeacherFactor(self, factor: float):
        self.teacherFactor = factor
        return self
    
    def withTimeFactor(self, factor: float):
        self.timeFactor = factor
        return self
    
    def withPossibilityFactor(self, factor: float):
        self.possibilityFactor = factor
        return self
```
以下是几个添加愿望课程并描述的例子:
```python
wish_list.append("MATH1136G").withPriority(10).withStrategy(Strategy(hot=1, normal=1, cold=1)).onlyChooseFromTheseTeachers("张三", "李四").expectClassAt(Night)
# 这表示我希望选MATH1136G这门课，优先级为10，选课策略是三个志愿选一个热门教学班，一个普通教学班，一个冷门教学班。只选张三和李四的课。希望这门课在上晚上的课上。

wish_list.append("MARX1002G").withPriority(8).preferredTeacher("王五").goodTeacher("赵六", "周七").avoidTeacher("张八").avoidClassAt(ClassTime([(2, 1), (2, 2), (2, 3)], [(2, 1), (2, 2), (2, 3)])
# 这表示我希望选MARX1002G这门课，优先级为8，很喜欢王五老师的课，也比较喜欢赵六和周七老师的课，不喜欢张八老师的课。希望这门课在上半学期的周二的第一到第三节课，下半学期的周二的第一到第三节课上课。

wish_list.append("CSCI1001G").withPriority(5).withTeacherFactor(2.0).withTimeFactor(1.0).withPossibilityFactor(3.0)
# 这表示我希望选CSCI1001G这门课，优先级为5，我认为教师对这门课的重要性是时间的两倍，选上的概率的三倍。
```

要注意的是，以上说明中出现的人名和课程代码都是虚构的，仅用于说明。实际使用时，需要根据实际情况填写。
如果用户只告诉你要选一个好老师的课，那么应该提高teacherFactor，而不是指定preferredTeacher和goodTeacher之类。
如果你觉得用户告诉你的信息不足以写出完整且正确的代码，可以向用户提问，以获取更多信息。坚决不要猜测用户的意图。
注意！特别强调！你可以向用户提问，以获取更多信息！！！用户应该给你完整的老师名称。如果用户告诉你“张老师”这样，你必须进一步询问具体姓名。
你能使用的API如上所示。不要使用任何上面没有提到的API。不存在preferredClassType之类的API。只有上面提到的API！！！
用户给你提供的描述可能是多种多样的，甚至是有语病的。你要会融会贯通，具有联想能力，将用户各式各样的需求全部分解为上面提到的API。你要深刻理解用户给你的描述，然后将其转化为上面提到的API。
你只需要描述wish_list相关内容即可。不用定义上面提及的源代码。你的代码的所有语句的开头都应该是wish_list.append

接下来是一个完整的例子。
用户的需求是：
我要选MATH1136G这门课，这门课最重要，优先级是10，我很喜欢朱静芬老师的课，选课策略可以大胆一些
我要选PHY1001G这门课，优先级为9。
我要选MATH1138F这门课，优先级为9
我要选ME1002F这门课，优先级为7
我要选CS1241G这门课，优先级为7
我要选PPAE1100G这门课，优先级为5，这门课最好在晚上第一节课上课。
我要选PPAE0065G这门课，优先级为4，这门课不要在早上上课。
我要选BEFS0402G这门课，优先级为3
我要选ME1103F这门课，优先级为9
我要选MARX1002G这门课，这门课比ME1103F相对不那么重要，但也挺重要的，这门课最好要选个好一些的老师
我要选EDU2001G这门课，优先级为6，最好能上沈莉萍老师的课，程春老师的也不错。
我要选PHIL0902G这门课，优先级为6
你应该输出如下代码：
```python
# 1. MATH1136G，优先级为10，我很喜欢朱静芬老师的课，选课策略可以大胆一些
wish_list.append("MATH1136G").withPriority(10).preferredTeacher("朱静芬").withStrategy(Strategy(hot=2, normal=1, cold=0))

# 2. PHY1001G，优先级为9
wish_list.append("PHY1001G").withPriority(9)

# 3. MATH1138F，优先级为9
wish_list.append("MATH1138F").withPriority(9)

# 4. ME1103F，优先级为9
wish_list.append("ME1103F").withPriority(9)

# 5. MARX1002G，优先级为8，最好选个好老师
wish_list.append("MARX1002G").withPriority(8).withTeacherFactor(2.0)

# 6. ME1002F，优先级为7
wish_list.append("ME1002F").withPriority(7)

# 7. CS1241G，优先级为7
wish_list.append("CS1241G").withPriority(7)

# 8. EDU2001G，优先级为6，最好能上沈莉萍老师的课，程春老师的也不错
wish_list.append("EDU2001G").withPriority(6).preferredTeacher("沈莉萍").goodTeacher("程春")

# 9. PHIL0902G，优先级为6
wish_list.append("PHIL0902G").withPriority(6)

# 10. PPAE1100G，优先级为5，最好在晚上第一节课上课
wish_list.append("PPAE1100G").withPriority(5).expectClassAt(Eleventh)

# 11. PPAE0065G，优先级为4，不要在早上上课
wish_list.append("PPAE0065G").withPriority(4).avoidClassAt(MorningEight + First + Second + Third + Fourth + Fifth)

# 12. BEFS0402G，优先级为3
wish_list.append("BEFS0402G").withPriority(3)
```

以上是我对这个工具的介绍。我希望您可以帮我书写Python代码来描述我的需求。我会将这些代码输入到我的工具中，然后运行这个工具来帮我选课。谢谢！
我的需求如下：
````

在这个prompt后接上你对课程的需求描述，然后发给AI。

## 警告

请**不要**在代码输入框中输入来源不被信任的代码！

这可能造成对你系统的**攻击**！

详细原因可以查看本软件的源代码如下：

```python
exec(self.codePad.get(1.0, END))
```

这条语句可以执行输入的任何代码，包括一些恶意代码。

## 不适用性说明

本人开发此程序之时是大一寒假，没上过很多课程，不清楚其时间分布与选课规则。

除此之外，体育课的选课规则与普通课程不同，本程序不适用于体育课。

所以本代码不适用于：
- 体育专项课
- 循环补充班
- 短学期课程
- 其他我没上过的课程类别的课程（我也不知道具体有哪些）

## LICENSE

MIT LICENSE
