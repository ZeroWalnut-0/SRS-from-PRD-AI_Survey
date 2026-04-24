---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-001: AI 파싱 정확도 및 문항 추출 검증 테스트"
labels: 'test, backend, ai, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-001] AI 파싱 정확도 및 문항 추출 검증 테스트
- 목적: 다양한 유형의 문서(HWPX, Word, PDF)를 입력했을 때, AI가 설문 문항과 선택지를 누락 없이 정확한 구조로 추출하는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-002`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 관련 태스크: #BE-PARSE-005 (AI SDK 연동)
- 성공 기준: 추출 성공률 95% 이상 (REQ-FUNC-002)

## :white_check_mark: Test Scenarios (검증 시나리오)
- [ ] `tests/integration/parser.accuracy.test.ts` 테스트 스크립트 작성
- [ ] 시나리오 1: 표준 객관식 문항 추출 (단일/복수 선택)
- [ ] 시나리오 2: 주관식 문항 및 안내 문구 구분 확인
- [ ] 시나리오 3: 5점/7점 척도형 문항의 단계 정보 추출 확인
- [ ] 시나리오 4: 특수 기호(①, ②, ⓐ 등)가 포함된 문항의 텍스트 정제 확인
- [ ] 시나리오 5: 표(Table) 내부에 포함된 문항 추출 여부 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 10개의 문항이 포함된 테스트용 HWPX 문서
- When: AI 파싱 프로세스를 실행함
- Then: 반환된 `structure_schema` 내에 10개의 문항 객체가 존재해야 하며, 각 문항의 텍스트와 선택지 내용이 원본과 95% 이상 일치해야 한다.

## :gear: Technical & Non-Functional Constraints
- 도구: Vitest 활용 (Node.js 환경의 고속 테스트 지원)
- 데이터: `MOCK-001`에서 준비한 3종 샘플 파일 사용
- 비용: 테스트 실행 시마다 실제 API 호출이 발생하므로, 캐시(`BE-PARSE-010`)를 활용하여 불필요한 비용 발생 방지

## :checkered_flag: Definition of Done (DoD)
- [ ] 3종 확장자에 대해 각각 최소 5회 이상의 파싱 테스트가 통과하는가?
- [ ] 문항 타입 매핑이 의도대로(Select, Text, Scale 등) 이루어지는가?
- [ ] 테스트 결과 리포트가 생성되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (AI SDK 연동), #MOCK-001 (샘플 데이터)
- Blocks: #NFR-PERF-002 (파싱 레이턴시 벤치마크)
