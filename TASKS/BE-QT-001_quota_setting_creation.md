---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-001: 쿼터 설정 생성 API 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-001] 쿼터 설정 생성 API (`POST /api/v1/quotas`)
- 목적: 엑셀 파일 등으로 입력된 성별×연령×지역 교차 쿼터 목표 데이터를 분석하여 DB에 설정 및 셀 정보를 일괄 등록한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L529)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L785)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L718)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] API Route Handler 구현 (`/app/api/v1/quotas/route.ts`)
- [ ] 엑셀 파일 파싱 로직 추가 (xlsx 라이브러리 활용)
- [ ] 추출된 JSON 데이터를 바탕으로 `QUOTA_SETTING` 레코드 및 하위 `QUOTA_CELL` 레코드 일괄 생성 (Prisma transaction 활용)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 설정 성공
- Given: 성별×연령×지역 조건이 명시된 유효한 엑셀 데이터가 제공됨
- When: 쿼터 생성 API가 호출됨
- Then: 201 Created 상태 및 생성된 `quota_id`가 반환된다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 대량의 셀(Cell) 데이터 인서트 시 병목 방지 및 DB 무결성 확보

## :checkered_flag: Definition of Done (DoD)
- [ ] 셀 정보가 정확한 데이터 매핑으로 DB에 들어갔는지 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-007, #DB-008, #API-010
- Blocks: #BE-QT-002, #BE-QT-003
