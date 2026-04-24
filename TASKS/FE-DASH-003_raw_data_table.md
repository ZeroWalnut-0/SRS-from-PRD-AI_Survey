---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-DASH-003: 응답 데이터 원본(Raw Data) 테이블 UI 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-DASH-003] 응답 데이터 원본(Raw Data) 테이블 UI 구현
- 목적: 통계적으로 요약된 데이터 외에, 개별 응답자 한 명 한 명의 전체 응답 내용을 리스트 형태로 상세히 확인할 수 있는 테이블을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-024`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3_RESPONSE`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/dashboard/RawDataTable.tsx` 컴포넌트 생성
- [ ] 동적 컬럼 생성 로직 구현 (설문 문항 수에 따라 가로 컬럼 확장)
- [ ] 페이지네이션(Pagination) 및 정렬(Sorting) 기능 구현
- [ ] 특정 응답자 상세 보기 모달 연동
- [ ] 개별 응답 삭제 기능 (관리용)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 응답 데이터 리스트 조회
- Given: 50명의 응답자가 존재하는 설문
- When: Raw Data 탭을 클릭함
- Then: 응답 시각, IP 해시(일부), 그리고 각 문항별 답변 내용이 표 형태로 나열되어야 한다.

Scenario 2: 대량 데이터 스크롤 테스트
- Given: 500건 이상의 응답 데이터
- When: 테이블을 탐색함
- Then: 성능 저하 없이 페이지네이션을 통해 원활하게 데이터를 확인할 수 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 가로로 긴 테이블의 경우 첫 번째 컬럼(응답 ID/시각)을 고정(Sticky)하여 탐색 편의성을 높인다.
- 보안: IP 주소는 해싱된 값의 일부만 노출하여 개인정보를 보호한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 응답 원본 데이터를 보여주는 테이블이 정상 작동하는가?
- [ ] 페이지네이션 및 필터링 기능이 정확한가?
- [ ] 동적 컬럼 생성 로직이 다양한 설문 구조를 수용하는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE), #BE-DASH-002 (조회 핸들러)
- Blocks: None
