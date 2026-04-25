---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-MON-003: 북극성 KPI(유료 ZIP 다운로드) DB 기록 및 집계"
labels: 'feature, nfr, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-MON-003] 북극성 KPI DB 기록 및 집계
- 목적: 비즈니스의 핵심 성과 지표(North Star Metric)인 '유료 ZIP 다운로드 건수'를 정확하게 트래킹하기 위한 AUDIT_LOG 전략을 수립한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L617)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 다운로드 Route Handler 내부 `AUDIT_LOG` 기록부(type='NORTH_STAR') 추가
- [ ] 특정 기간 내 집계를 위한 Prisma `count` 쿼리 메서드 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 다운로드 건수 증가
- Given: 누적 10건 상태
- When: 신규 유저가 결제 후 ZIP 다운로드 성공
- Then: 집계 수치가 11건으로 정상 반영된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 중복 클릭(다운로드) 시 1회만 인정하는 중복 방지 로직 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-005, #DB-010
- Blocks: #NFR-MON-005
