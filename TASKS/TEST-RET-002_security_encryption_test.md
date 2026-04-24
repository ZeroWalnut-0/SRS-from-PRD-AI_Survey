---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-RET-002: 저장 데이터 암호화(Encryption at-rest) 검증 테스트"
labels: 'test, security, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-RET-002] 저장 데이터 암호화(Encryption at-rest) 검증 테스트
- 목적: Supabase PostgreSQL 및 Storage에 저장된 모든 데이터가 물리적으로 암호화되어 보호되고 있는지, 그리고 통신 시 TLS 1.2+가 강제되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #NFR-SEC-001, #NFR-SEC-002
- 성공 기준: TC-FUNC-030

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: Supabase 대시보드 내 PostgreSQL 암호화 설정 상태 확인
- [ ] 시나리오 2: API 호출 시 HTTPS TLS 버전 검사 (1.2 미만 거절 확인)
- [ ] 시나리오 3: 비인가 경로를 통한 데이터 파일 직접 접근 차단 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 보안 스캐닝 도구 또는 브라우저 개발자 도구
- When: 서비스 엔드포인트에 접속함
- Then: 연결 정보가 TLS 1.3 또는 1.2로 표시되어야 하며, 데이터베이스 파일에 대한 물리적 탈취 시도가 무의미함을 확인한다 (매니지드 서비스 설정 기반).

## :gear: Technical Constraints
- 도구: SSL Labs Scan, Supabase Security Audit UI

## :checkered_flag: Definition of Done (DoD)
- [ ] 저장 및 전송 중인 모든 데이터의 보안 수준이 SRS 요구사항을 충족하는가?
- [ ] 암호화되지 않은 평문 통신 경로가 존재하지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RET-001, #NFR-SEC-001 (TLS)
- Blocks: None
