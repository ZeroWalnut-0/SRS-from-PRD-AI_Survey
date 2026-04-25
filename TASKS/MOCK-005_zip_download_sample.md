---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-005: ZIP 다운로드 Mock API 및 서명 URL 작성"
labels: 'mock, foundation, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-005] ZIP 다운로드 Mock API 작성
- 목적: 실제 Storage 업로드 로직이 구현되기 전, 클라이언트가 다운로드 버튼을 눌렀을 때 동작할 수 있도록 가상의 `presigned_url`을 리턴하는 Mock API를 설계한다.

## :link: References (Spec & Context)
- API 규격: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `GET /api/v1/packages/{package_id}/download` 응답 정의
- [ ] 테스트용 더미 ZIP 파일 리소스 준비

## :checkered_flag: Definition of Done (DoD)
- [ ] 다운로드 버튼 클릭 시 브라우저의 기본 다운로드 동작 실행 검증

## :construction: Dependencies & Blockers
- Depends on: #API-009
- Blocks: None
