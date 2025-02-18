import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
import tkinter.messagebox
import pandas as pd
from threading import Thread
import pivot_data
import treeview_operate
import filter_data
import chardet
from io import StringIO

def print_table_to_treeviwe(root,app_globals,df):
    trv = root.nametowidget("table_Frame.main_trv")
    trv.delete(*trv.get_children())

    if df.shape[0]>5000:
        if app_globals["show_all_data"]:
            Pro_top, proBar, percentage_label = popup_lodadingwin()

            def to_treeview(trv, Pro_top, proBar, percentage_label):
                treeview_operate.set_header(trv, df, app_globals)
                treeview_operate.insert_data(trv, df, progBar=proBar,
                                             percentage_label=percentage_label)
                Pro_top.destroy()

            thread = Thread(target=to_treeview, args=(trv, Pro_top, proBar, percentage_label))
            thread.start()
        else:
            treeview_operate.set_header(trv, df, app_globals)
            treeview_operate.insert_data(trv, df, data_df_len=5000)
    else:
        treeview_operate.set_header(trv, df, app_globals)
        treeview_operate.insert_data(trv,df)


# def print_select_df(root,app_globals):
#     trv = root.nametowidget("table_Frame.main_trv")
#     trv.delete(*trv.get_children())
#     app_globals["output_df"] = app_globals["input_df"]
#
#     if app_globals["input_df"].shape[0]>5000:
#         if app_globals["show_all_data"]:
#             Pro_top, proBar, percentage_label = popup_lodadingwin()
#
#             def to_treeview(trv, Pro_top, proBar, percentage_label):
#                 treeview_operate.set_header(trv, app_globals["input_df"])
#                 treeview_operate.insert_data(trv, app_globals["input_df"], progBar=proBar,
#                                              percentage_label=percentage_label)
#                 Pro_top.destroy()
#
#             thread = Thread(target=to_treeview, args=(trv, Pro_top, proBar, percentage_label))
#             thread.start()
#         else:
#             treeview_operate.set_header(trv, app_globals["input_df"])
#             treeview_operate.insert_data(trv, app_globals["input_df"], data_df_len=5000)
#     else:
#         treeview_operate.set_header(trv, app_globals["input_df"])
#         treeview_operate.insert_data(trv, app_globals["input_df"])


def choose_delimiter(root, app_globals, file_path):
    window = tk.Toplevel(root)
    window.geometry("360x290+300+300")
    window.title("選擇CSV讀取設定")

    label = tk.Label(window, text="請輸入 CSV 文件的分隔符:")
    label.pack(pady=5)

    delimiter_var = tk.StringVar(value=',')

    entry = tk.Entry(window, textvariable=delimiter_var, width=5, justify='center' ,font= tkFont.Font(family="Arial", size=18))
    entry.pack(pady=2)

    label2 = tk.Label(window, text="")
    label2.pack()

    label_error = tk.Label(window, text="錯誤處理方式:")
    label_error.pack(pady=5)

    error_options_dir={
        "默認顯示錯誤":"strict",
        "忽略无法解码":"ignore",
        "使用替換字符":"replace",
        "字節替換為反斜杠轉義序列":"backslashreplace",
        "字節替換為 \\N{...} 轉義序列":"namereplace",

    }
    error_var = tk.StringVar(value='默認顯示錯誤')
    error_options = list(error_options_dir.keys())
    error_menu = ttk.Combobox(window, textvariable=error_var, values=error_options)
    error_menu.pack(pady=2)

    label3 = tk.Label(window, text="")
    label3.pack()

    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(1024)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
    except Exception as e:
        print(e)
        tk.messagebox.showerror("錯誤", f"無法識別編碼方式:\n{e}")

    label_encoding = tk.Label(window, text="編碼方式:")
    label_encoding.pack(pady=5)

    encoding_var = tk.StringVar(value=encoding)
    encoding_options = ["UTF-8"]
    if encoding not in encoding_options:
        encoding_options.append(encoding)
    encoding_menu = ttk.Combobox(window, textvariable=encoding_var, values=encoding_options)
    encoding_menu.pack(pady=2)

    def load_csv():
        delimiter = delimiter_var.get()
        error_option = error_var.get()
        encoding_option = encoding_var.get()
        try:
            with open(file_path, 'r', encoding=encoding_option, errors=error_options_dir[error_option]) as file:
                content = file.read()

            app_globals["input_df"] = pd.read_csv(StringIO(content), delimiter=delimiter,encoding=encoding_option)

            #app_globals["input_df"] = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding ,errors=error_options_dir[error_option])
            tk.messagebox.showinfo("已載入", "CSV 文件已成功載入!")
            window.destroy()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("錯誤", f"讀取 CSV 文件時發生錯誤:\n{e}")

    button = tk.Button(window, text="載入", command=load_csv)
    button.pack(pady=10)

    window.wait_window()
def choose_sheet(root,app_globals,file_path):
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names

    def load_sheet():
        sheet_name = var.get()
        app_globals["input_df"] = pd.read_excel(file_path, sheet_name=sheet_name)
        tk.messagebox.showinfo("已載入", f"表 '{sheet_name}' 已成功載入!")
        window.destroy()

    if len(sheets) > 1:
        window = tk.Toplevel(root)
        window.title("選擇指定表")

        label = tk.Label(window, text="選擇要載入的工作表:")
        label.pack(pady=10)

        var = tk.StringVar(value=sheets[0])

        combobox = ttk.Combobox(window, textvariable=var, values=sheets)
        combobox.pack(pady=10)

        button = tk.Button(window, text="載入", command=load_sheet)
        button.pack(pady=10)
        window.wait_window()
    else:
        app_globals["input_df"] = pd.read_excel(file_path, sheet_name=sheets[0])
        tk.messagebox.showinfo("已載入", f"表 '{sheets[0]}' 已成功載入!")
    # 等待窗口關閉
def select_file(root,app_globals):
    file_path = tk.filedialog.askopenfilename()
    app_globals["file_path"]=file_path
    _, current_file_extension = os.path.splitext(app_globals["file_path"])
    #app_globals["input_df"] = pd.read_excel(file_path)
    if current_file_extension == '.xlsx':
        choose_sheet(root,app_globals,app_globals["file_path"])
    elif current_file_extension == '.csv':
        choose_delimiter(root, app_globals,app_globals["file_path"])

    if file_path != "":
        try:
            index_setting_SubFrame = root.nametowidget("index_setting_Frame.index_setting_SubFrame")
            index_setting_SubFrame.destroy()
            root.nametowidget("index_setting_Frame.index_setting_SubFrame_scrolly")
        except:
            pass

        Index_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.index_ListBox")
        Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
        calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
        Index_ListBox.delete(0, tk.END)
        Value_ListBox.delete(0, tk.END)
        calc_ListBox.delete(0, tk.END)

        filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
        filter_listbox.delete(0, tk.END)

        app_globals["index_list"] = []
        app_globals["values_list"] = []
        app_globals["checkBOX_list"] = []

        option_menu = root.nametowidget("main_menu.option_menu")
        if app_globals["input_df"].shape[0]>5000:
            choose = tkinter.messagebox.askyesno(title="資料過載",message=f"這個文件資料過多,共{app_globals['input_df'].shape[0]} 筆數據\n 是否顯示全部?(如\"否\"則只顯示前5000筆數據)")
            app_globals["output_df"] = app_globals["input_df"]
            if choose:
                app_globals["show_all_data"] = True
                option_menu.entryconfig(1, label="只顯示少量資料")
            else:
                app_globals["show_all_data"] = False
                option_menu.entryconfig(1, label="顯示所有資料")
        else:
            app_globals["show_all_data"] = True
            option_menu.entryconfig(1, label="只顯示少量資料")

        #print_select_df(root, app_globals)
        app_globals["output_df"] = app_globals["input_df"]
        print(app_globals["input_df"])
        print_table_to_treeviwe(root, app_globals, app_globals["input_df"])

        #add_indexTolistBox(root, app_globals)
        change_column_type(root, app_globals)

def save_as(root,app_globals):
    if app_globals["input_df"].empty:
        tk.messagebox.showerror(title="error", message="未開啟檔案")
    else:
        with filedialog.asksaveasfile(initialfile="Untitle.csv",defaultextension=".csv",filetypes=[("CSV","*.csv"),("Excel","*.xlsx"),("All Files","*.*")]) as file:
            print(file.name.split(".", -1)[-1])
            if file.name.split(".", -1)[-1] == "xlsx":
                try:
                    app_globals["output_df"].to_excel(file.name)
                except Exception as e:
                    tk.messagebox.showerror(title="error",message=str(e))
            else:
                app_globals["output_df"].to_csv(file.name)


def reset(root,app_globals):
    Index_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.index_ListBox")
    Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    Index_ListBox.delete(0, tk.END)
    Value_ListBox.delete(0, tk.END)
    calc_ListBox.delete(0, tk.END)
    try:
        app_globals["input_df"] = pd.read_csv(app_globals["file_path"])
    except Exception as e:
        tk.messagebox.showerror(title="error", message=str(e))


    filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
    filter_listbox.delete(0, tk.END)

    app_globals["index_list"] = []
    app_globals["values_list"] = []
    app_globals["checkBOX_list"] = []
    app_globals["output_df"] = []
    app_globals["CLT"] = True
    # app_globals["show_all_data"] = True

    for widget in root.winfo_children():
        if isinstance(widget,tk.Toplevel):
            widget.destroy()

    app_globals["output_df"] = app_globals["input_df"]
    print_table_to_treeviwe(root, app_globals, app_globals["input_df"])

    change_column_type(root, app_globals)



def chnage_mode(event,app_globals, root, cbox):
    selection = cbox.get()
    pivot_config_Frame = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame")
    filter_config_Frame = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame")
    pivot_config_Frame.pack_forget()
    filter_config_Frame.pack_forget()
    if selection == "樞紐分析表":
        pivot_config_Frame.pack(side="top",fill=tk.BOTH,expand=True)
        Index_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.index_ListBox")
        Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
        calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
        Index_ListBox.delete(0, tk.END)
        Value_ListBox.delete(0, tk.END)
        calc_ListBox.delete(0, tk.END)

        app_globals["index_list"] = []
        app_globals["values_list"] = []
        app_globals["checkBOX_list"] = []
        app_globals["output_df"] = []
    if selection == "過濾器":
        filter_config_Frame.pack(side="top",fill=tk.BOTH,expand=True)

    a = app_globals["output_df"].reset_index()
    try:
        app_globals["input_df"] = a.drop(columns=["index"])
    except:
        app_globals["input_df"] = a
    pass

def add_indexTolistBox(root,app_globals):
    top = tk.Toplevel()
    top.title("增減索引")
    top.geometry("400x400")


    # print out all header of the file
    for index, index_text in enumerate(app_globals["input_df"].columns.values):
        # print(app_globals["input_df"].columns.values)
        if len(app_globals["checkBOX_list"]) < len(app_globals["input_df"].columns.values):
            app_globals["checkBOX_list"].append(tk.IntVar(value=0))
        datatype = str(app_globals["input_df"].dtypes[index_text])
        checkbox = tk.Checkbutton(top, text=index_text + " :: " +datatype, variable=app_globals["checkBOX_list"][index], command=lambda: change_values(root, app_globals), onvalue=1, offvalue=0)
        checkbox.pack(side="top",anchor=tk.W)

def change_values(root,app_globals):
    app_globals["values_list"] = []

    Index_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.index_ListBox")
    Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")

    Value_ListBox.delete(0,tk.END)
    Index_ListBox.delete(0,tk.END)
    calc_ListBox.delete(0,tk.END)

    for i,checkBox in enumerate(app_globals["checkBOX_list"]):
        if checkBox.get() == 0:
            # print(app_globals["input_df"].columns.values[i])
            if app_globals["input_df"].columns.values[i] in app_globals["index_list"]:
                app_globals["index_list"].remove(app_globals["input_df"].columns.values[i])

            app_globals["values_list"].append(app_globals["input_df"].columns.values[i])
        else:
            if app_globals["input_df"].columns.values[i] not in app_globals["index_list"]:
                app_globals["index_list"].append(app_globals["input_df"].columns.values[i])

    for index,col in enumerate(app_globals["index_list"]):
        Index_ListBox.insert(index, col)

    for index,col in enumerate(app_globals["values_list"]):
        Value_ListBox.insert(index, col)



# add clac columns to calc_ListBox and table
def add_values_col(event, root, app_globals):
    Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")

    cs = Value_ListBox.curselection()
    calc_List = [tk.IntVar(value=0) for _ in range(6)]

    def close_top_window(top, list):
        top.destroy()
        if calc_List[0].get() == 1:
            calc_ListBox.insert(tk.END,"Count: "+Value_ListBox.get(list))
        if calc_List[1].get() == 1:
            calc_ListBox.insert(tk.END,"Mean: "+Value_ListBox.get(list))
        if calc_List[2].get() == 1:
            calc_ListBox.insert(tk.END,"Min: "+Value_ListBox.get(list))
        if calc_List[3].get() == 1:
            calc_ListBox.insert(tk.END,"Max: "+Value_ListBox.get(list))
        if calc_List[4].get() == 1:
            calc_ListBox.insert(tk.END,"Median: "+Value_ListBox.get(list))
        if calc_List[5].get() == 1:
            calc_ListBox.insert(tk.END,"Sum: "+Value_ListBox.get(list))

        ##get data------------------------
        print_gen_table(root, app_globals, trv, calc_ListBox.get(0, tk.END))



    for list in cs:
        top = tk.Toplevel()
        top.title("添加"+Value_ListBox.get(list)+"值")
        top.wm_attributes("-topmost", "true")
        top.attributes("-toolwindow", 1)
        top.geometry("400x200+300+300")

        count_checkbox = tk.Checkbutton(top, text="Count", variable=calc_List[0],onvalue=1, offvalue=0)
        count_checkbox.grid(row=0,column=0,padx=5)

        sum_checkbox = tk.Checkbutton(top, text="Sum", variable=calc_List[5],onvalue=1, offvalue=0)
        sum_checkbox.grid(row=0,column=1,padx=5)

        mean_checkbox = tk.Checkbutton(top, text="Mean", variable=calc_List[1],onvalue=1, offvalue=0)
        mean_checkbox.grid(row=0,column=2,padx=5)


        min_checkbox = tk.Checkbutton(top, text="Min", variable=calc_List[2],onvalue=1, offvalue=0)
        min_checkbox.grid(row=1,column=0,padx=5)


        max_checkbox = tk.Checkbutton(top, text="Max", variable=calc_List[3],onvalue=1, offvalue=0)
        max_checkbox.grid(row=1,column=1,padx=5)

        median_checkbox = tk.Checkbutton(top, text="Median", variable=calc_List[4],onvalue=1, offvalue=0)
        median_checkbox.grid(row=1,column=2,padx=5)

        submit_button = tk.Button(top, text="新增", command=lambda: close_top_window(top, list))
        submit_button.grid(row=2,column=0,padx=10)
    pass



def print_gen_table(root, app_globals, trv, Value_operate):
    data_df1 = None
    ##get data------------------------
    trv.delete(*trv.get_children())

    data_df1 = pivot_data.gen_table(app_globals["input_df"], app_globals["index_list"], Value_operate)

    if not isinstance(data_df1, pd.DataFrame) and data_df1 == "Exception":
        calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
        calc_ListBox.delete(0,tk.END)
    else:
        app_globals["output_df"] = data_df1

    def to_treeview_limited(trv,data_df1):
        if len(data_df1.index.names) == 1:
            treeview_operate.set_header(trv, data_df1, app_globals)
            treeview_operate.insert_data(trv, data_df1,data_df_len=5000)
        else:
            treeview_operate.set_header_for_pivot(trv, data_df1, app_globals)
            treeview_operate.insert_data_for_pivot(trv, data_df1, app_globals["CLT"],data_df_len=5000)

    def to_treeview(trv, Pro_top, proBar, percentage_label):
            if len(data_df1.index.names) == 1:
                treeview_operate.set_header(trv, data_df1, app_globals)
                treeview_operate.insert_data(trv, data_df1, progBar=proBar, percentage_label=percentage_label)
            else:
                treeview_operate.set_header_for_pivot(trv, data_df1, app_globals)
                treeview_operate.insert_data_for_pivot(trv, data_df1, app_globals["CLT"], progBar=proBar, percentage_label=percentage_label)
            Pro_top.destroy()


    if data_df1 is None:
        # print_select_df(root, app_globals)
        app_globals["output_df"] = app_globals["input_df"]
        print_table_to_treeviwe(root, app_globals, app_globals["input_df"])
    else:
        if app_globals["input_df"].shape[0] > 5000:
            if app_globals["show_all_data"]:
                Pro_top, proBar, percentage_label = popup_lodadingwin()
                t2 = Thread(target=to_treeview, args=(trv, Pro_top, proBar, percentage_label))
                t2.start()
            else:
                to_treeview_limited(trv,data_df1)
        else:
            to_treeview_limited(trv,data_df1)

def del_values_col(event, root, app_globals):
    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")
    cs = calc_ListBox.curselection()
    result = tk.messagebox.askyesno("確定", "是否刪除計算項 "+calc_ListBox.get(cs[0]))
    if result:
        calc_ListBox.delete(cs[0])

        ##get data------------------------
        print_gen_table(root, app_globals, trv, calc_ListBox.get(0, tk.END))
    pass

def popup_lodadingwin():
    Pro_top = tk.Toplevel()
    Pro_top.title("處理中....")
    Pro_top.geometry("500x60+300+300")
    Pro_top.wm_attributes("-topmost","true")
    Pro_top.attributes("-toolwindow",1)
    proBar = ttk.Progressbar(Pro_top, orient=tk.HORIZONTAL, mode="determinate", length=100)
    proBar.pack(fill=tk.X, padx=10, pady=5)
    percentage_label = tk.Label(Pro_top, text="正在生成表...", anchor="w")
    percentage_label.pack(fill=tk.X, padx=15)

    return (Pro_top,proBar,percentage_label)




def change_column_type(root,app_globals):
    columns_type_list = []
    cobx_list = []
    Canvas_Window_list=[]
    Index_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.index_ListBox")
    Value_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.value_ListBox")
    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")

    top = root.nametowidget("index_setting_Frame")

    #resize the element--------------------------------------
    def on_frame_resize(event):
        Frame_width = root.nametowidget("index_setting_Frame").winfo_width() - 25
        Frame_height = root.nametowidget("index_setting_Frame").winfo_height() - 70
        for i,index_text in enumerate(app_globals["input_df"].columns.values):
            sub_Frame.itemconfig(Canvas_Window_list[i],width=Frame_width)
            sub_Frame.itemconfig(change_button_w, width=Frame_width)
            if Frame_height <= 30*len(app_globals["input_df"].columns.values):
                sub_Frame.moveto(change_button_w, 0, 30*len(app_globals["input_df"].columns.values)+1)
            else:
                sub_Frame.moveto(change_button_w, 0, Frame_height)

    top.bind("<Configure>",on_frame_resize)
    scrollregion_hight=len(app_globals["input_df"].columns.values)*30+31
    sub_Frame = tk.Canvas(top,scrollregion=(0,0,0,scrollregion_hight),name="index_setting_SubFrame")

    scrolly = tk.Scrollbar(top,orient='vertical',name="index_setting_SubFrame_scrolly")
    scrolly.pack(side='right', fill='y')
    scrolly.config(command=sub_Frame.yview)

    sub_Frame.config(yscrollcommand=scrolly.set)

    sub_Frame.pack(side="left",expand=True,fill=tk.BOTH)




    def change_type_list(event, index, colu_cbox):
        columns_type_list[index] = colu_cbox.get()

    # print out all header of the file

    for index, index_text in enumerate(app_globals["input_df"].columns.values):
        datatype = str(app_globals["input_df"].dtypes[index_text])
        c_type = ("int64","float64","object","datetime64[ns]","str")

        row_Frame=tk.Frame(sub_Frame,name="row_Frame"+str(index))

        Frame_width = root.nametowidget("index_setting_Frame").winfo_width()-25
        Canvas_Window_list.append(sub_Frame.create_window(0, 30*index, height=30,width=Frame_width, window=row_Frame, anchor="nw"))

        column_label = tk.Label(row_Frame, text=index_text)
        column_label.pack(side="left",fill=tk.BOTH,anchor='w')
        column_cbox=ttk.Combobox(row_Frame,width=10)
        cobx_list.append(column_cbox)
        column_cbox.pack(side="right",pady=3,padx=2)
        column_cbox["value"] = c_type
        column_cbox.current(c_type.index(datatype))
        columns_type_list.append(datatype)

        cobx_list[index].bind("<<ComboboxSelected>>",lambda event, index=index, column_cbox=column_cbox: change_type_list(event,index,column_cbox))


    def chnage_type():
        df = app_globals["input_df"]
        for index, index_text in enumerate(df.columns.values):
            try:
                df[index_text]= df[index_text].astype(columns_type_list[index])
            except Exception as e:
                tk.messagebox.showerror(title="error", message=str(e))

        print(columns_type_list)
        sub_Frame.destroy()
        change_column_type(root, app_globals)

        ##print data------------------------
        Index_ListBox.delete(0,tk.END)
        Value_ListBox.delete(0,tk.END)
        calc_ListBox.delete(0,tk.END)
        app_globals["index_list"]=[]
        app_globals["values_list"] = []
        app_globals["checkBOX_list"] = []
        # print_select_df(root, app_globals)
        app_globals["output_df"] = app_globals["input_df"]
        print_table_to_treeviwe(root, app_globals, app_globals["input_df"])
        #add_indexTolistBox(root, app_globals)
        reset_filter_rule(root, app_globals)

    #update button-----------------------------------
    change_button = tk.Button(sub_Frame,text="更新",command=chnage_type,name="change_button")
    Frame_width = root.nametowidget("index_setting_Frame").winfo_width() - 25
    Frame_height = root.nametowidget("index_setting_Frame").winfo_height() - 70

    change_button_w = sub_Frame.create_window(0, Frame_height, height=30, width=Frame_width, window=change_button, anchor="nw")



def change_ClT(root,app_globals):
    mode_cbox = root.nametowidget("config_outside_Frame.config_Frame.mode_cbox")
    option_menu = root.nametowidget("main_menu.option_menu")
    if app_globals["CLT"]:
        app_globals["CLT"]= False
        option_menu.entryconfig(0,label="開啟合併索引同類項")
    else:
        app_globals["CLT"] =True
        option_menu.entryconfig(0,label="關閉合併索引同類項")

    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")

    if mode_cbox.get() == "樞紐分析表":
        print_gen_table(root, app_globals, trv, calc_ListBox.get(0, tk.END))
    elif mode_cbox.get() == "過濾器":
        show_filter_result(root, app_globals)

def change_show_all_data(root,app_globals):
    mode_cbox = root.nametowidget("config_outside_Frame.config_Frame.mode_cbox")
    option_menu = root.nametowidget("main_menu.option_menu")
    if app_globals["show_all_data"]:
        app_globals["show_all_data"]= False
        option_menu.entryconfig(1,label="顯示所有資料")
    else:
        app_globals["show_all_data"] =True
        option_menu.entryconfig(1,label="只顯示少量資料")

    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")

    if mode_cbox.get() == "樞紐分析表":
        print_gen_table(root, app_globals, trv, calc_ListBox.get(0, tk.END))
    elif mode_cbox.get() == "過濾器":
        show_filter_result(root, app_globals)


def change_auto_column_width(root,app_globals):
    mode_cbox = root.nametowidget("config_outside_Frame.config_Frame.mode_cbox")
    option_menu = root.nametowidget("main_menu.option_menu")
    if app_globals["auto_column_width"]:
        app_globals["auto_column_width"]= False
        option_menu.entryconfig(2,label="自動欄寬")
    else:
        app_globals["auto_column_width"] =True
        option_menu.entryconfig(2,label="手動欄寬")

    calc_ListBox = root.nametowidget("config_outside_Frame.config_Frame.pivot_config_Frame.calc_ListBox")
    trv = root.nametowidget("table_Frame.main_trv")

    if mode_cbox.get() == "樞紐分析表":
        print_gen_table(root, app_globals, trv, calc_ListBox.get(0, tk.END))
    elif mode_cbox.get() == "過濾器":
        show_filter_result(root, app_globals)



def show_filter_result(root, app_globals):
    filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
    operate_list = filter_listbox.get(0,tk.END)

    df = filter_data.filter(app_globals["input_df"],operate_list)
    app_globals["output_df"] = df

    print_table_to_treeviwe(root, app_globals, df)
    pass

def add_filter_rule(root,app_globals):
    top = tk.Toplevel(root)
    top.title("添加規則")
    top.geometry("500x400+300+300")
    top.wm_attributes("-topmost","true")
    top.attributes("-toolwindow",1)

    def chnage_column_unique_list(event, root, top, app_globals):
        cbox = top.nametowidget("column_setting_Frame.column_cbox")
        unuse_item_listbox = top.nametowidget("items_setting_Frame.unuse_item_Frame.unuse_item_listbox")
        used_item_listbox = top.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")
        select_column = app_globals["input_df"][cbox.get()]

        unuse_item_listbox.delete(0,tk.END)
        used_item_listbox.delete(0,tk.END)

        filter_listbox =root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
        ori_filter_list = filter_listbox.get(0, tk.END)
        op_dic = filter_data.separte_aggfunc(app_globals["input_df"],ori_filter_list)

        for i, item in enumerate(select_column.unique()):
            if cbox.get() in op_dic:
                if item not in op_dic[cbox.get()]:
                    unuse_item_listbox.insert(i, item)
            else:
                unuse_item_listbox.insert(i,item)
        pass

    def add_item(root, app_globals):
        unuse_item_listbox = root.nametowidget("items_setting_Frame.unuse_item_Frame.unuse_item_listbox")
        used_item_listbox = root.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")

        for index_of_selection in unuse_item_listbox.curselection():
            used_item_listbox.insert(tk.END, unuse_item_listbox.get(index_of_selection))

        sel = unuse_item_listbox.curselection()
        for index_of_selection in sel[::-1]:
            unuse_item_listbox.delete(index_of_selection)
        pass

    def del_item(root, app_globals):
        unuse_item_listbox = root.nametowidget("items_setting_Frame.unuse_item_Frame.unuse_item_listbox")
        used_item_listbox = root.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")

        for index_of_selection in  used_item_listbox.curselection():
            unuse_item_listbox.insert(tk.END, used_item_listbox.get(index_of_selection))

        sel = used_item_listbox.curselection()
        for index_of_selection in sel[::-1]:
            used_item_listbox.delete(index_of_selection)
        pass

    def add_all_item(root, app_globals):
        unuse_item_listbox = root.nametowidget("items_setting_Frame.unuse_item_Frame.unuse_item_listbox")
        used_item_listbox = root.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")

        unuse_list = unuse_item_listbox.get(0,tk.END)
        for i, item in enumerate(unuse_list):
            used_item_listbox.insert(tk.END, unuse_item_listbox.get(i))

        unuse_item_listbox.delete(0,tk.END)
        pass

    def del_all_item(root, app_globals):
        unuse_item_listbox = root.nametowidget("items_setting_Frame.unuse_item_Frame.unuse_item_listbox")
        used_item_listbox = root.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")

        used_list = used_item_listbox.get(0,tk.END)
        for i, item in enumerate(used_list):
            unuse_item_listbox.insert(tk.END, used_item_listbox.get(i))

        used_item_listbox.delete(0,tk.END)
        pass

    def add_to_filter(root,top, app_globals):
        cbox = top.nametowidget("column_setting_Frame.column_cbox")
        used_item_listbox = top.nametowidget("items_setting_Frame.used_item_Frame.used_item_listbox")
        filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
        filter_list = used_item_listbox.get(0,tk.END)
        for i, item in enumerate(filter_list):
            new_item = cbox.get()+" <give> "+str(item)
            filter_listbox.insert(tk.END,new_item)
        top.destroy()

        operate_list = filter_listbox.get(0,tk.END)

        df = filter_data.filter(app_globals["input_df"],operate_list)
        app_globals["output_df"] = df

        print_table_to_treeviwe(root, app_globals, df)
        pass


    # column_setting_Frame============================
    column_setting_Frame = tk.Frame(top,name="column_setting_Frame")
    column_setting_Frame.pack(fill=tk.BOTH,anchor="nw",padx=10,pady=5)

    column_setting_title_label = tk.Label(column_setting_Frame,text="Column: ")
    column_setting_title_label.pack(side="left")
    column_cbox = ttk.Combobox(column_setting_Frame,name="column_cbox")
    column_cbox.pack(side="left")
    column_cbox["value"] = list(app_globals["input_df"].columns.values)

    column_cbox.bind("<<ComboboxSelected>>",lambda event, app_globals=app_globals: chnage_column_unique_list(event,root, top, app_globals))

    rule_title_lable = tk.Label(column_setting_Frame,text="中")
    rule_title_lable.pack(side="left")



    # items_setting_Frame============================
    items_setting_Frame = tk.Frame(top,name="items_setting_Frame")
    items_setting_Frame.pack(fill=tk.BOTH, expand=True, anchor="nw", padx=10, pady=5)


    # unuse_item_Frame-----------------------------------
    unuse_item_Frame = tk.Frame(items_setting_Frame,name="unuse_item_Frame")
    unuse_item_Frame.pack(side="left",fill=tk.BOTH, expand=True,)

    unuse_item_title_lable = tk.Label(unuse_item_Frame,text="可過濾值:")
    unuse_item_title_lable.pack(side="top",anchor="w")

    unuse_item_listbox = tk.Listbox(unuse_item_Frame, selectmode="multiple", name="unuse_item_listbox")
    unuse_item_listbox.pack(side="top",expand=True,fill=tk.BOTH)
    
    # button_Frame-----------------------------------
    button_Frame = tk.Frame(items_setting_Frame,name="button_Frame")
    button_Frame.pack(side="left")
    
    add_button = tk.Button(button_Frame,text="->",command=lambda app_globals=app_globals: add_item(top, app_globals))
    add_button.pack(pady=3,padx=5,fill=tk.X)
    del_button = tk.Button(button_Frame,text="<-",command=lambda app_globals=app_globals: del_item(top, app_globals))
    del_button.pack(pady=3,padx=5,fill=tk.X)
    bank_label = tk.Label(button_Frame)
    bank_label.pack(pady=3,padx=5,fill=tk.X)
    add_button = tk.Button(button_Frame,text="->>",command=lambda app_globals=app_globals: add_all_item(top, app_globals))
    add_button.pack(pady=3,padx=5,fill=tk.X)
    del_button = tk.Button(button_Frame,text="<<-",command=lambda app_globals=app_globals: del_all_item(top, app_globals))
    del_button.pack(pady=3,padx=5,fill=tk.X)


    # used_item_Frame-----------------------------------
    used_item_Frame = tk.Frame(items_setting_Frame,name="used_item_Frame")
    used_item_Frame.pack(side="left",fill=tk.BOTH, expand=True,)

    used_item_title_lable = tk.Label(used_item_Frame,text="需過濾值:")
    used_item_title_lable.pack(side="top",anchor="w")

    used_item_listbox = tk.Listbox(used_item_Frame, selectmode="multiple", name="used_item_listbox")
    used_item_listbox.pack(side="top",expand=True,fill=tk.BOTH)


    submit_button = tk.Button(top,text=" 添加 ",command=lambda root=root, app_globals=app_globals: add_to_filter(root, top, app_globals))
    submit_button.pack(anchor="e",padx=10,pady=3)
    

    pass


def del_filter_rule(event, root, app_globals):
    filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")


    cs = filter_listbox.curselection()
    result = tk.messagebox.askyesno("確定", "是否刪除計算項 " + filter_listbox.get(cs[0]))
    if result:
        filter_listbox.delete(cs[0])

        ##get data------------------------
        operate_list = filter_listbox.get(0, tk.END)
        df = filter_data.filter(app_globals["input_df"],operate_list)
        app_globals["output_df"] = df
        print_table_to_treeviwe(root, app_globals, df)
    pass

def reset_filter_rule( root, app_globals):
    filter_listbox = root.nametowidget("config_outside_Frame.config_Frame.filter_config_Frame.filter_listbox")
    filter_listbox.delete(0,tk.END)
    print_table_to_treeviwe(root, app_globals, app_globals["input_df"])
