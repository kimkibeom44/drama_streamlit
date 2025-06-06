# 전체 JSON 파일을 불러와 모든 드라마 제목에 대해 XPath 기반 이미지 URL을 추출하는 스크립트

import json
import requests
from lxml import html
from urllib.parse import quote
import time
import os

# 설정 
# 입력 JSON 파일 경로 (환경에 맞게 수정하세요)
INPUT_JSON = r"C:\Users\kimho\OneDrive\바탕 화면\drama_alert\drama\grandma_dramas_100.json"
# 결과 저장 JSON 파일 경로
OUTPUT_JSON = r"C:\Users\kimho\OneDrive\바탕 화면\drama_alert\drama\drama_image_urls.json"
# User-Agent 헤더
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

#이미지 src 추출 함수 
def get_image_src_by_xpath(title):
    url = f"https://search.naver.com/search.naver?query={quote(title)}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    tree = html.fromstring(resp.content)

    # 1) 사용자 지정 XPath 시도
    srcs = tree.xpath('//*[@id="main_pack"]/div[3]/div[2]/div[1]/div[2]/div[1]/a/img/@src')
    # 2) 폴백: main_pack 아래 첫 번째 img 태그
    if not srcs:
        srcs = tree.xpath('//*[@id="main_pack"]//img/@src')
    return srcs[0] if srcs else None

#메인 처리
def main():
    # JSON 불러오기
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        dramas = json.load(f)

    result = {}
    total = len(dramas)
    print(f"총 {total}개의 드라마 이미지 URL 추출을 시작합니다.")

    # 모든 드라마에 대해 처리
    for idx, d in enumerate(dramas, start=1):
        title = d.get("programName", f"no_title_{idx}")
        print(f"[{idx}/{total}] '{title}' 검색 중...", end=" ")
        try:
            img_url = get_image_src_by_xpath(title)
            result[title] = img_url
            print("완료" if img_url else "이미지 없음")
        except Exception as e:
            result[title] = None
            print(f"실패 ({e.__class__.__name__})")
        time.sleep(1)  # 차단 방지 딜레이

    # 결과 저장
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 모든 작업 완료! 결과는 '{OUTPUT_JSON}'에 저장되었습니다.")

if __name__ == "__main__":
    main()


