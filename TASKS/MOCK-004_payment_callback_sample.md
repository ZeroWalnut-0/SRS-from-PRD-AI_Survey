---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-004: 결제 요청/콜백 Mock API 응답 작성"
labels: 'mock, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-004] 결제 요청/콜백 Mock API 응답 작성
- 목적: 토스페이먼츠 연동 시 발생할 수 있는 다양한 성공/실패/중단 시나리오를 프론트엔드에서 사전에 대응할 수 있게 응답 값을 모킹한다.

## :link: References (Spec & Context)
- 기술 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L461)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 성공 시나리오: `paymentKey`, `orderId`, `amount` 일치 페이로드
- [ ] 실패 시나리오: 한도 초과, 잔액 부족 에러 응답 모킹

## :checkered_flag: Definition of Done (DoD)
- [ ] 프론트엔드 결제 라우팅 분기 테스트 성공

## :construction: Dependencies & Blockers
- Depends on: #API-007, #API-008
- Blocks: #FE-PAY-001
