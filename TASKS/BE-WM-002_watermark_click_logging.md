---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-WM-002: 워터마크 클릭 이벤트 감사 로그 기록 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-WM-002] 워터마크 클릭 이벤트 감사 로그 기록 구현
- 목적: 사용자가 설문 폼 하단의 워터마크를 클릭할 때 발생하는 이벤트를 서버 측 `AUDIT_LOG`에 기록하여 바이럴 효과를 측정한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1_EXT-06`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.8_AUDIT_LOG`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 워터마크 클릭 시 거쳐가는 중간 리다이렉트 핸들러 또는 비동기 로깅 API 구현
- [ ] `AUDIT_LOG` 레코드 생성:
    - `action`: `WATERMARK_CLICK`
    - `resource_type`: `FORM`
    - `resource_id`: 해당 `form_id`
    - `details`: 클릭 시점의 User-Agent, Referer 등 정보 포함
- [ ] GA4 장애 시에도 유효한 마케팅 데이터 확보를 위한 로직 설계

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 워터마크 클릭 로그 기록
- Given: 무료 설문 폼의 워터마크가 노출됨
- When: 사용자가 워터마크를 클릭함
- Then: DB의 `AUDIT_LOG` 테이블에 신규 로그가 생성되어야 한다.

Scenario 2: 상세 정보 유효성
- Given: 로그가 생성됨
- When: `details` 필드를 조회함
- Then: 어떤 설문지에서 유입되었는지 식별할 수 있는 `form_id`가 포함되어 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 로깅 작업이 사용자의 리다이렉트 경험을 저해하지 않도록 비동기로 처리한다.
- 보안: 클릭한 응답자의 개인정보는 수집하지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 클릭 이벤트 발생 시 `AUDIT_LOG`가 정확히 기록되는가?
- [ ] 로깅 로직이 시스템 전반의 성능에 영향을 주지 않는가?
- [ ] 마케팅 분석에 필요한 데이터가 모두 포함되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-010 (AUDIT_LOG), #FE-WM-002 (클릭 연동)
- Blocks: None
