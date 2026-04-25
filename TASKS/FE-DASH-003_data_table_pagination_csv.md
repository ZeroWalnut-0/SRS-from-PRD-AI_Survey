---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-DASH-003: 대시보드 테이블 페이지네이션, 정렬 및 CSV 내보내기"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-DASH-003] 대시보드 테이블 페이지네이션, 정렬 및 CSV 내보내기
- 목적: 관리자 화면에서 수집된 수많은 응답 데이터를 한눈에 탐색하고, 특정 조건으로 필터링된 데이터를 로컬 CSV 파일로 내려받게 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L643)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `@tanstack/react-table`을 이용한 고성능 데이터 테이블 래핑
- [ ] 클라이언트 사이드 페이지네이션 및 정렬 상태값 연결
- [ ] `json-to-csv` 변환 로직을 통한 파일 다운로드 버튼 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: CSV 추출
- Given: 필터링된 50건의 데이터
- When: 'CSV로 내보내기' 클릭
- Then: `responses_export.csv` 파일이 즉시 저장된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 다국어 문자열(한글 깨짐 등) 인코딩(UTF-8 BOM) 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-DASH-001
- Blocks: None
