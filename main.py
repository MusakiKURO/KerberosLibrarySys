# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import json
from datetime import datetime, timedelta

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';

    text = json.loads(jsonData)
    print(text)


    target_time = '2022-05-19 15:22:00'
    format_pattern = '%Y-%m-%d %H:%M:%S'
    cur_time = datetime.now()
    # 将 'cur_time' 类型时间通过格式化模式转换为 'str' 时间
    cur_time = cur_time.strftime(format_pattern)

    if datetime.strptime(target_time, format_pattern) - datetime.strptime(cur_time, format_pattern) < timedelta(minutes=5):
        print(target_time, '在当前时间之前')
    else:
        print(target_time, '在当前时间之后')


