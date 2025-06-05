# 네이버 부동산 매물 정보 크롤링 시스템

네이버 부동산 웹사이트에서 특정 아파트 단지의 매물 정보를 자동으로 수집하는 시스템입니다.

## 📋 프로젝트 개요

이 프로젝트는 네이버 부동산 API를 통해 **Complex No. 27643** 단지의 매물 정보(아파트, 주상복합, 오피스텔, 분양권)를 정기적으로 수집하여 CSV 파일로 저장합니다.

### 주요 기능

- 🏠 **매물 정보 수집**: 아파트, 주상복합, 오피스텔, 분양권 정보
- 📊 **데이터 정제**: 가격, 면적, 층수, 방향 등 핵심 정보 추출
- 💾 **CSV 저장**: 분석하기 쉬운 형태로 데이터 저장
- ⏰ **자동 스케줄링**: 일일/주간/주기적 크롤링 지원
- 🔄 **페이지네이션**: 모든 매물 페이지 자동 순회
- 📝 **상세 로깅**: 크롤링 과정 추적 및 오류 관리

## 🛠 기술 스택

- **언어**: Python 3.x
- **핵심 라이브러리**:
  - `requests`: HTTP API 통신
  - `pandas`: 데이터 처리 및 CSV 저장
  - `selenium`: 동적 인증 (선택사항)
  - `APScheduler`: 작업 스케줄링
- **환경 관리**: venv (가상환경)

## 📦 설치 및 설정

### 1. 프로젝트 클론 및 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 디렉토리 구조

```
crawling/
├── config.py                     # 설정 파일
├── main_crawler.py               # 메인 크롤러
├── scheduler.py                  # 스케줄링 시스템
├── requirements.txt              # 의존성 목록
├── modules/                      # 핵심 모듈
│   ├── auth_manager.py          # 인증 관리
│   ├── request_handler.py       # HTTP 요청 처리
│   ├── data_extractor.py        # 데이터 추출
│   ├── storage_manager.py       # 데이터 저장
│   └── pagination_controller.py # 페이지네이션 제어
├── utils/                       # 유틸리티
│   └── logger.py               # 로깅 시스템
├── data/                        # 수집된 데이터 (자동 생성)
└── logs/                        # 로그 파일 (자동 생성)
```

## 🚀 사용 방법

### 기본 크롤링 실행

```bash
# 기본 크롤링 (Complex No. 27643)
python main_crawler.py

# 특정 단지 크롤링
python main_crawler.py --complex 12345

# 최대 페이지 수 제한
python main_crawler.py --max-pages 50

# 테스트 모드 (2페이지만)
python main_crawler.py --test

# 동적 인증 사용 (Selenium)
python main_crawler.py --dynamic-auth
```

### 스케줄링 실행

```bash
# 매일 오전 9시 크롤링
python scheduler.py --mode daily --hour 9 --minute 0

# 매주 월요일 오전 9시 크롤링
python scheduler.py --mode weekly --day-of-week 0 --hour 9

# 30분마다 주기적 크롤링
python scheduler.py --mode interval --interval-minutes 30

# 테스트 스케줄링 (1분 후 실행)
python scheduler.py --mode test
```

## 📊 수집되는 데이터

| 필드명 | 설명 | 예시 |
|--------|------|------|
| articleNo | 매물 고유 ID | "2024010101" |
| realEstateType | 부동산 유형 | "APT", "ABYG", "JGC", "PRE" |
| tradeType | 거래 유형 | "A1"(매매), "B1"(전세), "B2"(월세) |
| price | 가격 정보 | "5억 2000" |
| areaString | 면적 정보 | "84.50m²/62.30m²" |
| floorInfo | 층 정보 | "고층", "5/20" |
| buildingName | 동 정보 | "101동" |
| registDate | 등록일 | "2024.01.01" |
| confirmDate | 확인일 | "2024.01.01" |
| direction | 방향 | "남향", "동남향" |
| articleFeatureDesc | 매물 특징 | "리모델링 완료, 풀옵션" |
| agentName | 중개사명 | "○○공인중개사" |
| telNo | 연락처 | "02-1234-5678" |

## ⚙️ 설정 옵션

`config.py` 파일에서 다음 설정을 변경할 수 있습니다:

```python
# 크롤링 대상 단지
COMPLEX_NO = 27643

# 요청 간 지연 시간 (초)
REQUEST_DELAY = 2

# 최대 재시도 횟수
MAX_RETRIES = 3

# HTTP 요청 타임아웃 (초)
TIMEOUT = 10

# 출력 디렉토리
OUTPUT_DIR = './data'
LOG_DIR = './logs'
```

## 📈 출력 파일 형태

### CSV 파일
- 파일명: `YYYYMMDD_HHMMSS_complex_27643_articles.csv`
- 인코딩: UTF-8 with BOM (한글 지원)
- 형식: 헤더 포함, 쉼표 구분

### 메타데이터 파일
```json
{
  "crawling_info": {
    "complex_no": 27643,
    "start_time": "2024-01-01T09:00:00",
    "end_time": "2024-01-01T09:05:30",
    "duration_seconds": 330,
    "total_articles_collected": 150,
    "crawler_version": "1.0.0"
  }
}
```

## 🔧 고급 기능

### 동적 인증 (Selenium)
인증 토큰이 만료되거나 복잡한 인증이 필요한 경우:

```bash
# Chrome 드라이버 자동 설치 및 동적 인증
python main_crawler.py --dynamic-auth
```

### 오래된 파일 자동 정리
시스템이 자동으로 최신 10개 파일만 유지하고 오래된 파일을 삭제합니다.

### 에러 처리 및 재시도
- 네트워크 오류: 자동 재시도 (최대 3회)
- HTTP 429 (Too Many Requests): 지연 후 재시도
- 인증 오류: 즉시 실패 및 로깅

## 📋 로그 확인

```bash
# 실시간 로그 확인
tail -f logs/crawler_log_YYYYMMDD.log

# 최근 로그 확인
cat logs/crawler_log_$(date +%Y%m%d).log
```

## ⚠️ 주의사항

1. **법적 준수**: 네이버 부동산 이용약관 및 robots.txt를 준수해야 합니다
2. **요청 제한**: 과도한 요청으로 인한 IP 차단을 방지하기 위해 요청 간 지연 시간을 설정했습니다
3. **데이터 사용**: 수집된 데이터의 상업적 이용 시 법적 검토가 필요합니다
4. **시스템 리소스**: 대량 데이터 처리 시 메모리 사용량을 모니터링하세요

## 🔄 크론 작업 설정 (Linux/macOS)

```bash
# crontab 편집
crontab -e

# 매일 오전 9시 크롤링
0 9 * * * cd /path/to/crawling && /path/to/venv/bin/python main_crawler.py

# 매주 월요일 오전 9시 크롤링
0 9 * * 1 cd /path/to/crawling && /path/to/venv/bin/python main_crawler.py
```

## 🆘 문제 해결

### 인증 오류 (HTTP 401/403)
```bash
# 동적 인증 사용
python main_crawler.py --dynamic-auth
```

### 네트워크 오류
- 인터넷 연결 확인
- VPN 사용 시 VPN 연결 상태 확인
- 방화벽 설정 확인

### 크롤링 결과가 없는 경우
- 단지 번호(complexNo) 확인
- API URL 유효성 확인
- 로그 파일에서 상세 오류 메시지 확인

## 📞 기술 지원

프로젝트 관련 문의나 이슈는 로그 파일과 함께 제보해 주세요.

---

**버전**: 1.0.0  
**최종 업데이트**: 2025-01-03 