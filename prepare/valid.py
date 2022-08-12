
def is_mat(mat):
    m = -1
    for row in mat:
        if m == -1: m = len(row)
        elif m != len(row): return False
    return True
    

def test_json(args):
    _, fn = args
    import json
    with open(fn) as fp:
        data = json.load(fp)
        for k, v in data.items():
            assert is_mat(v['table_array'])
            print(f'v\t{k}')


if __name__ == '__main__':
    import sys
    test_json(sys.argv)