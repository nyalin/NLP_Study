import glob
import os
import pandas as pd
from collections import Counter


file_list = glob.glob(os.path.join('02_tags', '*.csv'))
for file_path in file_list:
    print(file_path)
    file_name = os.path.split(file_path)[-1].split('.')[0]

    # 데이터 불러오기
    df = pd.read_csv(file_path)
    df = df.fillna('')

    # 한 행씩 읽어서 포함된 단어 추출하기
    print('단어 추출 중')
    tmp_words = []
    for i, rows in df.iterrows():
        text = rows['title_tag'] + ' ' + rows['contents_tag']
        tagged_list = text.split(' ')
        untagged_list = [p.split('/')[0] for p in tagged_list if p != '']
        tmp_words.extend(untagged_list)

    dict_frq = dict(sorted(dict(Counter(tmp_words)).items(), key=lambda i: i[1], reverse=True))

    frq_df = pd.DataFrame(dict_frq.items(), columns=['words', 'count'])

    print("파일 쓰는 중")
    if not os.path.exists("03_freq"):
        os.mkdir("03_freq")
    frq_df.to_csv(os.path.join('03_freq', f"{file_name}_freq.csv"), encoding="utf-8-sig")
print("완료")
