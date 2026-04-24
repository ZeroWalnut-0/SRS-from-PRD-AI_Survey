---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Infra] NFR-INFRA-004: Supabase 프로젝트 생성 및 인프라 초기화"
labels: 'infrastructure, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-004] Supabase 프로젝트 생성 및 인프라 초기화
- 목적: 데이터베이스(PostgreSQL), 인증(Auth), 저장소(Storage) 기능을 제공하는 Supabase 프로젝트를 설정한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-003`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase Dashboard에서 새 프로젝트 생성 (Region: Seoul 선택 권장)
- [ ] 데이터베이스 접속 정보(Connection String) 확보
- [ ] Authentication 설정: 이메일 가입 활성화, 리다이렉트 URL 설정
- [ ] Storage 버킷 생성: `documents` (원본 문서용), `packages` (최종 ZIP용)
- [ ] API 권한 설정: Service Role Key 및 Anon Key 관리

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Supabase 프로젝트 생성 완료
- When: 외부 SQL 클라이언트 또는 Prisma를 통해 접속을 시도함
- Then: 데이터베이스 연결이 성공해야 하며, 빈 스키마 상태가 확인되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `Service Role Key`는 절대 클라이언트 측에 노출하지 않는다.
- 데이터: Storage 버킷의 Public/Private 권한을 용도에 맞게 철저히 분리한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Supabase 프로젝트가 정상 가동 중인가?
- [ ] 필수 버킷 및 인증 설정이 완료되었는가?
- [ ] DB 연결 속도가 허용 범위 내인가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-001
- Blocks: #DB-001, #NFR-INFRA-005
