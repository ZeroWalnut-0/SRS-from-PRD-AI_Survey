---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-006: 설문 배포 및 공유 설정 화면 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-006] 설문 배포 및 공유 설정 화면 구현
- 목적: 설문 배포가 완료된 후 생성된 URL과 QR 코드를 사용자에게 제공하고, 카카오톡/이메일 공유 및 배포 중단 기능을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-016`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-006_form_publish_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-006_form_publish_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/forms/[form_id]/publish/page.tsx` 생성
- [ ] 배포 완료 상태 UI 구현 (성공 애니메이션 포함)
- [ ] 설문 URL 표시 및 [복사] 버튼 구현 (Clipboard API 활용)
- [ ] QR 코드 이미지 표시 및 [다운로드] 버튼 구현
- [ ] 공유 채널 연동:
    - 카카오톡 공유 (JS SDK 활용)
    - URL 링크 공유
- [ ] [배포 중단] 버튼 구현 (설문 상태를 `PENDING` 또는 `CLOSED`로 변경)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: URL 복사 기능 테스트
- Given: 배포가 완료된 화면
- When: [URL 복사] 버튼을 클릭함
- Then: 클립보드에 설문 주소가 저장되어야 하며, "복사되었습니다" 토스트 알림이 표시되어야 한다.

Scenario 2: 배포 중단 시나리오
- Given: 현재 배포 중인 설문
- When: [배포 중단]을 클릭하고 확인 모달에서 승인함
- Then: 설문 상태가 변경되고, 더 이상 기존 URL로 설문에 접근할 수 없어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 배포 중단 시 서버 측 권한 검증을 통해 소유자만 중단할 수 있도록 한다.
- UX: QR 코드는 모바일 인쇄물 등에 활용 가능하도록 고해상도 이미지를 제공한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 설문 URL 및 QR 코드가 정상 노출되는가?
- [ ] 클립보드 복사 및 공유 기능이 작동하는가?
- [ ] 배포 상태 제어(시작/중단) 로직이 연동되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-006 (배포 DTO), #BE-FORM-003 (배포 구현)
- Blocks: None
