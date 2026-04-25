---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-SEC-004: 응답자 IP 해싱(비식별화) 처리 로직 구현 및 검증"
labels: 'feature, security, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-SEC-004] 응답자 IP 해싱(비식별화) 처리 로직 구현 및 검증
- 목적: 응답자의 개인정보(IP 주소) 노출을 방지하기 위해 SHA-256 단방향 해싱을 거쳐 중복 검사용 토큰으로만 활용한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 제약사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L829)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `crypto` 내장 모듈을 이용한 `hashIP(ip, salt)` 유틸리티 함수 작성
- [ ] 설문 제출 API 진입 시 원본 IP를 변환하여 `RESPONSE.ip_hash` 필드에 매핑

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: IP 비식별화
- Given: 클라이언트 IP `127.0.0.1`
- When: 설문 응답 적재
- Then: DB에 `127.0.0.1` 문자열은 저장되지 않고, 64자 해시 스트링이 저장된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 솔트(Salt) 값을 이용해 레인보우 테이블 공격 방어 여부 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-004, #DB-005
- Blocks: None
