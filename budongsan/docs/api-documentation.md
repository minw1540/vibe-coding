🏡 나만의 스마트 부동산 시트 웹/앱 서비스 API 명세서 🏡
본 문서는 '나만의 스마트 부동산 시트' 웹/앱 서비스의 API를 상세하게 정의합니다. 백엔드와 프론트엔드 간의 통신 규약, 요청 및 응답 형식, 인증 방식 등을 명세하여 개발팀의 이해를 돕고 협업 효율성을 극대화합니다.

1. 개요
목적: 서비스의 프론트엔드(웹/앱)와 백엔드 간의 데이터 교환 및 기능 호출을 위한 인터페이스를 정의합니다.

API 버전: v1

Base URL: https://api.yourdomain.com/v1 (예시)

인증: 모든 사용자 인증이 필요한 API는 JWT(JSON Web Token) 기반의 Bearer Token 방식을 사용합니다.

요청 헤더: Authorization: Bearer <access_token>

데이터 형식: 모든 요청 및 응답은 JSON 형식을 따릅니다.

공통 응답 구조:

성공 응답:

{
  "status": "success",
  "message": "요청이 성공적으로 처리되었습니다.",
  "data": {
    // API별 응답 데이터
  }
}

오류 응답:

{
  "status": "error",
  "message": "오류가 발생했습니다.",
  "code": "ERROR_CODE_001", // 백엔드 내부 정의 에러 코드
  "details": "오류에 대한 추가 상세 정보"
}

주요 오류 코드 예시:

AUTH_001: 인증 실패 (유효하지 않은 토큰)

AUTH_002: 권한 없음 (접근 권한 부족)

VALIDATION_001: 요청 파라미터 유효성 검증 실패

NOT_FOUND_001: 리소스를 찾을 수 없음

SERVER_ERROR_001: 서버 내부 오류

2. 인증 (Authentication) API
2.1. 소셜 로그인 시작 (POST)
엔드포인트: /auth/social/login

메서드: POST

인증: 불필요

설명: 프론트엔드에서 소셜 인증 후 받은 인가 코드(Auth Code)를 백엔드로 전송하여 로그인/회원가입 및 JWT를 발급받습니다.

요청 바디 (Request Body):

{
  "provider": "kakao", // 'kakao', 'naver', 'google'
  "code": "AQAB..." // 소셜 로그인 제공자로부터 받은 인가 코드 (Authorization Code)
}

provider: string, 필수, 소셜 로그인 제공자 이름.

code: string, 필수, 소셜 로그인 제공자로부터 발급받은 인가 코드.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "로그인 성공",
  "data": {
    "accessToken": "eyJ...", // 서비스 접근용 JWT
    "refreshToken": "eyJ...", // Access Token 갱신용 JWT
    "userId": "user_12345",
    "nickname": "스마트_부동산_유저",
    "email": "user@example.com" // 소셜에서 제공된 경우
  }
}

3. 사용자 관리 (User Management) API
3.1. 내 프로필 조회 (GET)
엔드포인트: /users/me

메서드: GET

인증: 필요

설명: 현재 로그인된 사용자의 프로필 정보를 조회합니다.

요청 파라미터: 없음

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "프로필 조회 성공",
  "data": {
    "userId": "user_12345",
    "nickname": "스마트_부동산_유저",
    "email": "user@example.com",
    "unitPreference": "sqm", // 'sqm' 또는 'pyeong'
    "createdAt": "2024-01-01T10:00:00Z"
  }
}

3.2. 사용자 선호 설정 업데이트 (PUT)
엔드포인트: /users/me/preferences

메서드: PUT

인증: 필요

설명: 사용자의 서비스 선호 설정(예: 면적 단위)을 업데이트합니다.

요청 바디 (Request Body):

{
  "unitPreference": "pyeong" // 'sqm' 또는 'pyeong'
}

unitPreference: string, 필수, 업데이트할 면적 단위 선호 설정.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "사용자 선호 설정이 업데이트되었습니다.",
  "data": null
}

3.3. 회원 탈퇴 (DELETE)
엔드포인트: /users/me

메서드: DELETE

인증: 필요

설명: 현재 로그인된 사용자의 계정을 탈퇴하고 모든 개인 데이터를 삭제합니다.

요청 파라미터: 없음

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "회원 탈퇴가 성공적으로 처리되었습니다.",
  "data": null
}

4. 매물 검색 및 상세 정보 (Property Search & Detail) API
4.1. 단지 목록 검색 (GET)
엔드포인트: /properties/search

메서드: GET

인증: 선택 사항 (비로그인 사용자도 검색 가능)

설명: 지역 코드 또는 주소 키워드와 필터 조건을 기반으로 아파트 단지 목록을 검색합니다.

요청 쿼리 파라미터 (Request Query Parameters):

lawdCd: string, 법정동 코드 (앞 5자리, addressKeyword와 택 1). 예: 11110

addressKeyword: string, 주소 키워드 (단지명, 도로명 등, lawdCd와 택 1). 예: 종로중흥S클래스

dealYm: string, 조회 기준 계약년월 (YYYYMM, 백엔드에서 1년치 데이터로 확장). 예: 202407

minPrice: number, 최소 가격 (만원). 예: 50000

maxPrice: number, 최대 가격 (만원). 예: 100000

minArea: number, 최소 전용면적 (㎡). 예: 60

maxArea: number, 최대 전용면적 (㎡). 예: 85

minBuildYear: number, 최소 건축년도. 예: 2000

maxBuildYear: number, 최대 건축년도. 예: 2020

minHouseholds: number, 최소 세대수. 예: 500

maxHouseholds: number, 최대 세대수. 예: 2000

heatingType: string, 난방방식 (콤마로 구분). 예: 개별난방,중앙난방

page: number, 페이지 번호 (기본값: 1).

limit: number, 한 페이지 결과 수 (기본값: 10).

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "단지 목록 조회 성공",
  "data": {
    "totalCount": 12345,
    "currentPage": 1,
    "limit": 10,
    "complexes": [
      {
        "aptSeq": "11110-2339",
        "aptNm": "종로중흥S클래스",
        "addressDisplay": "서울 종로구 숭인동",
        "representativeAreaSqm": 84.99, // ㎡
        "representativeAreaPyeong": 25.71, // 평 (클라이언트 변환)
        "minDealAmount": 95000, // 만원
        "maxDealAmount": 120000, // 만원
        "totalHouseholds": 800,
        "buildYear": 2013,
        "developer": "중흥건설"
      }
    ]
  }
}

4.2. 단지 상세 정보 조회 (GET)
엔드포인트: /properties/complexes/{aptSeq}

메서드: GET

인증: 선택 사항

설명: 특정 아파트 단지의 상세 정보 및 면적별 최신 거래 정보를 조회합니다.

요청 경로 파라미터 (Request Path Parameters):

aptSeq: string, 필수, 단지 일련번호 (예: 11110-2339).

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "단지 상세 정보 조회 성공",
  "data": {
    "aptSeq": "11110-2339",
    "aptNm": "종로중흥S클래스",
    "addressDisplay": "서울 종로구 숭인동 202-3",
    "totalHouseholds": 800,
    "buildYear": 2013,
    "floorAreaRatio": 250.50, // 용적률
    "buildingToLandRatio": 20.10, // 건폐율
    "developer": "중흥건설",
    "heatingType": "개별난방",
    "managementOfficeContact": "02-1234-5678",
    "parkingPerHousehold": 1.25, // 세대당 주차 대수
    "unitTypes": [ // 면적별 정보
      {
        "exclusiveUseAreaSqm": 59.87, // ㎡
        "exclusiveUseAreaPyeong": 18.11, // 평 (클라이언트 변환)
        "latestDealAmount": 75000, // 만원
        "latestJeonseAmount": 45000, // 만원 (전세가 API 연동)
        "jeonseToSaleRatio": 60.00, // 전세가율 (%)
        "latestDealDate": "2024-06-25",
        "totalTransactionsLastYear": 15 // 최근 1년간 해당 면적 거래량
      },
      {
        "exclusiveUseAreaSqm": 84.99,
        "exclusiveUseAreaPyeong": 25.71,
        "latestDealAmount": 120000,
        "latestJeonseAmount": 70000,
        "jeonseToSaleRatio": 58.33,
        "latestDealDate": "2024-07-23",
        "totalTransactionsLastYear": 25
      }
    ],
    "schoolDistrictInfo": "OO초등학교, △△중학교 배정 가능",
    "subwayStationInfo": "종로3가역 (도보 5분)"
  }
}

4.3. 개별 매물 시세 변동 내역 조회 (GET)
엔드포인트: /properties/complexes/{aptSeq}/units/{exclusiveUseArea}/transactions

메서드: GET

인증: 선택 사항

설명: 특정 단지의 특정 면적에 대한 과거 매매 및 전세 거래 내역을 조회합니다.

요청 경로 파라미터 (Request Path Parameters):

aptSeq: string, 필수, 단지 일련번호.

exclusiveUseArea: number, 필수, 전용면적 (㎡).

요청 쿼리 파라미터 (Request Query Parameters):

startDate: string, 조회 시작일 (YYYY-MM-DD). 기본값: 1년 전.

endDate: string, 조회 종료일 (YYYY-MM-DD). 기본값: 오늘.

transactionGbn: string, 거래 구분 (콤마로 구분). 예: 매매,전세. 기본값: 매매.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "시세 변동 내역 조회 성공",
  "data": {
    "monthlyData": [ // 월별 집계 데이터 (그래프/테이블용)
      {
        "month": "2023-08",
        "avgDealAmount": 105000, // 만원
        "avgJeonseAmount": 60000, // 만원
        "jeonseToSaleRatio": 57.14,
        "transactionCount": 5
      },
      {
        "month": "2023-09",
        "avgDealAmount": 107000,
        "avgJeonseAmount": 61000,
        "jeonseToSaleRatio": 57.01,
        "transactionCount": 7
      }
      // ...
    ],
    "rawTransactions": [ // 상세 거래 내역 (테이블용)
      {
        "dealDate": "2024-07-23",
        "dealAmount": 120000,
        "floor": 10,
        "transactionGbn": "매매",
        "transactionType": "중개거래"
      },
      {
        "dealDate": "2024-07-01",
        "dealAmount": 70000,
        "floor": 5,
        "transactionGbn": "전세",
        "transactionType": "중개거래"
      }
      // ...
    ]
  }
}

5. 개인화된 시트 (Personalized Sheet) API
5.1. 내 시트 조회 (GET)
엔드포인트: /users/me/sheet

메서드: GET

인증: 필요

설명: 현재 로그인된 사용자의 개인화된 매물 시트 목록을 조회합니다.

요청 파라미터: 없음

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "내 시트 조회 성공",
  "data": {
    "properties": [
      {
        "sheetPropertyId": "sheet_prop_abc123", // 시트 내 항목 고유 ID
        "aptSeq": "11110-2339",
        "aptNm": "종로중흥S클래스",
        "exclusiveUseAreaSqm": 84.99, // ㎡
        "exclusiveUseAreaPyeong": 25.71, // 평 (클라이언트 변환)
        "addressDisplay": "서울 종로구 숭인동",
        "latestDealAmount": 120000,
        "latestJeonseAmount": 70000,
        "buildYear": 2013,
        "totalHouseholds": 800,
        "myMemo": "남향, 학군 좋음",
        "tags": ["실거주", "역세권"],
        "userDefinedColumns": { // 사용자 정의 컬럼
          "개인점수": 4.5,
          "대출가능액": 50000 // 만원
        },
        "addedAt": "2024-07-01T15:30:00Z",
        "updatedAt": "2024-07-09T11:20:00Z"
      }
      // ...
    ]
  }
}

5.2. 시트에 매물 추가 (POST)
엔드포인트: /users/me/sheet

메서드: POST

인증: 필요

설명: 선택한 매물 정보를 사용자의 시트에 추가합니다.

요청 바디 (Request Body):

{
  "aptSeq": "11110-2339",
  "exclusiveUseAreaSqm": 84.99,
  "aptNm": "종로중흥S클래스",
  "addressDisplay": "서울 종로구 숭인동 202-3",
  "latestDealAmount": 120000,
  "latestJeonseAmount": 70000,
  "buildYear": 2013,
  "totalHouseholds": 800,
  "myMemo": "",
  "tags": [],
  "userDefinedColumns": {}
}

aptSeq: string, 필수.

exclusiveUseAreaSqm: number, 필수.

나머지 필드는 5.1. 내 시트 조회 응답의 properties 객체와 동일한 구조.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "매물이 시트에 추가되었습니다.",
  "data": {
    "sheetPropertyId": "sheet_prop_abc123" // 새로 추가된 항목의 고유 ID
  }
}

5.3. 시트 매물 정보 업데이트 (PUT)
엔드포인트: /users/me/sheet/{sheetPropertyId}

메서드: PUT

인증: 필요

설명: 시트 내 특정 매물의 '나만의 메모', 태그, 사용자 정의 컬럼 정보를 업데이트합니다.

요청 경로 파라미터 (Request Path Parameters):

sheetPropertyId: string, 필수, 업데이트할 시트 항목의 고유 ID.

요청 바디 (Request Body - 부분 업데이트 가능):

{
  "myMemo": "역세권, 재건축 잠재력 높음",
  "tags": ["투자", "재건축"],
  "userDefinedColumns": {
    "개인점수": 5.0
  }
}

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "시트 매물 정보가 업데이트되었습니다.",
  "data": null
}

5.4. 시트 매물 삭제 (DELETE)
엔드포인트: /users/me/sheet/{sheetPropertyId}

메서드: DELETE

인증: 필요

설명: 시트에서 특정 매물 항목을 삭제합니다.

요청 경로 파라미터 (Request Path Parameters):

sheetPropertyId: string, 필수, 삭제할 시트 항목의 고유 ID.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "시트 매물이 삭제되었습니다.",
  "data": null
}

5.5. 매물 비교 분석 리포트 생성 (POST)
엔드포인트: /users/me/sheet/compare

메서드: POST

인증: 필요

설명: 시트 내 선택된 여러 매물 간의 비교 분석 리포트를 생성합니다.

요청 바디 (Request Body):

{
  "sheetPropertyIds": ["sheet_prop_abc123", "sheet_prop_def456"] // 비교할 시트 항목 ID 목록 (최소 2개)
}

sheetPropertyIds: Array<string>, 필수, 비교할 시트 항목 ID 목록.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "매물 비교 리포트 생성 성공",
  "data": {
    "summaryText": "선택하신 두 매물은 면적은 유사하나, A매물은 최근 1년간 5% 상승, B매물은 2% 하락했습니다. A매물이 더 역세권에 위치합니다.",
    "comparisonPoints": [
      {
        "category": "가격 변동성",
        "itemA": "최근 1년 +5%",
        "itemB": "최근 1년 -2%",
        "analysis": "매물 A가 더 긍정적인 가격 흐름을 보임."
      },
      {
        "category": "세대당 주차",
        "itemA": "1.25대",
        "itemB": "1.01대",
        "analysis": "매물 A의 주차 환경이 더 여유로움."
      }
      // ... 기타 비교 항목
    ],
    "metricsForChart": { // 차트 생성을 위한 데이터
        "priceChangeRate": {
            "itemA": 5,
            "itemB": -2
        },
        "pyeongdangPrice": {
            "itemA": 3000,
            "itemB": 2800
        }
    }
  }
}

6. 알림 (Notification) API
6.1. 알림 설정 업데이트 (PUT)
엔드포인트: /users/me/notifications

메서드: PUT

인증: 필요

설명: 사용자의 알림 수신 설정을 업데이트합니다.

요청 바디 (Request Body):

{
  "priceChangeAlertEnabled": true,
  "priceChangeThreshold": 5.0, // 5%
  "newTransactionAlertEnabled": false,
  "customConditionAlertEnabled": true,
  "customAlertConditions": {
    "lawdCd": "11230",
    "minArea": 80,
    "maxPrice": 90000
  },
  "webPushToken": "fcm_token_web_...", // 웹 푸시 토큰 (업데이트 시 포함)
  "appPushToken": "fcm_token_app_..."  // 앱 푸시 토큰 (업데이트 시 포함)
}

각 필드는 boolean 또는 number/object/string 타입이며, notification_settings 컬렉션의 스키마와 일치합니다.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "알림 설정이 업데이트되었습니다.",
  "data": null
}

6.2. 푸시 토큰 등록/업데이트 (POST)
엔드포인트: /users/me/push-token

메서드: POST

인증: 필요

설명: 디바이스/브라우저의 푸시 알림 토큰을 서버에 등록하거나 업데이트합니다.

요청 바디 (Request Body):

{
  "token": "fcm_device_token_string", // FCM 발급 토큰
  "deviceType": "web" // 'web' 또는 'app'
}

token: string, 필수.

deviceType: string, 필수.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "푸시 토큰이 성공적으로 등록/업데이트되었습니다.",
  "data": null
}

6.3. 푸시 토큰 등록 해제 (DELETE)
엔드포인트: /users/me/push-token/{token}

메서드: DELETE

인증: 필요

설명: 특정 푸시 알림 토큰을 서버에서 제거합니다.

요청 경로 파라미터 (Request Path Parameters):

token: string, 필수, 해제할 FCM 토큰.

응답 바디 (Response Body - 성공):

{
  "status": "success",
  "message": "푸시 토큰이 성공적으로 해제되었습니다.",
  "data": null
}

7. 백엔드에서 활용하는 외부 API (External API Consumption by Backend)
이 섹션은 백엔드 서비스가 데이터를 수집하고 기능을 구현하기 위해 사용하는 외부 API에 대한 설명입니다. 프론트엔드에서 직접 호출하는 API가 아닙니다.

7.1. 국토교통부 아파트 매매 실거래가 상세 자료 API
API명: getRTMSDataSvcAptTradeDev

[cite_start]서비스 URL: http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev [cite: 1]

**※ 국토부 공식 API 정보 (2024.07.17 기준)**:
- 정식 API명: 아파트 매매 실거래가 상세 자료 (Detailed data on actual apartment sales prices)
- 서비스 URL: http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev
- 서비스 버전: 1.0
- 최대 TPS: 30
- 평균 응답시간: 500ms
- 일일 갱신 주기: 1회
- 인증 방식: Service Key (URL Encode 필수)

**요청 파라미터 (참조: apartment-sale-transaction-details-tech-doc.md)**:
- serviceKey (필수): 공공데이터포털 발급 인증키 (URL 인코딩 필요)
- LAWD_CD (필수): 법정동코드 5자리 (예: 11110)
- DEAL_YMD (필수): 계약년월 6자리 (예: 202407)
- pageNo (선택): 페이지번호 (기본값: 1)
- numOfRows (선택): 페이지당 결과수 (기본값: 10)

**주요 응답 필드**:
- 기본 정보: aptNm(단지명), aptSeq(단지일련번호), sggCd(시군구코드), umdNm(법정동)
- 거래 정보: dealAmount(거래금액), dealYear/Month/Day(계약일), excluUseAr(전용면적)
- 부가 정보: floor(층), buildYear(건축년도), dealingGbn(거래유형), estateAgentSggNm(중개사소재지)
- 매도자/매수자: slerGbn(매도자), buyerGbn(매수자) - 개인/법인/공공기관/기타 구분

[cite_start]요청 파라미터: serviceKey, LAWD_CD, DEAL_YMD, pageNo, numOfRows [cite: 1]

활용: property_transactions 테이블에 매매 실거래 데이터를 주기적으로 수집 및 캐싱합니다.

7.2. 국토교통부 아파트 전월세 실거래가 상세 자료 API
API명: getRTMSDataSvcAptTradeDev (※ 매매 API와 유사한 구조일 것으로 예상, 정확한 API 명세 확인 필요)

서비스 URL: (국토부 공식 문서 확인 후 업데이트 필요)

요청 파라미터: serviceKey, LAWD_CD, DEAL_YMD, pageNo, numOfRows (예상)

활용: property_transactions 테이블에 전세/월세 실거래 데이터를 주기적으로 수집 및 캐싱합니다.

7.3. 공공데이터포털 주소-법정동 코드 변환 API
API명: (정확한 API 명세 확인 필요)

서비스 URL: (공공데이터포털 확인 후 업데이트 필요)

요청 파라미터: 주소 문자열

활용: 사용자의 주소 입력 시 LAWD_CD를 조회하여 검색에 활용합니다.

7.4. 소셜 로그인 제공자별 OAuth API
제공자: Kakao, Naver, Google

활용: 소셜 로그인 과정에서 인가 코드(Authorization Code)를 통해 Access Token을 획득하고 사용자 프로필 정보를 조회합니다.

7.5. Firebase Cloud Messaging (FCM) Send API
서비스 URL: https://fcm.googleapis.com/fcm/send

활용: 백엔드에서 사용자 디바이스의 푸시 토큰을 이용하여 웹 및 앱 푸시 알림 메시지를 발송합니다.