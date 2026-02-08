import pymupdf
import os

pdf_file_path = 'chap04/data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정지원시스템 설계 및 구축.pdf'

doc = pymupdf.open(pdf_file_path) # pdf를 페이지별로 내용을 읽음 

# 높이 기반으로 헤더와 푸터를 제거
header_height = 80 # 헤더 높이
footer_height = 80 # 푸터 높이

full_text = ''

for page in doc: # 문서 페이지 반복
    rect = page.rect # 페이지 크기 가져오기 
    
    header = page.get_text(clip=(0, 0, rect.width, header_height))
    footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))
    text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))

    full_text += text + '\n-----------------------------\n'

# 원본 pdf 파일의 이름 추출
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0] # 확장자 제거

# output 폴더에 텍스트 파일 형식으로 저장 
txt_file_path = f"chap04/output/{pdf_file_name}_with_preprocessing.txt"
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

