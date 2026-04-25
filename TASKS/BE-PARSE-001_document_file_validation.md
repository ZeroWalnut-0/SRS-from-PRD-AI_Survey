---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-001: 문서 파일 서버 측 검증 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-001] 문서 파일 서버 측 검증 로직 구현
- 목적: 업로드된 파일의 확장자(HWPX, DOCX, PDF), 파일 크기(5MB 이하), 암호화 여부, 파일 손상 여부를 서버 측에서 엄격하게 검증하여 비정상 데이터의 시스템 유입을 차단한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L711)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js Route Handler `POST /api/v1/documents/upload` 내 파일 검증 모듈 구현
- [ ] 파일 크기 체크 로직 구현 (5MB 초과 시 즉시 차단)
- [ ] 파일 확장자 체크 로직 구현 (HWPX, DOCX, PDF 외 확장자 필터링)
- [ ] 파일 매직 바이트(Magic Byte) 분석을 통한 파일 변조/손상 탐지
- [ ] 검증 실패 시 `DOCUMENT` 테이블에 `status='FAILED'` 및 에러 코드 저장

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 파일 검증 통과
- Given: 5MB 이하의 정상적인 `.docx` 파일이 주어짐
- When: 파일 업로드 API가 호출됨
- Then: 검증을 통과하고 DB에 `DOCUMENT` 레코드가 `PENDING` 상태로 생성된다.

Scenario 2: 크기 제한 초과
- Given: 10MB 용량의 파일이 주어짐
- When: 파일 업로드 API가 호출됨
- Then: 400 Bad Request 응답과 함께 크기 제한 에러를 반환한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 파일 검증에 소요되는 레이턴시 ≤ 1,000ms 보장
- 보안: 서버 리소스 고갈 공격(Zip Bomb 등) 방지 대책 마련

## :checkered_flag: Definition of Done (DoD)
- [ ] 파일 유효성 검증 통합 테스트 수행 및 통과
- [ ] 에러 메시지 및 HTTP Status Code 규격 준수 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-003 (DOCUMENT 스키마), #API-001
- Blocks: #BE-PARSE-002, #BE-PARSE-003, #BE-PARSE-004
