---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Perf] NFR-PERF-002: 문서 파싱 레이턴시 벤치마크 테스트"
labels: 'infrastructure, performance, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-PERF-002] 문서 파싱 레이턴시 벤치마크 테스트
- 목적: 문서 업로드부터 AI 파싱 완료까지의 전체 소요 시간을 측정하여, 비기능 요구사항(15초 이내)을 충족하는지 검증한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.1_REQ-NF-002`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 샘플 문서(10문항, 30문항, 50문항)별 파싱 시간 측정 스크립트 작성
- [ ] 네트워크 지연을 포함한 E2E(End-to-End) 시간 측정
- [ ] Gemini API 응답 지연 시간과 전처리 시간의 비중 분석
- [ ] 15초 초과 시의 사용자 UI(스켈레톤 연장 표시) 트리거 지점 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 평균 30문항 규모의 HWPX 문서
- When: 파싱을 요청함
- Then: 전체 파이프라인(업로드 -> 전처리 -> AI -> 저장) 완료까지 총 15,000ms를 초과하지 않아야 한다.

## :gear: Technical & Non-Functional Constraints
- 정확성: Vercel의 10초 타임아웃 제약을 극복하기 위해 비동기 처리 및 폴링(Polling) 구조가 정상 작동하는지 함께 확인한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 문서 규모별 파싱 벤치마크 결과가 확보되었는가?
- [ ] 15초 이내 파싱 목표가 달성되었는가?
- [ ] 지연 발생 구간에 대한 분석이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: None
