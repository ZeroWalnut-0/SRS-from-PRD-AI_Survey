---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RET-001: Zero-Retention 데이터 삭제 스케줄러 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RET-001] Zero-Retention 데이터 삭제 스케줄러 구현
- 목적: 개인정보 보호 및 저장소 최적화를 위해 업로드된 문서와 파편 데이터를 생성 24시간 후 자동 영구 파기(Zero-Retention)한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L556)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `expires_at ≤ NOW()` 조건에 맞는 문서 ID 조회 쿼리 작성
- [ ] Supabase Storage 연동 객체 삭제 API 연동
- [ ] DB 내 해당 레코드 완전 삭제(Hard Delete) 또는 익명화 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 24시간 지난 문서 자동 파기
- Given: 24시간 전에 생성되어 작업이 종료된 문서가 존재함
- When: 삭제 스케줄러 프로세스가 구동됨
- Then: DB와 클라우드 스토리지 양측 모두에서 파일이 완전 소거된다.

## :gear: Technical & Non-Functional Constraints
- 보안: 삭제 로그 기록 및 복구 불가한 완전 파기 수행

## :checkered_flag: Definition of Done (DoD)
- [ ] 스케줄러 수동 실행을 통한 파일 삭제 정상 동작 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-003, #DB-010
- Blocks: #BE-RET-002
