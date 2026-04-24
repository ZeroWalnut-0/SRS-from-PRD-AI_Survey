---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-010: 파일 해시 기반 파싱 캐시 조회 로직 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-010] 파일 해시 기반 파싱 캐시 조회 로직 구현
- 목적: 동일한 파일이 중복 업로드될 경우, AI 파이프라인을 재실행하지 않고 기존 DB에 저장된 파싱 결과를 재사용하여 비용을 절감하고 응답 속도를 향상시킨다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-028`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- ADR 결정: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md#L445`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md) (Vercel KV 대신 Supabase DB 캐시 활용)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 파일 업로드 시 SHA-256 해시 생성 로직 구현
- [ ] `DOCUMENT` 테이블에서 동일한 `file_hash`를 가진 `status='COMPLETED'` 레코드 검색
- [ ] 캐시 히트(Hit) 시:
    - 기존 `PARSED_FORM` 데이터를 복제하거나 참조하여 즉시 `doc_id` 반환
    - AI 파서(`BE-PARSE-005`) 호출 건너뜀
- [ ] 캐시 미스(Miss) 시: 일반 파싱 프로세스 진행
- [ ] 캐시 사용 시 AUDIT_LOG 기록 (action=CACHE_HIT)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 중복 파일 업로드 시 속도 향상
- Given: 이미 파싱이 완료된 `A.hwpx` 파일이 존재함
- When: 동일한 파일을 다시 업로드함
- Then: AI 호출 없이 1초 이내에 기존 결과를 반환해야 한다.

Scenario 2: 내용이 수정된 파일 업로드 (Hash 변경)
- Given: 파일 명은 같으나 내용이 일부 수정된 파일이 업로드됨
- When: 해시를 계산함
- Then: 기존 해시와 다르므로 캐시 히트가 발생하지 않고 신규 파싱이 시작되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 비용: 중복 파싱 방지를 통해 Gemini API 호출 원가를 절감한다 (REQ-NF-021).
- 정확성: 해시 충돌 가능성이 극히 낮은 SHA-256 알고리즘을 사용한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 파일 해시 생성 및 DB 조회 로직이 구현되었는가?
- [ ] 캐시 히트 시 AI 파이프라인이 정상적으로 건너뛰어지는가?
- [ ] 성능 향상(1초 이내 응답)이 확인되었는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001 (서버 검증), #DB-003 (DOCUMENT 테이블)
- Blocks: #TEST-PARSE-009 (캐시 검증 테스트)
