---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-005: ZIP 다운로드 Mock API 및 서명 URL 샘플 작성"
labels: 'feature, foundation, mock, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-005] ZIP 다운로드 Mock API 및 서명 URL 샘플 작성
- 목적: 결제 완료 후 ZIP 파일 다운로드 퍼널을 테스트하기 위해, Supabase Storage 서명 URL과 가상의 ZIP 파일을 준비한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.4_ZIP_DATAMAP`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 테스트용 가상 ZIP 파일 생성 (`mock_package.zip` - 응답 엑셀, 코드북 등 샘플 포함)
- [ ] `GET /api/v1/packages/{package_id}/download` Mock 핸들러 작성
- [ ] 결제 여부에 따른 차등 응답 시뮬레이션:
    - 결제 완료: 가상 다운로드 URL 반환
    - 미결제: 403 Forbidden 응답 반환
- [ ] 서명 URL 만료 시나리오 테스트를 위한 타임아웃 데이터 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 다운로드 시작 성공
- Given: 결제가 완료된 상태
- When: 다운로드 버튼을 클릭함
- Then: Mock API가 가상 URL을 반환하고 브라우저에서 파일 다운로드가 트리거되어야 한다.

Scenario 2: 미결제 다운로드 시도 차단
- Given: 결제가 완료되지 않은 상태
- When: 다운로드 API를 강제 호출함
- Then: 403 에러와 함께 결제가 필요하다는 안내가 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 가상 ZIP 파일에는 실제 데이터가 아닌 익명화된 샘플 데이터만 포함한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 테스트용 샘플 ZIP 파일이 준비되었는가?
- [ ] 결제 상태에 따른 조건부 Mock 응답이 작동하는가?
- [ ] 다운로드 트리거 및 에러 처리가 프론트엔드에서 확인되는가?

## :construction: Dependencies & Blockers
- Depends on: #API-009 (ZIP Download DTO)
- Blocks: #FE-PAY-004 (결제 후 다운로드 UI)
