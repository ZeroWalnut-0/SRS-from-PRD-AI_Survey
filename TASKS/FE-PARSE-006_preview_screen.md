---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-006: 파싱 완료 후 생성된 설문 폼 미리보기 화면 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-006] 파싱 완료 후 생성된 설문 폼 미리보기 화면 구현
- 목적: AI 파싱이 완료된 직후, 생성된 설문 문항들을 사용자에게 보여주고 파싱 결과(건너뛴 요소 등)를 브리핑한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-007`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/parser/preview/[form_id]/page.tsx` 생성
- [ ] 파싱 결과(`PARSED_FORM`) 데이터 페칭 및 렌더링
- [ ] 문항 목록 표시 UI 구현 (제목, 유형, 옵션 리스트)
- [ ] 건너뛴 요소(`skipped_elements`) 알림 영역 구현: 이미지/수식 스킵 안내
- [ ] [수정하기] 및 [배포하기] 버튼 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 결과 정상 표시
- Given: 파싱이 성공적으로 완료됨
- When: 미리보기 페이지로 리다이렉트됨
- Then: 추출된 모든 문항이 목록 형태로 표시되어야 하며, `question_count`가 일치해야 한다.

Scenario 2: 스킵된 요소 안내 확인
- Given: 원본 문서에 이미지나 수식이 포함되어 있었음
- When: 미리보기 화면 상단을 확인함
- Then: "이미지/수식 3개가 스킵되었습니다"와 같은 안내 메시지가 명확히 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- UI/UX: 사용자가 파싱 결과를 한눈에 검토할 수 있도록 리스트 뷰를 최적화한다.
- 성능: 50문항 기준 초기 렌더링 레이턴시 ≤ 500ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] `structure_schema` 기반의 문항 목록 렌더링이 완료되었는가?
- [ ] 스킵된 요소에 대한 알림 로직이 구현되었는가?
- [ ] 후속 작업(에디터 이동, 배포) 버튼이 정상 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-002 (상태 조회 Mock), #BE-PARSE-005 (AI 파싱 완료)
- Blocks: #FE-FORM-001 (에디터 구현)
