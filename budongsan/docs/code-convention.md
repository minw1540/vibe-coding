🏡 나만의 스마트 부동산 시트 웹/앱 서비스 코딩 컨벤션 가이드 🏡
본 문서는 '나만의 스마트 부동산 시트' 웹(Next.js) 및 모바일 앱(React Native) 프론트엔드 개발을 위한 코딩 컨벤션 가이드입니다. 일관된 코드 스타일과 구조는 개발 효율성을 높이고, 코드의 가독성, 유지보수성, 품질을 향상시키는 데 필수적입니다.

1. 개요
이 가이드는 React, Next.js, React Native, TypeScript, Tailwind CSS를 사용하는 프론트엔드 개발에 적용됩니다. ESLint, Prettier와 같은 도구를 활용하여 자동화된 코드 품질 관리를 지원합니다.

2. 일반 원칙 (General Principles)
가독성 (Readability): 코드는 다른 개발자가 쉽게 읽고 이해할 수 있어야 합니다.

일관성 (Consistency): 프로젝트 내 모든 코드는 이 가이드라인을 일관되게 따라야 합니다.

유지보수성 (Maintainability): 코드는 향후 변경 및 확장이 용이해야 합니다.

DRY (Don't Repeat Yourself): 중복 코드를 최소화하고 재사용 가능한 컴포넌트 및 유틸리티를 활용합니다.

명확성 (Clarity): 복잡한 로직은 주석으로 설명하고, 변수/함수명은 목적을 명확히 드러내야 합니다.

접근성 (Accessibility): 모든 UI 요소는 웹 접근성 표준을 고려하여 구현합니다.

3. TypeScript 사용 규칙
명시적인 타입 선언: 가능한 한 모든 변수, 함수 매개변수, 반환 값에 타입을 명시합니다. any 타입 사용은 지양합니다.

인터페이스(Interface) vs 타입 별칭(Type Alias):

객체 형태의 타입을 정의할 때는 interface를 선호합니다. (확장성, 선언적 병합)

유니온 타입, 튜플 타입, 함수 타입 등 복잡한 타입을 정의할 때는 type을 사용합니다.

공통 타입 관리: packages/types 디렉토리에 공통으로 사용되는 타입을 정의하고 각 프로젝트에서 참조합니다.

타입 가드 (Type Guards): 런타임에 타입 검증이 필요할 때 타입 가드를 적극 활용합니다.

4. JavaScript/TypeScript 문법 및 스타일
변수 선언: const를 기본으로 사용하고, 재할당이 필요한 경우에만 let을 사용합니다. var는 사용하지 않습니다.

함수 선언:

컴포넌트, 유틸리티 함수 등 대부분의 함수는 const를 사용하여 화살표 함수(Arrow Function) 형태로 선언합니다.

예시: const handleClick = (event: React.MouseEvent) => { ... };

클래스 메서드나 React 컴포넌트 내부의 이벤트 핸들러는 handle 접두사를 사용합니다. (예: handleClick, handleSubmit, handleInputChange)

조건문:

if/else 문 사용 시 중첩을 최소화하고, early return을 적극 활용하여 가독성을 높입니다.

짧은 조건문은 삼항 연산자(condition ? true : false)를 활용할 수 있습니다.

반복문: for...of, forEach, map, filter, reduce 등 배열 메서드를 선호합니다.

객체 및 배열:

객체 리터럴 및 배열 리터럴 사용 시 trailing comma를 사용합니다.

구조 분해 할당(Destructuring Assignment)을 적극 활용합니다.

모듈 임포트/익스포트:

import 문은 파일 상단에 배치하고, 외부 라이브러리, 공통 패키지, 로컬 파일 순으로 정렬합니다.

export default는 컴포넌트 파일의 최하단에 한 번만 사용합니다.

export const를 사용하여 여러 함수나 변수를 내보낼 수 있습니다.

5. React/Next.js/React Native 특정 규칙
컴포넌트 선언:

함수형 컴포넌트와 React Hooks를 기본으로 사용합니다. 클래스 컴포넌트는 지양합니다.

컴포넌트 파일명과 컴포넌트명은 PascalCase를 사용합니다. (예: MyComponent.tsx)

Props:

Props는 명시적으로 타입을 정의합니다.

Props가 많을 경우 구조 분해 할당을 사용하여 가독성을 높입니다.

상태 관리: useState, useEffect, useContext 등 React Hooks와 Zustand를 활용하여 상태를 관리합니다.

JSX/TSX:

JSX 내에서 JavaScript 표현식을 사용할 때는 중괄호 {}를 사용합니다.

자체 닫는 태그는 항상 />로 닫습니다.

속성(props)이 많을 경우 여러 줄로 나누어 작성합니다.

조건부 렌더링: early return 또는 삼항 연산자, && 연산자를 활용합니다.

class: 사용 (Tailwind CSS): Tailwind CSS 클래스를 적용할 때는 class="조건 ? '클래스1' : '클래스2'" 대신, clsx 또는 class-variance-authority와 같은 라이브러리를 활용하여 조건부 클래스를 관리하거나, 직접 문자열 템플릿 리터럴을 사용하는 것을 권장합니다. 단, class: 구문은 HTML/JSX 표준이 아니므로, className 속성 내에서 조건부 로직을 구현합니다.

예시 (React/Next.js):

import clsx from 'clsx'; // clsx 라이브러리 사용 예시

const MyButton = ({ isActive }: { isActive: boolean }) => {
  return (
    <button
      className={clsx(
        'px-4 py-2 rounded-md',
        isActive ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
      )}
    >
      버튼
    </button>
  );
};

키 (Key): 리스트 렌더링 시 key prop을 항상 제공하며, 안정적인 고유 ID를 사용합니다. (인덱스 사용 지양)

Next.js (웹):

app 라우터 구조를 기본으로 사용합니다.

데이터 페칭은 getServerSideProps, getStaticProps (Pages Router) 또는 fetch API 및 async/await (App Router)를 활용합니다.

API Routes는 백엔드 API와의 프록시 또는 경량 API로 사용합니다.

React Native (모바일 앱):

Expo 또는 React Native CLI 프로젝트 구조를 따릅니다.

React Navigation을 사용하여 화면 간 이동을 관리합니다.

네이티브 모듈 사용 시, 플랫폼별 코드 분리(.ios.tsx, .android.tsx)를 고려합니다.

6. 스타일링 (Tailwind CSS)
유틸리티 우선: 가능한 한 Tailwind CSS 유틸리티 클래스를 사용하여 스타일을 적용합니다.

컴포넌트 기반 스타일링: 복잡하거나 재사용되는 컴포넌트의 경우 @apply 지시어를 사용하여 Tailwind 클래스를 CSS 파일로 추출하거나, clsx와 같은 라이브러리를 사용하여 조건부 클래스를 관리합니다.

반응형 디자인: Tailwind의 반응형 접두사(sm:, md:, lg:)를 적극 활용하여 다양한 화면 크기에 대응합니다.

커스텀 설정: tailwind.config.js 파일을 통해 프로젝트의 디자인 시스템(색상, 폰트, 간격 등)을 정의합니다.

7. 접근성 (Accessibility)
시맨틱 HTML/JSX: div 남용을 지양하고 button, a, input, form, header, main, footer, nav 등 시맨틱 태그를 적절히 사용합니다.

ARIA 속성: 필요한 경우 aria-label, aria-describedby, role 등 ARIA 속성을 사용하여 스크린 리더 사용자에게 추가 정보를 제공합니다.

키보드 접근성:

모든 인터랙티브 요소(버튼, 링크, 입력 필드)는 키보드로 접근 가능해야 합니다.

tabIndex="0"를 사용하여 기본 탭 순서에 포함되지 않는 요소에 키보드 접근성을 부여합니다. (남용 주의)

onKeyDown 이벤트 핸들러를 사용하여 Enter 키나 Space 키로 버튼/링크를 활성화할 수 있도록 합니다.

예시 (버튼):

const MyAccessibleButton = ({ onClick, label }: { onClick: () => void; label: string }) => {
  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      onClick();
    }
  };

  return (
    <button
      onClick={onClick}
      onKeyDown={handleKeyPress}
      tabIndex={0}
      aria-label={label}
      className="px-4 py-2 rounded-md bg-blue-500 text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
    >
      {label}
    </button>
  );
};

색상 대비: 텍스트와 배경색 간의 충분한 대비를 확보하여 시각 장애가 있는 사용자도 내용을 읽을 수 있도록 합니다.

8. 주석 (Comments)
복잡한 로직: 이해하기 어려운 복잡한 로직이나 알고리즘에는 충분한 주석을 작성합니다.

TODO 주석: 임시로 남겨두는 작업이나 개선 사항은 // TODO: [내용] 형식으로 작성합니다.

JSDoc: 함수, 컴포넌트, 인터페이스 등 주요 코드 블록에는 JSDoc 형식의 주석을 사용하여 파라미터, 반환 값, 설명 등을 명시합니다.

9. 파일 명명 규칙 및 구조
파일/폴더명: kebab-case (예: my-component.tsx, user-profile/)

컴포넌트 파일명: PascalCase (예: Button.tsx, UserProfile.tsx)

훅스 파일명: use 접두사 + PascalCase (예: useAuth.ts)

유틸리티 파일명: camelCase 또는 kebab-case (예: dateUtils.ts, api-client.ts)

인덱스 파일: 디렉토리의 진입점 역할을 하는 index.ts 파일을 사용하여 모듈을 한곳에서 내보냅니다.

10. ESLint 및 Prettier 설정
ESLint: 코드 품질 및 잠재적 오류를 감지하기 위해 ESLint를 설정합니다. eslint-plugin-react, eslint-plugin-react-hooks, @typescript-eslint/eslint-plugin, eslint-plugin-prettier 등을 포함합니다.

Prettier: 코드 포맷팅을 자동화하여 일관된 코드 스타일을 유지합니다. ESLint와 통합하여 사용합니다.

CI/CD 연동: 코드 커밋 또는 푸시 전에 ESLint와 Prettier 검사를 강제하여 코드 품질을 지속적으로 관리합니다.

이 코딩 컨벤션 가이드는 '나만의 스마트 부동산 시트' 서비스의 프론트엔드 개발팀이 고품질의 코드를 생산하고 효율적으로 협업하는 데 중요한 기준이 될 것입니다.

🏡 나만의 스마트 부동산 시트 웹/앱 서비스 백엔드 코딩 컨벤션 가이드 🏡
본 문서는 '나만의 스마트 부동산 시트' 서비스의 백엔드(Node.js/Express) 개발을 위한 코딩 컨벤션 가이드입니다. 일관된 코드 스타일과 구조는 개발 효율성을 높이고, 코드의 가독성, 유지보수성, 품질을 향상시키는 데 필수적입니다. 이 가이드는 기술 스택 및 데이터베이스 설계 문서를 기반으로 합니다.

1. 개요
이 가이드는 Node.js, Express.js, TypeScript, MySQL (Sequelize), MongoDB (Mongoose)를 사용하는 백엔드 개발에 적용됩니다. ESLint, Prettier와 같은 도구를 활용하여 자동화된 코드 품질 관리를 지원합니다.

2. 일반 원칙 (General Principles)
가독성 (Readability): 코드는 다른 개발자가 쉽게 읽고 이해할 수 있어야 합니다.

일관성 (Consistency): 프로젝트 내 모든 코드는 이 가이드라인을 일관되게 따라야 합니다.

유지보수성 (Maintainability): 코드는 향후 변경 및 확장이 용이해야 합니다.

DRY (Don't Repeat Yourself): 중복 코드를 최소화하고 재사용 가능한 모듈 및 유틸리티를 활용합니다.

명확성 (Clarity): 복잡한 로직은 주석으로 설명하고, 변수/함수명은 목적을 명확히 드러내야 합니다.

성능 (Performance): 우선적으로 가독성과 유지보수성에 중점을 두되, 데이터베이스 쿼리, 외부 API 호출, 대량 데이터 처리 등 성능 병목 구간은 최적화를 고려합니다.

보안 (Security): 모든 개발 단계에서 보안 취약점을 최소화하고 안전한 코드 작성을 지향합니다.

3. TypeScript 사용 규칙
명시적인 타입 선언: 가능한 한 모든 변수, 함수 매개변수, 반환 값에 타입을 명시합니다.

타입 추론 활용: TypeScript의 강력한 타입 추론 기능을 활용하여 명시적인 타입 선언이 불필요한 경우에는 생략하여 코드의 간결성을 유지합니다. 단, 명확성이 필요한 경우나 any로 추론될 수 있는 경우에는 반드시 명시합니다.

any 타입 사용 지양: any 타입 사용은 지양하며, 불가피하게 알 수 없는 타입을 다룰 때는 unknown 타입을 사용하여 런타임 검증을 강제합니다.

인터페이스(Interface) vs 타입 별칭(Type Alias):

객체 형태의 타입을 정의할 때는 interface를 선호합니다. (확장성, 선언적 병합)

유니온 타입, 튜플 타입, 함수 타입 등 복잡한 타입을 정의할 때는 type을 사용합니다.

공통 타입 관리: packages/types 디렉토리에 공통으로 사용되는 타입을 정의하고 백엔드 프로젝트에서 참조합니다.

타입 가드 (Type Guards): 런타임에 타입 검증이 필요할 때 타입 가드를 적극 활용합니다.

4. JavaScript/TypeScript 문법 및 스타일
변수 선언: const를 기본으로 사용하고, 재할당이 필요한 경우에만 let을 사용합니다. var는 사용하지 않습니다.

함수 선언:

대부분의 함수는 const를 사용하여 화살표 함수(Arrow Function) 형태로 선언합니다.

예시: const getUserById = async (userId: string) => { ... };

조건문:

if/else 문 사용 시 중첩을 최소화하고, early return을 적극 활용하여 가독성을 높입니다.

짧은 조건문은 삼항 연산자(condition ? true : false)를 활용할 수 있습니다.

반복문: for...of, forEach, map, filter, reduce 등 배열 메서드를 선호합니다.

객체 및 배열:

객체 리터럴 및 배열 리터럴 사용 시 trailing comma를 사용합니다.

구조 분해 할당(Destructuring Assignment)을 적극 활용합니다.

비동기 코드: async/await 패턴을 사용하여 비동기 작업을 처리하여 가독성을 높입니다. Promise를 직접 다룰 때는 try...catch를 통해 오류를 명확하게 처리합니다.

모듈 임포트/익스포트:

import 문은 파일 상단에 배치하고, 외부 라이브러리, 공통 패키지, 로컬 파일 순으로 정렬합니다.

export default는 지양하고, export const를 사용하여 여러 함수나 변수를 내보냅니다.

5. Node.js/Express 특정 규칙
폴더/파일 구조: packages/backend/src 아래의 구조를 따릅니다.

config/: 환경 변수, DB 연결 설정 등. 환경별 설정 파일을 분리합니다.

controllers/: 요청 처리 로직. 클라이언트의 요청을 받아 유효성 검사를 서비스 계층에 위임하고, 서비스 계층의 결과를 클라이언트에 응답합니다. 직접적인 비즈니스 로직이나 DB 접근은 지양합니다.

services/: 비즈니스 로직. 실제 핵심 로직, 데이터베이스 상호작용, 외부 API 호출 등을 담당합니다. 컨트롤러는 서비스를 호출하고, 서비스는 모델 또는 다른 서비스를 호출합니다.

models/: 데이터베이스 모델 정의. MySQL (Sequelize) 및 MongoDB (Mongoose) 모델을 각 서브 디렉토리에 정의합니다.

routes/: API 엔드포인트 라우팅 정의. Express Router를 사용하여 각 도메인별 라우터를 모듈화합니다.

middlewares/: 미들웨어. 인증, 유효성 검사, 에러 처리 등 요청 처리 파이프라인에 공통적으로 적용되는 로직을 정의합니다.

jobs/: 주기적인 배치 작업. 국토부 데이터 수집, 알림 모니터링 등 스케줄러에 의해 실행되는 작업을 정의합니다.

utils/: 백엔드 전용 유틸리티 함수. JWT 생성/검증, 로깅 설정, API 문서화 설정 등 특정 계층에 속하지 않는 공통 함수를 모아둡니다.

app.ts: Express 애플리케이션 진입점. 미들웨어 및 라우터 설정을 포함합니다.

server.ts: 서버 실행 로직. DB 연결, 포트 리스닝 등을 담당합니다.

컨트롤러 (Controllers):

요청 유효성 검사는 validationMiddleware에 위임합니다.

try...catch 블록으로 에러를 처리하고, next(error)를 통해 중앙 에러 핸들러로 전달합니다.

예시:

import * as userService from '../services/userService';
import { Request, Response, NextFunction } from 'express';

export const getUserProfile = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = req.user.id; // 인증 미들웨어에서 추가된 사용자 ID
    const userProfile = await userService.getProfileById(userId);
    return res.status(200).json({ status: 'success', message: '프로필 조회 성공', data: userProfile });
  } catch (error) {
    next(error); // 에러 미들웨어로 전달
  }
};

서비스 (Services):

순수한 비즈니스 로직을 포함하며, DB 모델이나 외부 API를 직접 호출합니다.

컨트롤러에서 전달받은 데이터를 가공하고, 필요한 경우 여러 모델/API를 조합하여 복잡한 작업을 수행합니다.

예시:

import { User } from '../models/mysql';
import { CustomError } from '../middlewares/errorMiddleware';

export const getProfileById = async (userId: string) => {
  const user = await User.findByPk(userId);
  if (!user) {
    throw new CustomError('NOT_FOUND_001', '사용자를 찾을 수 없습니다.', 404);
  }
  return user;
};

라우팅 (Routing):

각 도메인별로 라우터 파일을 분리하고, express.Router()를 사용하여 라우트를 정의합니다.

API 버전 관리를 위해 라우트 경로에 버전을 포함합니다. (예: /v1/users)

미들웨어 (Middlewares):

인증, 유효성 검사, 로깅, 에러 처리 등 공통 로직을 미들웨어로 분리합니다.

next() 함수를 호출하여 다음 미들웨어 또는 라우트 핸들러로 제어를 전달합니다.

환경 설정 (Configuration):

config/index.ts에서 환경 변수를 로드하고, config/env.ts에서 환경 변수의 유효성을 검사합니다.

.env 파일을 사용하여 환경별 설정을 분리합니다.

배치/스케줄러 (Jobs/Schedulers):

jobs/ 디렉토리에 주기적으로 실행될 작업을 정의하고, jobs/index.ts에서 스케줄러(Node.js의 node-cron 등)에 등록합니다.

장기적으로 AWS Lambda/ECS Fargate와 같은 서버리스 스케줄링 서비스로 전환을 고려합니다.

6. 데이터베이스 상호작용
Sequelize (MySQL):

models/mysql/ 디렉토리에 각 테이블에 대한 모델을 정의합니다.

모델 간의 관계(1:1, 1:N, N:M)를 명확하게 설정합니다.

쿼리 작성 시 async/await를 사용하여 비동기 작업을 처리합니다.

복잡한 작업에는 트랜잭션(Transaction)을 사용하여 데이터 일관성을 보장합니다.

Mongoose (MongoDB):

models/mongodb/ 디렉토리에 각 컬렉션에 대한 스키마와 모델을 정의합니다.

스키마는 데이터의 구조와 유효성을 정의하며, 유연성을 유지하되 필요한 제약 조건을 명시합니다.

쿼리 작성 시 Mongoose의 메서드를 활용하고 async/await를 사용합니다.

다중 DB 트랜잭션 (Multi-DB Transactions): MySQL과 MongoDB 간에 트랜잭션이 필요한 복합 작업의 경우, Saga 패턴 또는 2단계 커밋(2PC)과 같은 분산 트랜잭션 패턴을 고려하여 데이터 일관성을 유지합니다. (초기에는 단순한 롤백 로직으로 시작하고 필요시 고도화)

7. API 설계 및 구현
RESTful 원칙: API는 RESTful 원칙을 따르도록 설계합니다. (자원 기반 URL, HTTP 메서드 활용)

API 버전 관리: URL에 버전을 포함하여 API 변경에 유연하게 대응합니다. (예: /v1/users)

응답 형식: 모든 API 응답은 status, message, data, code, details를 포함하는 공통 JSON 응답 구조를 따릅니다.

입력값 유효성 검사: validationMiddleware를 사용하여 모든 API 요청의 입력값에 대해 서버 측 유효성 검사를 철저히 수행합니다. (예: Joi 스키마 정의)

8. 에러 처리
중앙 집중식 에러 미들웨어: middlewares/errorMiddleware.ts를 통해 모든 API 요청에서 발생하는 에러를 한 곳에서 처리합니다.

커스텀 에러 클래스: 서비스의 특정 에러 상황을 나타내는 커스텀 에러 클래스를 정의하여 에러 메시지, HTTP 상태 코드, 내부 코드 등을 명확하게 관리합니다. (예: CustomError 클래스)

에러 로깅: 에러 발생 시 상세한 로그를 기록하고, 모니터링 시스템에 연동하여 실시간으로 에러를 감지합니다.

9. 로깅 및 모니터링
로깅 라이브러리: Winston을 사용하여 애플리케이션 로그를 관리하고, Morgan을 사용하여 HTTP 요청 로그를 기록합니다.

로깅 레벨: info, warn, error, debug 등 적절한 로깅 레벨을 사용하여 로그의 중요도를 구분합니다.

중앙 집중식 로깅: AWS CloudWatch Logs와 같은 서비스에 로그를 전송하여 중앙에서 로그를 수집, 저장, 분석할 수 있도록 합니다.

모니터링 도구: AWS CloudWatch를 사용하여 백엔드 서버의 CPU/메모리 사용량, 네트워크 트래픽, API 응답 시간, 에러율 등을 모니터링하고 알람을 설정합니다.

10. 보안
입력값 검증: 모든 사용자 입력값에 대한 서버 측 유효성 검증을 철저히 수행하여 SQL Injection, XSS 등의 공격을 방어합니다.

인증/인가: JWT 기반 인증 및 역할 기반 인가(Role-Based Access Control)를 구현하여 사용자 접근 권한을 제어합니다.

민감 정보 관리: API 키, 데이터베이스 인증 정보 등 민감한 자격 증명은 AWS Secrets Manager를 통해 안전하게 관리하고 환경 변수로 직접 노출하지 않습니다.

의존성 관리: npm audit 또는 yarn audit를 주기적으로 실행하여 프로젝트의 의존성에서 발견된 보안 취약점을 점검하고 업데이트합니다.

HTTPS/SSL: 모든 통신은 HTTPS/SSL을 통해 암호화하여 데이터 가로채기를 방지합니다.

CORS: 필요한 도메인에 대해서만 CORS(Cross-Origin Resource Sharing)를 허용하여 보안을 강화합니다.

11. 테스팅
단위 테스트 (Unit Test): Jest를 사용하여 각 컨트롤러, 서비스, 유틸리티 함수 등 개별 모듈의 기능을 검증합니다.

통합 테스트 (Integration Test): Supertest와 Jest를 사용하여 API 엔드포인트와 백엔드 서비스 간의 연동을 검증합니다. (DB 연동 포함)

성능 테스트 (Performance Test): JMeter 또는 Locust와 같은 도구를 사용하여 예상 동시 접속자 수 및 데이터 양에 따른 시스템 부하 테스트를 수행합니다.

12. 주석 및 문서화
코드 주석: 이해하기 어려운 복잡한 로직, 중요한 비즈니스 규칙, 외부 API 연동 부분에는 충분한 주석을 작성합니다.

JSDoc: 함수, 클래스, 인터페이스 등 주요 코드 블록에는 JSDoc 형식의 주석을 사용하여 파라미터, 반환 값, 설명 등을 명시하여 자동 문서화를 돕습니다.

API 문서: Swagger/OpenAPI를 사용하여 백엔드 API 명세서를 자동으로 생성하고 최신 상태로 유지하여 프론트엔드 개발자와의 협업을 용이하게 합니다.

13. 파일 명명 규칙 및 구조
파일/폴더명: kebab-case (예: user-controller.ts, auth-middleware.ts)

클래스/인터페이스/타입명: PascalCase (예: UserController, IUser, AuthResponse)

함수/변수명: camelCase (예: getUserProfile, userList)

상수: UPPER_SNAKE_CASE (예: API_KEY, DEFAULT_PAGE_SIZE)

이 백엔드 코딩 컨벤션 가이드는 '나만의 스마트 부동산 시트' 서비스의 백엔드 개발팀이 고품질의 코드를 생산하고 효율적으로 협업하며, 서비스의 안정성과 확장성을 확보하는 데 중요한 기준이 될 것입니다.