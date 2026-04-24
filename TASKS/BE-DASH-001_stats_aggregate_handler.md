---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-DASH-001: 설문 응답 통계 집계 Route Handler 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-DASH-001] 설문 응답 통계 집계 Route Handler 구현
- 목적: 프론트엔드 통계 차트 렌더링을 위해 특정 설문의 전체 응답 데이터를 문항별로 집계(Count, Avg 등)하여 가공된 형태의 JSON으로 반환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-025`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: Prisma `groupBy` 또는 Raw SQL 집계 쿼리

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/forms/[form_id]/stats/route.ts` 구현
- [ ] 문항별 응답 분포 집계 로직 구현:
    - 객관식: `{ "option_id": count }` 맵 생성
    - 척도형: 합계 및 평균 계산
- [ ] 시간대별 응답 추이 데이터 생성 (차트용)
- [ ] 이탈률 및 완료율 계산 로직 포함
- [ ] 데이터 크기가 클 경우를 대비한 쿼리 최적화 및 캐싱(선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 집계 데이터 정확성 확인
- Given: 특정 문항에 대해 A보기를 선택한 응답자가 30명임
- When: 통계 API를 호출함
- Then: 해당 문항의 집계 결과 내 A보기 카운트가 정확히 30이어야 한다.

Scenario 2: 대량 응답 집계 속도
- Given: 1,000건 이상의 응답이 쌓인 설문
- When: 통계 조회를 요청함
- Then: 서버 측 처리 시간이 500ms 이내여야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 복잡한 JSON 내의 데이터를 효율적으로 집계하기 위해 필요한 경우 PostgreSQL의 JSONB 함수를 활용한다.
- 무결성: 현재 수집 중인 실시간 데이터를 정확히 반영한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 프론트엔드 차트 컴포넌트에 적합한 집계 데이터 형식을 반환하는가?
- [ ] 문항 타입별 집계 로직이 모두 구현되었는가?
- [ ] 대량 데이터 처리 시 성능 저하가 없는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE)
- Blocks: #FE-DASH-002 (통계 차트 연동)
