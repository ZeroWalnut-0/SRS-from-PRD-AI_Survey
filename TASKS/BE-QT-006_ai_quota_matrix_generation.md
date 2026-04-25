---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-006: AI 기반 쿼터 할당표 자동 생성"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-006] AI 기반 쿼터 할당표 자동 생성
- 목적: 사용자의 자연어 요청("전국 성별 연령 500명 할당표 짜줘")을 입력받아 인구통계학적 데이터를 기반으로 비례 배분된 교차 쿼터 매트릭스를 AI를 통해 자동 구성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L529)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Vercel AI SDK를 활용하여 프롬프트 기반 통계적 쿼터 비율 추론 로직 구성
- [ ] Zod 기반 쿼터 매트릭스 포맷(`quota_matrix`) 반환 규격 정의
- [ ] 사용자의 전체 조사 모수(N=)에 따른 셀별 정수형 인원수 변환 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 자연어 기반 생성 성공
- Given: "수도권 2030 남녀 300명 할당" 프롬프트가 주어짐
- When: AI 생성 API가 실행됨
- Then: 총합이 300이 되는 구조화된 JSON 할당표 데이터가 200 OK로 반환된다.

## :gear: Technical & Non-Functional Constraints
- 비용: Gemini API 호출 쿼터 제한 관리

## :checkered_flag: Definition of Done (DoD)
- [ ] 생성된 할당 모수의 총합과 사용자가 요청한 모수가 정확히 일치하는지 확인

## :construction: Dependencies & Blockers
- Depends on: #API-010
- Blocks: #FE-QT-004
