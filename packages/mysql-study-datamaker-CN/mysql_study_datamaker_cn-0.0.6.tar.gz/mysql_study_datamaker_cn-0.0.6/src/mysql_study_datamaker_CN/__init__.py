content="""欢迎使用MySQL学习语句自动生成器，这是 0.0.6版本。
该版本支持了，file参数的自定义，在构造函数中，
file的默认值为None，如果不是None，则必须是字符串格式，否则报错，
如果是None，则名称是：_mysql_date.txt
可以写'date'来自动获取当前时间，例如：one = DataMaker(15, args, left=2010, gender="cn", file='date')
也可以自定义，但是需要注意，文件不能重复，如果重复则会报 文件重复 错误，避免误操作导致原有数据被覆盖。
建议使用 date 模式 生成。
"""

print(content)