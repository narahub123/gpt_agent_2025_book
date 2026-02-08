import pymupdf
import os

pdf_file_path = 'chap04/data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정지원시스템 설계 및 구축.pdf'
# 경로가 제대로 되었는지 확인하는 방법은? 

doc = pymupdf.open(pdf_file_path) # pdf를 페이지별로 내용을 읽음 

full_text = ''

for page in doc: # 문서 페이지 반복
    text = page.get_text()
    full_text += text

# 원본 pdf 파일의 이름 추출
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0] # 확장자 제거

# output 폴더에 텍스트 파일 형식으로 저장 
txt_file_path = f"chap04/output/{pdf_file_name}.txt"
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

