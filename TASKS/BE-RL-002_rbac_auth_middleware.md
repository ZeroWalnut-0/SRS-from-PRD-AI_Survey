---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RL-002: 역할 기반 접근 제어(RBAC) 및 권한 검증 구현"
labels: 'feature, backend, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RL-002] 역할 기반 접근 제어(RBAC) 및 권한 검증 구현
- 목적: 사용자의 등급(일반, 유료, 운영자)에 따라 접근 가능한 API와 기능을 철저히 격리하여 보안을 강화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.3_REQ-NF-019`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: `USER.role` 또는 `is_paid_user` 필드

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `lib/auth.ts` 내에 `checkRole` 유틸리티 함수 구현
- [ ] 운영자 전용 API(`/api/v1/admin/*`) 접근 시 관리자 권한 체크 로직 추가
- [ ] 유료 전용 기능(데이터 다운로드 등) 접근 시 결제 여부/등급 체크 로직 강화
- [ ] 권한 위반 시 HTTP 403 Forbidden 응답 및 보안 감사 로그(`AUDIT_LOG`) 기록
- [ ] Supabase RLS(Row Level Security) 정책과의 상호 보완성 검토

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 일반 사용자의 관리자 페이지 접근 차단
- Given: `role = 'USER'`인 일반 계정으로 로그인함
- When: `/api/v1/admin/stats` 조회를 시도함
- Then: 403 Forbidden 에러와 함께 접근이 차단되어야 한다.

Scenario 2: 유료 사용자의 프리미엄 기능 접근 허용
- Given: `is_paid_user = true`인 계정
- When: 데이터맵 ZIP 다운로드 API를 호출함
- Then: 권한 검증을 통과하고 성공 응답을 받아야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클라이언트 측 UI 숨김에 의존하지 않고, 반드시 모든 서버 측 API 핸들러에서 권한을 재검증한다.
- 유연성: 향후 등급 세분화(예: Enterprise)가 가능하도록 확장 가능한 구조로 설계한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 역할별 접근 제한이 명세대로 작동하는가?
- [ ] 권한 위반 시도에 대한 로깅이 수행되는가?
- [ ] 권한 체크 로직이 중앙 집중화되어 관리가 용이한가?

## :construction: Dependencies & Blockers
- Depends on: #DB-002 (USER), #BE-AUTH-002 (세션 핸들러)
- Blocks: None
