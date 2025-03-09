import glob
import os
import pandas as pd


# 매트릭스용 키워드 불러오기
words = []
with open('matrix_keywords.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip('\r\n').strip().lower()
        if line != '' and line not in words:
            words.append(line.lower())

file_list = glob.glob(os.path.join('02_tags', '*.csv'))
for file_path in file_list:
    print(file_path)
    file_name = os.path.split(file_path)[-1].split('.')[0]

    # 데이터 불러오기
    df = pd.read_csv(file_path)
    df = df.fillna('')

    # 동시출현 값 계산 중
    print('동시출현 값 계산 중')
    tmp_dict = {}
    for i, rows in df.iterrows():
        text = rows['title_tag'] + ' ' + rows['contents_tag']

        tagged_list = text.split(' ')
        untagged_list = [p.split('/')[0] for p in tagged_list if p != '']

        for j, w1 in enumerate(words):
            for k, w2 in enumerate(words):
                if j >= k:
                    continue
                try:
                    tmp_dict[str(w1) + "/" + str(w2)] += untagged_list.count(w1) * untagged_list.count(w2)
                except KeyError:
                    tmp_dict[str(w1) + "/" + str(w2)] = untagged_list.count(w1) * untagged_list.count(w2)

    # 행렬 구성
    print('행렬 구성 중')
    matrix_df = pd.DataFrame(0, columns=words, index=words)
    for words, count in tmp_dict.items():
        w1, w2 = words.split('/')
        matrix_df.loc[w1, w2] = count
        matrix_df.loc[w2, w1] = count

    print("파일 쓰는 중")
    matrix_df.to_csv(os.path.join('04_matrix', f"{file_name}_mat.csv"), encoding="utf-8-sig")
print("완료")
