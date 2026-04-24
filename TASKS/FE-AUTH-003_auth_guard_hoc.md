---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-AUTH-003: 인증 가드(Auth Guard) 및 미들웨어 적용"
labels: 'feature, frontend, infrastructure, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-AUTH-003] 인증 가드(Auth Guard) 및 미들웨어 적용
- 목적: 인증되지 않은 사용자가 대시보드나 에디터 등 보호된 경로(Protected Routes)에 접근하는 것을 차단하고 로그인 페이지로 강제 이동시킨다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4_Architecture`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: Next.js Middleware, Supabase Auth Helpers

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `middleware.ts` 파일 생성 및 Supabase 세션 체크 로직 구현
- [ ] 보호 경로 정의: `/(dashboard)/*`, `/api/v1/protected/*` 등
- [ ] 비인증 사용자 접근 시 `/login`으로 리다이렉트 처리
- [ ] 인증된 사용자가 로그인/회원가입 페이지 접근 시 대시보드로 리다이렉트
- [ ] 클라이언트 측 HOC 또는 Hook(`useAuth`)을 이용한 페이지 내 세션 검증 보조

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 비인증 사용자의 대시보드 접근 차단
- Given: 로그아웃 상태임
- When: 브라우저 주소창에 `/surveys`를 직접 입력함
- Then: 페이지가 렌더링되기 전 `/login` 페이지로 즉시 리다이렉트되어야 한다.

Scenario 2: 인증 성공 후 원래 페이지로 복귀
- Given: 대시보드 접근 차단으로 로그인 페이지로 이동함
- When: 로그인을 성공함
- Then: 이전에 접근하려던 `/surveys` 페이지로 자동으로 리다이렉트되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 미들웨어 체크 로직은 요청 지연을 최소화하기 위해 50ms 이내에 완료되어야 한다.
- 보안: 쿠키 변조 등을 방지하기 위해 Supabase 서버 측 세션 검증을 반드시 병행한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 미들웨어 기반의 경로 보호가 완벽히 작동하는가?
- [ ] 리다이렉트 흐름(로그인 전/후)이 자연스러운가?
- [ ] 서버 측 API 요청 시에도 인증 토큰 검증이 이루어지는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-001 (Next.js 초기 셋업), #FE-AUTH-001 (인증 연동)
- Blocks: 전체 서비스의 보안성 확보
