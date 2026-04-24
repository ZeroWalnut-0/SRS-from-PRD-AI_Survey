---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-AUTH-002: 사용자 프로필 및 계정 설정 화면 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-AUTH-002] 사용자 프로필 및 계정 설정 화면 구현
- 목적: 사용자가 자신의 이름, 비밀번호를 변경하거나 유료 서비스 구독 상태를 확인하고 관리할 수 있는 환경을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.9_USER`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/settings/profile/page.tsx` 생성
- [ ] 개인정보 수정 폼: 이름(Name) 변경 기능 구현
- [ ] 비밀번호 변경 UI 및 Supabase Auth 연동 로직 구현
- [ ] 계정 상태 표시: 유료 사용자 여부(`is_paid_user`) 및 가입일 표시
- [ ] 로그아웃(Logout) 버튼 및 세션 초기화 연동
- [ ] 회원 탈퇴 기능 (데이터 삭제 정책 안내 포함)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 프로필 정보 수정
- Given: 사용자가 이름을 '홍길동'에서 '이몽룡'으로 수정함
- When: [저장]을 클릭함
- Then: DB의 `User` 레코드가 갱신되고 화면에 즉시 반영되어야 한다.

Scenario 2: 유료 사용자 배지 확인
- Given: 결제를 완료한 유료 사용자 계정
- When: 프로필 페이지에 진입함
- Then: "Premium" 또는 "유료 회원" 배지가 이름 옆에 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 비밀번호 변경 시 기존 비밀번호 확인 절차를 반드시 포함한다.
- UX: 탈퇴 기능은 실수 방지를 위해 확인 절차를 거치도록 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 이름 변경 및 비밀번호 갱신 기능이 정상 작동하는가?
- [ ] 유료/무료 계정 상태가 정확히 표시되는가?
- [ ] 로그아웃 시 세션이 파기되고 로그인 페이지로 이동하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-AUTH-001 (인증 연동), #DB-002 (USER 테이블)
- Blocks: None
