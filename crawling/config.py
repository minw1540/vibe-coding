"""
네이버 부동산 크롤링 설정 파일
"""

# API 설정
NAVER_REAL_ESTATE_API_URL = "https://new.land.naver.com/api/articles/complex/27643"

# 기본 파라미터
DEFAULT_PARAMS = {
    'realEstateType': 'APT:ABYG:JGC:PRE',
    'tradeType': '',
    'tag': '::::::::',
    'rentPriceMin': 0,
    'rentPriceMax': 900000000,
    'priceMin': 0,
    'priceMax': 900000000,
    'areaMin': 0,
    'areaMax': 900000000,
    'oldBuildYears': '',
    'recentlyBuildYears': '',
    'minHouseHoldCount': '',
    'maxHouseHoldCount': '',
    'showArticle': False,
    'sameAddressGroup': False,
    'minMaintenanceCost': '',
    'maxMaintenanceCost': '',
    'priceType': 'RETAIL',
    'directions': '',
    'complexNo': 27643,
    'buildingNos': '',
    'areaNos': '',
    'type': 'list',
    'order': 'rank'
}

# HTTP 헤더 설정
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://new.land.naver.com/complexes/27643?ms=37.5341,126.9062,17&a=APT:ABYG:JGC:PRE&e=RETAIL',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDkwOTM4NzksImV4cCI6MTc0OTEwNDY3OX0.JR6-_3CjyN9MKCPi_PrJecao_ZnftoXNaOtLejqr1gM'
}

# 크롤링 설정
COMPLEX_NO = 27643
REQUEST_DELAY = 2  # 요청 간 지연 시간(초)
MAX_RETRIES = 3    # 최대 재시도 횟수
TIMEOUT = 10       # HTTP 요청 타임아웃(초)

# 저장 설정
OUTPUT_DIR = './data'
LOG_DIR = './logs' 