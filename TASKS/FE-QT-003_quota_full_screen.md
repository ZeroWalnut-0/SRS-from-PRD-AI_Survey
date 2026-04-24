---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-003: 쿼터 도달(Quota Full) 안내 페이지 및 이탈 로직 구현"
labels: 'feature, frontend, mobile, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-003] 쿼터 도달(Quota Full) 안내 페이지 및 이탈 로직 구현
- 목적: 응답자가 자신의 속성(성별, 연령 등)에 해당하는 쿼터가 이미 가득 찬 경우, 정중히 안내하고 설문을 종료하거나 외부 URL로 리다이렉트 처리한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-019`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.3`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(survey)/forms/[form_id]/quota-full/page.tsx` 생성
- [ ] 안내 내용 구성: "정해진 응답 인원이 초과되어 조사가 조기 종료되었습니다" 등
- [ ] 외부 라우팅 연동 로직:
    - 패널사 리다이렉트 URL이 설정된 경우, 3초 후 자동 리다이렉트 처리
- [ ] 응답 제출 핸들러(`FE-FORM-007`)와의 연동: 쿼터풀 응답 수신 시 이 페이지로 리다이렉트

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 도달 시 이탈 안내
- Given: 설문 응답을 시작하려 하나 해당 쿼터가 만료됨
- When: 서버로부터 `QUOTA_FULL` 응답을 받음
- Then: 즉시 쿼터풀 안내 페이지로 이동하여 상황을 설명해야 한다.

Scenario 2: 자동 리다이렉트 수행
- Given: 쿼터풀 안내 페이지에 진입함
- When: 패널사 리다이렉트 설정(`quotafull_url`)이 존재함
- Then: 안내 문구 노출 후 일정 시간 뒤에 해당 URL로 자동 이동해야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 응답자가 불쾌감을 느끼지 않도록 정중한 문구와 디자인을 적용한다.
- 성능: 리다이렉트 판단 및 페이지 전환 레이턴시 ≤ 500ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터풀 전용 안내 페이지가 구현되었는가?
- [ ] 상태에 따른 리다이렉트 연동 로직이 작동하는가?
- [ ] 모바일 응답 폼과의 흐름 연동이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-007 (모바일 폼), #BE-QT-003 (쿼터 증가/체크 로직)
- Blocks: #BE-RT-002 (리다이렉트 구현)
