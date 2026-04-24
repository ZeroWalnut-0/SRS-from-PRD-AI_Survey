---
name: UI/UX Task
about: 관리자 대시보드 레이아웃 구축
title: "[UI] FE-ADMIN-001: 관리자 전용 대시보드 기본 레이아웃 및 인증 보호 설정"
labels: 'frontend, admin, ui'
assignees: ''
---

## :dart: Summary
- 목적: 운영자가 시스템을 관리할 수 있는 전용 공간(Dashboard)의 UI 구조를 구축하고, 비인가자의 접근을 원천 차단한다.

## :link: References (Spec & Context)
- SRS 문서: `§1.3 (RBAC), §3.2 CLI-01`
- 경로: `/admin/*`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Admin Layout 조립:
    - 전용 사이드바 (시스템 통계, 결제 관리, 쿼터 모니터링)
    - 상단 글로벌 검색 (문서 ID 또는 유저 검색)
- [ ] 접근 제어(Guard) 구현:
    - `middleware.ts` 또는 Layout 수준에서 `isAdmin` 체크 수행
    - 권한 없을 시 메인 페이지로 리다이렉트 및 토스트 알림
- [ ] 테마 설정: 관리자 화면임을 인지할 수 있도록 차별화된 색상 테마(예: Dark/Slate) 적용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 관리자 접근 성공
- Given: `role: 'ADMIN'`인 계정으로 로그인함
- When: `/admin` 경로로 진입하면
- Then: 관리자 대시보드 레이아웃이 정상적으로 노출되어야 한다.

Scenario 2: 일반 사용자 접근 차단
- Given: `role: 'USER'`인 계정으로 로그인함
- When: `/admin` 경로로 강제 진입 시도 시
- Then: `/` (메인)으로 리다이렉트되며 "접근 권한이 없습니다" 메시지가 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클라이언트 측 가드뿐만 아니라 서버 사이드(Route Handler)에서도 권한 재검증 필수.
- 반응형: 관리자 페이지 특성상 데스크탑 뷰(1280px 이상) 최적화를 우선하되 모바일에서도 가독성 유지.

## :checkered_flag: Definition of Done (DoD)
- [ ] 관리자 전용 레이아웃이 구현되었는가?
- [ ] 비관리자의 접근이 차단되는가?

## :construction: Dependencies & Blockers
- Depends on: `BE-RL-002` (RBAC Middleware)
- Blocks: `FE-ADMIN-002`
