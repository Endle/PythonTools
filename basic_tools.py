if __name__ == '__main__':
    print("Not allowed to run it directly!")
    exit()

def split_str(s):
    return [float(i) for i in s.strip().split()]

def get_input(line_handler=lambda s: float(s)):
    n = int( input() )
    data = []
    for i in range(n):
        s = input()
        data.append(line_handler(s))
    return data
