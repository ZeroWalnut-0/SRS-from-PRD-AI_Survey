---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-001: 설문 폼 조회 API 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-001] 설문 폼 조회 API (`GET /api/v1/forms/{form_id}`)
- 목적: 파싱 및 생성이 완료된 설문 폼의 문항 구조 스키마 및 바이럴 워터마크 URL을 안전하게 클라이언트로 서빙한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L713)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js App Router 기반 API Route Handler 구현 (`/app/api/v1/forms/[form_id]/route.ts`)
- [ ] Prisma Client를 활용하여 Supabase PostgreSQL에서 `form_id`를 PK로 하는 데이터 조회 로직 구현
- [ ] `structure_schema` 내 문항 데이터 JSON 무손실 파싱 및 직렬화 처리
- [ ] `viral_watermark_url` 유무 및 유효성 확인
- [ ] 404 Not Found 및 500 Internal Server Error 예외 처리 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 존재하는 설문 폼 정상 조회
- Given: 유효하게 저장된 설문 폼 ID(`valid-form-id`)가 주어짐
- When: `GET /api/v1/forms/valid-form-id`로 요청함
- Then: 200 OK 응답과 함께 `structure_schema`와 `viral_watermark_url`이 반환된다.

Scenario 2: 존재하지 않는 설문 폼 조회 시도
- Given: DB에 등록되지 않은 설문 폼 ID(`non-exist-id`)가 주어짐
- When: `GET /api/v1/forms/non-exist-id`로 요청함
- Then: 404 Not Found 에러 코드와 함께 지정된 에러 메시지를 반환한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 응답시간 p95 ≤ 500ms 달성
- 안정성: 데이터베이스 커넥션 풀 관리 및 불필요한 오버헤드 방지

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 Acceptance Criteria를 충족하는가?
- [ ] 단위 테스트(Unit Test) 작성이 완료되고 통과했는가?
- [ ] Swagger 규격(DTO 구조)과 실제 응답 포맷이 일치하는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 스키마), #API-003 (Form 도메인 계약)
- Blocks: #FE-FORM-001 (폼 에디터 문항 상태 관리 연동)
