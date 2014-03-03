#Use python3!

def get_input():
    ret = dict()
    print ("N = ?", end="     ")
    n = int(input())
    ret['n'] = n

    for i in range(n):
        print(str(i)+":  ", end="")
        x = int(input())
        ret[i] = x
    
    return ret
    

def compute(data):
    pass


data = get_input()
S = compute(data)
print ("S = " + str(S))
