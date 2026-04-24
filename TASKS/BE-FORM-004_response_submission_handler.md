---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-004: 설문 응답 제출 및 무결성 검증 핸들러 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-004] 설문 응답 제출 및 무결성 검증 핸들러 구현
- 목적: 응답자가 모바일 폼을 통해 제출한 데이터를 수신하여 유효성을 검증하고, `RESPONSE` 테이블에 안전하게 저장한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-004_response_submission_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-004_response_submission_dto.md)
- 보안 요건: IP 해싱 (REQ-NF-017)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/forms/[form_id]/responses/route.ts` 구현
- [ ] 요청 데이터(`raw_record`) 유효성 검증:
    - 해당 폼의 `structure_schema`와 비교하여 필수 문항 응답 확인
    - 데이터 타입(String, Array 등) 일치 여부 확인
- [ ] 응답자 식별 정보 처리: `x-forwarded-for` 등에서 IP 추출 후 SHA-256 해싱 저장
- [ ] `RESPONSE` 레코드 생성 및 `quota_group` 분석
- [ ] 쿼터 도달 여부 사전 체크 (Soft Check) 및 후속 쿼터 카운트 증가(`BE-QT-003`) 연동 준비

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 응답 제출 성공
- Given: 필수 항목이 모두 채워진 응답 데이터
- When: 제출 API를 호출함
- Then: 201 Created와 함께 응답 ID가 반환되고 DB에 정확히 저장되어야 한다.

Scenario 2: 중복 제출 차단 (동일 IP)
- Given: 동일한 `ip_hash`를 가진 응답자가 짧은 시간 내에 재제출함
- When: 중복 방지 로직이 실행됨
- Then: 설정에 따라 제출을 차단하거나 기존 응답을 업데이트해야 한다 (정책 확인 필요).

## :gear: Technical & Non-Functional Constraints
- 성능: 응답 수집은 고부하 작업이 될 수 있으므로 인덱싱 및 쿼리 최적화에 집중한다 (REQ-NF-001).
- 보안: 원본 IP는 절대 저장하지 않으며 로그에도 남기지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-004` 규격에 맞는 요청/응답 처리가 완료되었는가?
- [ ] 서버 측 응답 무결성 검증 로직이 작동하는가?
- [ ] IP 해싱 및 익명화 처리가 올바르게 수행되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE), #API-004 (Submission DTO)
- Blocks: #BE-QT-003 (쿼터 증가 로직), #BE-PAY-003 (데이터맵 생성)
