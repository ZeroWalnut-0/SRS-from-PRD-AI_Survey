---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-WM-002: 워터마크 클릭 감사 로그(Audit Log) 기록 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-WM-002] 워터마크 클릭 감사 로그 기록 로직
- 목적: 무료 사용자의 설문 폼 하단 워터마크를 클릭하여 서비스로 유입된 이벤트를 감지하고, `AUDIT_LOG` 테이블에 기록하여 마케팅 전환율을 측정한다.

## :link: References (Spec & Context)
- 기술 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L377)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `POST /api/v1/watermark/click` 엔드포인트 구현
- [ ] 클라이언트 IP 및 User-Agent와 함께 `event_type: "WATERMARK_CLICK"` 적재

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 로그 기록 성공
- Given: 워터마크 클릭 발생
- When: API 요청
- Then: DB `AUDIT_LOG`에 신규 레코드가 201 Created로 생성된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 동일 유저의 중복 클릭에 대한 어뷰징 방지 로직 검토

## :construction: Dependencies & Blockers
- Depends on: #DB-010
- Blocks: #TEST-WM-002
