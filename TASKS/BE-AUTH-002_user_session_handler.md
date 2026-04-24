---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-AUTH-002: 사용자 세션 및 권한 검증 미들웨어 구현"
labels: 'feature, backend, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-AUTH-002] 사용자 세션 및 권한 검증 미들웨어 구현
- 목적: 서버 측 Route Handler 호출 시, 요청 헤더의 세션 토큰을 검증하여 유효한 사용자인지 확인하고 요청 객체에 사용자 정보를 주입한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.3_REQ-NF-013`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: `supabase-js`, `next/headers`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `lib/auth.ts` 또는 유사 위치에 세션 검증 공통 함수 구현
- [ ] API 요청 시 헤더/쿠키에서 Supabase 세션 추출 및 서버 측 검증 (`getUser`)
- [ ] 유효하지 않은 세션의 경우 401 Unauthorized 즉시 반환 로직 구현
- [ ] 특정 도메인(예: 결제 확인 등)에 대한 추가 권한 체크 함수 작성
- [ ] Route Handler에서 쉽게 사용할 수 있는 래퍼(HOC) 패턴 도입

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: API 권한 검증 성공
- Given: 유효한 로그인 세션을 보유한 클라이언트
- When: `/api/v1/surveys` 목록을 요청함
- Then: 서버 측 미들웨어가 세션을 확인하고 200 OK와 함께 데이터를 반환해야 한다.

Scenario 2: 토큰 만료 시 대응
- Given: 세션이 만료된 사용자가 API를 호출함
- When: 서버 측 세션 검증을 수행함
- Then: 401 Unauthorized 에러와 함께 재로그인 필요 메시지를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클라이언트가 보낸 세션 정보를 신뢰하지 않고, 반드시 Supabase 서버와 직접 통신하여 유효성을 교차 검증한다.
- 성능: 검증 로직으로 인한 API 지연을 최소화하기 위해 효율적인 인스턴스 관리를 수행한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 서버 측 세션 검증 로직이 공통 모듈화되었는가?
- [ ] API 접근 시 401 에러 핸들링이 철저히 이루어지는가?
- [ ] 사용자 식별 정보(`user_id`)가 안전하게 추출되어 로직에 전달되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-AUTH-001 (Supabase 설정)
- Blocks: 모든 보호된 API 핸들러 구현
