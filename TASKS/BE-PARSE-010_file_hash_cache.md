---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-010: 파일 해시(SHA-256) 기반 파싱 캐시 조회 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-010] 파일 해시 기반 파싱 캐시 조회 구현
- 목적: 동일한 파일의 중복 업로드 시, 고비용의 LLM API 재호출 없이 기존 가공 데이터를 즉각 재사용하여 연산 원가를 절감한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L219)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 파일 스트림의 SHA-256 해시 생성 헬퍼 함수 구현
- [ ] DB `DOCUMENT` 테이블의 `file_hash` 인덱스 조회 로직 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 중복 파일 캐시 히트(Hit)
- Given: 예전에 파싱 완료된 `survey.pdf`
- When: 동일한 파일 재업로드
- Then: API를 거치지 않고 1초 이내에 이전 `form_id`를 반환한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 캐시 히트 시 로그 인쇄 유무

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001, #DB-003
- Blocks: None
