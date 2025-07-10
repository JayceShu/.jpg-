import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font


class CheckpointRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkpoint Name_changing_tool")

        # 设置窗口大小和字体
        self.root.geometry("650x450")  # 稍微增大窗口尺寸
        try:
            # 尝试使用等线字体，如果系统没有则使用默认字体
            self.large_font = Font(family="等线", size=12)
            self.title_font = Font(family="等线", size=25, weight="bold")
        except:
            # 如果等线字体不可用，使用默认字体
            self.large_font = Font(size=12)
            self.title_font = Font(size=25, weight="bold")

        # 添加主标题
        title_frame = tk.Frame(root)
        title_frame.pack(pady=15)
        title_label = tk.Label(title_frame, text="Checkpoint Name_changing_tool",font=self.title_font, fg="#333333")
        title_label.pack()

        self.root_dir = None

        # 获取程序所在目录的Config.txt
        self.config_options = {}
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Config.txt")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.config_options[key.strip()] = value.strip()

        if not self.config_options:
            messagebox.showerror("错误", "程序目录下没有找到有效的Config.txt文件")
            self.root.destroy()
            return

        # 创建主内容框架
        main_frame = tk.Frame(root)
        main_frame.pack(padx=20, pady=10)

        # 文件夹选择部分
        folder_frame = tk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(50,10))
        tk.Label(folder_frame, text="请选择包含.jpg文件的文件夹：",
                font=self.large_font).pack(side=tk.LEFT)
        self.folder_btn = tk.Button(folder_frame, text="选择文件夹",
                                  command=self.select_folder,
                                  font=self.large_font, bg="#f0f0f0")
        self.folder_btn.pack(side=tk.LEFT, padx=10)
        self.folder_display = tk.Label(folder_frame, text="未选择",
                                      font=self.large_font, fg="#666666")
        self.folder_display.pack(side=tk.LEFT)

        # 当前检查点输入框
        entry_frame = tk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)
        tk.Label(entry_frame, text="当前检查点：",
                font=self.large_font).pack(side=tk.LEFT)
        self.text_entry = tk.Entry(entry_frame, font=self.large_font)
        self.text_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # 表带类型下拉菜单
        dropdown_frame = tk.Frame(main_frame)
        dropdown_frame.pack(fill=tk.X, pady=10)
        tk.Label(dropdown_frame, text="表带类型：",
                font=self.large_font).pack(side=tk.LEFT)
        self.config_var = tk.StringVar()
        self.dropdown = ttk.Combobox(dropdown_frame,textvariable=self.config_var,state='readonly',font=self.large_font)
        self.dropdown['values'] = [f"{k}={v}" for k, v in self.config_options.items()]
        self.dropdown.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.dropdown.current(0)

        # 确认按钮
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        self.confirm_btn = tk.Button(btn_frame, text="确认修改",command=self.process_files,font=self.title_font,bg="#4CAF50", fg="white",height=1, width=15)
        self.confirm_btn.pack()

    def select_folder(self):
        # 获取文件夹
        self.root_dir = filedialog.askdirectory(title="选择包含.jpg文件的文件夹")
        if not self.root_dir:
            return

        # 检查文件夹中是否有.jpg文件
        jpg_files = [f for f in os.listdir(self.root_dir) if f.lower().endswith('.jpg')]
        if not jpg_files:
            messagebox.showerror("错误", "所选文件夹中没有.jpg文件")
            return

        # 更新UI显示
        self.folder_display.config(text=os.path.basename(self.root_dir), fg="#333333")

    def process_files(self):
        if not self.root_dir:
            messagebox.showerror("错误", "请先选择文件夹")
            return

        config_selection = self.config_var.get()
        if '=' not in config_selection:
            messagebox.showerror("错误", "配置选择无效")
            return

        config_key, insert_position = config_selection.split('=', 1)
        try:
            insert_position = int(insert_position)
        except ValueError:
            messagebox.showerror("错误", "插入位置必须是数字")
            return

        text_to_insert = self.text_entry.get().strip()
        if not text_to_insert:
            messagebox.showerror("错误", "没有要插入的文本")
            return

        # 处理文件
        modified_count = 0
        for filename in os.listdir(self.root_dir):
            if filename.lower().endswith('.jpg'):
                name, ext = os.path.splitext(filename)

                if len(name) >= insert_position:
                    # 插入文本并添加下划线
                    new_name = f"{name[:insert_position]}_{text_to_insert}_{name[insert_position:]}{ext}"

                    old_path = os.path.join(self.root_dir, filename)
                    new_path = os.path.join(self.root_dir, new_name)

                    try:
                        os.rename(old_path, new_path)
                        modified_count += 1
                    except Exception as e:
                        messagebox.showerror("错误", f"重命名文件 {filename} 失败: {str(e)}")

        messagebox.showinfo("完成", f"成功修改了 {modified_count} 个文件名")


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckpointRenamer(root)
    root.mainloop()