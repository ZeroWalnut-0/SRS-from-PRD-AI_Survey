---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F1-001: HWPX 파서 텍스트 추출 정확도 테스트"
labels: 'feature, test, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F1-001] HWPX 파서 텍스트 추출 정확도 테스트
- 목적: HWPX 형식 문서에 포함된 표 내부 텍스트 및 문항 번호가 유실 없이 정규화되는지 Jest 기반의 Unit Test를 진행한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L222)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 테스트용 더미 HWPX 파일(문항 10개 포함) 준비
- [ ] `describe('HWPX Parser', ...)` 테스트 스위트 작성
- [ ] 추출된 텍스트의 단어 수, 개행 패턴이 원본과 일치하는지 `expect()` 단언문 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 텍스트 매칭
- Given: 샘플 설문 문서 `test_survey.hwpx`
- When: 파서 함수를 실행함
- Then: "Q1. 귀하의 성별은?" 텍스트가 정확히 반환된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 테스트 커버리지 80% 이상 달성

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-002
- Blocks: None
