---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-DASH-001: 설문별 응답 통계 집계 Route Handler"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-DASH-001] 설문별 응답 통계 집계 Route Handler
- 목적: 특정 설문의 일별/주별 응답 수 추이, 완료율, 평균 소요 시간 등을 DB에서 연산하여 대시보드용 JSON 데이터로 반환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L657)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L756)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js Route Handler `/app/api/v1/dashboard/surveys/[form_id]/stats/route.ts` 작성
- [ ] `RESPONSE` 테이블 대상 Prisma GroupBy 및 Aggregate 쿼리 작성
- [ ] 프론트엔드 차트(Recharts)에서 읽기 편한 데이터 구조(Array of Objects)로 포매팅

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 유효한 설문 통계 요청
- Given: 응답 데이터가 적재된 `form_id`가 주어짐
- When: 통계 API 요청이 인입됨
- Then: 200 OK와 함께 일자별 응답 추이 배열이 반환된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 응답 데이터가 많을 경우를 대비해 필요한 컬럼만 Select하여 속도 최적화(p95 ≤ 500ms)

## :checkered_flag: Definition of Done (DoD)
- [ ] 계산된 평균 소요 시간의 산술적 정확성 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-005
- Blocks: #FE-DASH-002
