from tkinter import Tk, Text, Menu, messagebox, simpledialog
from datetime import datetime


class gui_textbox_class:
    def __init__(self, main_module):
        self.main_module = main_module
        self.root = self.main_module.root
        self.notebox = self.main_module.文本框_笔记
        self.msgbox = self.main_module.文本框_主消息
        self.search_text = None
        self.last_index = '1.0'
        self.initialize_styles()
        self.create_context_menu()
        self.bind_events()
        self.add_right_menu()

    def initialize_styles(self):
        styles = {"saddlebrown": "saddlebrown", "darkorange": "darkorange", "blue": "blue", "purple": "purple", "green": "green", "red": "red", "yellow": "yellow", "浅灰色": "#8E236B", "olive": "olive", "steelblue": "steelblue", "orangered": "orangered", "maroon": "maroon", "chocolate": "chocolate", "navajowhite": "navajowhite", "gray_bg": "gray"}
        for tag, style in styles.items():
            self.msgbox.tag_configure(tag, foreground=style)

        self.msgbox.tag_configure("bold", font=("黑体", 12))

    def add_right_menu(self):
        # 创建右键菜单
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="剪切", command=lambda: self.root.event_generate("<Control-x>"))
        self.menu.add_command(label="复制", command=lambda: self.root.event_generate("<Control-c>"))
        self.menu.add_command(label="粘贴", command=lambda: self.root.event_generate("<Control-v>"))
        self.menu.add_separator()
        self.menu.add_command(label="清空", command=lambda: self.文本框_主消息.delete("1.0", "end"))
        self.menu.add_separator()
        self.menu.add_command(label="全选", command=lambda: self.root.event_generate("<Control-a>"))
        self.notebox.bind_class("Text", "<Button-3>", self.show_context_menu)
        self.notebox.bind_class("Text", "<Double-Button>", self.toggle_fullscreen)
        self.notebox.bind_class("Text", "<Double-Button-1>", self.toggle_fullscreen)

    def create_context_menu(self):
        self.menu = Menu(self.root, tearoff=0)
        menu_commands = [("剪切", lambda: self.root.event_generate("<Control-x>")), ("复制", lambda: self.root.event_generate("<Control-c>")), ("粘贴", lambda: self.root.event_generate("<Control-v>")), ("清空", lambda: self.msgbox.delete("1.0", "end")), ("全选", lambda: self.root.event_generate("<Control-a>"))]
        for label, command in menu_commands:
            self.menu.add_command(label=label, command=command)
        self.menu.add_separator()

    def bind_events(self):
        self.notebox.bind_class("Text", "<Button-3>", self.show_context_menu)
        self.notebox.bind_class("Text", "<Double-Button>", self.toggle_fullscreen)
        self.notebox.bind_class("Text", "<Double-Button-1>", self.toggle_fullscreen)

    def show_context_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def toggle_fullscreen(self, event):
        current_font = self.msgbox.cget("font")
        font_family, original_font_size = current_font.split()
        font_size = int(original_font_size)

        if event.widget.winfo_toplevel().attributes("-fullscreen"):
            font_size -= 6
            event.widget.winfo_toplevel().attributes("-fullscreen", False)
        else:
            font_size += 6
            event.widget.winfo_toplevel().attributes("-fullscreen", True)
        new_font = (font_family, font_size)
        self.msgbox.config(font=new_font)
        self.notebox.config(font=new_font)

    def find(self, event=None):
        self.search_text = simpledialog.askstring("Find", "Enter the text to find:")
        
        
        if self.search_text:
            self.last_index = '1.0'  # 重置last_index
            self.find_next()

    def find_next(self, event=None):
        print("enter find_next")
        if not self.search_text:
            print("没有搜索内容，返回。")
            return  # 如果没有搜索内容，直接返回

        # 从上一次找到的索引之后开始搜索
        start_index = self.msgbox.search(self.search_text, self.last_index + "+1c", "end")
        if start_index:
            end_index = f"{start_index}+{len(self.search_text)}c"
            self.msgbox.tag_remove("search", "1.0", "end")  # 移除上一次的高亮
            self.msgbox.tag_add("search", start_index, end_index)
            self.msgbox.tag_config("search", background="red", foreground="black")
            self.msgbox.see(start_index)
            self.last_index = end_index  # 更新最后找到的索引
        else:
            messagebox.showinfo("Find", "No more occurrences found.")
            self.last_index = '1.0'  # 重置搜索起点


    def process_and_display_text(self, row):
        rpltxt = str(datetime.now())[5:10] + " "
        msg_time = row[1].replace(rpltxt, "") + " "
        msg_teacher = row[2].replace("vip", "").replace("理解", "").replace("游资", "").replace("投研", "") + ":"
        if row[2] != self.last_teacher:
            prefix = "\n" + msg_time + msg_teacher
        else:
            prefix = msg_time
        full_msg = prefix + row[3] + "\n"
        self.display_text(full_msg, msg_teacher)
        self.last_teacher = row[2]

    def display_text(self, tmptext, msg_teacher):
        dict_color = {"顶级": "blue", "公子复盘": "green", "妖股刺客": "purple", "梅森投研": "orange"}
        for key, value in dict_color.items():
            if key in msg_teacher:
                self.msgbox.tag_configure(value, foreground=value)
                break
        self.msgbox.insert("end", tmptext, value)
        self.msgbox.see("end")

    def filter_and_display_text(self, text, location="end", color="black"):
        self.msgbox.insert(location, text, color)


def main():
    root = Tk()
    notebox = Text(root)
    msgbox = Text(root)
    gui_textbox = gui_textbox_class(root, notebox, msgbox)
    root.mainloop()


if __name__ == "__main__":
    main()
