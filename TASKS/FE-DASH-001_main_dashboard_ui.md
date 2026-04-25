---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-DASH-001: 사용자 메인 대시보드(설문 목록) 화면 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-DASH-001] 사용자 메인 대시보드 화면 구현
- 목적: 로그인 후 진입하는 홈 화면으로, 내가 생성한 설문의 진행 현황 및 빠른 생성 바로가기 기능을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L576)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 설문 리스트 카드 뷰 그리드 레이아웃 구현
- [ ] 설문 상태별(작성중, 수집중, 종료) 태그 배지 스타일링
- [ ] 신규 설문 생성(문서 업로드) 모달 트리거 버튼 배치

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 생성된 설문 목록 출력
- Given: 사용자가 보유한 설문이 3건 존재함
- When: 대시보드 진입
- Then: 3개의 설문 카드가 서버 데이터와 일치하게 화면에 렌더링된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 페이지 네이션 혹은 무한 스크롤 적용하여 뷰포트 렌더링 부하 최소화

## :checkered_flag: Definition of Done (DoD)
- [ ] 빈 목록(Empty State)일 때의 대체 화면 존재 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-DASH-002
- Blocks: #FE-DASH-002
