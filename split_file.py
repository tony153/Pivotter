import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread

def split_file(top,file_name_prefix_entry, save_path_entry, df, chunk_size_entry):
    Pro_top, proBar, percentage_label = popup_lodadingwin()

    def split_and_save_file(Pro_top, proBar, Percentage_label):
        path = save_path_entry.get()
        chunk_size = int(chunk_size_entry.get())
        file_name_prefix = file_name_prefix_entry.get()
        chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
        if path != "":
            for i, chunk in enumerate(chunks):
                proBar["value"] += 100 /len(chunks)
                chunk.to_csv(f'{path}/{file_name_prefix}{i+1}.csv')
        else:
            tk.messagebox.showerror(title="error", message="未選擇檔案路徑")

        Pro_top.destroy()
        top.destroy()

    thread = Thread(target=split_and_save_file, args=(Pro_top,proBar,percentage_label))
    thread.start()

def select_folder_path(top, save_path_entry):
    top.wm_attributes("-topmost",False)
    file_path = tk.filedialog.askdirectory()
    save_path_entry.delete(0,tk.END)
    save_path_entry.insert(0,file_path)
    top.wm_attributes("-topmost",True)

def to_split_file(root, app_globals):
    if app_globals["input_df"].empty:
        tk.messagebox.showerror(title="error",message="未開啟檔案")
    else:
        top = tk.Toplevel(root)
        top.title("分割檔案")
        top.geometry("260x113+300+300")
        top.wm_attributes("-topmost","true")
        top.attributes("-toolwindow",1)

        chunk_size_label = tk.Label(top,text="每文件最大數據量:")
        chunk_size_label.grid(row=0,column=0,sticky="w")

        chuck_size_entry = tk.Entry(top,width=21)
        chuck_size_entry.insert(0,"5000")
        chuck_size_entry.grid(row=0,column=1,columnspan=2,sticky="w")

        file_name_prefix_label = tk.Lable(top, text="檔名前綴")
        file_name_prefix_label.grid(row=1, column=0, sticky="w")

        file_name_prefix_entry = tk.Entry(top,width=21)
        file_name_prefix_entry.insert(0,"Untitle_")
        file_name_prefix_entry.grid(row=1,column=1,columnspan=2,sticky="w")

        save_path_lable =tk.Label(top,text="儲存位置")
        save_path_lable.grid(row=2,column=0,sticky="w")

        save_path_entry =tk.Entry(top,width=18)
        save_path_entry.grid(row=2,column=1,sticky="w")

        save_path_button = tk.Button(top,text="...",command=lambda :select_folder_path(top,save_path_entry))
        save_path_button.grid(row=2,column=2,pady=3,padx=3)

        save_button = tk.Button(top,text="儲存",command=lambda: split_file(top,file_name_prefix_entry,save_path_entry,app_globals['output_df'],chuck_size_entry))
        save_button.grid(row=3,column=1,sticky="e")

def popup_lodadingwin():
    Pro_top = tk.Toplevel()
    Pro_top.title("處理中....")
    Pro_top.geometry("500x80+300+300")
    Pro_top.wm_attributes("-topmost","true")
    Pro_top.attributes("-toolwindow",1)
    proBar = ttk.Progressbar(Pro_top, orient=tk.HORIZONTAL, mode="determinate", length=100)
    proBar.pack(fill=tk.X, padx=10, pady=5)
    percentage_label = tk.Label(Pro_top, text="正在生成表...", anchor="w")
    percentage_label.pack(fill=tk.X, padx=15)

    return (Pro_top,proBar,percentage_label)

