import threading
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from threading import Thread


def set_header(trv,data_df,app_globals):
    l1 = data_df.columns.values
    trv["columns"] = l1.tolist()
    # 加入 MultiIndex 的header
    if data_df.index.names[0] != None:
        trv["columns"] = list(data_df.index.names) + l1.tolist()
        for i in data_df.index.names:
            column_min_w = len(i) * 9 + 10
            column_w = int(trv.winfo_width() / len(l1) + len(data_df.index.names))
            if app_globals["auto_column_width"]:
                trv.column(i, minwidth=column_min_w, width=column_w, anchor="c")
            else:
                trv.column(i, minwidth=column_min_w, width=column_w, anchor="c", stretch=tk.NO)
            trv.heading(i, text=i)

    # 加入 column 的header
    for i in l1:
        column_min_w = len(i) * 9 + 10
        column_w = int(trv.winfo_width() / len(l1) + len(data_df.index.names)) - 1
        if app_globals["auto_column_width"]:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c")
        else:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c",stretch=tk.NO)

        trv.heading(i, text=i)

def insert_data(trv,data_df,progBar=None,percentage_label=None,data_df_len=None):
    trv["show"] = 'headings'
    if data_df_len == None:
        data_df_len = data_df.shape[0]
    elif data_df_len >  data_df.shape[0]:
            data_df_len = data_df.shape[0]


    #插入data
    check_list = [None for _ in range(len(data_df.index.names))]
    for i in range(data_df_len):
        v = [r for r in data_df.iloc[i]]
        total_v = v

        if data_df.index.names[0] != None:
            total_v = [data_df.index[i]] + v


        if i % 2 == 0:
            trv.insert("", "end", text=data_df.index[i], iid=i, values=total_v)
        else:
            trv.insert("", "end", text=data_df.index[i], iid=i, values=total_v, tags=("evenColor"))

        if progBar is not None:
            progBar["value"] += 100 / data_df.shape[0]
            percentage_label.config(text="列印數據中: " + str(round(progBar["value"], 2)) + "% - 己列印"+str(i)+"筆數據")


def set_header_for_pivot(trv,data_df,app_globals):
    l1 = data_df.columns.values
    trv["columns"] = list(data_df.index.names) + l1.tolist()
    # 加入 MultiIndex 的header
    for i in data_df.index.names:
        column_min_w = len(i) * 9 + 10
        column_w = int(trv.winfo_width() / len(l1) + len(data_df.index.names)) - 1
        #trv.column(i, minwidth=column_w, width=column_w, anchor="c")
        if app_globals["auto_column_width"]:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c")
        else:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c", stretch=tk.NO)
        trv.heading(i, text=i)

    # 加入 column 的header
    for i in l1:
        column_min_w = len(i) * 9 + 10
        column_w = int(trv.winfo_width() / len(l1) + len(data_df.index.names)) - 1
        if app_globals["auto_column_width"]:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c")
        else:
            trv.column(i, minwidth=column_min_w, width=column_w, anchor="c",stretch=tk.NO)
        trv.heading(i, text=i)


def insert_data_for_pivot(trv,data_df,CLT, progBar=None,percentage_label=None, data_df_len=None):
    if data_df_len == None:
        data_df_len = data_df.shape[0]
    elif data_df_len >  data_df.shape[0]:
            data_df_len = data_df.shape[0]


    # 插入data
    check_list = [None for _ in range(len(data_df.index.names))]
    for i in range(data_df_len):
        v = [r for r in data_df.iloc[i]]
        # tb_index = [data_df.index[i][0],data_df.index[i][1]]
        tb_index = []

        if CLT:
            for j in range(len(data_df.index.names)):
                if data_df.index[i][j] != check_list[j]:
                    check_list[j] = data_df.index[i][j]
                    tb_index.append(data_df.index[i][j])
                else:
                    tb_index.append("")
        else:
            for j in range(len(data_df.index.names)):
                check_list[j] = data_df.index[i][j]
                tb_index.append(data_df.index[i][j])

        total_v = tb_index + v


        if i % 2 == 0:
            trv.insert("", "end", text=data_df.index[i], iid=i, values=total_v)
        else:
            trv.insert("", "end", text=data_df.index[i], iid=i, values=total_v, tags=("evenColor"))
        if progBar is not None:
            progBar["value"] += 100/data_df.shape[0]
            percentage_label.config(text="列印數據中: " + str(round(progBar["value"], 2)) + "% - 己列印"+str(i)+"筆數據")