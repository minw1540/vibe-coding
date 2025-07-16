🏡 나만의 스마트 부동산 시트 웹/앱 서비스 데이터베이스 설계서 🏡
본 문서는 '나만의 스마트 부동산 시트' 웹/앱 서비스의 데이터베이스 스키마를 상세하게 정의합니다. MySQL과 MongoDB의 이원화된 데이터베이스 아키텍처를 기반으로, 각 데이터베이스의 역할과 저장될 데이터의 구조를 명확히 합니다. 데이터의 무결성, 효율성, 확장성, 그리고 보안을 최우선으로 고려하여 설계합니다.

1. 개요
서비스는 관계형 데이터의 강점과 NoSQL의 유연성을 모두 활용하는 하이브리드 데이터베이스 전략을 채택합니다.

MySQL: 정형화되고 관계가 중요한 마스터 데이터(사용자 계정, 지역/단지 기본 정보, 국토부 API 캐싱 데이터)를 저장합니다.

MongoDB: 유연한 스키마가 필요하고 사용자별 개인화된 데이터(사용자 시트, 알림 설정, 알림 모니터링 스냅샷)를 저장합니다.

2. MySQL 데이터베이스 설계 (관계형 데이터)
2.1. 테이블 목록 및 스키마
2.1.1. users 테이블 (사용자 계정 정보)
설명: 서비스에 가입한 사용자들의 기본 계정 정보를 저장합니다.

역할: 사용자 인증 및 인가, 기본 프로필 관리.

컬럼명

데이터 타입

제약 조건

설명

id

BIGINT

PRIMARY KEY, AUTO_INCREMENT

사용자 고유 ID (서비스 내부용)

social_id

VARCHAR(255)

UNIQUE, NOT NULL

소셜 로그인 제공자별 사용자 ID

social_provider

VARCHAR(50)

NOT NULL

소셜 로그인 제공자 ('kakao', 'naver', 'google')

nickname

VARCHAR(100)

NOT NULL

사용자 닉네임 (초기 소셜 프로필에서 가져옴)

email

VARCHAR(255)

UNIQUE, NULLABLE

소셜 프로필에서 제공된 이메일 (선택 사항)

unit_preference

VARCHAR(10)

DEFAULT 'sqm'

면적 단위 선호 설정 ('sqm' 또는 'pyeong')

created_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP

계정 생성 일시

updated_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

계정 정보 최종 수정 일시

2.1.2. regions 테이블 (지역 정보)
설명: 법정동 코드 기반의 지역 정보를 저장합니다. 국토부 API 연동 및 지역별 특성 데이터에 활용됩니다.

역할: 지역 기반 검색 필터링, 지역 개요 정보 제공.

컬럼명

데이터 타입

제약 조건

설명

id

BIGINT

PRIMARY KEY, AUTO_INCREMENT

지역 정보 고유 ID

lawd_cd

VARCHAR(5)

UNIQUE, NOT NULL

법정동 코드 앞 5자리 (예: 11110 - 서울 종로구)

sido_nm

VARCHAR(50)

NOT NULL

시/도 명칭 (예: 서울특별시)

sgg_nm

VARCHAR(50)

NOT NULL

시/군/구 명칭 (예: 종로구)

umd_nm

VARCHAR(50)

NULLABLE

읍/면/동 명칭 (법정동 코드 10자리까지 확장 시 사용)

characteristics

JSON 또는 TEXT

NULLABLE

주요 상권, 교통 환경, 학군, 인구 밀도, 개발 호재 등 지역 특성 요약 (JSON 형식 권장)

updated_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

정보 최종 갱신 일시

2.1.3. complexes 테이블 (아파트 단지 기본 정보)
설명: 아파트 단지의 고유 정보 및 정적인 특징을 저장합니다. (국토부 API에서 제공되지 않는 세대수, 주차, 용적률 등 포함)

역할: 단지 미리보기, 단지 상세 정보 제공, 비교 분석 시 기본 데이터.

컬럼명

데이터 타입

제약 조건

설명

id

BIGINT

PRIMARY KEY, AUTO_INCREMENT

단지 정보 고유 ID (서비스 내부용)

apt_seq

VARCHAR(20)

UNIQUE, NOT NULL

국토부 API의 단지 일련번호 (예: 11110-2339)

apt_nm

VARCHAR(100)

NOT NULL

단지명

lawd_cd

VARCHAR(5)

NOT NULL, FOREIGN KEY (regions.lawd_cd)

법정동 코드 (앞 5자리)

umd_nm

VARCHAR(60)

NOT NULL

법정동명 (API 응답 필드와 일치)

jibun

VARCHAR(20)

NULLABLE

지번

road_nm

VARCHAR(100)

NULLABLE

도로명

build_year

YEAR

NULLABLE

건축년도 (사용승인일)

total_households

INT

NULLABLE

총 세대수

total_parking_spaces

INT

NULLABLE

총 주차 대수

parking_per_household

DECIMAL(4,2)

NULLABLE

세대당 주차 대수 (계산 값)

floor_area_ratio

DECIMAL(5,2)

NULLABLE

용적률 (%)

building_to_land_ratio

DECIMAL(5,2)

NULLABLE

건폐율 (%)

developer

VARCHAR(100)

NULLABLE

건설사

heating_type

VARCHAR(50)

NULLABLE

난방방식 (예: '개별난방', '중앙난방', '지역난방')

management_office_contact

VARCHAR(50)

NULLABLE

관리사무소 연락처

key_summary

TEXT

NULLABLE

개별 매물 상세 분석 시 제공될 핵심 요약 텍스트

school_district_info

JSON 또는 TEXT

NULLABLE

학군 정보 (배정 학교, 선호도 등)

subway_station_info

JSON 또는 TEXT

NULLABLE

인근 지하철역 정보 (역명, 도보 시간 등)

updated_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

정보 최종 갱신 일시

2.1.4. property_transactions 테이블 (부동산 거래 상세 내역 캐싱)
설명: 국토부 아파트 매매/전월세 실거래가 API를 통해 수집된 원본 및 가공 데이터를 캐싱하여 저장합니다.

역할: 매물 검색, 단지 상세 정보, 시세 변동 추이, 알림 모니터링의 기본 데이터 소스.

데이터 갱신: 백엔드 배치 시스템을 통해 주기적으로 국토부 API를 호출하여 최신 데이터를 수집하고 업데이트합니다.

컬럼명

데이터 타입

제약 조건

설명

id

BIGINT

PRIMARY KEY, AUTO_INCREMENT

거래 내역 고유 ID

apt_seq

VARCHAR(20)

NOT NULL, FOREIGN KEY (complexes.apt_seq)

단지 일련번호

lawd_cd

VARCHAR(5)

NOT NULL, FOREIGN KEY (regions.lawd_cd)

법정동 코드 (앞 5자리)

exclusive_use_area

DECIMAL(10,3)

NOT NULL

전용면적 (㎡)

deal_amount

BIGINT

NOT NULL

거래금액 (만원 단위, 정수)

deal_year

YEAR

NOT NULL

계약년도

deal_month

TINYINT

NOT NULL

계약월

deal_day

TINYINT

NOT NULL

계약일

contract_date

DATE

NOT NULL

계약 일자 (YYYY-MM-DD 형식)

floor

SMALLINT

NULLABLE

층

transaction_type

VARCHAR(50)

NULLABLE

거래유형 (예: '중개거래', '직거래')

transaction_gbn

VARCHAR(10)

NOT NULL

거래 구분 ('매매', '전세', '월세')

sgg_cd

VARCHAR(5)

NULLABLE

법정동시군구코드

umd_cd

VARCHAR(5)

NULLABLE

법정동읍면동코드

umd_nm

VARCHAR(60)

NULLABLE

법정동명

jibun

VARCHAR(20)

NULLABLE

지번

build_year

YEAR

NULLABLE

건축년도

apt_dong

VARCHAR(400)

NULLABLE

아파트 동명

cdeal_type

VARCHAR(1)

NULLABLE

해제여부

cdeal_day

VARCHAR(8)

NULLABLE

해제사유발생일

dealing_gbn

VARCHAR(10)

NULLABLE

거래유형 (중개거래/직거래)

estate_agent_sgg_nm

VARCHAR(3000)

NULLABLE

중개사소재지

rgst_date

VARCHAR(8)

NULLABLE

등기일자

sler_gbn

VARCHAR(100)

NULLABLE

매도자 구분 (개인/법인/공공기관/기타)

buyer_gbn

VARCHAR(100)

NULLABLE

매수자 구분 (개인/법인/공공기관/기타)

land_leasehold_gbn

VARCHAR(1)

NULLABLE

토지임대부 아파트 여부 (Y/N)

road_nm

VARCHAR(100)

NULLABLE

도로명

road_nm_sgg_cd

VARCHAR(5)

NULLABLE

도로명시군구코드

road_nm_cd

VARCHAR(7)

NULLABLE

도로명코드

road_nm_seq

VARCHAR(2)

NULLABLE

도로명일련번호코드

road_nmb_cd

VARCHAR(1)

NULLABLE

도로명지상지하코드

road_nm_bonbun

VARCHAR(5)

NULLABLE

도로명건물본번호코드

road_nm_bubun

VARCHAR(5)

NULLABLE

도로명건물부번호코드

land_cd

VARCHAR(1)

NULLABLE

법정동지번코드

bonbun

VARCHAR(4)

NULLABLE

법정동본번코드

bubun

VARCHAR(4)

NULLABLE

법정동부번코드

created_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP

데이터 생성 일시 (수집 일시)

**참조**: apartment-sale-transaction-details-tech-doc.md의 응답 메시지 명세와 완전히 일치하도록 설계됨

updated_at

DATETIME

NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

데이터 최종 수정 일시

2.2. MySQL 인덱스 전략
users: social_id (UNIQUE), email (UNIQUE)

regions: lawd_cd (UNIQUE)

complexes: apt_seq (UNIQUE), lawd_cd (FK), apt_nm

property_transactions:

(apt_seq, exclusive_use_area, contract_date, transaction_gbn): 특정 단지/면적의 시계열 거래 내역 조회에 필수.

(lawd_cd, deal_year, deal_month, transaction_gbn): 지역별 월별 거래량/평균가 집계에 필수.

(contract_date): 최신 거래 내역 조회 및 기간별 필터링.

2.3. MySQL 관계도 (Conceptual)
+-------+       +---------+       +-----------+       +---------------------+
| users |-----< | regions |-----< | complexes |-----< | property_transactions |
+-------+       +---------+       +-----------+       +---------------------+
  ^               ^                   ^                   ^
  |               |                   |                   |
  | (user_id)     | (lawd_cd)         | (apt_seq)         | (apt_seq, lawd_cd)
  |               |                   |                   |
  |               |                   |                   |
  v               v                   v                   v
MongoDB (user_sheets, notification_settings, price_snapshots)

users.id <-> user_sheets.user_id, notification_settings.user_id

regions.lawd_cd <-> complexes.lawd_cd, property_transactions.lawd_cd

complexes.apt_seq <-> property_transactions.apt_seq, user_sheets.properties.apt_seq, price_snapshots.apt_seq

3. MongoDB 데이터베이스 설계 (NoSQL 데이터)
3.1. 컬렉션 목록 및 스키마
3.1.1. user_sheets 컬렉션 (사용자 개인화 매물 시트)
설명: 각 사용자가 '나만의 시트'에 추가한 매물 목록을 저장합니다. 사용자 정의 컬럼과 태그를 포함할 수 있도록 유연한 문서 구조를 가집니다.

역할: 사용자별 맞춤형 매물 관리, 비교 분석 대상 데이터.

필드명

데이터 타입

제약 조건

설명

_id

ObjectId

PRIMARY KEY

MongoDB 문서 고유 ID

user_id

String

UNIQUE, NOT NULL

MySQL users.id 참조 (사용자 고유 ID)

properties

Array of Object

NULLABLE

사용자가 시트에 추가한 매물 목록

properties.sheet_property_id

String

UNIQUE (within array)

시트 내 매물 항목 고유 ID (UUID 등)

properties.apt_seq

String

NOT NULL

단지 일련번호 (MySQL complexes.apt_seq 참조)

properties.apt_nm

String

NOT NULL

단지명

properties.exclusive_use_area

Decimal128

NOT NULL

전용면적 (㎡)

properties.address_display

String

NOT NULL

표시용 전체 주소 (예: 서울 종로구 숭인동 종로중흥S클래스)

properties.latest_deal_amount

Double

NOT NULL

최신 실거래가 (만원)

properties.latest_jeonse_amount

Double

NULLABLE

최신 전세가 (만원)

properties.build_year

Int32

NULLABLE

건축년도

properties.total_households

Int32

NULLABLE

총 세대수

properties.my_memo

String

NULLABLE

'나만의 메모'

properties.tags

Array of String

NULLABLE

사용자 정의 태그 (예: ["급매", "역세권"])

properties.user_defined_columns

Object

NULLABLE

사용자 정의 컬럼 (유연한 스키마)

properties.added_at

Date

NOT NULL

시트에 추가된 일시

properties.updated_at

Date

NOT NULL

시트 내 해당 항목 최종 수정 일시

created_at

Date

NOT NULL

문서 생성 일시

updated_at

Date

NOT NULL

문서 최종 수정 일시

3.1.2. notification_settings 컬렉션 (사용자 알림 설정)
설명: 각 사용자의 알림 설정 및 푸시 토큰 정보를 저장합니다.

역할: 개인화된 알림 발송 조건 관리.

필드명

데이터 타입

제약 조건

설명

_id

ObjectId

PRIMARY KEY

MongoDB 문서 고유 ID

user_id

String

UNIQUE, NOT NULL

MySQL users.id 참조 (사용자 고유 ID)

price_change_alert_enabled

Boolean

DEFAULT false

가격 변동 알림 활성화 여부

price_change_threshold

Double

NULLABLE

가격 변동률 임계치 (예: 5.0 for 5%)

new_transaction_alert_enabled

Boolean

DEFAULT false

신규 실거래가 알림 활성화 여부

custom_condition_alert_enabled

Boolean

DEFAULT false

맞춤 조건 매물 알림 활성화 여부

custom_alert_conditions

Object

NULLABLE

맞춤 알림 필터 조건 (예: { lawd_cd: "11110", min_area: 80, max_price: 100000 })

web_push_token

String

NULLABLE

웹 푸시 알림 토큰 (FCM 토큰)

app_push_token

String

NULLABLE

앱 푸시 알림 토큰 (FCM 토큰)

updated_at

Date

NOT NULL

설정 최종 수정 일시

3.1.3. price_snapshots 컬렉션 (알림 모니터링용 가격 스냅샷)
설명: 알림 발송을 위한 가격 변동 감지를 위해 특정 단지/면적의 일별/주기별 가격 및 거래량 스냅샷을 저장합니다. (3개월 보관 후 삭제)

역할: 알림 백엔드 시스템의 변경 감지 로직에 활용.

필드명

데이터 타입

제약 조건

설명

_id

ObjectId

PRIMARY KEY

MongoDB 문서 고유 ID

apt_seq

String

NOT NULL

단지 일련번호 (MySQL complexes.apt_seq 참조)

exclusive_use_area

Decimal128

NOT NULL

전용면적 (㎡)

snapshot_date

Date

NOT NULL

스냅샷 생성 일시 (예: 매일 자정)

average_deal_amount

Double

NULLABLE

해당 시점의 평균 매매 거래금액 (만원)

average_jeonse_amount

Double

NULLABLE

해당 시점의 평균 전세 거래금액 (만원)

transaction_count

Int32

NULLABLE

해당 시점의 거래 건수

created_at

Date

NOT NULL

문서 생성 일시

3.2. MongoDB 인덱스 전략
user_sheets: user_id (UNIQUE), properties.apt_seq (sparse index for embedded array elements)

notification_settings: user_id (UNIQUE)

price_snapshots: (apt_seq, exclusive_use_area, snapshot_date) (복합 인덱스, 변경 감지 쿼리 최적화)

4. 데이터베이스 설계의 주요 고려사항
4.1. 데이터 동기화 및 일관성
국토부 API -> MySQL:

백엔드 배치 시스템이 국토부 API를 주기적(예: 매일 새벽 2시)으로 호출하여 최신 실거래가 데이터를 수집합니다.

수집된 데이터는 정제 및 가공(콤마 제거, 단위 통일, 날짜 형식 변환 등) 과정을 거쳐 property_transactions 테이블에 삽입 또는 업데이트됩니다.

complexes 테이블의 '대표 면적', '최저/최고 실거래가 범위' 등은 property_transactions 데이터를 기반으로 주기적으로 집계하여 업데이트됩니다.

MySQL -> MongoDB (사용자 데이터 관련):

사용자가 '시트에 추가' 기능을 통해 매물을 추가할 때, MySQL의 complexes 및 property_transactions 테이블에서 필요한 정보를 조회하여 MongoDB의 user_sheets 컬렉션에 저장합니다.

MySQL의 마스터 데이터(예: complexes의 총 세대수, 주차 정보)가 변경될 경우, 이를 MongoDB의 user_sheets 내 properties 문서에 반영하는 배치 또는 이벤트 기반 동기화 로직을 고려해야 합니다. (예: MySQL Change Data Capture (CDC) -> Kafka -> MongoDB 업데이트)

MongoDB (알림 스냅샷):

알림 백엔드 시스템이 MySQL의 property_transactions 데이터를 기반으로 일별/주기별 가격 스냅샷을 생성하여 price_snapshots 컬렉션에 저장합니다.

이 스냅샷은 알림 변경 감지에만 사용되며, 3개월 후 자동으로 삭제되도록 TTL(Time-To-Live) 인덱스를 설정하거나 배치 작업을 통해 관리합니다.

4.2. 보안
데이터 암호화: 민감한 정보(예: 푸시 토큰)는 저장 시 암호화하고, 데이터 전송 시에는 HTTPS/SSL을 적용하여 통신 보안을 강화합니다.

접근 제어: 데이터베이스 사용자 계정은 최소 권한 원칙(Least Privilege)에 따라 필요한 권한만 부여합니다.

AWS Secrets Manager: API 키, 데이터베이스 인증 정보 등 민감한 자격 증명은 AWS Secrets Manager를 통해 안전하게 관리하고 애플리케이션에 주입합니다.

4.3. 확장성 (Scalability)
MySQL:

읽기 확장: AWS RDS Read Replicas를 사용하여 읽기 트래픽을 분산합니다.

쓰기 확장/수평 확장: 장기적으로 데이터 볼륨이 매우 커질 경우, 샤딩(Sharding) 전략을 고려할 수 있습니다.

MongoDB:

수평 확장: MongoDB Atlas와 같은 관리형 서비스는 샤딩을 통해 손쉽게 수평 확장을 지원합니다. user_sheets 컬렉션은 user_id를 샤드 키로 고려하여 사용자별 데이터 분산을 최적화할 수 있습니다.

실시간 동기화: MongoDB Change Streams는 실시간 데이터 변경을 감지하여 알림 시스템 등 후속 로직을 트리거하는 데 활용됩니다.

4.4. 백업 및 복구
정기 백업: AWS RDS 및 MongoDB Atlas의 자동 백업 기능을 활용하여 정기적인 데이터 백업을 설정합니다.

복구 전략: 특정 시점 복구(Point-in-Time Recovery) 기능을 활성화하여 데이터 유실 시 복구 시간을 최소화합니다.

재해 복구: Multi-AZ 또는 Multi-Region 배포를 고려하여 지역적 재해 발생 시 서비스 연속성을 확보합니다.

4.5. 성능 최적화
인덱스: 각 테이블/컬렉션의 쿼리 패턴을 분석하여 적절한 인덱스를 생성하고 주기적으로 최적화합니다.

캐싱: MySQL에 국토부 API 데이터를 미리 캐싱하고, 필요시 Redis와 같은 인메모리 캐시를 활용하여 자주 조회되는 데이터를 빠르게 제공합니다.

쿼리 최적화: 복잡한 쿼리는 성능 프로파일링을 통해 병목 현상을 식별하고 최적화합니다.