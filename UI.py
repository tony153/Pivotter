import tkinter as tk
from tkinter import ttk
import split_file
import pandas as pd
import UIfun

#========global values============
input_df = pd.DataFrame()
output_df = pd.DataFrame()
index_list=[]
values_list = []
checkBOX_list= []

input_df = pd.DataFrame()
app_globals = {
    "file_path": None,
    "input_df": input_df,
    "output_df": output_df,
    "index_list": index_list,
    "values_list": values_list,
    "checkBOX_list": checkBOX_list,
    "CLT":True,#Combining Like Terms
    "show_all_data":True,
    "auto_column_width":True,
}

#========global setting============
pd.set_option('display.float_format',lambda x: '%.2f' % x)


##get data------------------------
# data_df = test.gen_data()

#input_file_df = pd.read_csv("input/ICBCM_PBC_list_2023.csv")

#======create Frame==============
# root wiondown -----------------
root = tk.Tk()
root.title("Pivotter")
root.geometry("900x600")

# panedWindow -------------------
P_window1 = tk.PanedWindow(root,showhandle=False,sashrelief="groove",handlesize=5,handlepad=0,sashpad=0,sashwidth=4)
P_window1.pack(fill=tk.BOTH,expand=True)

# Index_setting -----------------
index_setting_Frame = tk.Frame(root,padx=2, name="index_setting_Frame")

# Config Frame ------------------
config_outside_Frame = tk.Frame(root,padx=2, name="config_outside_Frame")
config_outside_Frame.pack(fill=tk.BOTH,expand=True)

config_Frame = tk.Frame(config_outside_Frame,pady=5,padx=4, name="config_Frame")

pivot_config_Frame = tk.Frame(config_Frame,pady=5,padx=4, name="pivot_config_Frame")
filter_config_Frame = tk.Frame(config_Frame,pady=5,padx=4, name="filter_config_Frame")


# Title Frame -------------------
Title_Frame1 =tk.Frame(pivot_config_Frame)
Title_Frame1.pack(fill=tk.BOTH)

Title_Frame2 =tk.Frame(filter_config_Frame)
Title_Frame2.pack(fill=tk.BOTH)
#=================================





# Menu ============================
main_menu =tk.Menu(root, name="main_menu")
file_menu = tk.Menu(main_menu, tearoff=False)

#file------------------------------
file_menu.add_command(label="開啟檔案",command=lambda: UIfun.select_file(root,app_globals))
file_menu.add_command(label="另存新檔",command=lambda: UIfun.save_as(root,app_globals))
file_menu.add_command(label="分割檔案",command=lambda: split_file.to_split_file(root,app_globals))
main_menu.add_cascade(label="文件",menu=file_menu)

#option------------------------------
option_menu = tk.Menu(main_menu, tearoff=False, name="option_menu")
option_menu.add_command(label="關閉合併索引同類項",command=lambda: UIfun.change_ClT(root,app_globals))
option_menu.add_command(label="只顯示少量資料",command=lambda: UIfun.change_show_all_data(root,app_globals))
option_menu.add_command(label="手動欄寬",command=lambda: UIfun.change_auto_column_width(root,app_globals))
option_menu.add_command(label="重置所有",command=lambda: UIfun.reset(root,app_globals))
main_menu.add_cascade(label="選項",menu=option_menu)

root.config(menu=main_menu)
#===================================





# mode ==============================
mode_cbox = ttk.Combobox(config_Frame,name="mode_cbox")
mode_cbox.pack(fill=tk.X)
mode_cbox["value"]=("樞紐分析表","過濾器")
mode_cbox.current(0)
mode_cbox.bind("<<ComboboxSelected>>",lambda event, app_globals=app_globals, root=root, mode_cbox=mode_cbox: UIfun.chnage_mode(event,app_globals,root, mode_cbox))

separator = ttk.Separator(config_Frame,orient='horizontal')
separator.pack(fill='x',pady=6)
#===================================





#index BOX===================================
index_setting_Frame_title= tk.Label(index_setting_Frame,text="列類型:",font=("Arial",13),anchor="nw")
index_setting_Frame_title.pack(fill=tk.X,pady=6)
#============================================





# Table initialization ========================
Table_Frame = tk.Frame(name="table_Frame")
Table_Frame.pack(side="left",fill=tk.BOTH, expand=True)
trv = ttk.Treeview(Table_Frame, selectmode='extended', name="main_trv")
trv.pack(fill=tk.BOTH,expand=True)
trv["show"] = 'headings'

##set scrollbar-------------------------------
yscrollbar = tk.Scrollbar(config_outside_Frame)
yscrollbar.pack(side="left",fill=tk.Y, padx=0)
yscrollbar.config(command=trv.yview)
trv.configure(yscrollcommand=yscrollbar.set)

xscrollbar = tk.Scrollbar(Table_Frame,orient='horizontal')
xscrollbar.place(anchor=tk.S, relx=0.5,rely=1.0, relwidth=1.0)
xscrollbar.config(command=trv.xview)
trv.configure(xscrollcommand=xscrollbar.set)


config_Frame.pack(side="left",fill=tk.BOTH,expand=True)
pivot_config_Frame.pack(side="top",fill=tk.BOTH,expand=True)
#style 設定-----------------------------------
trv.tag_configure("evenColor",background="#efefef")
s = ttk.Style()
s.theme_use('classic')
s.configure('Treeview.Heading',background="#eeeeee")
#============================================





# pivot_config_Frame.title ===========================
add_index_button = tk.Button(Title_Frame1,text="+/-",command=lambda: UIfun.add_indexTolistBox(root,app_globals))
# change_column_type_button = tk.Button(Title_Frame1,text="更改列類型",command=lambda: UIfun.change_column_type(root,app_globals))
Index_label = tk.Label(Title_Frame1,text="索引值:",anchor="w",pady=0,borderwidth=0)
calc_label = tk.Label(pivot_config_Frame,text="可計項:",anchor="w",pady=0,borderwidth=0)
Val_label = tk.Label(pivot_config_Frame,text="值:",anchor="w",pady=0,borderwidth=0)
##pivot_config_Frame.config BOX------------------------
Index_ListBox = tk.Listbox(pivot_config_Frame, name="index_ListBox")
Value_ListBox = tk.Listbox(pivot_config_Frame, name="value_ListBox")
calc_ListBox = tk.Listbox(pivot_config_Frame, name="calc_ListBox")

# Index_checkBOXlist_Frame.pack(fill=tk.BOTH, expand=True)
Index_label.pack(side="left", fill=tk.BOTH, pady=5)
# change_column_type_button.pack(side="right")
add_index_button.pack(side="right")
Index_ListBox.pack(fill=tk.BOTH,expand=True)
calc_label.pack(fill=tk.BOTH, pady=5)
Value_ListBox.bind('<Double-1>', lambda event, root=root, app_globals=app_globals: UIfun.add_values_col(event, root, app_globals))
Value_ListBox.pack(fill=tk.BOTH,expand=True)
Val_label.pack(fill=tk.BOTH, pady=5)
calc_ListBox.bind('<Double-1>', lambda event, root=root, app_globals=app_globals: UIfun.del_values_col(event, root, app_globals))
calc_ListBox.pack(fill=tk.BOTH,expand=True)




#filter_config_Frame.================
filter_title_label = tk.Label(Title_Frame2,text="己加入的規則:")
filter_title_label.pack(side="left")

add_filter_button = tk.Button(Title_Frame2,text="重置",command=lambda root=root, app_globals=app_globals: UIfun.reset_filter_rule(root,app_globals))
add_filter_button.pack(side="right")
add_filter_button = tk.Button(Title_Frame2,text="+",command=lambda root=root, app_globals=app_globals: UIfun.add_filter_rule(root,app_globals))
add_filter_button.pack(side="right")

filter_listbox = tk.Listbox(filter_config_Frame,name="filter_listbox")
filter_listbox.pack(expand=True,fill=tk.BOTH)

filter_listbox.bind('<Double-1>', lambda event, root=root, app_globals=app_globals: UIfun.del_filter_rule(event, root, app_globals))



#====================================
P_window1.add(index_setting_Frame, minsize=190)
P_window1.add(Table_Frame, minsize=510)
P_window1.add(config_outside_Frame, minsize=21)
root.mainloop()
