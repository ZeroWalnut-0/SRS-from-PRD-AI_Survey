---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Mon] NFR-MON-003: 북극성 KPI(결제 전환) 대시보드 집계 로직 구현"
labels: 'infrastructure, monitoring, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-MON-003] 북극성 KPI(결제 전환) 대시보드 집계 로직 구현
- 목적: 서비스의 핵심 지표인 '유료 ZIP 다운로드 완료 건수'를 실시간으로 집계하여 운영자에게 통찰력을 제공한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.5_REQ-NF-027`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 북극성 지표: §4.2.8 REQ-NF-033

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `AUDIT_LOG` 및 `ZIP_DATAMAP` 데이터를 기반으로 한 집계 쿼리 작성
- [ ] 일별/주별 결제 성공률(Conversion Rate) 계산 로직 구현
- [ ] Prisma `groupBy` 또는 Raw SQL을 활용한 고속 집계 최적화
- [ ] 집계 결과를 운영자 대시보드 API로 노출

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 지난 7일간 100건의 파싱과 5건의 결제가 발생함
- When: KPI 집계 API를 호출함
- Then: 결제 성공률 5%와 총 매출액이 정확하게 계산되어 반환되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 정확성: 취소되거나 실패한 결제 건을 제외한 실 결제 완료 건수만 집계한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 핵심 KPI에 대한 DB 집계 로직이 검증되었는가?
- [ ] 대량 로그 데이터 상황에서도 쿼리 성능이 유지되는가?
- [ ] 데이터가 시각화에 적합한 JSON 형태로 반환되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-002, #DB-010
- Blocks: #NFR-MON-005
