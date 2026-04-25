---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-COST-001: 단건 파싱 원가 ≤ 20원(KRW) 검증 스크립트"
labels: 'feature, nfr, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-COST-001] 단건 파싱 원가 검증 스크립트
- 목적: Gemini API 호출 시 사용된 Input/Output 토큰 수를 기록하고, 환율을 반영하여 실제 파싱 원가가 예산(20원) 이하인지 측정한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 비용 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L611)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Gemini SDK 응답 메타데이터의 `usageMetadata` 추출
- [ ] 토큰당 단가(USD) x 환율 변환 알고리즘 구현 및 `AUDIT_LOG` 기록

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 원가 측정
- Given: 10문항 규모의 HWPX 파싱
- When: 처리 완료
- Then: `AUDIT_LOG`에 기록된 예상 원가가 20원 이하(예: 약 1.5원)로 찍힌다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 토큰 집계 누락 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: None
