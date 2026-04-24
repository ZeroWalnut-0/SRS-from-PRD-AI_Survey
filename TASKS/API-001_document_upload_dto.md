---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-001: Document 업로드 API 계약 정의"
labels: 'feature, foundation, api, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-001] Document 업로드 API 계약 정의
- 목적: 비정형 문서(HWPX, Word, PDF)를 업로드하고 파싱 프로세스를 시작하기 위한 API의 요청/응답 규격 및 DTO를 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/documents/upload`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `multipart/form-data` 형식 (file: File)
- [ ] 응답 DTO 정의: `{ doc_id: string, status: DocumentStatus }`
- [ ] 에러 코드 정의:
    - 400: 유효하지 않은 파일 형식, 크기 초과, 파일 손상
    - 429: 일일 파싱 한도 초과 (Rate Limit)
- [ ] TypeScript 인터페이스/타입 선언 파일 생성 (`types/api/documents.ts`)
- [ ] 클라이언트에서 호출 시 사용할 Zod 검증 스키마 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 업로드 요청
- Given: 유효한 HWPX 파일이 준비됨
- When: `POST /api/v1/documents/upload`로 요청함
- Then: 200 OK와 함께 고유한 `doc_id`를 반환해야 한다.

Scenario 2: 한도 초과 요청
- Given: 무료 계정의 일일 파싱 횟수(3회)를 모두 소진함
- When: 추가 업로드를 시도함
- Then: 429 Too Many Requests와 함께 안내 메시지를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 업로드 요청 수신 및 `doc_id` 발급까지 2초 이내 완료 (REQ-NF-007)
- 제약: 파일 크기는 최대 5MB로 제한한다 (REQ-FUNC-001)

## :checkered_flag: Definition of Done (DoD)
- [ ] API 요청/응답 DTO가 SRS 규격대로 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 에러 케이스에 대한 명세가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003 (DOCUMENT 테이블), #DB-011 (Enum 정의)
- Blocks: #BE-PARSE-001 (업로드 로직 구현), #MOCK-001 (Mock API)
