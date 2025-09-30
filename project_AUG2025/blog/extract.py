# extract.py
# 정규표현식으로 가격/기간/날짜 범위를 헐겁게 추출해 "잠금(locks)" JSON 생성

import re                      # 정규표현식
from typing import Dict, Any   # 타입 힌트

# 간단한 정규식 패턴(필요시 확장)
RE_PRICE = re.compile(r"(?:₩|원|KRW)?\s*([0-9]{1,3}(?:[,\.][0-9]{3})+|[0-9]+)\s*(?:원|KRW)?")
RE_NIGHTS = re.compile(r"(\d+)\s*박")        # 예: 3박
RE_DAYS = re.compile(r"(\d+)\s*일")          # 예: 4일
RE_DATE_RANGE = re.compile(r"(\d{1,2}\/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2})\s*[-~]\s*(\d{1,2}\/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2})")

def extract_locks(text: str) -> Dict[str, Any]:
    """본문 텍스트에서 가격/기간/날짜범위 등 잠금을 추출"""
    prices = [m.group(1) for m in RE_PRICE.finditer(text)]           # 가격 후보들
    nights = [int(m.group(1)) for m in RE_NIGHTS.finditer(text)]     # 박 수 후보
    days = [int(m.group(1)) for m in RE_DAYS.finditer(text)]         # 일 수 후보
    date_ranges = [m.groups() for m in RE_DATE_RANGE.finditer(text)] # 기간 후보
    # 우선값 선택(가장 처음 등장)
    price = prices[0] if prices else None                             # 대표 가격
    duration = None                                                   # 기간 텍스트
    if nights and days:
        duration = f"{nights[0]}박 {days[0]}일"
    elif nights:
        duration = f"{nights[0]}박"
    elif days:
        duration = f"{days[0]}일"
    date_range = None
    if date_ranges:
        a, b = date_ranges[0]
        date_range = f"{a} ~ {b}"
    # 결과 조립
    return {
        "price": price,            # 예: "1,290,000"
        "duration": duration,      # 예: "3박 4일"
        "date_range": date_range,  # 예: "2025.10.01 ~ 2025.10.04"
    }
