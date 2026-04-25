---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-AUTH-002: 비밀번호 찾기 및 이메일 인증 화면 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-AUTH-002] 비밀번호 찾기 및 이메일 인증 화면 구현
- 목적: 사용자가 비밀번호를 분실했을 때 재설정 링크를 이메일로 요청하고 처리하는 UI를 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L597)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 비밀번호 찾기 링크 요청 화면 구현
- [ ] 이메일 링크 클릭 후 진입하는 '새 비밀번호 설정' 폼 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 재설정 이메일 발송 성공
- Given: 가입된 이메일 주소 입력
- When: '링크 발송' 클릭
- Then: "이메일이 발송되었습니다." 모달 안내문이 노출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 재설정 후 자동 로그인 처리 및 대시보드 진입 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-AUTH-001
- Blocks: #FE-AUTH-003
