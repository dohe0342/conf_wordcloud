import fitz
import shutil
from glob import glob
from tqdm import tqdm

path_list = sorted(glob('/Users/mbp/Downloads/ICASSP2024_Proceedings/pdfs/*.pdf')) ## pdf 파일 리스트
keyword_file = open("./asr_keyword.txt", "w") ## 키워드, 빈도수를 저장하기 위한 텍스트 파일

index_dict = {}
for path in tqdm(path_list):
    filename = path.split('/')[-1]
    doc = fitz.open(path)
    texts = doc[0].get_text()
    texts = texts.split('\n')

    index_lines = []
    for enum, line in enumerate(texts):
        ## pdf 에서 키워드만 추출
        if 'index term' in line.lower() or 'keywords:' in line.lower() or 'keywords-' in line.lower():
            index_lines.append(enum)
        if "1. intro" in line.lower():
            index_lines.append(enum)
    
    if len(index_lines) < 2:
        continue

    index_terms = []
    for line in range(index_lines[0], index_lines[1]):
        index_terms.append(texts[line])
    
    ## 키워드 텍스트 전처리
    index_terms = ', '.join(index_terms)
    index_terms = index_terms.lower()
    index_terms = index_terms.replace('-, ', '')
    if len(index_terms) < 5:
        continue
    
    if 'index' not in index_terms[:8] and 'key' not in index_terms[:8]:
        continue
    
    index_terms = index_terms.replace('index terms: ', '')
    index_terms = index_terms.replace('index terms— ', '')
    index_terms = index_terms.replace('index terms-, ', '')
    index_terms = index_terms.replace('index terms-', '')
    
    ## 키워드 중 "asr", "speech recog"를 가지고 있는 경우 ditionary에 append 
    ## dictionary는{ 키워드 : 빈도수 } 로 표현
    if 'asr' in index_terms or 'speech recog' in index_terms:
        #if 'language' in index_terms or 'llm' in index_terms:
        #    shutil.copy(path, f"./{filename}")
        index_terms = index_terms.split(', ')
        for term in index_terms:
            try: index_dict[term] += 1
            except: index_dict[term] = 1

index_dict = sorted(index_dict.items(), key=lambda x:x[1], reverse=True)
llm = 0
for k, v in index_dict:
    #print(k, v)
    keyword_file.write(f"{k} {v}\n")
