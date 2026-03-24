import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import random
from datetime import datetime, timedelta
import os

# ---------------------- 步骤1：生成2000条模拟监控数据（按分钟粒度） ----------------------
# 计算总时间跨度：2000分钟 ≈ 33.3小时，确保能按2小时划分节点
end_time = datetime.now()
start_time = end_time - timedelta(minutes=2000)  # 从当前时间往前推2000分钟

# 生成2000个按分钟递增的时间点
time_points = []
current_time = start_time
for _ in range(2000):
    time_points.append(current_time)
    current_time += timedelta(minutes=1)

# 生成CPU和内存占用率（模拟真实波动）
cpu_usage = []
mem_usage = []
cpu_base = 40
mem_base = 50

for i in range(2000):
    # 加入趋势性波动
    if i % 100 == 0:
        cpu_base += random.uniform(-5, 5)
        mem_base += random.uniform(-3, 3)
    # 限制合理范围
    cpu_base = max(10, min(85, cpu_base))
    mem_base = max(30, min(75, mem_base))

    # 实时波动噪声
    cpu_val = cpu_base + random.uniform(-8, 8)
    mem_val = mem_base + random.uniform(-5, 5)

    cpu_usage.append(round(cpu_val, 1))
    mem_usage.append(round(mem_val, 1))

# 构造DataFrame
df = pd.DataFrame({
    "时间": [t.strftime("%Y-%m-%d %H:%M:%S") for t in time_points],
    "CPU占用率(%)": cpu_usage,
    "内存占用率(%)": mem_usage
})
# 转换时间列为datetime类型，方便后续筛选
df["时间_原始"] = time_points

# ---------------------- 步骤2：设置绘图参数 ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows
# plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]  # Mac
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['figure.figsize'] = (15, 8)

# ---------------------- 步骤3：写入Excel并生成按2小时节点的图表 ----------------------
excel_file = "系统监控数据_2小时节点.xlsx"
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

# 1. 写入原始数据
df[["时间", "CPU占用率(%)", "内存占用率(%)"]].to_excel(writer, sheet_name="监控数据", index=False)

# 2. 创建图表sheet
workbook = writer.book
chart_sheet = workbook.add_worksheet("趋势图表")

# 3. 绘制图表（核心：按2小时设置x轴标签）
fig, ax = plt.subplots(figsize=(18, 9))

# 绘制趋势线
ax.plot(df.index, df["CPU占用率(%)"], color="#FF6B6B", linewidth=1, label="CPU占用率")
ax.plot(df.index, df["内存占用率(%)"], color="#4ECDC4", linewidth=1, label="内存占用率")

# ---------------------- 关键优化：按2小时生成x轴标签 ----------------------
# 计算2小时间隔的时间点（单位：分钟）
two_hours_minutes = 120  # 2小时=120分钟
# 生成标签位置：从0开始，每120分钟一个节点
tick_positions = list(range(0, 2000, two_hours_minutes))
# 对应位置的时间标签（格式化：只保留 小时:分钟 或 日期+小时，更简洁）
tick_labels = []
for pos in tick_positions:
    time_val = df["时间_原始"].iloc[pos]
    # 格式化：如果跨天显示日期+小时，否则只显示小时:分钟
    if pos == 0 or time_val.date() != df["时间_原始"].iloc[pos - 1].date():
        tick_labels.append(time_val.strftime("%m-%d %H:%M"))
    else:
        tick_labels.append(time_val.strftime("%H:%M"))

# 设置x轴
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=10)

# 图表样式优化
ax.set_title("2000条系统监控数据趋势（按2小时节点展示）", fontsize=16, pad=20)
ax.set_xlabel("时间（每2小时一个节点）", fontsize=12)
ax.set_ylabel("占用率(%)", fontsize=12)
ax.legend(loc="upper right", fontsize=11)
ax.grid(alpha=0.3)
ax.set_ylim(0, 100)  # 占用率范围固定0-100%，更直观
plt.tight_layout()

# 4. 嵌入图表到Excel
fig.savefig("temp_trend_2h.png", dpi=100, bbox_inches="tight")
chart_sheet.insert_image("A1", "temp_trend_2h.png", {
    "x_scale": 1.1,
    "y_scale": 1.1,
    "x_offset": 5,
    "y_offset": 5
})

# ---------------------- 步骤4：清理资源 ----------------------
writer.close()
# 删除临时图片
if os.path.exists("temp_trend_2h.png"):
    os.remove("temp_trend_2h.png")

# 输出验证信息
print(f"✅ 数据生成完成！共{len(df)}条记录")
print(f"📁 文件保存路径：{os.path.abspath(excel_file)}")
print(f"🕒 时间跨度：{start_time.strftime('%Y-%m-%d %H:%M')} 至 {end_time.strftime('%Y-%m-%d %H:%M')}")
print(f"📌 x轴节点：每2小时（120分钟）一个标签，共{len(tick_positions)}个节点")
print("\n📊 数据预览：")
print(df[["时间", "CPU占用率(%)", "内存占用率(%)"]].head(3))