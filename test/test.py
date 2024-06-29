import csv
import os


def update_votepool2(n):
    input_file = './1.csv'
    output_file = './1.csv'
    # 如果输出文件与输入文件相同，则使用临时文件
    if output_file == input_file:
        temp_file = 'temp_output.csv'
    else:
        temp_file = output_file

    with open(input_file, 'r', newline='') as csv_in, open(temp_file, 'w', newline='') as csv_out:
        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out)

        # 跳过前n行
        for _ in range(n):
            next(reader, None)

            # 写入剩余的行
        for row in reader:
            writer.writerow(row)

            # 如果输出文件与输入文件相同，则替换原始文件
    if output_file == input_file:
        # 先删除原始文件，防止替换失败（例如，如果新文件与旧文件大小不同）
        try:
            os.remove(input_file)
        except FileNotFoundError:
            pass
            # 然后重命名临时文件为原始文件名
        os.rename(temp_file, input_file)

update_votepool2(5)