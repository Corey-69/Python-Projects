import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import os

# 1. 准备数据
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月"],
    "销售额": [12000, 15000, 11000, 18000, 20000],
    "利润": [3000, 4500, 2800, 5000, 6000]
})

# 2. 初始化Excel写入器
excel_path = "销售分析报告.xlsx"
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
df.to_excel(writer, sheet_name="原始数据", index=False)

# 3. 设置绘图样式
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 4. 创建图表sheet并插入多个图表
workbook = writer.book
chart_sheet = workbook.add_worksheet("可视化图表")

# 绘制折线图（销售额趋势）
fig1, ax1 = plt.subplots(figsize=(8, 4))
df.plot(x="月份", y="销售额", kind="line", marker="o", ax=ax1, color="red")
ax1.set_title("月度销售额趋势")
ax1.set_xlabel("月份")
ax1.set_ylabel("金额（元）")
fig1.tight_layout()
fig1.savefig('chart1.png', dpi=100, bbox_inches='tight')
chart_sheet.insert_image('A1', 'chart1.png', {'x_scale': 1, 'y_scale': 1})

# 绘制柱状图（销售额+利润对比）
fig2, ax2 = plt.subplots(figsize=(8, 4))
df.plot(x="月份", y=["销售额", "利润"], kind="bar", ax=ax2, color=["blue", "green"])
ax2.set_title("销售额vs利润对比")
ax2.set_xlabel("月份")
ax2.set_ylabel("金额（元）")
fig2.tight_layout()
fig2.savefig('chart2.png', dpi=100, bbox_inches='tight')
chart_sheet.insert_image('A30', 'chart2.png', {'x_scale': 1, 'y_scale': 1})  # 放在A30位置，避免重叠

# 5. 完成写入并清理临时文件
writer.close()
for f in ['chart1.png', 'chart2.png']:
    if os.path.exists(f):
        os.remove(f)

print(f"文件已保存至：{os.path.abspath(excel_path)}")