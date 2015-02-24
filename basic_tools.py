if __name__ == '__main__':
    print("Not allowed to run it directly!")
    exit()

def load_csv(filename):
    import csv
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return tuple(reader)

def split_str(s):
    return [float(i) for i in s.strip().split()]

def get_input(line_handler=lambda s: float(s)):
    n = int( input() )
    data = []
    for i in range(n):
        s = input()
        data.append(line_handler(s))
    return data

def is_prefix(a:str, b:str):
    '''If a is the prefix of b
    '''
    return b[:len(a)] == a

def longest_common_prefix(strings):
    '''strings is an iterable object
    Current implement is VERY VERY slow

    Return a string
    '''
    max_length = min( map(len, strings) )

    prefix = strings[0]
    while prefix:
        res = [is_prefix(prefix, s) for s in strings]
        if False not in set(res): break
        prefix = prefix[:-1]

    return prefix

def get_range(li):
    return (min(li), max(li))

