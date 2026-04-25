---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-001: 교차 쿼터 엑셀 데이터 파싱 및 매트릭스 상태 바인딩"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-001] 교차 쿼터 엑셀 데이터 파싱 및 매트릭스 상태 바인딩
- 목적: 사용자가 업로드한 할당표(성별 x 연령 x 지역) 엑셀 파일을 클라이언트 사이드에서 파싱하여 가시적인 표(Grid) 데이터로 변환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L514)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `xlsx` (SheetJS) 패키지 연동
- [ ] 업로드된 바이너리 엑셀 파일 로드 및 JSON 2차원 배열 추출 로직 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 할당표 엑셀 로드
- Given: 표준 쿼터 엑셀 파일
- When: 파일 선택 후 로드
- Then: 화면의 쿼터 설정 표에 각 조건별 목표 인원수(Target)가 자동 채워진다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 잘못된 셀 양식 업로드 시 명확한 줄 번호와 함께 파싱 에러 경고 출력

## :checkered_flag: Definition of Done (DoD)
- [ ] 데이터 정합성 일치 확인

## :construction: Dependencies & Blockers
- Depends on: #API-010
- Blocks: #FE-QT-002
