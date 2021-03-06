import os

count_only_first_error = True

def load():
    if os.path.exists('statementErrors.csv'):
        with open('statementErrors.csv','r') as f:
            res = {}
            l = f.readline().strip()
            while len(l) > 0:
                n = int(l)
                f.readline()
                counts = map(lambda x: int(x.strip()), f.readline().strip().split(','))
                res[n] = dict(map(lambda i: (i+1,counts[i]), range(len(counts))))
                f.readline()
                l = f.readline().strip()
            return res
    else:
        return {}

def store(data):
    with open('statementErrors.csv','w') as f:
        for n in sorted(data.keys()):
            f.write(str(n)+'\n')
            f.write(','.join(map(lambda i: str(i+1), range(n)))+'\n')
            f.write(','.join(map(lambda i: str(data[n][i+1]), range(n)))+'\n')
            f.write('\n')

def filter(c,ll,out):
    if not c:
        return False
    if not out:
        return False
    if len(out) == 0:
        return False
    out = out[0]  # only count best translation
    n = c.count(';')
    out = out+';'*(n-out.count(';'))
    data = load()
    if n not in data.keys():
        data[n] = {}
        for i in range(n):
            data[n][i+1] = 0
    c = map(lambda x: x.strip(), c.split(';'))
    out = map(lambda x: x.strip(), out.split(';'))
    for i in range(n):
        if c[i] != out[i]:
            data[n][i+1] += 1
            if count_only_first_error:
                break
    store(data)
    return True
