import glob
import os
import pandas as pd
import re
from konlpy.tag import Komoran
from konlpy.tag import Okt  # Open Korean Text : (구)Twitter
EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)


def get_tagger(tagger_name=None):
    tagger = None
    if tagger_name == "Komoran":
        tagger = Komoran(userdic='user_dic.txt')
    elif tagger_name == "Okt":
        tagger = Okt()
    else:
        exit()
    return tagger


# 토크나이징 및 형태소분석
def pos_tagging(line, tagger=None, tagger_name=None):
    # https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0
    list_tags = []
    if tagger_name == "Komoran":
        list_tags = ['NNG', 'NNP']
    elif tagger_name == "Okt":
        list_tags = ['Noun']
    else:
        exit()

    # 불용어 불러오기
    stop_words = []

    # 형태소분석 진행
    line = EMOJI.sub('', line)  # 이모지 제거
    tagged_list = tagger.pos(line.strip())
    tagged_list = [t for t in tagged_list if t[0] not in stop_words]  # 불용어 제거
    tagged_list = [t for t in tagged_list if t[1] in list_tags]  # 필요한 형태소만
    tmp_pos = ["/".join(p) for p in tagged_list]

    return tmp_pos


def main(tagger_name="Komoran"):
    tagger = get_tagger(tagger_name)
    file_list = glob.glob(os.path.join('01_data', '*.csv'))
    for file_path in file_list:
        print(file_path)
        file_name = os.path.split(file_path)[-1].split('.')[0]

        # 데이터 불러오기
        df = pd.read_csv(file_path, encoding='utf-8-sig', index_col=0)
        df = df.fillna('')

        # 형태소 분석하기
        tmp_title = []
        tmp_text = []
        for i, rows in df.iterrows():
            if i % 1000 == 0:
                print(f"{i + 1}번째 줄 진행 중")
            for text_col in ['title', 'contents']:
                text = rows[text_col]
                tagged_list = pos_tagging(text, tagger, tagger_name)
                tagged_text = " ".join(tagged_list)
                if text_col == 'title':
                    tmp_title.append(tagged_text)
                else:
                    tmp_text.append(tagged_text)

        df['title_tag'] = tmp_title
        df['contents_tag'] = tmp_text

        print("파일 쓰는 중")
        if not os.path.exists("02_tags"):
            os.mkdir("02_tags")
        df.to_csv(os.path.join('02_tags', f"{file_name}_{tagger_name}.csv"), encoding="utf-8-sig")
    print("완료")


if __name__ == "__main__":
    main(tagger_name="Komoran")
    # main(tagger_name="Okt")
