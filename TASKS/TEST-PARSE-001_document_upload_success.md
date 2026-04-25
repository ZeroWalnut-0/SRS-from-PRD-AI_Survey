---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-001: 유효 문서 업로드 및 파싱 성공 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-001] 유효 문서 업로드 성공 테스트
- 목적: 정상적인 HWPX/Word/PDF 파일을 업로드했을 때, 예외 없이 `PARSED_FORM` 레코드가 생성되고 상태가 `COMPLETED`로 전이되는지 E2E 관점에서 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L477)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Playwright 기반 E2E 테스트 스크립트 작성 (`/tests/e2e/upload.spec.ts`)
- [ ] Mock 데이터를 활용한 파일 드롭 이벤트 시뮬레이션
- [ ] API 응답 인터셉트(Intercept) 및 HTTP 200 OK 상태 코드 확인
- [ ] DB 검증 로직: `Prisma.document.findUnique`를 통한 `status='COMPLETED'` 확인
- [ ] 생성된 `structure_schema`의 JSON 필드 누락 여부 검사 (Zod Schema 기반)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: HWPX 파싱 성공
- Given: 유효한 HWPX 샘플 파일 (문항 10개 포함)
- When: 랜딩 페이지의 업로드 영역에 드롭 후 파싱 요청
- Then: 로딩 바가 100%에 도달하고, `doc_id`를 포함한 200 응답을 수신한다.

Scenario 2: DOCX 파싱 성공
- Given: 유효한 DOCX 샘플 파일
- When: 파일 선택 창을 통해 업로드 시도
- Then: `COMPLETED` 상태로 정상 전환되며 폼 에디터로 자동 진입한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 3가지 파일 포맷(HWPX, DOCX, PDF)에 대해 각각 최소 1회 이상 E2E 테스트 통과
- [ ] DB에 적재된 문항 수가 원본 파일의 문항 수와 일치하는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: None

