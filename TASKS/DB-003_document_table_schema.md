---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-003: DOCUMENT 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-003] DOCUMENT 테이블 스키마 및 마이그레이션 작성
- 목적: 사용자가 업로드한 문서의 메타데이터, 파싱 상태 및 유효기간 정보를 관리하기 위한 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1_DOCUMENT`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 보안 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.7_REQ-FUNC-029`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md) (Zero-Retention)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `Document` 모델 정의
- [ ] 필수 필드 추가: `doc_id` (UUID), `user_id` (FK), `file_type` (Enum), `file_name`, `file_size_bytes`, `file_hash`, `parsed_success`, `status` (Enum), `expires_at`
- [ ] `expires_at` 필드에 대한 기본값 설정 로직 검토 (생성 후 24시간)
- [ ] `User` 모델과의 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: Document 레코드 생성
- Given: 업로드된 파일의 메타데이터가 준비됨
- When: DB에 `Document` 레코드를 생성함
- Then: 모든 필드가 올바른 타입으로 저장되어야 하며, `expires_at`이 생성 시점 기준 24시간 후로 설정되어야 한다.

Scenario 2: 파일 해시 유니크성 확인 (선택 사항)
- Given: 동일한 파일이 업로드됨
- When: `file_hash`를 기반으로 조회함
- Then: 캐시 활용을 위해 기존 레코드를 찾을 수 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: Zero-Retention 정책을 위해 `expires_at` 필드를 인덱싱하여 삭제 스케줄러 성능을 확보한다.
- 성능: `file_hash` 필드에 인덱스를 추가하여 중복 파일 조회 속도를 높인다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 SRS 명세대로 Document 모델이 반영되었는가?
- [ ] 마이그레이션이 성공적으로 수행되어 테이블이 생성되었는가?
- [ ] `expires_at` 필드가 24시간 영구 삭제 정책을 지원하도록 설계되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-002 (USER 테이블), #DB-011 (Enum 정의)
- Blocks: #DB-004 (PARSED_FORM 테이블), #BE-PARSE-001 (문서 검증 로직)
