import glob
import os
import pandas as pd
import re

import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis


TOPIC_K = 20

print(f"토픽 값 : {TOPIC_K}")
file_list = glob.glob(os.path.join('02_tags', '*.csv'))
for file_path in file_list:
    print(file_path)
    file_name = os.path.split(file_path)[-1].split('.')[0]

    # 데이터 불러오기
    df = pd.read_csv(file_path)
    df = df.fillna('')

    # 문서(형태소분석 단어) 추출하기
    print('단어 추출 중')
    phr_text = []
    for i, rows in df.iterrows():
        text = rows['title_tag'] + ' ' + rows['contents_tag']
        tagged_list = text.split(' ')
        untagged_list = [p.split('/')[0] for p in tagged_list if p != '']
        phr_text.append(untagged_list)

    # 토픽모델링을 수행하기 위한 기초자료 구성
    id2word = gensim.corpora.Dictionary(phr_text)
    corpus = [id2word.doc2bow(text) for text in phr_text]

    # 토픽모델링 수행
    print('LDA 모델 구성 중')
    model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=TOPIC_K, alpha='auto', random_state=7)

    # gensim 토픽모델링 weights 정리
    tmp_weight = {}
    for topic_number, values in model.print_topics(num_topics=TOPIC_K, num_words=10):
        # print(topic_number, values)
        tmp_weight[topic_number] = re.findall('(\d\.\d{3})\*\"(\w*)\"', values)

    # 가중치값 구성
    tmp_list = []
    for topic_num, ww in tmp_weight.items():
        for (weight, word) in ww:
            tmp_list.append([topic_num, word, weight])
    weight_df = pd.DataFrame(tmp_list, columns=['topic_num', 'words', 'weights'])

    # 시각화 구성
    print("시각화 자료 만들기")
    vis = gensimvis.prepare(model, corpus, id2word, sort_topics=False)

    print("파일 쓰는 중")
    weight_df.to_csv(os.path.join('05_topicmodel', f"{file_name}_{TOPIC_K}_weight.csv"), encoding='utf-8-sig')
    pyLDAvis.save_html(vis, os.path.join('05_topicmodel', f"{file_name}_{TOPIC_K}.html"))
print("완료")
