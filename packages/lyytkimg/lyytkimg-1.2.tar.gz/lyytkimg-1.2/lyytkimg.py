from datetime import datetime
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk

class gui_zoomimg_class:

    def __init__(self, main_module):
        self.main_module = main_module

    def init_var(self):
        self.win_img = tk.Toplevel()
        self.win_img.title("图片查看器")
        self.img_viewer_scale_factor = 1.1
        self.prev_mode = True
        self.var = None
        self.my_index = 0
        self.current_width = 0
        self.current_height = 0
        # self.frame = tk.Frame(self.win_img)
        # self.frame.place(relx=0, rely=0, relheight=0.8, relwidth=1)

        # self.selected_label = Label(self.frame)
        # 创建一个 Canvas 控件来显示图片
        self.canvas = tk.Canvas(self.win_img)
        self.canvas.place(relx=0, rely=0, relheight=0.9, relwidth=1)
        # 创建一个 Scrollbar 控件
        self.scrollbar = tk.Scrollbar(self.win_img, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        # 将 Canvas 控件的滚动命令设置为 Scrollbar 控件的 set 方法
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # # 将图片添加到 Canvas 控件
        # self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        # 设置 Canvas 控件的滚动区域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.label = tk.Label(self.canvas)
        self.label.place(relx=0, rely=0)

        # 将 Label 控件添加到 Canvas 控件
        self.canvas.create_window(0, 0, window=self.label, anchor="nw")
        # 初始化鼠标的位置
        self.mouse_x = 0
        self.mouse_y = 0

    def resize(self, w, h, w_box, h_box, pil_image):
        """
        resize a pil_image object so it will fit into
        a box of size w_box times h_box, but retain aspect ratio
        对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
        """
        f1 = w_box / w
        f2 = h_box / h
        factor = min(f1, f2)
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def open_last_img(self):
        self.init_var()

        # 将图片添加到 Canvas 控件
        # self.canvas.create_image(0, 0, image=self.main_module.image_list[self.my_index], anchor='nw')

        self.my_index = len(self.main_module.image_list) - 1
        self.win_width = min(int(self.main_module.image_list[self.my_index].width()), 1500)
        self.win_height = min(int(self.main_module.image_list[self.my_index].height()), 1300)
        self.win_img.geometry(f"{int(self.win_width*1.1)}x{int(self.win_height*1.1)}")

        print("图库中有", len(self.main_module.image_list), "张图片, current_index=", self.my_index, "current_width=", self.current_width, "current_height=", self.current_height)

        self.var = tk.IntVar()
        self.var.set(1)  # 设置初始值为1，即翻页模式
        self.zoom_radiobutton = tk.Radiobutton(self.win_img, text="放大模式", variable=self.var, value=0, command=lambda: self.change_mode(0))
        self.zoom_radiobutton.place(relx=0.1, rely=0.9, relheight=0.05)
        self.scroll_radiobutton = tk.Radiobutton(self.win_img, text="翻页模式", variable=self.var, value=1, command=lambda: self.change_mode(1))
        self.scroll_radiobutton.place(relx=0.6, rely=0.9, relheight=0.05)

        # 初始时显示最后一张图片
        self.show_selected_image()

        # 监听窗口的尺寸变化事件，并调用resize函数
        self.win_img.bind("<MouseWheel>", self.on_mousewheel)
        self.label.bind("<Double-Button-1>", lambda event: self.change_mode(0 if self.var.get() == 1 else 1, event))

        # 当鼠标进入图片时，改变鼠标的形状为手形
        self.label.bind("<Enter>", lambda event: self.label.config(cursor="hand2"))
        # 当鼠标离开图片时，改变鼠标的形状为箭头
        self.label.bind("<Leave>", lambda event: self.label.config(cursor=""))
        # 当鼠标左键按下时，记录下当前的位置
        self.label.bind("<Button-1>", self.on_mouse_down)

        # 当鼠标移动时，移动图片
        self.label.bind("<B1-Motion>", self.move_image)

        # self.win_img.bind("<Double-Button-1>", change_mode)
        # 初始化图像大小
        # original_image = photo
        # label.configure(image=original_image)

        # 运行新窗口的事件循环
        self.win_img.mainloop()

    def on_mouse_down(self, event):
        # 记录下鼠标的位置
        self.mouse_x = event.x
        self.mouse_y = event.y

    def move_image(self, event):
        # 计算鼠标的移动距离
        dx = event.x - self.mouse_x
        dy = event.y - self.mouse_y

        # 获取图片的当前位置
        x = self.label.winfo_x()
        y = self.label.winfo_y()

        # 移动图片到新的位置
        self.label.place(x=x + dx, y=y + dy)

        # 更新鼠标的位置
        self.mouse_x = event.x
        self.mouse_y = event.y

    def show_previous_image(self):
        if self.my_index > 0:
            print("show_previous_image, 处于正常范围的myindex=", self.my_index)
            self.my_index -= 1
            self.current_width = 0
            self.current_height = 0
        self.show_selected_image()

    def show_next_image(self):
        if self.my_index < len(self.main_module.image_list) - 1:
            print("show_next_image, 处于正常范围的myindex=", self.my_index)
            self.my_index += 1
            self.current_width = 0
            self.current_height = 0
        self.show_selected_image()

    def on_mousewheel(self, event):
        # print("on_mousewheel", event.widget, "滚动值=", event.delta)
        img = self.main_module.image_list[self.my_index]
        if self.current_width == 0 and self.current_height == 0:
            self.current_width, self.current_height = img.width(), img.height()

        if self.prev_mode:  # 如果当前单选框的值为翻页模式
            if event.delta > 0:  # 鼠标往前滚动
                print("翻页模式，鼠标往前滚动")
                self.show_previous_image()
            else:  # 鼠标向后滚动
                print("翻页模式，鼠标向后滚动")
                self.show_next_image()

        else:  # 如果当前单选框的值为放大模式，则还是原来的代码不变
            if event.delta < 0:  # 鼠标往后滚动
                print("缩放模式，缩小，鼠标往前滚动,delta=", event.delta)
                self.current_width = self.current_width / self.img_viewer_scale_factor
                self.current_height = self.current_height / self.img_viewer_scale_factor

            else:
                print("缩放翻页模式，放大，鼠标向后滚动,delta=", event.delta)
                self.current_width = self.current_width * self.img_viewer_scale_factor
                self.current_height = self.current_height * self.img_viewer_scale_factor
            byte_data = ImageTk.getimage(img)
            resized_img = byte_data.resize((int(self.current_width), int(self.current_height)))
            new_photo = ImageTk.PhotoImage(resized_img)
            event.widget.configure(image=new_photo)  # 将PhotoImage对象的像素数据转换为字节字符串并更新标签中的图像
            event.widget.image = new_photo  # 保存图像的引用，以免被垃圾回收

    def change_mode(self, mode, event=None):

        self.prev_mode = mode
        print("enter change_mode, mode=", mode, ",event=", event)
        self.var.set(mode)
        if mode == 0:
            self.zoom_radiobutton.select()
        else:
            print("mode 不等于0")
            self.scroll_radiobutton.select()

    def show_selected_image(self):
        print("show select img,  myindex=", self.my_index)
        if self.my_index >= 0 and self.my_index < len(self.main_module.image_list):
            selected_image = self.main_module.image_list[self.my_index]
            self.label.configure(image=selected_image)
            self.label.image = selected_image
            self.win_width = min(int(selected_image.width()), 1500)
            self.win_height = min(int(selected_image.height()), 1300)
            self.win_img.geometry(f"{int(self.win_width*1.1)}x{int(self.win_height*1.1)}")
