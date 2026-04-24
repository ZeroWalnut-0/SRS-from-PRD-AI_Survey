---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Cost] NFR-COST-001: 단건 파싱 원가 검증 및 모니터링 스크립트"
labels: 'infrastructure, cost, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-COST-001] 단건 파싱 원가 검증 및 모니터링 스크립트
- 목적: Gemini API 호출 시 발생하는 토큰 사용량을 기반으로 파싱 1건당 발생하는 원가를 계산하고, 목표치(20원 이내)를 유지하는지 감시한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.4_REQ-NF-021`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] AI 파싱 API 응답에서 `usage` 필드(Input/Output tokens) 추출 로직 추가
- [ ] 현재 Gemini API 단가(예: $0.125 / 1M tokens) 기반의 KRW 환산 로직 작성
- [ ] `AUDIT_LOG`의 `details` 필드에 각 요청당 계산된 비용 기록
- [ ] 일간 평균 파싱 원가 집계 쿼리 작성
- [ ] 목표 단가(20원) 초과 시 알림 트리거 설정

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 평균적인 문서(약 2,000 토큰) 파싱 완료
- When: 원가 계산 로직을 실행함
- Then: 계산된 금액이 원화 기준 20원 이하로 산출되어야 하며, 이 데이터가 로그에 기록되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 정확성: 환율 변동 및 API 단가 변경에 대응할 수 있도록 상수로 관리한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 파싱 원가 측정 및 기록 시스템이 가동 중인가?
- [ ] 목표 원가 준수 여부를 상시 확인 가능한가?
- [ ] 고비용 요청 발생 시 원인 분석(문서 크기 등)이 가능한가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: None
