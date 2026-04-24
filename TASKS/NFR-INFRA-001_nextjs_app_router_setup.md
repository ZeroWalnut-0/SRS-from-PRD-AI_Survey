---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-INFRA-001: Next.js App Router 프로젝트 초기 셋업"
labels: 'feature, infrastructure, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-001] Next.js App Router 프로젝트 초기 셋업
- 목적: MVP 개발의 토대가 되는 Next.js 풀스택 프로젝트 환경을 구성하고, 도메인별 라우트 그룹 및 기본 폴더 구조를 설정한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-001`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시스템 아키텍처: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 클라이언트 애플리케이션 정의: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js (최신 버전) 프로젝트 초기화 (`npx create-next-app@latest ./`)
- [ ] TypeScript, ESLint, Tailwind CSS 적용 확인
- [ ] `/app` 디렉토리 내 라우트 그룹 구조 생성:
    - `/app/(dashboard)/`: 관리자 및 작성자용 대시보드 영역
    - `/app/(survey)/`: 응답자용 설문 폼 렌더링 영역
- [ ] 공통 라이브러리 및 유틸리티 디렉토리 구성:
    - `/lib/services/`: 비즈니스 로직(Service Layer)
    - `/lib/utils/`: 공통 유틸리티
    - `/components/ui/`: shadcn/ui 컴포넌트 저장소
- [ ] 전역 레이아웃 및 폰트 설정 (Inter 등 모던 폰트 적용)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 프로젝트 초기 구동 확인
- Given: 프로젝트 셋업이 완료됨
- When: `npm run dev` 명령어를 실행함
- Then: 로컬 개발 서버가 에러 없이 실행되어야 하며, 기본 페이지가 브라우저에 표시되어야 한다.

Scenario 2: 라우트 그룹 접근성 확인
- Given: `/app/(dashboard)/page.tsx`와 `/app/(survey)/page.tsx`가 정의됨
- When: 브라우저에서 각각의 경로에 접근함
- Then: 별도의 서브 디렉토리 명칭 없이 의도한 페이지가 각각 렌더링되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 아키텍처: 단일 풀스택 프레임워크 설계 준수 (C-TEC-001, 002)
- 유지보수: 도메인별 폴더/레이어 분리 구조 준수 (REQ-NF-032)
- 배포: Vercel Hobby 플랜 배포가 가능하도록 경량화된 설정 유지.

## :checkered_flag: Definition of Done (DoD)
- [ ] `npx create-next-app`으로 생성된 기본 프로젝트가 존재하는가?
- [ ] `/app/(dashboard)` 및 `/app/(survey)` 라우트 그룹이 생성되었는가?
- [ ] TypeScript 컴파일 에러 및 ESLint 경고가 없는가?
- [ ] `tailwind.config.ts` 및 기초 디자인 시스템 토큰이 설정되었는가?

## :construction: Dependencies & Blockers
- Depends on: None
- Blocks: #NFR-INFRA-002 (Tailwind/shadcn 설정), #DB-001 (Prisma 초기화)
