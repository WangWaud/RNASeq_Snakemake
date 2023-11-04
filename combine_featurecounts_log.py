# 用于统计当前目录下所有由featurecounts生成的log文件，汇总并根据SampleName排序
import os
import pandas as pd
import argparse

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="统计featureCounts结果并排序")

# 添加输入文件路径参数
parser.add_argument("-i", "--input", type=str, help="输入log文件所在路径")

# 添加输出文件路径参数
parser.add_argument("-o", "--output", type=str, help="输出统计结果文件路径")

# 解析命令行参数
args = parser.parse_args()

# 确保输入和输出参数都已提供
if not args.input or not args.output:
    print("请提供输入文件路径(-i)和输出文件路径(-o)。")
    exit(1)

# 获取输入路径下所有的log文件
log_files = [file for file in os.listdir(args.input) if file.endswith(".log")]

# 创建一个用于保存结果的列表
results = []

# 遍历每个log文件并统计信息
for log_file in log_files:
    # 构建log文件的完整路径
    log_file_path = os.path.join(args.input, log_file)
    
    # 获取样本名
    sample_name = os.path.splitext(log_file)[0]
    
    # 初始化统计变量
    assigned = 0
    total_reads = 0
    
    # 打开log文件并读取内容
    with open(log_file_path, "r") as file:
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

# 构建输出文件的完整路径
output_file_path = os.path.join(args.output, "featurecount_summary.tsv")

# 将结果写入到输出文件中
df_sorted.to_csv(output_file_path, sep="\t", index=False)

print(f"统计结果已保存到 {output_file_path} 文件中，并按样本名排序，Assigned Rate已保留两位小数。")
