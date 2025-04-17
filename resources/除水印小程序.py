import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser  # 新增导入模块


def fetch_video():
    try:
        # 获取用户输入
        target_url = url_entry.get()
        user_token =''
        user_id =''

        # 构造请求数据
        data = {
            "url": target_url,
            "token": user_token,
            "id": user_id,
            "user_id": 8
        }

        # 发送POST请求
        response = requests.post(
            "https://qq.yyymvp.com/query",
            data=data,
        )

        # 处理响应
        if response.status_code == 200:
            res_data = response.json()
            if 'data' in res_data and 'downurl' in res_data['data']:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, res_data['data']['downurl'])
                global download_url
                download_url = res_data['data']['downurl']
                open_btn.config(state=tk.NORMAL)
            else:
                messagebox.showerror("错误", "未找到下载链接")
        else:
            messagebox.showerror("错误", f"请求失败，状态码：{response.status_code}")

    except Exception as e:
        messagebox.showerror("异常", f"发生错误：{str(e)}")


def open_download_link():
    try:
        if download_url:
            webbrowser.open(download_url, new=2)  # 在新标签页打开
        else:
            messagebox.showwarning("警告", "请先获取有效链接")
    except Exception as e:
        messagebox.showerror("打开失败", f"无法打开链接：{str(e)}")



# 创建主窗口
root = tk.Tk()
root.title("短视频除水印工具")
root.geometry("600x400")
global download_url


# 使用ttk样式
style = ttk.Style()
style.configure("TLabel", padding=6, font=('微软雅黑', 10))
style.configure("TButton", font=('微软雅黑', 10))

# 输入框框架
input_frame = ttk.Frame(root, padding=20)
input_frame.pack(fill=tk.X)

# URL输入
ttk.Label(input_frame, text="目标视频URL:").grid(row=0, column=0, sticky=tk.W)
url_entry = ttk.Entry(input_frame, width=50)
url_entry.grid(row=0, column=1, padx=10)

# 结果显示
result_frame = ttk.Frame(root, padding=20)
result_frame.pack(fill=tk.BOTH, expand=True)
ttk.Label(result_frame, text="下载链接:").pack(anchor=tk.W)
result_text = tk.Text(result_frame, height=4, wrap=tk.WORD)
result_text.pack(fill=tk.X)


# 在原有UI代码中添加按钮
# 在 button_frame 部分新增按钮
button_frame = ttk.Frame(root, padding=20)
button_frame.pack()
ttk.Button(button_frame, text="获取下载链接", command=fetch_video).pack(side=tk.LEFT, padx=5)
open_btn = ttk.Button(button_frame, text="打开链接",
                     command=open_download_link,
                     state=tk.DISABLED)  # 初始不可用
open_btn.pack(side=tk.LEFT, padx=5)

# 滚动条
scroll = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_text.configure(yscrollcommand=scroll.set)

root.mainloop()