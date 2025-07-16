🏡 나만의 스마트 부동산 시트 웹/앱 서비스 프로젝트 구조 정의서 🏡
본 문서는 '나만의 스마트 부동산 시트' 웹/앱 서비스의 프로젝트 폴더 구조 및 코드 조직 방법을 정의합니다. 일관된 구조는 개발 효율성을 높이고, 코드의 가독성을 향상시키며, 장기적인 유지보수와 확장에 필수적입니다. 웹(Next.js), 모바일 앱(React Native), 백엔드(Node.js/Express) 간의 코드 공유 및 분리를 고려한 모노레포(Monorepo) 구조를 기반으로 설계합니다.

1. 개요
프로젝트는 **yarn workspaces**와 같은 워크스페이스 관리 도구를 활용하여 하나의 리포지토리 안에서 여러 개의 패키지(웹, 앱, 백엔드, 공통 유틸리티)를 관리하는 모노레포 형태로 구성됩니다. 이는 코드 재사용성을 극대화하고 의존성 관리를 용이하게 합니다.

2. 전체 프로젝트 최상위 구조 (Monorepo Root)
smart-real-estate/
├── apps/
│   ├── web/                     # Next.js 웹 프론트엔드 애플리케이션
│   └── mobile/                  # React Native 모바일 앱 애플리케이션
├── packages/
│   ├── backend/                 # Node.js/Express 백엔드 서비스
│   ├── common-ui/               # 웹/앱 공통 UI 컴포넌트 (선택 사항, 필요시)
│   ├── common-utils/            # 웹/앱/백엔드 공통 유틸리티 함수
│   └── types/                   # 웹/앱/백엔드 공통 TypeScript 타입 정의
├── .env.example                 # 환경 변수 예시 파일 (모든 프로젝트 공통 환경 변수)
├── .gitignore                   # Git 무시 파일
├── package.json                 # 워크스페이스 정의 및 스크립트
├── yarn.lock                    # Yarn 워크스페이스 설정 및 의존성 잠금 파일
└── README.md                    # 프로젝트 설명 문서

apps/: 최종 사용자에게 제공되는 애플리케이션(웹, 모바일 앱)을 포함합니다.

packages/: 여러 애플리케이션에서 공유되거나 독립적인 서비스(백엔드)를 포함합니다.

3. apps/web (Next.js 웹 프론트엔드)
웹 애플리케이션의 코드와 자산을 관리합니다.

smart-real-estate/apps/web/
├── public/                      # 정적 자산 (이미지, 폰트 등)
├── src/
│   ├── app/                     # Next.js 13+ App Router 구조 (또는 pages/ for Pages Router)
│   │   ├── (auth)/              # 인증 관련 라우트 그룹 (예: /login)
│   │   │   └── login/
│   │   │       └── page.tsx
│   │   ├── (main)/              # 메인 서비스 라우트 그룹
│   │   │   ├── search/          # 매물 검색 페이지
│   │   │   │   └── page.tsx
│   │   │   ├── properties/
│   │   │   │   ├── [aptSeq]/    # 단지 상세 페이지
│   │   │   │   │   └── page.tsx
│   │   │   │   └── [aptSeq]/units/[exclusiveUseArea]/transactions/ # 개별 매물 상세 분석
│   │   │   │       └── page.tsx
│   │   │   ├── my-sheet/        # 나만의 시트 페이지
│   │   │   │   └── page.tsx
│   │   │   ├── settings/        # 알림 설정 페이지
│   │   │   │   └── page.tsx
│   │   │   └── mypage/          # 마이페이지
│   │   │       └── page.tsx
│   │   ├── api/                 # Next.js API Routes (백엔드와 통신하는 프록시 또는 경량 API)
│   │   │   └── auth/
│   │   │       └── social.ts
│   │   ├── components/          # 재사용 가능한 UI 컴포넌트
│   │   │   ├── common/          # 전역적으로 사용되는 컴포넌트 (Header, Footer 등)
│   │   │   ├── search/          # 검색 페이지 전용 컴포넌트 (필터 UI 등)
│   │   │   ├── sheet/           # 시트 페이지 전용 컴포넌트 (테이블 행, 컬럼 추가 모달 등)
│   │   │   └── ...
│   │   ├── hooks/               # 커스텀 React Hooks
│   │   ├── lib/                 # 클라이언트 측 유틸리티 함수 및 설정 (API 클라이언트, 상수 등)
│   │   │   ├── api-client.ts    # 백엔드 API 호출 클라이언트
│   │   │   ├── constants.ts     # 웹 전용 상수
│   │   │   └── utils.ts         # 웹 전용 유틸리티 함수 (일반적인 순수 함수)
│   │   ├── styles/              # 전역 스타일 및 Tailwind CSS 설정
│   │   │   ├── globals.css
│   │   │   └── tailwind.config.js
│   │   ├── store/               # Zustand 스토어 정의
│   │   │   └── useAppStore.ts
│   │   └── types/               # 웹 전용 TypeScript 타입 정의 (공통 타입은 `packages/types` 참조)
├── .env.local                   # 로컬 환경 변수
├── next.config.js               # Next.js 설정
├── package.json                 # 웹 프로젝트 의존성 및 스크립트
├── tsconfig.json                # TypeScript 설정
└── README.md

4. apps/mobile (React Native 모바일 앱 프론트엔드)
모바일 앱의 코드와 자산을 관리합니다.

smart-real-estate/apps/mobile/
├── assets/                      # 앱 내 사용되는 이미지, 폰트 등 정적 자산
├── src/
│   ├── components/              # 재사용 가능한 UI 컴포넌트
│   │   ├── common/              # 전역적으로 사용되는 컴포넌트 (Header, LoadingIndicator 등)
│   │   ├── search/              # 검색 화면 전용 컴포넌트
│   │   └── ...
│   ├── screens/                 # 페이지 단위 컴포넌트
│   │   ├── AuthScreen.tsx       # 로그인/회원가입 화면
│   │   ├── SearchScreen.tsx     # 매물 검색 화면
│   │   ├── PropertyDetailScreen.tsx # 단지 상세 화면
│   │   ├── MySheetScreen.tsx    # 나만의 시트 화면
│   │   ├── NotificationSettingsScreen.tsx # 알림 설정 화면
│   │   └── MyPageScreen.tsx     # 마이페이지 화면
│   ├── navigation/              # React Navigation 설정 (Stack, Tab Navigator 등)
│   │   ├── AppNavigator.tsx
│   │   └── AuthNavigator.tsx
│   ├── hooks/                   # 커스텀 React Hooks
│   ├── lib/                     # 앱 측 유틸리티 함수 및 설정 (API 클라이언트, 상수 등)
│   │   ├── api-client.ts        # 백엔드 API 호출 클라이언트
│   │   ├── constants.ts         # 앱 전용 상수
│   │   └── utils.ts             # 앱 전용 유틸리티 함수 (일반적인 순수 함수)
│   ├── store/                   # Zustand 스토어 정의
│   │   └── useAppStore.ts
│   └── types/                   # 앱 전용 TypeScript 타입 정의 (공통 타입은 `packages/types` 참조)
├── .env                         # 로컬 환경 변수
├── app.json                     # Expo 또는 React Native 앱 설정
├── babel.config.js              # Babel 설정
├── metro.config.js              # Metro Bundler 설정
├── package.json                 # 모바일 프로젝트 의존성 및 스크립트
├── tsconfig.json                # TypeScript 설정
└── README.md

5. packages/backend (Node.js/Express 백엔드 서비스)
백엔드 API 로직 및 데이터베이스 상호작용을 관리합니다.

smart-real-estate/packages/backend/
├── src/
│   ├── config/                  # 환경 변수, DB 연결 설정 등 (환경별 설정 파일 포함)
│   │   ├── index.ts
│   │   ├── database.ts
│   │   └── env.ts               # 환경 변수 로드 및 유효성 검사
│   ├── controllers/             # 요청 처리 로직 (Request-Response 핸들러)
│   │   ├── authController.ts
│   │   ├── userController.ts
│   │   ├── propertyController.ts
│   │   └── notificationController.ts
│   ├── services/                # 비즈니스 로직 (Controller에서 호출)
│   │   ├── authService.ts
│   │   ├── userService.ts
│   │   ├── propertyService.ts   # 국토부 API 연동 및 데이터 가공 로직 포함
│   │   └── notificationService.ts
│   ├── models/                  # 데이터베이스 모델 정의 (Sequelize, Mongoose)
│   │   ├── mysql/               # MySQL 모델 (Sequelize)
│   │   │   ├── User.ts
│   │   │   ├── Region.ts
│   │   │   ├── Complex.ts
│   │   │   ├── PropertyTransaction.ts
│   │   │   └── index.ts         # 모델 초기화 및 관계 정의
│   │   └── mongodb/             # MongoDB 모델 (Mongoose)
│   │       ├── UserSheet.ts
│   │       ├── NotificationSetting.ts
│   │       ├── PriceSnapshot.ts
│   │       └── index.ts         # 모델 초기화
│   ├── routes/                  # API 엔드포인트 라우팅 정의
│   │   ├── authRoutes.ts
│   │   ├── userRoutes.ts
│   │   ├── propertyRoutes.ts
│   │   └── notificationRoutes.ts
│   ├── middlewares/             # 미들웨어 (인증, 유효성 검사, 에러 처리 등)
│   │   ├── authMiddleware.ts    # JWT 인증, 권한 확인
│   │   ├── validationMiddleware.ts # Joi/express-validator를 통한 입력 유효성 검사
│   │   └── errorMiddleware.ts   # 중앙 집중식 에러 처리
│   ├── jobs/                    # 주기적인 배치 작업 (예: 국토부 데이터 수집, 알림 모니터링)
│   │   ├── dataCollector.ts
│   │   └── notificationMonitor.ts
│   │   └── index.ts             # 스케줄러 등록
│   ├── utils/                   # 백엔드 전용 유틸리티 함수 (JWT 생성/검증, 데이터 포맷터, 로깅 등)
│   │   ├── jwt.ts               # JWT 관련 유틸리티
│   │   ├── logger.ts            # Winston/Morgan 로깅 설정
│   │   └── api-docs.ts          # Swagger/OpenAPI 문서화 설정
│   ├── app.ts                   # Express 애플리케이션 진입점 (미들웨어, 라우트 설정)
│   └── server.ts                # 서버 실행 로직 (DB 연결, 포트 리스닝)
├── migrations/                  # MySQL 데이터베이스 마이그레이션 파일 (Umzug/Sequelize-cli)
│   └── 20240717_create_users_table.js
├── seeders/                     # 개발/테스트용 초기 데이터 (시더)
│   └── 20240717_seed_regions.js
├── .env                         # 로컬 환경 변수
├── package.json                 # 백엔드 프로젝트 의존성 및 스크립트
├── tsconfig.json                # TypeScript 설정
└── README.md

6. packages/common-utils (공통 유틸리티 함수)
웹, 앱, 백엔드에서 공통으로 사용될 수 있는 순수 함수들을 모아둔 패키지입니다.

smart-real-estate/packages/common-utils/
├── src/
│   ├── converters.ts            # 단위 변환 (㎡ <-> 평), 금액 포맷팅 등
│   ├── validators.ts            # 공통 유효성 검사 로직 (예: 이메일 형식, 비밀번호 강도)
│   ├── date-helpers.ts          # 날짜/시간 관련 유틸리티
│   └── index.ts                 # 공통 유틸리티 내보내기
├── package.json
├── tsconfig.json
└── README.md

7. packages/types (공통 TypeScript 타입 정의)
웹, 앱, 백엔드 간에 공유되는 TypeScript 타입 정의를 모아둔 패키지입니다. 이는 데이터 일관성을 유지하는 데 매우 중요합니다.

smart-real-estate/packages/types/
├── src/
│   ├── auth.ts                  # 인증 관련 타입 (예: UserProfile, AuthResponse)
│   ├── property.ts              # 부동산 매물/단지 관련 타입 (예: Complex, Transaction)
│   ├── sheet.ts                 # 사용자 시트 관련 타입 (예: SheetProperty, UserDefinedColumn)
│   ├── notification.ts          # 알림 관련 타입 (예: NotificationSetting, PushToken)
│   ├── common.ts                # 공통 응답 구조, 에러 타입 등
│   └── index.ts                 # 공통 타입 내보내기
├── package.json
├── tsconfig.json
└── README.md

8. packages/common-ui (웹/앱 공통 UI 컴포넌트) - 선택 사항
웹(Next.js)과 앱(React Native) 간에 완전히 추상화된 형태의 UI 컴포넌트 또는 디자인 토큰, 아이콘 등을 공유할 경우에만 활용합니다. Shadcn UI와 React Native Paper는 각각의 플랫폼에 최적화된 컴포넌트를 제공하므로, 시각적인 컴포넌트 자체의 공유는 제한적일 수 있습니다. 주로 디자인 시스템의 토큰(색상, 폰트 크기), 공통 아이콘 SVG/리액트 컴포넌트, 또는 UI 관련 커스텀 훅 등이 여기에 포함될 수 있습니다.

smart-real-estate/packages/common-ui/
├── src/
│   ├── icons/                   # 공통 아이콘 컴포넌트 (SVG 또는 플랫폼 독립적)
│   ├── theme/                   # 디자인 토큰 (색상 팔레트, 폰트 스케일 등)
│   ├── hooks/                   # UI 관련 공통 커스텀 훅 (예: useDebounce)
│   └── index.ts                 # 공통 UI 요소 내보내기
├── package.json
├── tsconfig.json
└── README.md

9. 코드 조직 방법 및 원칙
모듈성 (Modularity): 각 디렉토리와 파일은 명확한 단일 책임을 가집니다. (예: controllers는 요청 처리, services는 비즈니스 로직)

관심사 분리 (Separation of Concerns): 로직의 종류에 따라 파일을 분리하여 코드의 재사용성과 유지보수성을 높입니다.

레이어드 아키텍처 (Layered Architecture): 백엔드는 컨트롤러-서비스-모델(데이터베이스)의 계층 구조를 따릅니다.

재사용성 (Reusability): packages/common-utils 및 packages/types를 통해 웹, 앱, 백엔드 간에 공통 로직과 타입 정의를 공유하여 중복 코드를 최소화합니다.

명명 규칙 (Naming Conventions): 일관된 파일 및 변수 명명 규칙을 따릅니다 (예: camelCase for variables, PascalCase for components/classes, kebab-case for directories).

TypeScript 활용: 모든 프로젝트에서 TypeScript를 사용하여 타입 안정성을 확보하고 개발 생산성을 높입니다.

환경 변수 관리: .env 파일을 통해 환경별 설정을 분리하고, 민감 정보는 클라우드 서비스(AWS Secrets Manager)를 통해 안전하게 관리합니다.

데이터베이스 마이그레이션: MySQL 스키마 변경 이력을 migrations/ 폴더에서 관리하여 데이터베이스 변경 이력을 추적하고 협업을 용이하게 합니다.

시드 데이터: seeders/ 폴더를 통해 개발 및 테스트 환경에서 필요한 초기 데이터를 관리합니다.

이 프로젝트 구조 정의서는 개발팀이 효율적이고 체계적으로 서비스를 구축하는 데 강력한 기반을 제공할 것입니다.