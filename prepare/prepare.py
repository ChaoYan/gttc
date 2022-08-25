import os
import json
import numpy as np
import pandas as pd
from argparse import *
from collections import *

def prepare(data, label):
    # ans = {'table0': [{
    #             'SheetName': 'sheet0',
    #             'RowCount': 2,
    #             'ColumnCount': 1,
    #             'CellAttributes': [
    #                     [{'Text': 'header', 'CellRole': '1'}],
    #                     [{'Text': 'data', 'CellRole': '0'}],
    #             ],
    #             'MergedRegions': [{"FirstRow": 0, "LastRow": 0, "FirstColumn": 0, "LastColumns": 0}]
    #         }]
    # }
    
    # ret_data = {'tablename-sheetname': array}, ret_label = {'tab-sht': i}
    ret_data, ret_label = {}, {}

    label_dict = defaultdict(dict)
    for i, t, s, y in label.itertuples():
        label_dict[str(t)][str(s)] = str(int(y[0] == 'S' and y[6] == 'H'))
    
    # combine data and labels
    ret = defaultdict(dict)
    root = {}
    for rec in data:
        selected = rec[0], rec[1], rec[2], rec[5], rec[6], rec[7], rec[10]
        tid, sid, rid, cs, ce, txt, vm = selected
        rid, cs, ce = map(int, (rid, cs, ce))
        vm = 0 if vm[0] == 'N' else 1 if vm[0] == 'S' else 2
        txt = txt.split('þ')
        assert txt[-1] == ''
        txt = '\n'.join(txt[:-1])
        txts = ['' if i != cs else txt for i in range(cs, ce)]
        assert tid in label_dict
        assert sid in label_dict[tid]
        cells = list(zip(txts, [label_dict[tid][sid]] * len(txts)))
        if tid not in ret or sid not in ret[tid]:
            ret[tid][sid] = [[], {}]
        stca, stmr = ret[tid][sid]
        assert rid <= len(stca)
        if rid == len(stca): # Add a new row
            stca.append(cells)
        else:                # Add a new col
            assert cs <= len(stca[rid])
            if cs == len(stca[rid]):
                stca[rid].extend(cells)
            else:            # Skip a new þ
                continue
        if (vm == 0 and ce - cs > 1) or vm == 1:
            r, c = root[(rid, cs)] = (rid, cs)
            stmr[(r, c)] = [rid, ce - 1]
        elif vm == 2:
            r, c = root[rid - 1, cs]
            stmr[(r, c)][0] = rid
            root[(rid, cs)] = (r, c)
    ans = defaultdict(list)
    for t, sheets in ret.items():
        for s, z in sheets.items():
            mat, dct = z
            
            for i, row in enumerate(mat):
                assert len(row) == len(mat[0])
                for j in range(len(row)):
                    txt, lab = row[j]
                    row[j] = {'Text': txt, 'CellRole': lab, 'RowNumber': i, 'ColumnNumber': j, 'NumberFormatString': ''}

            lst = []
            for tl, br in dct.items():
                (xr, xc), (yr, yc) = (tl, br)
                # assert yr - xr > 0 or yc - xc > 0  # ! important
                if yr - xr > 0 or yc - xc > 0:
                    lst.append({"FirstRow": xr, "LastRow": yr, "FirstColumn": xc, "LastColumn": yc})
            
            ans[t].append({
                'SheetName': s,
                'CellAttributes': mat,
                'MergedRegions': lst,
                'RowCount': len(mat),
                'ColumnCount': len(mat[0]),
                'FirstRowNumber': 0,             # ? review
                'FirstColumnNumber': 0           # ? review
            })
            tabname = f'{t}-{s}'
            ret_data[tabname] = {'table_array': mat}
            ret_label[tabname] = lab
    assert len(label) ==  sum(len(v) for k, v in ans.items())
    return ret_data, ret_label

    
def read_csv(src, sep=','):
    data = []
    with open(src, 'r') as f:
        header = next(f).split(sep)
        nrow = len(header)
        for i, line in enumerate(f):
            if not line: break
            rec = line.split(sep)
            assert len(rec) == nrow, f'Record {i + 2}: {line}'
            data.append(rec)
    return header, data


def main(args):
    print(args)
    
    data_splits = []
    qtrel = []
    
    fname_id = {'train.csv': 0, 'valid.csv': 1, 'test.csv': 2}
    
    for name in os.listdir(args.data_dir):
        print(f'{name} ...')
        src = os.path.join(args.data_dir, name)
        header, data = read_csv(src, sep='\t')
        label = pd.read_csv(os.path.join(args.label_dir, name))
        # output = prepare(data, label)
        # for table_id, sheets in output.items():
        #     dist = os.path.join(args.output_dir, '-'.join((name, table_id)))
        #     with open(dist, 'w') as f:
        #         for s in sheets:
        #             f.write(json.dumps(s) + '\n')
        ret_data, ret_label = prepare(data, label)
        data_splits.append(ret_data)
        for tab, lab in ret_label.items():
            qtrel.append([fname_id[name], 0, tab, lab])
        
        print(f'{name} done.')
        
    pd.DataFrame.from_records(qtrel)
    data_all = {}
    for i in data_splits: data_all.update(i)
    assert len(data_all) == sum(len(i) for i in data_splits)
    with open('tables.json', 'w') as f: json.dump(data_all, f)
    pd.DataFrame.from_records(qtrel).to_csv('qtrels.txt', sep='\t', header=False, index=False)
            

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument('data_dir')
    parser.add_argument('label_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()
    main(args)