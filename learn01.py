import datetime

# 数字
from collections import deque
from math import pi


def learn_number():
    a = 2 + 2
    print(a)

    print((50 - 5 * 6) / 4)  # 5.0

    print(8 / 5)  # 1.6

    # 混合类型运算数的运算会把整数转换为浮点数
    print(4 * 3.75 - 1)

    # 最好把该变量当作只读类型。不要为它显式赋值，否则会创建一个同名独立局部变量，该变量会用它的魔法行为屏蔽内置变量。
    tax = 12.5 / 100
    price = 100.50
    print(price * tax)

    # Python 还内置支持 复数，后缀 j 或 J 用于表示虚数（例如 3+5j ）。
    print(3 + 5j)


# 字符串
def learn_string():
    # 字符串有多种表现形式，用单引号（'……'）或双引号（"……"）标注的结果相同
    print("双引号字符串")
    print('单引号字符串')

    # 不转义特殊字符
    print(r'C:\some\name')

    print("""
 跨行输出
1
2
3
    """)

    print("""\
 不跨行输出\
1\
2\
3\
    """)

    # 字符串可以用 + 合并（粘到一起），也可以用 * 重复
    print(3 * 'un' + 'ium')

    # 相邻的两个或多个 字符串字面值 （引号标注的字符）会自动合并
    # 这项功能只能用于两个字面值，不能用于变量或表达式
    print('Py' 'thon')
    # 不能用于变量或表达式
    # prefix = 'Py'
    # print(prefix 'thon') # error

    # 字符串支持 索引 （下标访问）
    word = 'Python'
    print(word[0])
    # 索引还支持负数，用负数索引时，从右边开始计数
    print(word[-1])
    print(word[-2])
    # -0 和 0 一样，因此，负数索引从 -1 开始
    print(word[-0])

    # 字符串还支持 切片
    print(word[0:2])
    # 省略开始索引时，默认值为 0
    print(word[:2])
    print(word[2:])
    print(word[:2] + word[2:])
    # # 索引越界会报错
    # print(word[32])
    # 生成新的字符串
    print('J' + word[1:])
    print(len(word[1:]))


# 列表
def learn_list():
    print("")
    # Python 支持多种 复合 数据类型，可将不同值组合在一起。最常用的 列表 ，是用方括号标注，逗号分隔的一组值。
    # 列表 可以包含不同类型的元素，但一般情况下，各个元素的类型相同
    squares = [1, 2, 3, 4, 5, 6]
    print(squares)
    print(squares[-3:])

    # 切片操作返回包含请求元素的新列表。以下切片操作会返回列表的 浅拷贝：
    print(squares[:])

    # 列表还支持合并操作：
    print(squares + [36, 49, 64, 81, 100])

    # 列表是 mutable 类型
    squares[3] = 64
    print(squares)

    # append() 方法 可以在列表结尾添加新元素
    squares.append(200)
    print(squares)

    print(len(squares))

    # 嵌套列表（创建包含其他列表的列表）
    nest = [['a', 'b', 'c'], [1, 2, 3]]
    print(nest[0])


# 斐波那契数列
def fibonacci_number(months):  # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    i, a, b = 0, 0, 1
    while i < months:
        print(a)
        a, b = b, a + b
        i += 1


# 流程控制
def test_controlflow():
    words = ['cat', 'window', 'defenestrate']
    for w in words:
        print(w, len(w))

    # 遍历某个集合的同时修改该集合的内容，很难获取想要的结果。要在遍历时修改集合的内容，应该遍历该集合的副本或创建新的集合
    for item in words.copy():
        if item == 'window':
            print(item)
            words.remove(item)

    print(words)

    # 内置函数 range() 常用于遍历数字序列，该函数可以生成算术级数
    # 可以按指定幅度递增（递增幅度称为 '步进'，支持负数）
    for i in range(5, 20, 2):
        print(i)

    names = ['Mary', 'had', 'a', 'little', 'lamb']
    for i in range(len(names)):
        print(i, names[i])

    print(list(names))

    print('---------------------------')
    # 循环语句支持 else 子句；for 循环中，可迭代对象中的元素全部循环完毕时，或 while 循环的条件为假时，执行该子句；
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n / x)
                break
        else:
            print(n, 'is a prime number')
    print('---------------------------')

    # pass 语句不执行任何操作。
    # while True:
    #     print('pass...', datetime.datetime.today())
    #     pass # Busy-wait for keyboard interrupt (Ctrl+C)

    # ask_ok('Do you really wangt to quit?')
    # ask_ok('OK to overwrite the file?', 2)
    # ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')

    print(f(1))
    print(f(2))
    print(f(3))

    cheeseshop("Limburger", "It's very runny, sir.",
               "It's really very, VERY runny, sir.",
               shopkeeper="Michael Palin",
               client="John Cleese",
               sketch="Cheese Shop Sketch")

    fun_annotaion('spam')


# pass 还可以用作函数或条件子句的占位符，让开发者聚焦更抽象的层次。
def initlog(*args):
    pass


# 空类
class MyEmptyClass:
    pass


def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


def f(a, L=[]):
    # 不想在后续调用之间共享默认值时，应以如下方式编写函数
    # def f(a, L=None):
    # if L is None:
    #     L = []
    L.append(a)
    return L


# 最后一个形参为 **name 形式时，接收一个字典（详见 映射类型 --- dict），该字典包含与函数中已定义形参对应之外的所有关键字参数。
# **name 形参可以与 *name 形参（下一小节介绍）组合使用（*name 必须在 **name 前面）， *name 形参接收一个 元组，该元组包含
# 形参列表之外的位置参数
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 80)
    for kw in keywords:
        print(kw, ":", keywords[kw])


def fun_annotaion(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", fun_annotaion.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs


# 数据结构
def test_datastruct():
    fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']

    print(fruits.count('apple'))
    print(fruits.index('apple'))

    copy = fruits.copy();
    copy.reverse()
    print(copy)

    print(fruits.index('banana', 4))

    fruits.sort()
    print(fruits)

    print(fruits.pop())

    queue = deque(["Eric", "John", "Michael"])
    queue.append("Terry")
    queue.append("Graham")
    print(queue)

    print(queue.popleft())

    squares = []
    for x in range(10):
        squares.append(x ** 2)
    print(squares)

    print(list(map(lambda x: x ** 2, range(10))))

    # 列表推导式的方括号内包含以下内容：一个表达式，后面跟一个 for 子句，然后，是零个或多个 for 或 if 子句。
    print([x ** 2 for x in range(10)])

    # 表达式是元组（例如上例的 (x, y)）时，必须加上括号
    print([(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y])

    # 上面的公式等价于这段代码
    combs = []
    for x in [1, 2, 3]:
        for y in [3, 1, 4]:
            if x != y:
                combs.append((x, y))

    print([str(round(pi, i)) for i in range(1, 16)])

    # 5.1.4. 嵌套的列表推导式

    # 3x4 矩阵
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    print(matrix)

    # 下面的列表推导式可以转置行列
    print([[row[i] for row in matrix] for i in range(4)])

    # 上面的转置行列的表达式可以写成下面的代码
    transposed = []
    for i in range(4):
        # the following 3 lines implement the nested listcomp
        transposed_row = []
        for row in matrix:
            transposed_row.append(row[i])
        transposed.append(transposed_row)
    print(transposed)

    # 使用内置函数
    print(list(zip(*matrix)))

    # 5.2. del 语句
    # del 语句按索引，而不是值从列表中移除元素。与返回值的 pop() 方法不同，
    # del 语句也可以从列表中移除切片，或清空整个列表（之前是将空列表赋值给切片）。
    a = [-1, 1, 66.25, 333, 333, 1234.5]
    print(a)

    del a[0]
    print(a)

    del a[2:5]
    print(a)

    del a[:]
    print(a)

    # 5.3. 元组和序列

    # 元组由多个被逗号隔开的值组成
    t = 12345, 54321, 'hello!'
    print(t)

    # 元组在输出时总被圆括号包围，以便能正确地解释嵌套元组
    # 不允许为元组中的单个元素赋值，当然，可以创建含列表等可变对象的元组

    # 虽然，元组与列表很像，但使用场景不同，用途也不同。元组是 immutable （不可
    # 变的），一般可包含异质元素序列，通过解包（见本节下文）或索引访问（如果
    # 是 namedtuples，可以属性访问）。列表是 mutable （可变的），列表元素一般为同质类型，可迭代访问。
    # 用一对空圆括号就可以创建空元组；只有一个元素的元组可以通过在这个元素后添加逗号来构建
    empty = ()
    singleton = 'hello',
    print(empty)
    print(singleton)

    # 元组的逆操作，称之为 序列解包，序列解包时，左侧变量与右侧序列元素的数量应相等
    x, y, z = t
    print(x, y, z)

    # 5.4. 集合
    # 集合是由不重复元素组成的无序容器

    # 创建集合用花括号或 set() 函数。注意，创建空集合只能用 set()，不能用 {}，后者创建的是空字典
    basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
    print(basket)
    print('apple' in basket)

    a = set('abracadabra')
    b = set('alacazam')
    print(a)

    print(a - b)
    print(a | b)
    print(a & b)
    print(a ^ b)

    # 集合也支持推导式
    a = {x for x in 'abracadabra' if x not in 'abc'}
    print(a)


if __name__ == '__main__':
    # learn_number()
    # learn_string()
    # learn_list()
    # fibonacci_number(30)
    # test_controlflow()

    test_datastruct()
