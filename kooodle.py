from jamo import h2j, j2hcj, is_jamo_modern
import pandas as pd
from tqdm import tqdm
from kooodle_function import s2j, koodle_input_parser
import csv




# 엑셀 파일 로딩
# NIAic_data = pd.read_excel('NIADic.xlsx')
# GUKRIP_data = pd.read_excel('한국어 학습용 어휘 목록.xls')

# NIAic_ncn_jamo_koddle = []
# for i in tqdm(NIAic_data.index):
#     if NIAic_data['tag'][i] == 'ncn':
#         temp_result = s2j(NIAic_data['term'][i])
#         if temp_result is not None:
#             NIAic_ncn_jamo_koddle.append(temp_result)

# GUKRIP_dataset_koddle = []
# for i in tqdm(GUKRIP_data.index):
#     if GUKRIP_data['품사'][i] == '명':
#         temp_result = s2j(GUKRIP_data['단어'][i])
#         if temp_result is not None:
#             GUKRIP_dataset_koddle.append(temp_result)

# word_dict_full = list(set(GUKRIP_dataset_koddle + NIAic_ncn_jamo_koddle))

# with open("word_dict.csv", 'w', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(word_dict_full)

word_dict_full = list()
with open("word_dict.csv", 'r', encoding='utf-8-sig') as file:
    rea = csv.reader(file)
    for row in rea:
        for elem in row:
            word_dict_full.append(elem)

# print(word_dict_full[:10])        

# 모든 자모음 리스트
all_jamo_list = 'ㅂㅈㄷㄱㅅㅛㅕㅑㅁㄴㅇㄹㅎㅗㅓㅏㅣㅋㅌㅊㅍㅠㅜㅡ'

# input_on은 [입력 단어, 색깔(y=yellow, g=green, r=grey)] 배열의 집합
input_on = []

length = int(input("꼬들의 길이는 : "))

word_dict_len_fixed = []
for i in tqdm(word_dict_full):
    if len(i) == length:
        word_dict_len_fixed.append(i)

top_k = int(input("후보 단어중 상위 몇개까지 출력할건지 (기본=3) : "))

while True:
    temp_word = input("입력한 단어는? 문제 풀었으면 solved 입력 : ")
    if temp_word == 'solved':
        break
    temp_pattern = input("결과 패턴은? (노랑=y, 초록=g, 회색=r): ")

    input_on.append([temp_word, temp_pattern])

    koodle_input_parser(input_on, length, word_dict_len_fixed, top_k)

    print("사이클 순환 완료")
    print()

print("코드 종료")