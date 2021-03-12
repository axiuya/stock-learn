def test_format():
    year = 2021
    event = 'Referendum'
    print(f'Result of the {year} {event}')

    yes_votes = 42_572_654
    no_votes = 43_132_495
    percentage = yes_votes / (yes_votes + no_votes)
    print('{:-9} yes votes {:2.2%}'.format(yes_votes, percentage))

    s = 'Hello world.'
    print(str(s))

    print(repr('hello, world\n'))

    for x in range(1, 11):
        print('{0:2d} {1:3d} {2:4d}'.format(x, x * x, x * x * x))

    # 通过使用 '**' 符号将 table 作为关键字参数传递
    table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
    print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))



def read_che_file():
    print("read_che_file")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('main')

    test_format()
