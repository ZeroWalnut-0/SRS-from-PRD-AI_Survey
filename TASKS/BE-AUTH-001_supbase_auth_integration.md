---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-AUTH-001: Supabase Auth 설정 및 초기화"
labels: 'feature, backend, infrastructure, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-AUTH-001] Supabase Auth 설정 및 초기화
- 목적: Supabase 프로젝트 내에서 인증 기능을 활성화하고, 이메일 템플릿, 비밀번호 정책 등을 설정하여 백엔드 인증 기반을 마련한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-003`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase Dashboard 내 Authentication 설정 활성화
- [ ] 이메일 기반 가입(Signup) 활성화 및 인증 메일 발송 설정
- [ ] 비밀번호 정책 설정 (최소 길이, 대소문자 포함 등)
- [ ] 환경 변수(`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`) Next.js 프로젝트 설정
- [ ] 서버 측 관리용 `SUPABASE_SERVICE_ROLE_KEY` 설정 (제한적 활용)
- [ ] 로그아웃 후 세션 파기 정책 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: Supabase 연결 테스트
- Given: 환경 변수 설정 완료
- When: Supabase Client 인스턴스를 생성함
- Then: 인증 관련 메서드(`signUp`, `signIn`) 호출이 가능한 상태여야 한다.

Scenario 2: 인증 메일 발송 확인
- Given: 신규 회원가입 시도
- When: Supabase가 이메일 발송을 트리거함
- Then: 지정된 사용자 이메일로 정상적으로 인증 링크가 도달해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `SERVICE_ROLE_KEY`는 절대 클라이언트 측에 노출되지 않도록 서버 컴포넌트나 Route Handler에서만 사용한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Supabase Auth 설정이 완료되어 실제 가입/로그인이 가능한가?
- [ ] 환경 변수가 `.env.local` 및 운영 환경에 정상 등록되었는가?
- [ ] 이메일 인증 절차가 의도대로 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-001 (인프라 셋업)
- Blocks: #FE-AUTH-001 (인증 UI 연동)
