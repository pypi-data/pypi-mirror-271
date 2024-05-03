
class gui_ico_class:
    def __init__(self, main_module) -> None:
        self.main_module = main_module


    def read_notice(self):
        text = self.main_module.文本框_笔记.get("1.0", tk.END)

    def load_notice(self):
        with open("notice\\notice.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            # 获取最后10行
            # 将最后10行显示在self.main_module.文本框中
            self.main_module.文本框_笔记.insert("1.0", "".join(lines))

    def set_notice(self, text):
        self.main_module.文本框_笔记.insert(tk.END, text)

    def save_notice(self):
        # 先备份原来的
        # new_file=os.path.join(path,"project30.jpg")

        newfile = f1999cfg.resource_path + "\\notice" + "\\notice" + "_" + datetime.now().strftime("%Y-%m-%d") + ".txt"
        if not os.path.isfile(newfile):
            os.rename(f1999cfg.resource_path + "\\notice" + "\\notice.txt", newfile)

        alltext = self.main_module.文本框_笔记.get("1.0", "end-1c")
        with open(f1999cfg.resource_path + "\\notice" + "\\notice.txt", "w", encoding="utf-8") as f:
            f.write(alltext)
            self.main_module.状态栏文本变量1.set("保存完毕")    
if __name__ == "__main__":    
    show_msg_once()
    #show_toast()