---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-AUTH-001: Supabase Auth 통합"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-AUTH-001] Supabase Auth 통합
- 목적: Supabase의 Authentication 기능을 프로젝트 백엔드에 통합하여 이메일 로그인 및 JWT 검증 체계를 안착시킨다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)
- 제약사항 (C-TEC-003): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase JS Client 모듈 초기화 및 환경변수 바인딩
- [ ] 서버 측 세션 상태 감지 헬퍼 함수 작성
- [ ] 로그인, 로그아웃, 비밀번호 찾기 등 기본 API Proxy Route 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 유효한 JWT 토큰을 통한 유저 식별
- Given: Supabase Auth를 통해 정상 발급된 Access Token이 존재함
- When: 서버가 토큰을 파싱함
- Then: 해당 토큰과 매칭되는 `user_id` 및 권한(Role) 정보를 획득한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 토큰 만료 시간 및 Refresh Token 갱신 주기를 안전하게 통제

## :checkered_flag: Definition of Done (DoD)
- [ ] 로그인 실패 시 401 상태 코드 출력 확인

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-004 (Supabase 프로젝트 셋업)
- Blocks: #BE-AUTH-002
