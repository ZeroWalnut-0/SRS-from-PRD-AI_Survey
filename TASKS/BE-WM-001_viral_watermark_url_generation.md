---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-WM-001: 바이럴 워터마크 URL 자동 생성"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-WM-001] 바이럴 워터마크 URL 자동 생성
- 목적: `PARSED_FORM` 생성 시점에 무료 플랜 사용자 설문용으로 GA4 추적 파라미터(`utm_source=watermark`)를 포함한 링크를 미리 조합해 둔다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L522)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `PARSED_FORM`을 생성하는 Service 클래스 내부에 URL 생성 모듈 작성
- [ ] 환경 변수(Base URL)와 정해진 UTM 파라미터를 문자열로 결합
- [ ] `is_paid_user`의 상태에 따라 워터마크 URL을 빈 값으로 남기거나 데이터 주입 분기 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 무료 사용자의 설문 생성
- Given: 유료 구독을 하지 않은 사용자가 문서를 업로드함
- When: 설문 폼 파싱이 완료될 때
- Then: `viral_watermark_url`에 `utm_source=watermark`가 올바르게 적용되어 저장된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 문자열 조작으로 수행되므로 별도의 레이턴시를 유발하지 않아야 함

## :checkered_flag: Definition of Done (DoD)
- [ ] 유/무료 조건별 데이터베이스 적재 상태 검증 완료

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (LLM 파싱)
- Blocks: #FE-WM-001 (클라이언트 렌더링 로직)
