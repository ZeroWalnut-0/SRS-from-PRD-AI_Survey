---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PAY-003: 결제 완료 성공 화면 및 다운로드 활성화"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PAY-003] 결제 완료 성공 화면 및 다운로드 활성화
- 목적: 결제가 성공적으로 완료되었음을 알리고, 그동안 차단되었던 ZIP 파일 다운로드 버튼을 활성화하여 사용자가 산출물을 획득할 수 있게 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/payments/success/page.tsx` 생성
- [ ] 결제 승인 완료 안내 UI 구현 (주문 번호, 결제 금액 등 표시)
- [ ] 서버로부터 최종 결제 승인 확인 및 DB 상태 반영 대기 (Polling 또는 Push)
- [ ] 성공 페이지에서 해당 설문의 결과 페이지로 리다이렉트 또는 다운로드 버튼 즉시 노출
- [ ] [산출물 다운로드] 버튼 활성화 상태 갱신

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 성공 페이지 진입
- Given: PG사 결제가 완료되어 성공 URL로 진입함
- When: 화면이 로드됨
- Then: 결제 완료 축하 메시지와 함께 다운로드 준비가 완료되었음을 안내해야 한다.

Scenario 2: 다운로드 기능 해제
- Given: 결제 전에는 비활성화되었던 [ZIP 다운로드] 버튼
- When: 결제 성공 후 대시보드로 돌아옴
- Then: 버튼이 활성화 상태로 변경되어 클릭 시 파일 다운로드가 시작되어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 결제 완료 후 실제 파일 생성(BE-PAY-003)까지 시간이 걸릴 수 있으므로, "파일을 생성 중입니다"라는 로딩 상태를 친절히 안내한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 성공 안내 화면이 구현되었는가?
- [ ] 결제 상태에 따른 다운로드 버튼 활성화 로직이 정확히 연동되는가?
- [ ] 결제 후속 프로세스(파일 생성 대기 등)에 대한 UI 안내가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PAY-002 (결제 연동), #BE-PAY-002 (결제 콜백)
- Blocks: #FE-PAY-004 (다운로드 시작)
