---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-002: 파싱 완료 상태 조회 Mock 데이터 작성"
labels: 'mock, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-002] 파싱 완료 상태 조회 Mock 데이터 작성
- 목적: Gemini API 연동 전에 프론트엔드가 폼 에디터 UI를 조립할 수 있도록 표준 `structure_schema` JSON 객체 샘플을 구축한다.

## :link: References (Spec & Context)
- API 규격: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `GET /api/v1/documents/{doc_id}/status`에 대응하는 정적 JSON 파일 생성
- [ ] 객관식/주관식/매트릭스 문항이 모두 포함된 10문항 규모의 스키마 작성

## :checkered_flag: Definition of Done (DoD)
- [ ] 프론트엔드 폼 렌더러에 Mock 데이터 주입 시 에러 없이 렌더링 확인

## :construction: Dependencies & Blockers
- Depends on: #API-002, #API-003
- Blocks: #FE-PARSE-006
