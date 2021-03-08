

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('main')

    test_format()
