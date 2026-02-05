# A_Jeff_Text_Tips 使用说明

## 项目地址

[https://github.com/Halomaple/A_Jeff_Text_Tips](https://github.com/Halomaple/A_Jeff_Text_Tips)

## 功能介绍

这是一个 Windows 系统下的文本提示工具，主要功能包括：

- 显示自定义提示信息
- 支持开机自启动设置
- 可拖拽移动窗口位置
- 窗口自动贴靠屏幕右下角显示
- 透明窗口设计，可与任务栏透明效果配合使用

## 安装依赖

```bash
python.exe -m pip install --upgrade pip
pip install tk
```

## 打包命令

```bash
pyinstaller --onefile --hidden-import=tk A_Jeff_Text_Tips.pyw
```

## 使用说明

1. 运行程序后，窗口会自动显示在屏幕右下角
2. 可以通过鼠标拖拽来移动窗口位置
3. 程序支持开机自启动功能，启动后会自动运行

## 注意事项

- 程序需要 Python 3.6+环境运行
- 打包时需要包含 tk 模块依赖
- 窗口尺寸为 1100x48 像素，自动贴靠屏幕右下角显示
- 程序会自动设置开机自启动（注册表项：Software\Microsoft\Windows\CurrentVersion\Run）
- 为获得最佳显示效果，建议配合 TranslucentTB 使用
  - TranslucentTB 可设置任务栏透明，解决窗口被任务栏遮挡问题
  - 下载地址：https://github.com/TranslucentTB/TranslucentTB
