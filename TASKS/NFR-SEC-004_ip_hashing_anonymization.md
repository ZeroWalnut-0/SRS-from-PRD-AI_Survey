---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Sec] NFR-SEC-004: 응답자 IP 해싱 및 개인정보 비식별화 구현"
labels: 'infrastructure, security, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-SEC-004] 응답자 IP 해싱 및 개인정보 비식별화 구현
- 목적: 중복 참여 방지 및 쿼터 체크를 위해 수집되는 응답자의 IP 주소를 원본 그대로 저장하지 않고, 해싱 처리를 통해 개인정보 유출 위험을 최소화하고 GDPR/개인정보보호법을 준수한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3_RESPONSE.ip_hash`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 관련 태스크: #BE-FORM-004 (응답 제출 핸들러)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js `x-forwarded-for` 헤더를 통한 실제 클라이언트 IP 추출 로직 구현
- [ ] Node.js 내장 `crypto` 모듈을 사용한 SHA-256 해싱 유틸리티 작성 (`lib/utils/hash.ts`)
- [ ] 환경 변수(`IP_HASH_SALT`)를 활용한 솔트 추가 로직 (레인보우 테이블 공격 방지)
- [ ] `RESPONSE` 테이블 저장 시 원본 IP는 버리고 해싱된 `ip_hash`만 전달
- [ ] 중복 참여 방지(REQ-FUNC-020) 로직에서 해싱된 값을 비교 기준으로 사용하도록 통합

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 동일한 IP를 가진 사용자가 두 번 설문을 제출함
- When: 서버가 각 응답의 `ip_hash`를 생성함
- Then: 두 응답의 `ip_hash` 값은 동일해야 하며, DB에는 실제 IP 주소를 유추할 수 없는 64자리의 16진수 문자열이 저장되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 솔트(Salt) 값은 소스 코드에 노출하지 않고 환경 변수로 엄격히 관리한다.
- 성능: 해싱 연산 레이턴시 ≤ 10ms.
- 법규: 개인정보 비식별화 기술 가이드라인(KISA)의 단방향 해시 알고리즘 권고 사항을 준수한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `lib/utils/hash.ts` 공통 유틸리티가 작성되었는가?
- [ ] `RESPONSE.ip_hash` 필드에 해시 값이 정상 적재되는가?
- [ ] 로컬/Vercel 환경에서 환경 변수 기반 솔트가 올바르게 적용되는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-005 (환경 변수 관리), #BE-FORM-004 (응답 제출 서비스)
- Blocks: #TEST-QT-002 (쿼터 체크 테스트)
