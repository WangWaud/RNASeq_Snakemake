# 用于统计当前目录下所有由featurecounts生成的log文件，汇总并根据samplename排序
import os
import pandas as pd

# 获取当前目录下所有的log文件
log_files = [file for file in os.listdir() if file.endswith(".log")]

# 创建一个用于保存结果的列表
results = []

# 遍历每个log文件并统计信息
for log_file in log_files:
    # 获取样本名
    sample_name = os.path.splitext(log_file)[0]

    # 初始化统计变量
    assigned = 0
    total_reads = 0

    # 打开log文件并读取内容
    with open(log_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Assigned"):
                assigned = int(line.split()[1])
            elif line.startswith("Unassigned_"):
                total_reads += int(line.split()[1])

    # 计算Assigned Rate并保留两位小数
    assigned_rate = round((assigned / (assigned + total_reads)) * 100, 2)

    # 添加统计结果到列表中
    results.append([sample_name, assigned, assigned + total_reads, assigned_rate])

# 创建DataFrame对象并排序
df = pd.DataFrame(results, columns=["SampleName", "Assigned", "TotalReads", "AssignedRate"])
df_sorted = df.sort_values(by="SampleName")

# 将结果写入到featurecount_summary.tsv文件中
df_sorted.to_csv("featurecount_summary.tsv", sep="\t", index=False)

print("统计结果已保存到featurecount_summary.tsv文件中，并按样本名排序，Assigned Rate已保留两位小
数。")
