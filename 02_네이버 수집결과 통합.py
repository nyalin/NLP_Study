import os
import glob
import pandas as pd


file_list = glob.glob(os.path.join("naverFile", "*"))

keyword_list = []
for file_path in file_list:
    keyword_list.append(file_path.split(os.sep)[1])

for keyword in keyword_list:
    print(keyword)
    file_list = glob.glob(os.path.join("naverFile", keyword, "*", "*.txt"))
    tmp_list = []
    for file_path in file_list:
        date = file_path.split(os.sep)[-2]
        file_name = os.path.basename(file_path)
        platform = file_name.replace('_summary.txt', '')
        tmp_df = pd.read_csv(file_path, encoding='utf-8', sep="\t", names=['title', 'contents', 'url', 'writer'])
        tmp_df['date'] = date
        tmp_df['platform'] = platform
        tmp_list.append(tmp_df)

    df = pd.concat(tmp_list, ignore_index=True)

    if not os.path.exists("01_data"):
        os.mkdir("01_data")

    df.to_csv(os.path.join("01_data", f"{keyword}.csv"), encoding="utf-8-sig")
