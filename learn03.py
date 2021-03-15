import json
import os.path as osp


def file_op():
    """
    文件操作，读取和写入
    :return:
    """
    # with open('./resources/docker-compose.yml', 'r') as f:
    #     read_data = f.read()
    #     print(read_data)
    #     print(f.name)

    # with open('./resources/docker-compose.yml', 'r') as f:
    #     # # 循环文件
    #     # for line in f:
    #     #     print(line)
    #
    #     # 读取文件行
    #     lines = f.readlines()
    #     print(lines)

    # with open("./resources/test-write.txt", 'w') as f:
    #     count = f.write("This is a test\n")
    #     print(count)
    #
    #     value = ("the answer", 343)
    #     count = f.write(str(value))
    #     print(count)
    #
    #     print("tell:", f.tell())

    print(osp.exists('./resources/swagger-api.json'))
    print(osp.isdir('./resources/swagger-api.json'))
    print(osp.isfile('./resources/swagger-api.json'))

    with open('./resources/swagger-api.json', 'rb+') as f:
        api_json = json.load(f)
        print(api_json)
        print(json.dumps(api_json))


def try_exception():
    """
    异常处理
    :return: None
    """
    first = True
    while True:
        try:
            if first:
                x = int(input('Please enter a number: '))
            else:
                x = int(input())
            print('x =', x)
            break
        except ValueError:
            first = False
            print("Oops! That was no valid number. Try again...")
        except Exception as err:
            print('错误信息:', err.args)
            raise CustomException('自定义的异常')


class CustomException(Exception):
    """
    自定义异常
    """


def test_class():
    x = MyClass()
    print(x.func())
    print(x.i)
    print(x.__doc__)
    print(x.data)

    cpx = Complex(3.0, -4.5)
    print(cpx.r, cpx.i)


class MyClass:
    """A simple example class"""
    i = 1232

    def __init__(self):
        self.data = []

    def func(self):
        return "Hello world!"


class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


if __name__ == '__main__':
    print()
    file_op()
    # try_exception()
    # test_class()
