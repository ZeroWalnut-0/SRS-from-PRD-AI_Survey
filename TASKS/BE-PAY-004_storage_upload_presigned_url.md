---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-004: ZIP 파일 스토리지 업로드 및 서명 URL 발급"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-004] ZIP 파일 스토리지 업로드 및 서명 URL 발급
- 목적: 컴파일된 ZIP 바이너리를 Supabase Storage에 안전하게 보관하고, 보안이 적용된 임시 다운로드 URL을 클라이언트에 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 제약사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase Storage SDK의 버킷 업로드 API 호출부 작성
- [ ] 10분(600초) 유효 기간을 갖는 Presigned URL 발급 헬퍼 함수 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 서명된 URL 테스트
- Given: 스토리지 업로드 완료
- When: Presigned URL 생성
- Then: 해당 URL을 통해 결제자 브라우저에서 즉각 다운로드가 시작된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 10분 경과 후 만료 여부 검사

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-003
- Blocks: #BE-PAY-005
