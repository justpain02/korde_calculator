from jamo import h2j, j2hcj, is_jamo_modern
from tqdm import tqdm

# 자모 변환 리스트
jamo_exchange_tupple = (
    ('ㄲ', 'ㄱㄱ'),
    ('ㄸ', 'ㄷㄷ'),
    ('ㅃ', 'ㅂㅂ'),
    ('ㅆ', 'ㅅㅅ'),
    ('ㅉ', 'ㅈㅈ'),
    ('ㄳ', 'ㄱㅅ'),
    ('ㄵ', 'ㄴㅈ'),
    ('ㄶ', 'ㄴㅎ'),
    ('ㄺ', 'ㄹㄱ'),
    ('ㄻ', 'ㄹㅁ'),
    ('ㄼ', 'ㄹㅂ'),
    ('ㄽ', 'ㄹㅅ'),
    ('ㄾ', 'ㄹㅌ'),
    ('ㄿ', 'ㄹㅍ'),
    ('ㅀ', 'ㄹㅎ'),
    ('ㅄ', 'ㅂㅅ'),
    ('ㅐ', 'ㅏㅣ'),
    ('ㅒ', 'ㅑㅣ'),
    ('ㅔ', 'ㅓㅣ'),
    ('ㅖ', 'ㅕㅣ'),
    ('ㅘ', 'ㅗㅏ'),
    ('ㅙ', 'ㅗㅏㅣ'),
    ('ㅚ', 'ㅗㅣ'),
    ('ㅝ', 'ㅜㅓ'),
    ('ㅞ', 'ㅜㅓㅣ'),
    ('ㅟ', 'ㅜㅣ'),
    ('ㅢ', 'ㅡㅣ')
)


def s2j(sentence_input):
    try:
        sentence_jamo_extracted = ''.join(_ for _ in j2hcj(h2j(sentence_input)) if is_jamo_modern(_))
        sentence_jamo_koodle = ''
        for i in sentence_jamo_extracted:
            is_changed = False
            for jamo_before, jamo_after in jamo_exchange_tupple:
                if i == jamo_before:
                    sentence_jamo_koodle += jamo_after
                    is_changed = True
                    break
            if not is_changed:
                sentence_jamo_koodle += i
        return sentence_jamo_koodle
    except:
        return None
    
def how_many_word_is_used(sentence_for_test, word_list_for_check):
    sentence_for_test = s2j(sentence_for_test)
    word_list_for_check = s2j(word_list_for_check)
    number_count = 0
    for i in word_list_for_check:
        for j in sentence_for_test:
            if i == j:
                number_count += 1
                break
    return number_count

def find_possible_word_with_dict(used_word, not_used_word, word_dict):
    # 모든 자모음 리스트
    all_jamo_list = 'ㅂㅈㄷㄱㅅㅛㅕㅑㅁㄴㅇㄹㅎㅗㅓㅏㅣㅋㅌㅊㅍㅠㅜㅡ'

    # 안쓰인 white_word 정의
    white_word = ''
    
    # used_word, not_used_word 변환, 여기서 used는 yellow+green, not_used는 grey
    used_word = s2j(used_word)
    not_used_word = s2j(not_used_word)
    print(used_word, not_used_word)
    # 안쓰인 자모 확인용
    for i in all_jamo_list:
        if i not in used_word and i not in not_used_word: # 만약 used나 not_used에 단어가 없으면 == 아직 확인이 안된 단어라면
            white_word += i # white_word에 단어 추가
        
    koodle_out_grey = [] # grey 자모 빠진 단어 목록

    # word_dict 전체에 대해 안쓰인 단어가 들어간 단어는 빼고 나머지만 out_grey 여기에 넣음
    for i in tqdm(word_dict):
        is_in = False
        for j in not_used_word:
            if j in i:
                is_in = True
        if not is_in:
            koodle_out_grey.append(i)
    
    print(f"{len(koodle_out_grey)}/{len(word_dict)} passed") # 결과 공유

    koodle_out_used = [] # used 자모가 쓰인 단어 목록

    # 1차로 거른 목록에서 사용되어야 하는 단어가 안쓰인 단어 목록은 다 베재
    for i in tqdm(koodle_out_grey):
        is_not_in = False
        for j in used_word:
            if j not in i:
                is_not_in = True
        if not is_not_in:
            koodle_out_used.append(i)

    print(f"{len(koodle_out_used)}/{len(koodle_out_grey)} passed") # 결과 공유

    return koodle_out_used, white_word

# yellow : 그냥 쭉 나열한거, 그대신 공백은 _로 대체됨 어차피 이거 안쓰임
# grey = 그냥 쭉 나열한거
# green = 그냥 쭉 나열한거, 그대신 공백은 _로 대체됨 어차피 이거 안쓰임

def koodle_solver(used_word, not_used_word, length, word_dict):
    word_dict_len_fixed = [] # 고정된 길이의 단어만 출력

    
    # 정해진 단어 길이만 목록에 넣는 코드
    for i in tqdm(word_dict):
        if len(i) == length:
            word_dict_len_fixed.append(i)

    # 가능한 단어 목록이랑 미사용된 단어 목록 출력
    koodle_out_used, white_word = find_possible_word_with_dict(used_word=used_word, not_used_word=not_used_word, word_dict=word_dict)

    # 가능한 후보 단어중 안쓰인 자모가 많은 순으로 정렬된 단어 배열
    koodle_white_high = []

    for i in koodle_out_used:
        koodle_white_high.append((how_many_word_is_used(i, white_word), i))
    
    koodle_white_high.sort(reverse=True)

    # 가능한 단어 생각 안하고 안쓰인 자모가 가장 많은 순으로 정렬된 배열
    koodle_white_high_all = []

    for i in tqdm(word_dict):
        koodle_white_high_all.append((how_many_word_is_used(i, white_word), i))
    
    koodle_white_high_all.sort(reverse=True)

    return koodle_white_high, koodle_white_high_all

# input_on은 [입력 단어, 색깔(y=yellow, g=green, r=grey)] 배열의 집합
# top_k는 상위 몇번째 단어까지 출력할지, 기본값은 3
def koodle_input_parser(input_on, length, word_dict, top_k=3):
    # 사용될 문자열 먼저 선언
    used_word = ''
    not_used_word = ''

    # 단어를 자모 분리해서 다시 저장
    for i in range(len(input_on)):
        input_on[i][0] = s2j(input_on[i][0])
    
    print(input_on)
    
    # yellow, green은 사용된 단어로, 나머지는 미사용된 단어로
    for word, pattern in input_on:
        for j in range(length):
            if pattern[j] == 'y':
                used_word += word[j]
            elif pattern[j] == 'g':
                used_word += word[j]
    for word, pattern in input_on:
        for j in range(length):
            if word[j] not in used_word:
                not_used_word += word[j]

    # 중복제거
    used_word = ''.join(dict.fromkeys(used_word))
    not_used_word = ''.join(dict.fromkeys(not_used_word))

    koodle_white_high, koodle_white_high_all = koodle_solver(used_word=used_word, not_used_word=not_used_word, length=length, word_dict=word_dict)
    
    # green, yellow word set 정의
    green_word_set = ['' for _ in range(length)]
    yellow_word_set = ['' for _ in range(length)]

    # green, yellow word set에 순서 맞춰서 단어 목록 채우기
    for word, pattern in input_on:
        for j in range(length):
            if pattern[j] == 'y' or pattern[j] == 'r':
                yellow_word_set[j] += word[j]
            elif pattern[j] == 'g':
                green_word_set[j] += word[j]
    
    # 사용된 자모가 있는 단어중 패턴매칭 성공한 단어의 목록
    koodle_white_high_matching = []

    print(green_word_set)
    print(yellow_word_set)


    for i in koodle_white_high:
        ts = i[1]
        is_it = True
        try:
            for j in range(length):
                if green_word_set[j] != '':
                    for k in list(green_word_set[j]):
                        if ts[j] != k:
                            is_it = False
            for j in range(length):
                if yellow_word_set[j] != '':
                    for k in list(yellow_word_set[j]):
                        if ts[j] == k:
                            is_it = False
            if is_it:
                koodle_white_high_matching.append(i)
        except:
            print(ts)
            exit

    print("조건 만족하는 단어 후보")
    for i in range(min(len(koodle_white_high_matching), top_k)):
        print(f"white_word : {koodle_white_high_matching[i][0]}, word = {koodle_white_high_matching[i][1]}")
    print()

    print("조건은 만족하지 않지만 안쓰인 단어가 많은 목록")
    for i in range(min(len(koodle_white_high_all), top_k)):
        print(f"white_word : {koodle_white_high_all[i][0]}, word = {koodle_white_high_all[i][1]}")
    print()
    