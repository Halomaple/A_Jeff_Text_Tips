import tkinter as tk
from tkinter import font
import tkinter.font as tkFont
import winreg
import sys
import ctypes
from ctypes import wintypes

class AutoStartupManager:
    # 管理程序开机自启动设置的类
    
    def __init__(self):
        self.run_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    def set_auto_startup(self, app_name, app_path):
        # 设置程序开机自启动
        
        # 参数:
        # app_name: 程序名称（注册表中的键名）
        # app_path: 程序完整路径
        try:
            # 打开注册表键
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.run_key_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # 写入程序路径
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
            
            # 关闭注册表键
            winreg.CloseKey(key)
            
            print(f"已成功设置 {app_name} 开机自启动")
            return True
            
        except Exception as e:
            print(f"设置开机自启动失败: {e}")
            return False

    def remove_auto_startup(self, app_name):
        # 取消开机自启动设置
        
        # 参数:
        # app_name: 程序名称
        try:
            # 打开注册表键
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.run_key_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # 删除注册表项
            winreg.DeleteValue(key, app_name)
            
            # 关闭注册表键
            winreg.CloseKey(key)
            
            print(f"已成功取消 {app_name} 开机自启动")
            return True
            
        except Exception as e:
            print(f"取消开机自启动失败: {e}")
            return False

def get_screen_size():
    # 获取屏幕尺寸
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def adjust_window_position(window, width, height):
    # 调整窗口位置，使其右下角贴靠屏幕右下角
    
    # 参数:
    # window: Tkinter窗口对象
    # width: 窗口宽度
    # height: 窗口高度
    screen_width, screen_height = get_screen_size()
    
    # 计算窗口位置
    x = screen_width - width
    y = screen_height - height
    
    # 确保位置在屏幕范围内
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    
    return x, y

def setup_window(window):
    # 设置窗口的基本属性和样式
    window.title("A_Jeff_Text_Tips")
    window.overrideredirect(True)        # 去掉边框和标题栏
    window.attributes("-alpha", 1.0)     # 完全不透明
    window.update_idletasks()
    window.configure(bg="white")         # 设置窗口背景为白色

    # 设置窗口样式以去除阴影效果
    try:
        # 获取窗口句柄
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        # 设置窗口样式为工具窗口，这样不会在任务栏显示图标
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, 0x00000080)  # 设置为工具窗口
    except:
        pass

def setup_window_geometry(window, width, height):
    # 设置窗口的几何位置
    adjusted_x, adjusted_y = adjust_window_position(window, width, height)
    window.geometry(f"{width}x{height}+{adjusted_x}+{adjusted_y}")

def setup_font(window):
    # 设置窗口字体
    default_font = tkFont.nametofont("TkDefaultFont")
    custom_font = default_font.copy()
    custom_font.configure(size=11, underline=False, overstrike=False)
    return custom_font

def create_layout(window, key_descriptions, custom_font):
    # 创建窗口布局
    # 创建主布局框架
    main_frame = tk.Frame(window, bg="white")
    main_frame.pack(fill="both", expand=True, padx=0, pady=0)

    # 创建分组框架
    for i, (group_name, items) in enumerate(key_descriptions.items()):        
        # 创建分组框架
        group_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=0,
            padx=1,
            pady=0
        )
        group_frame.grid(row=i//2, column=i%2, padx=0, pady=0, sticky="nsew")
        # 根据分组位置设置不同的宽度
        target_width = 11 if (i % 2) == 0 else 14
        # 添加分组内的项目（横向布局）
        for j, desc in enumerate(items):
            label = tk.Label(
                group_frame,
                text=desc,
                font=custom_font,
                fg="black",
                bg="white",
                padx=1,
                pady=0,
                anchor="w",
                width=target_width
            )
            label.grid(row=0, column=j, sticky="w")

def setup_mouse_events(window):
    # 设置鼠标拖拽事件
    # 全局变量用于记录鼠标偏移量
    offset_x = 0
    offset_y = 0

    # 鼠标按下事件
    def onmousedown(event):
        nonlocal offset_x, offset_y
        # 记录鼠标相对于窗口左上角的偏移量
        offset_x = event.x
        offset_y = event.y

    # 鼠标移动事件
    def onmousemove(event):
        # 获取鼠标在屏幕上的绝对位置
        mouse_x = event.x_root
        mouse_y = event.y_root
        
        # 计算窗口的新位置
        new_x = mouse_x - offset_x
        new_y = mouse_y - offset_y
        
        # 移动窗口
        window.geometry(f"+{new_x}+{new_y}")

    # 鼠标释放事件
    def onmouseup(event):
        pass

    # 绑定鼠标事件
    window.bind("<Button-1>", onmousedown)
    window.bind("<B1-Motion>", onmousemove)
    window.bind("<ButtonRelease-1>", onmouseup)

def setup_auto_startup():
    # 设置开机自启动
    # 获取当前程序路径
    current_exe = sys.executable
    app_name = "A_Jeff_Text_Tips"
    
    # 创建自启动管理器实例
    auto_startup_manager = AutoStartupManager()
    
    # 设置开机自启动
    auto_startup_manager.set_auto_startup(app_name, current_exe)

def hide_console():
    # 隐藏控制台窗口（如果在Windows环境下）
    try:
        # 隐藏控制台窗口
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# 分组功能键说明
key_descriptions = {
    "命令工具1": [
        "Win+`:命令行",
        "Alt+`:截图", 
    ],
    "媒体1": [
        "Fn+F5:静音",
        "Fn+F6:音量增", 
        "Fn+F7:音量减",
        "Fn+F8:计算器",
    ],
    "命令工具2": [
        "Alt+1:搜文件"
    ],
    "媒体2": [
        "Fn+F9:播放/暂停",
        "Fn+F10:停止播放",
        "Fn+F11:上一首",
        "Fn+F12:下一首"
    ],
}

# 窗口配置常量
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 48

# 主程序入口
if __name__ == "__main__":
    # 创建窗口
    window = tk.Tk()
    
    # 设置窗口属性
    setup_window(window)
    
    # 设置窗口大小和位置
    setup_window_geometry(window, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # 设置字体
    custom_font = setup_font(window)
    
    # 创建布局
    create_layout(window, key_descriptions, custom_font)
    
    # 设置鼠标事件
    setup_mouse_events(window)
    
    # 设置开机自启动
    setup_auto_startup()
    
    # 隐藏控制台窗口（如果在Windows环境下）
    if sys.platform == "win32":
        hide_console()
    
    # 运行窗口
    window.mainloop()
