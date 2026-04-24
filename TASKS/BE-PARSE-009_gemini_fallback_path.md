---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-009: Gemini API Fallback 파싱 경로 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
-功能명: [BE-PARSE-009] Gemini API Fallback 파싱 경로 구현
- 목적: 메인 AI 엔진(Gemini API)의 장애 또는 할당량 초과 시, 기본적인 텍스트 추출 라이브러리를 활용하여 최소한의 파싱 결과를 제공함으로써 서비스 가용성을 확보한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1_EXT-07`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md) (Fallback 전략)
- 관련 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#REQ-FUNC-006`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Gemini API 호출 실패(Exception/Timeout) 감지 로직 구현
- [ ] Fallback 파싱 엔진 활성화:
    - 라이브러리(`pdf-parse`, `mammoth`, `jszip`)에서 추출된 순수 텍스트 활용
    - 텍스트 개행 문자를 기준으로 임시 설문 문항(주관식 위주) 생성 로직 구현
- [ ] Fallback 상태임을 기록하여 사용자에게 "정밀 파싱 실패로 인한 기본 텍스트 추출" 안내 제공
- [ ] Fallback 모드 실행 시 AUDIT_LOG 기록

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: Gemini API 장애 발생 시 자동 전환
- Given: Gemini API Key가 무효하거나 네트워크 장애가 발생함
- When: 문서 파싱을 시도함
- Then: 시스템이 중단되지 않고 Fallback 로직이 실행되어 텍스트 데이터가 추출되어야 한다.

Scenario 2: Fallback 결과물의 유효성
- Given: Fallback 모드로 파싱이 완료됨
- When: 생성된 설문 폼을 확인함
- Then: AI 기반의 정밀한 구조화는 부족하더라도, 원본의 텍스트 내용은 모두 포함되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 가용성: 메인 엔진 장애 시에도 서비스 치명률을 0.5% 이하로 유지하기 위한 핵심 전략이다 (REQ-NF-009).
- 성능: Fallback 파싱은 AI 호출이 없으므로 레이턴시 ≤ 3,000ms를 유지한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Gemini API 에러 핸들링 및 자동 전환 로직이 구현되었는가?
- [ ] 로컬 라이브러리 기반의 텍스트 추출 결과가 성공적으로 저장되는가?
- [ ] Fallback 실행 로그가 남는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (AI SDK 연동)
- Blocks: None
