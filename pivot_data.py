import pandas as pd
import numpy as np
import tkinter as tk


def translate_textTOaggfunc(Text):
    if Text == "Count":
        return "count"
    if Text == "Mean":
        return np.mean
    if Text == "Min":
        return np.min
    if Text == "Max":
        return np.max
    if Text == "Median":
        return np.median
    if Text == "Sum":
        return np.sum


def separte_aggfunc(operate_list):
    op_dict={}
    for operate in operate_list:
        sp_op=operate.split(": ",1)
        print(sp_op)
        if sp_op[1] in op_dict.keys():
            print(type(op_dict[sp_op[1]]))
            op_dict[sp_op[1]].append(translate_textTOaggfunc(sp_op[0]))
        else:
            op_dict[sp_op[1]] = [translate_textTOaggfunc(sp_op[0])]
    # print(op_dict)
    return op_dict


def gen_table(input_df, Table_index, Value_operate):
    print(input_df)

    op_dic = separte_aggfunc(Value_operate)
    result_df = None


    for index in op_dic.keys():
        # print(index)
        # print(Table_index)
        # print(op_dic[index])

        try:
            PVT_df = input_df.pivot_table(values=index, index=Table_index, aggfunc=op_dic[index])
            print(f'input_df.pivot_table(values={index}, index={Table_index}, aggfunc={op_dic[index]})')
            PVT_df.columns = PVT_df.columns.map(lambda x: f"{x[0]}.{x[1]}" if isinstance(x, tuple) else x)

            if result_df is None:
                result_df = PVT_df
            else:
                for key in PVT_df.columns.values:
                    result_df[key] = PVT_df[key]
            print("===============================")
            # print(result_df)
        except Exception as e:
            tk.messagebox.showerror(title="error", message=str(e))
            return "Exception"
    return result_df