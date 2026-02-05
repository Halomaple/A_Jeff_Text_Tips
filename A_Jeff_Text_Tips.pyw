import tkinter as tk
from tkinter import font
import tkinter.font as tkFont
import winreg
import sys
import ctypes
from ctypes import wintypes

def set_auto_startup(app_name, app_path):
    """
    设置程序开机自启动
    
    参数:
    app_name: 程序名称（注册表中的键名）
    app_path: 程序完整路径
    """
    try:
        # 打开注册表键
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
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

def remove_auto_startup(app_name):
    """
    取消开机自启动设置
    
    参数:
    app_name: 程序名称
    """
    try:
        # 打开注册表键
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
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
    """获取屏幕尺寸"""
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def adjust_window_position(window, width, height):
    screen_width, screen_height = get_screen_size()
    
    # 计算窗口位置
    x = screen_width - width
    
    # 窗口下边靠屏幕底部，所以窗口上边位置是：屏幕高度 - 窗口高度
    y = screen_height - height
    
    # 确保位置在屏幕范围内
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    
    return x, y

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

# 创建窗口
window = tk.Tk()
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
    # WS_EX_TOOLWINDOW = 0x00000080  # 工具窗口样式，不会在任务栏显示
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, 0x00000080)  # 设置为工具窗口
except:
    pass

# 设置窗口初始位置和大小
window_width = 1050
window_height = 48

# 调整位置：窗口右边靠屏幕右边，下边靠屏幕底部
adjusted_x, adjusted_y = adjust_window_position(window, window_width, window_height)
window.geometry(f"{window_width}x{window_height}+{adjusted_x}+{adjusted_y}")

# 使用系统默认字体并设置抗锯齿
default_font = tkFont.nametofont("TkDefaultFont")
custom_font = default_font.copy()
custom_font.configure(size=11, underline=False, overstrike=False)

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
    target_width = 0
    if (i % 2) == 0 :
        target_width = 11
    else :
        target_width = 14
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

# 全局变量用于记录鼠标偏移量
offset_x = 0
offset_y = 0

# 鼠标按下事件
def onmousedown(event):
    global offset_x, offset_y
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

# 设置开机自启动
def setup_auto_startup():
    # 获取当前程序路径
    current_exe = sys.executable
    app_name = "A_Jeff_Text_Tips"
    
    # 设置开机自启动
    set_auto_startup(app_name, current_exe)

# 在程序启动时设置自启动
setup_auto_startup()

# 隐藏控制台窗口（如果在Windows环境下）
def hide_console():
    try:
        # 隐藏控制台窗口
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# 如果在Windows环境下运行，隐藏控制台窗口
if sys.platform == "win32":
    hide_console()

# 运行窗口
window.mainloop()