import pandas as pd


def separte_aggfunc(df,operate_list):
    op_dict={}
    for operate in operate_list:
        sp_op=operate.split(" <give> ",1)

        if df.dtypes[sp_op[0]] == "int64":
            sp_op[1] = int(sp_op[1])
        if df.dtypes[sp_op[0]] == "float64":
            sp_op[1] = float(sp_op[1])

        if sp_op[0] in op_dict.keys():
            op_dict[sp_op[0]].append(sp_op[1])
        else:
            op_dict[sp_op[0]] = [sp_op[1]]
    print(op_dict)
    return op_dict

def filter(df,operate_list):
    print(operate_list)
    op_dic = separte_aggfunc(df,operate_list)
    filter_df =df
    for i,row in enumerate(op_dic):
        filter_df = filter_df[filter_df[row].isin(op_dic[row])]

    print(filter_df)
    return filter_df
    pass