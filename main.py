#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作版水印工具 - 确保界面和功能正常
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import json

class WorkingWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("照片水印工具")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # 数据存储
        self.images = []
        self.current_image_index = 0
        self.current_image = None
        self.watermark_config = {
            'text': '水印文字',
            'font_size': 24,
            'font_color': (255, 0, 0),
            'opacity': 80,
            'position': (50, 50),
            'rotation': 0
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建主界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧控制面板
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 右侧预览区域
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建各个面板
        self.create_file_panel(control_frame)
        self.create_watermark_panel(control_frame)
        self.create_position_panel(control_frame)
        self.create_export_panel(control_frame)
        self.create_preview_panel(preview_frame)
        
    def create_file_panel(self, parent):
        """创建文件处理面板"""
        frame = ttk.LabelFrame(parent, text="文件处理", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # 导入按钮
        ttk.Button(frame, text="导入图片", command=self.import_images).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="导入文件夹", command=self.import_folder).pack(fill=tk.X, pady=(0, 5))
        
        # 图片列表
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.image_listbox = tk.Listbox(list_frame, height=6)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
        
    def create_watermark_panel(self, parent):
        """创建水印设置面板"""
        frame = ttk.LabelFrame(parent, text="水印设置", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # 水印文本
        ttk.Label(frame, text="水印文本:").pack(anchor=tk.W)
        self.text_entry = ttk.Entry(frame)
        self.text_entry.pack(fill=tk.X, pady=(0, 5))
        self.text_entry.insert(0, self.watermark_config['text'])
        self.text_entry.bind('<KeyRelease>', self.update_watermark)
        
        # 字体大小
        ttk.Label(frame, text="字体大小:").pack(anchor=tk.W)
        self.font_size_var = tk.IntVar(value=self.watermark_config['font_size'])
        font_scale = ttk.Scale(frame, from_=10, to=100, variable=self.font_size_var, 
                             orient=tk.HORIZONTAL, command=self.update_watermark)
        font_scale.pack(fill=tk.X, pady=(0, 5))
        
        # 颜色选择
        color_frame = ttk.Frame(frame)
        color_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(color_frame, text="选择颜色", command=self.choose_color).pack(side=tk.LEFT)
        self.color_label = tk.Label(color_frame, text="●", fg="#ff0000", font=("Arial", 16))
        self.color_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 透明度
        ttk.Label(frame, text="透明度:").pack(anchor=tk.W)
        self.opacity_var = tk.IntVar(value=self.watermark_config['opacity'])
        opacity_scale = ttk.Scale(frame, from_=0, to=100, variable=self.opacity_var,
                                orient=tk.HORIZONTAL, command=self.update_watermark)
        opacity_scale.pack(fill=tk.X, pady=(0, 5))
        
        # 旋转
        ttk.Label(frame, text="旋转角度:").pack(anchor=tk.W)
        self.rotation_var = tk.IntVar(value=self.watermark_config['rotation'])
        rotation_scale = ttk.Scale(frame, from_=-180, to=180, variable=self.rotation_var,
                                 orient=tk.HORIZONTAL, command=self.update_watermark)
        rotation_scale.pack(fill=tk.X)
        
    def create_position_panel(self, parent):
        """创建位置设置面板"""
        frame = ttk.LabelFrame(parent, text="位置设置", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # 预设位置
        ttk.Label(frame, text="预设位置:").pack(anchor=tk.W)
        pos_frame = ttk.Frame(frame)
        pos_frame.pack(fill=tk.X, pady=(5, 0))
        
        positions = [
            ("左上", (0, 0)), ("中上", (0.5, 0)), ("右上", (1, 0)),
            ("左中", (0, 0.5)), ("居中", (0.5, 0.5)), ("右中", (1, 0.5)),
            ("左下", (0, 1)), ("中下", (0.5, 1)), ("右下", (1, 1))
        ]
        
        for i, (name, pos) in enumerate(positions):
            btn = ttk.Button(pos_frame, text=name, width=6,
                           command=lambda p=pos: self.set_position(p))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
        
    def create_export_panel(self, parent):
        """创建导出设置面板"""
        frame = ttk.LabelFrame(parent, text="导出设置", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输出文件夹
        ttk.Button(frame, text="选择输出文件夹", command=self.choose_output_folder).pack(fill=tk.X, pady=(0, 5))
        self.folder_label = ttk.Label(frame, text="未选择", foreground="gray")
        self.folder_label.pack(anchor=tk.W)
        
        # 导出按钮
        ttk.Button(frame, text="导出所有图片", command=self.export_all).pack(fill=tk.X, pady=(10, 0))
        
    def create_preview_panel(self, parent):
        """创建预览面板"""
        frame = ttk.LabelFrame(parent, text="预览", padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 预览画布
        self.preview_canvas = tk.Canvas(frame, bg="white", width=600, height=400)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 显示提示
        self.preview_canvas.create_text(300, 200, text="请导入图片", font=("Arial", 16), fill="gray")
        
        # 预览控制
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="上一张", command=self.prev_image).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="下一张", command=self.next_image).pack(side=tk.LEFT, padx=(5, 0))
        
        self.image_info_label = ttk.Label(control_frame, text="请导入图片")
        self.image_info_label.pack(side=tk.RIGHT)
        
    def import_images(self):
        """导入图片"""
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff")
        ]
        
        files = filedialog.askopenfilenames(title="选择图片文件", filetypes=filetypes)
        if files:
            self.images.extend(files)
            self.update_image_list()
            if len(self.images) == len(files):  # 第一次导入
                self.current_image_index = 0
                self.load_current_image()
    
    def import_folder(self):
        """导入文件夹"""
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if folder:
            supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(supported_formats):
                        self.images.append(os.path.join(root, file))
            self.update_image_list()
            if self.images and self.current_image_index == 0:
                self.load_current_image()
    
    def update_image_list(self):
        """更新图片列表显示"""
        self.image_listbox.delete(0, tk.END)
        for i, img_path in enumerate(self.images):
            filename = os.path.basename(img_path)
            self.image_listbox.insert(tk.END, f"{i+1}. {filename}")
    
    def on_image_select(self, event):
        """图片选择事件"""
        selection = self.image_listbox.curselection()
        if selection:
            self.current_image_index = selection[0]
            self.load_current_image()
    
    def load_current_image(self):
        """加载当前选中的图片"""
        if not self.images or self.current_image_index >= len(self.images):
            return
        
        try:
            img_path = self.images[self.current_image_index]
            self.current_image = Image.open(img_path)
            self.display_image()
            self.update_image_info()
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {e}")
    
    def display_image(self):
        """在预览区域显示图片"""
        if not self.current_image:
            return
        
        # 计算显示尺寸
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.display_image)
            return
        
        # 缩放图片
        img = self.current_image.copy()
        scale_x = canvas_width / img.width
        scale_y = canvas_height / img.height
        scale = min(scale_x, scale_y, 1.0)
        
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 添加水印
        img = self.add_watermark_to_image(img)
        
        # 转换为PhotoImage
        self.photo = ImageTk.PhotoImage(img)
        
        # 显示图片
        self.preview_canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
        
        # 保存缩放信息
        self.display_scale = scale
        self.display_offset_x = x
        self.display_offset_y = y
    
    def add_watermark_to_image(self, img):
        """在图片上添加水印"""
        if not self.watermark_config['text']:
            return img
        
        # 创建绘图对象
        draw = ImageDraw.Draw(img)
        
        # 计算字体
        try:
            font = ImageFont.truetype("arial.ttf", self.watermark_config['font_size'])
        except:
            font = ImageFont.load_default()
        
        # 计算水印位置
        if hasattr(self, 'display_scale'):
            pos_x = int(self.watermark_config['position'][0] * self.display_scale)
            pos_y = int(self.watermark_config['position'][1] * self.display_scale)
            font_size = int(self.watermark_config['font_size'] * self.display_scale)
        else:
            pos_x, pos_y = self.watermark_config['position']
            font_size = self.watermark_config['font_size']
        
        # 调整字体大小
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 计算透明度
        alpha = int(255 * self.watermark_config['opacity'] / 100)
        color = (*self.watermark_config['font_color'], alpha)
        
        # 绘制水印
        if self.watermark_config['rotation'] != 0:
            # 创建临时图片用于旋转
            temp_img = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.text((pos_x, pos_y), self.watermark_config['text'], font=font, fill=color)
            
            # 旋转
            rotated = temp_img.rotate(self.watermark_config['rotation'], expand=True)
            
            # 合并到原图
            img = Image.alpha_composite(img.convert('RGBA'), rotated).convert(img.mode)
        else:
            draw.text((pos_x, pos_y), self.watermark_config['text'], font=font, fill=color)
        
        return img
    
    def update_watermark(self, *args):
        """更新水印设置"""
        self.watermark_config['text'] = self.text_entry.get()
        self.watermark_config['font_size'] = self.font_size_var.get()
        self.watermark_config['opacity'] = self.opacity_var.get()
        self.watermark_config['rotation'] = self.rotation_var.get()
        
        if self.current_image:
            self.display_image()
    
    def choose_color(self):
        """选择颜色"""
        color = colorchooser.askcolor(title="选择水印颜色")
        if color[0]:
            self.watermark_config['font_color'] = tuple(int(c) for c in color[0])
            self.color_label.config(fg=self.rgb_to_hex(self.watermark_config['font_color']))
            self.update_watermark()
    
    def rgb_to_hex(self, rgb):
        """RGB转十六进制颜色"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def set_position(self, position):
        """设置水印位置"""
        if not self.current_image:
            return
        
        # 计算实际位置
        img_width = self.current_image.width
        img_height = self.current_image.height
        
        pos_x = int(position[0] * img_width)
        pos_y = int(position[1] * img_height)
        
        self.watermark_config['position'] = (pos_x, pos_y)
        self.display_image()
    
    def prev_image(self):
        """上一张图片"""
        if self.images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_image_index)
            self.load_current_image()
    
    def next_image(self):
        """下一张图片"""
        if self.images and self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_image_index)
            self.load_current_image()
    
    def update_image_info(self):
        """更新图片信息显示"""
        if self.images:
            current = self.current_image_index + 1
            total = len(self.images)
            filename = os.path.basename(self.images[self.current_image_index])
            self.image_info_label.config(text=f"{current}/{total} - {filename}")
        else:
            self.image_info_label.config(text="请导入图片")
    
    def choose_output_folder(self):
        """选择输出文件夹"""
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_folder = folder
            self.folder_label.config(text=os.path.basename(folder), foreground="black")
    
    def export_all(self):
        """导出所有图片"""
        if not self.images:
            messagebox.showwarning("警告", "请先导入图片")
            return
        
        if not hasattr(self, 'output_folder') or not self.output_folder:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
        
        try:
            total = len(self.images)
            for i, img_path in enumerate(self.images):
                # 更新进度
                self.image_info_label.config(text=f"导出中: {i+1}/{total}")
                self.root.update()
                
                # 加载原图
                original_img = Image.open(img_path)
                
                # 添加水印
                watermarked_img = self.add_watermark_to_image(original_img)
                
                # 生成输出文件名
                filename = os.path.basename(img_path)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_watermarked{ext}"
                
                # 保存图片
                output_path = os.path.join(self.output_folder, new_filename)
                watermarked_img.save(output_path, quality=95)
            
            messagebox.showinfo("成功", f"已导出 {total} 张图片到 {self.output_folder}")
            self.image_info_label.config(text=f"导出完成: {total} 张图片")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")

def main():
    root = tk.Tk()
    app = WorkingWatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
