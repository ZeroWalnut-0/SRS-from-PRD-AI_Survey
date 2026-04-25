---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-005: RESPONSE 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-005] RESPONSE 테이블 스키마 및 마이그레이션 작성
- 목적: 설문 참여자들의 응답 본문과 유효성 검증 상태(AI Data Bouncer)를 기록할 `RESPONSE` 테이블을 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L756)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `Response` 모델 작성 (`id`, `form_id`, `raw_record`, `ip_hash`, `quota_status`, `duration_seconds`)
- [ ] `quota_status` 필드 Enum화 (`VALID`, `SCREENOUT`, `SUSPECT`, `QUOTAFULL`)
- [ ] IP 해시값 저장을 위한 문자열 컬럼 길이 지정 (SHA-256 규격 확보)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 참여자 응답 저장
- Given: 설문 문항 답변 및 소요 시간 데이터가 전달됨
- When: Response 테이블에 기록됨
- Then: 레코드가 정상 생성되며 PK가 발급된다.

## :gear: Technical & Non-Functional Constraints
- 보안: IP 정보를 평문으로 저장하지 않고 해시화된 상태로 저장

## :checkered_flag: Definition of Done (DoD)
- [ ] Prisma 스키마 상의 Relation 설정 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-004
- Blocks: #BE-FORM-004
