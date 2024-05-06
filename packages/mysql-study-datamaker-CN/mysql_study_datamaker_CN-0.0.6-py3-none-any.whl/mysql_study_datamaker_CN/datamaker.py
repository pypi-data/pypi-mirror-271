import random as r
from datetime import datetime


class DataMaker:
    """
    这个类的目的是为了在学习 MySQL 语言时，创建表结构后，需要很多插入的数据来进行学习测试；
    DataMaker会根据指定的数量生成指定多的随机项，且支持自定义顺序；
    当前的版本只会生成一个 txt 文本，注意最后一行的","要替换成";"才能够插入数据；
    xxx 是你的 MySQL 表名，需要替换，很傻瓜很简单的一个类
    """

    def __init__(self, N, args=("姓名", "年龄", "性别", "生日", "部门"), left=1950, right=2000,
                 department=None, gender="int", a=0, b=150, file=None):
        """
        __information：数据字典
        N：数据个数
        args：字段列表，目前只支持：姓名,年龄,部门,生日,性别,分数
        left:出生日期左边界，默认情况下不允许小于 1950 （如有需求可自行修改源代码中的判定）
        right:出生日期有边界，默认情况下不允许小于当前年 （自动判定当前年份，拒绝未来人）
        department：默认给了：‘销售部,技术部,售后部,企划部,咨询部,人事部,财务部’，如果需要重新定义部门，需要写字符串，用','分割；
        gender：
            int：默认是数字类型，0 和 1 代表不同性别，没有严格的去区分哪个数字代表男和女；
            cn：中文的 男 女
            en：英文的 M F
            english：英文的 Male  Female
        a：考试分数的随机，最小值；
        b:考试分数的随机，最大值；
        分数只要识别前两个字符是分数就可以，如果想创建多个分数的学生信息，可以写成：
        ("姓名", "年龄", "性别",  "分数1", "分数2", "分数3")
        考试分数默认是 ； 0~150 分，则 a 就是 0， b：就是 150，做了判定修改，支持 b < a
        file：文件名，写入以 x 格式，所以创建后，再次生成会报文件已存在的错误，建议写入当前日期时间，模式为：None或者'date'，
              如果是None则使用 "_mysql_date.txt" , 如果是 "date" 则以此刻时间为基准，也可以自定义名直接写；
        """
        self.__informations = {}

        self.__N = N
        self.__args = args
        self.__left = left
        self.__right = right
        self.__department = department
        self.__gender = gender
        self.__a = a
        self.__b = b

        if file is None:
            self.file = "_mysql_date.txt"
        elif not isinstance(file, str):
            raise TypeError("'file' should be a str")
        elif file.lower() == "date":
            now = datetime.now()
            self.file = f"{now.year}{now.month:>02}{now.day:>02} {now.hour:>02}.{now.minute:>02}.{now.second:>02}.txt"
        else:
            self.file = file
        self.get_info()

    def get_name(self):
        """
        返回随机生成的姓名系统，总共有 300个姓氏，3579个名字；
        如果超过 1,073,700 个姓名，就一定会有重复的名字出现；
        因为没有做去重处理，所以就算生成 2 个随机姓名也有重复出现的概率！
        :param N: 生成名字的个数；
        :return: 返回一个迭代器；
        """
        with open(__file__[:__file__.rfind("d")] + 'new_names.txt', encoding="utf-8") as f:
            names = f.read().splitlines()

        with open(__file__[:__file__.rfind("d")] + 'new_family.txt', encoding="utf-8") as f:
            familys = f.read().splitlines()

        return ("'" + r.choice(familys) + r.choice(names) + "'" for _ in range(self.__N))

    def is_leapyear(self, year):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return True
        return False

    def get_birthday_age(self, left=1950, right=2000, types="birthday"):
        """
        返回的是一个生成器, 根据types的类型来判断返回什么，默认返回的是生日类型；
        年龄具有时效性！如果是前一年生成的，那么下一年则需要变动；
        随机生成生日的函数，这里做了限定，不能低于 1950 生人；
        如果左右的限定不符合规则（如 年份超出当今年份）都会触发异常；
        :param N: 数量
        :param left: 1950年起，今年；
        :param right: 同 left
        :param types: 只能是 'birthday' 或者 'age'
        :return: 生成器
        """

        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError('left or right must be int')
        today = datetime.now()
        if left < 1950 or left > today.year:
            raise ValueError(f"left must be '1950 <= left <= {today.year}.'")
        if right < 1950 or right > today.year:
            raise ValueError(f"right must be '1950 <= right <= {today.year}.'")
        if types not in ["birthday", "age"]:
            raise ValueError(f"types must be 'birthday' or 'age'")
        if left > right:
            left, right = right, left

        years = [year for year in range(left, right + 1)]
        months = [month for month in range(1, 13)]
        days1 = [day for day in range(1, 32)]
        days2 = [day for day in range(1, 31)]
        days3 = [day for day in range(1, 30)]
        days4 = [day for day in range(1, 29)]

        for i in range(self.__N):
            year = r.choice(years)
            if types == "birthday":
                month = r.choice(months)
                if month in [1, 3, 5, 7, 8, 10, 12]:
                    day = r.choice(days1)
                elif month in [4, 6, 9, 11]:
                    day = r.choice(days2)
                else:
                    if self.is_leapyear(year):
                        day = r.choice(days3)
                    else:
                        day = r.choice(days4)
                yield f"'{year:>02}-{month:>02}-{day:>02}'"
            else:
                yield str(today.year - year)

    def get_gender(self, types="int"):
        """
        根据传递的类型不同，可以分别用，英文，中文，整数来表达性别；
        注意，英文如果是全拼的 'english' 返回 'Male' 'Female'；
        如果是 'en' 返回 'M' 'F'
        中文的'chinese' 'cn' 都是 ‘男’  ‘女’
        :param N: 返回的数量
        :param types: english, chinese, int, cn, en
        :return: 生成器
        """
        if types not in ["int", "english", "chinese", "en", "cn"]:
            raise ValueError('types can be "int"  "english"  "chinese" "cn" "en" .')
        if types == "int":
            return ("'" + r.choice("01") + "'" for _ in range(self.__N))
        elif types == "english":
            return ("'" + r.choice(["Male", "Female"]) + "'" for _ in range(self.__N))
        elif types == "en":
            return ("'" + r.choice("MF") + "'" for _ in range(self.__N))
        else:
            return ("'" + r.choice("男女") + "'" for _ in range(self.__N))

    def get_department(self, department=None):
        """
        部门默认是："销售部,技术部,售后部,企划部,咨询部,人事部,财务部"
        可以自定义传递，传递必须是字符串，且用英文','分割
        :param N: 生成个数
        :param department:默认是None
        :return: 生成器
        """
        if department is None:
            department = "销售部,技术部,售后部,企划部,咨询部,人事部,财务部"
        department = department.split(",")
        return ("'" + r.choice(department) + "'" for _ in range(self.__N))

    def get_score(self, a=0, b=150):
        """
        返回随机分数
        :param N: 个数
        :param a: 最低值
        :param b: 最高值
        :return: 返回生成器
        """
        if a > b:
            a, b = b, a
        return (str(r.randint(a, b)) for _ in range(self.__N))

    def get_info(self):
        infos = "姓名,年龄,部门,生日,性别,分数".split(",")
        for info in self.__args:
            if info[:2] not in infos:
                raise ValueError(f"All must be in {infos}, {info} not in.")

        for item in self.__args:
            if item == "姓名":
                self.__informations[item] = self.get_name()
            elif item == "年龄":
                self.__informations[item] = self.get_birthday_age(left=self.__left, right=self.__right, types="age")
            elif item == "部门":
                self.__informations[item] = self.get_department(department=self.__department)
            elif item == "生日":
                self.__informations[item] = self.get_birthday_age(self.__left, self.__right, types="birthday")
            elif item == "性别":
                self.__informations[item] = self.get_gender(self.__gender)
            elif item[:2] == "分数":
                self.__informations[item] = self.get_score(self.__a, self.__b)

    def __iter__(self):
        return self

    def __next__(self):

        result = ""
        for v in self.__informations.values():
            result += next(v) + ","
        result = result[:-1]
        if not result:
            raise StopIteration
        return result

    @classmethod
    def create_insertinto(cls, self):
        """
        需要先生成一个DataMaker对象，来创建指定数量和字段，再调用该方法，写入到一个txt文本中；
        :param self: 生成的对象
        :param file: txt文件名
        :return: None
        """
        with open("insert_into_" + self.file, "x", encoding="utf-8") as f:
            f.write("insert into xxx values \n")
            id = 1
            for line in self:
                comment = "(" + str(id) + "," + line + "),\n"
                id += 1
                f.write(comment)


if __name__ == '__main__':
    """
    下面是案例，直接运行可以获得测试代码，生成15个随机数据；
    """
    args = ("姓名", "年龄", "性别")
    one = DataMaker(15, args, left=2010, gender="cn", file='date')
    DataMaker.create_insertinto(one)

