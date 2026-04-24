---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-001: 문서 업로드 UI 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-001] 문서 업로드 UI 구현
- 목적: 사용자가 HWPX, Word, PDF 파일을 편리하게 업로드할 수 있는 드래그 앤 드롭 영역 및 파일 선택 인터페이스를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-001`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 컴포넌트: `shadcn/ui` (Dropzone)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-001_document_upload_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-001_document_upload_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/parser/UploadZone.tsx` 컴포넌트 생성
- [ ] 드래그 앤 드롭 영역 구현 (React Dropzone 등 활용)
- [ ] 클라이언트 측 파일 검증 로직 구현:
    - 확장자 체크: .hwpx, .docx, .pdf 만 허용
    - 크기 체크: 최대 5MB (REQ-FUNC-001)
- [ ] 파일 선택 시 즉시 업로드 API (`POST /api/v1/documents/upload`) 호출 연동
- [ ] 업로드 진행 상태 표시 (Progress Bar)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파일 드래그 앤 드롭 성공
- Given: 지원되는 형식의 3MB 파일이 준비됨
- When: 업로드 영역에 파일을 드롭함
- Then: 파일 검증을 통과하고 업로드 API 호출이 시작되어야 한다.

Scenario 2: 지원하지 않는 확장자 차단
- Given: `.txt` 파일 또는 `.hwp` 파일이 준비됨
- When: 업로드를 시도함
- Then: 클라이언트 측에서 즉시 차단되고 사용자에게 안내 메시지를 표시해야 한다. (HWP의 경우 별도 모달 유도)

## :gear: Technical & Non-Functional Constraints
- UI/UX: `shadcn/ui` 스타일을 준수하여 일관된 디자인 제공.
- 성능: 파일 검증은 즉각적으로 수행되어야 함.

## :checkered_flag: Definition of Done (DoD)
- [ ] 드래그 앤 드롭 및 파일 선택 기능이 정상 작동하는가?
- [ ] 확장자 및 크기 검증 로직이 정확히 동작하는가?
- [ ] 업로드 API와의 연동이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-001 (Mock API), #API-001 (Upload DTO)
- Blocks: #FE-PARSE-002 (로딩 UI), #FE-PARSE-005 (에러 모달)
