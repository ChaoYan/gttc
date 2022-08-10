def flatten(dct):
    ans = {}
    v = []
    def dfs(i):
        if not isinstance(i, dict):
            ans['/'.join(map(str, v))] = i
            return 
        for kk, ii in i.items():
            v.append(kk)
            dfs(ii)
            del v[-1]
    dfs(dct)
    return ans

if __name__ == '__main__':
    dct = {'label 1': {'precision':0.5,
             'recall':1.0,
             'f1-score':0.67,
             'support':1}, 'label 2': {'foo': {'bar': 404}}}
    print(flatten(dct))
