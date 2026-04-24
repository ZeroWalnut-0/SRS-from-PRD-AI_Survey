---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-WM-001: 바이럴 워터마크 URL 자동 생성 로직 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-WM-001] 바이럴 워터마크 URL 자동 생성 로직 구현
- 목적: 무료 사용자의 설문 폼 하단에 노출될 워터마크 배너의 타겟 URL을 생성한다. 마케팅 성과 추적을 위해 UTM 파라미터를 자동으로 포함한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-017`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `BE-PARSE-005` (AI 파싱) 프로세스 내에 워터마크 URL 생성 단계 추가
- [ ] 베이스 URL 설정 (예: `https://ai-survey.indie.com/signup`)
- [ ] UTM 파라미터 구성: `utm_source=watermark`, `utm_medium=survey_footer`, `utm_campaign={form_id}`
- [ ] 구성된 URL을 `PARSED_FORM.viral_watermark_url` 필드에 저장
- [ ] 유료 사용자의 경우 해당 필드를 `null`로 처리하는 조건 로직 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 무료 사용자 설문 생성 시 URL 생성
- Given: 일반(무료) 사용자가 문서를 파싱함
- When: `PARSED_FORM` 레코드가 생성됨
- Then: `viral_watermark_url` 필드에 UTM 파라미터가 포함된 유효한 URL이 저장되어야 한다.

Scenario 2: 유료 사용자 설문 생성 시 URL 제외
- Given: 유료 결제 계정 사용자가 문서를 파싱함
- When: 레코드가 생성됨
- Then: `viral_watermark_url` 필드는 `null`이어야 한다.

## :gear: Technical & Non-Functional Constraints
- 유지보수: UTM 파라미터 구조는 설정 파일에서 관리하여 변경이 용이하도록 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 워터마크 URL 생성 로직이 비즈니스 규칙을 정확히 따르는가?
- [ ] UTM 파라미터가 누락 없이 포함되는가?
- [ ] DB 저장 시 데이터 타입이 일치하는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (AI SDK 연동), #DB-004 (PARSED_FORM)
- Blocks: #FE-WM-001 (워터마크 배너 UI)
