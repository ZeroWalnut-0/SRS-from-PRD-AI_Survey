---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-RT-002: 리다이렉트 대기 및 안내 화면 구현"
labels: 'feature, frontend, mobile, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-RT-002] 리다이렉트 대기 및 안내 화면 구현
- 목적: 외부 패널 응답자가 조사를 마친 후, 외부 사이트로 안전하게 돌아가기 전 "데이터 저장 중"임을 안내하고 자동 이동을 처리하는 화면을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5_REQ-FUNC-023`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(survey)/forms/[form_id]/redirect/page.tsx` 생성
- [ ] 로딩 애니메이션 및 안내 문구 구현 (예: "패널 사이트로 안전하게 이동 중입니다. 잠시만 기다려 주세요.")
- [ ] `GET /api/v1/routing/redirect/{resp_id}` API를 통한 자동 리다이렉트 브릿지 역할 수행
- [ ] 리다이렉트 실패 시 수동 클릭 링크 및 안내 제공

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 성공적인 자동 리다이렉트
- Given: 설문 응답을 완료한 응답자
- When: 리다이렉트 브릿지 페이지에 진입함
- Then: 3초 이내에 외부 패널사의 성공 페이지로 자동 이동해야 한다.

Scenario 2: 리다이렉트 오류 시 수동 안내
- Given: 네트워크 오류 등으로 자동 이동이 실패함
- When: 10초 이상 페이지가 머물러 있음
- Then: "[여기]를 클릭하여 직접 이동하세요"라는 문구와 함께 수동 링크가 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 페이지 진입 후 리다이렉트 결정까지 레이턴시 ≤ 500ms.
- 가용성: 모바일 브라우저의 팝업 차단 등을 고려하여 `window.location.replace` 방식을 권장한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 리다이렉트 대기 UI가 모바일 최적화되어 구현되었는가?
- [ ] 자동 이동 로직이 의도대로 작동하는가?
- [ ] 에러 발생 시의 폴백 처리가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-002 (리다이렉트 핸들러)
- Blocks: None
