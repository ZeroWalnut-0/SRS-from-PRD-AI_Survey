---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-RT-001: 포스트백 URL 설정 입력 폼 UI 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-RT-001] 포스트백 URL 설정 입력 폼 UI 구현
- 목적: 외부 패널 서비스 연동을 위해 설문 완료, 스크린아웃, 쿼터 마감 시에 해당하는 각각의 리다이렉트 URL을 입력받는 폼을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L537)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 3종 URL(Complete, Screenout, QuotaFull) 입력용 텍스트 필드 컴포넌트 구성
- [ ] 올바른 URL 형식(http/https)인지 클라이언트 정규식 밸리데이션 적용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: URL 유효성 검사 실패
- Given: 포스트백 설정 탭
- When: Complete URL 칸에 "invalid-string" 입력 후 저장 시도
- Then: "올바른 URL 주소를 입력해주세요." 안내와 함께 저장이 차단된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] API 연동 후 성공 토스트 메시지 노출 확인

## :construction: Dependencies & Blockers
- Depends on: #API-012
- Blocks: None
