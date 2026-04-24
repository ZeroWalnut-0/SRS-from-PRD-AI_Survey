---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-005: 파일 유효성 검증 실패 에러 모달 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-005] 파일 유효성 검증 실패 에러 모달 구현
- 목적: 서버 또는 클라이언트 측 파일 검증 실패 시, 사용자에게 에러 사유를 명확히 안내하고 후속 조치를 유도한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-005`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 성능 요건: 2초 이내 표시 (REQ-NF-007)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/parser/ErrorModal.tsx` 컴포넌트 생성
- [ ] API 에러 응답(`API-014`) 연동 로직 구현
- [ ] 에러 유형별 메시지 매핑:
    - `INVALID_FILE`: "지원하지 않는 파일 형식입니다."
    - `FILE_TOO_LARGE`: "파일 크기가 5MB를 초과했습니다."
    - `FILE_CORRUPTED`: "손상된 파일이거나 암호가 걸려 있습니다."
    - `RATE_LIMIT`: "오늘의 파싱 한도를 모두 사용하셨습니다."
- [ ] `shadcn/ui` Alert Dialog 활용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 서버 에러 발생 시 모달 노출
- Given: 업로드 API가 400 에러를 반환함
- When: 에러 상태가 감지됨
- Then: 2초 이내에 해당 에러 사유가 포함된 모달이 표시되어야 한다.

Scenario 2: 모달 확인 후 복구
- Given: 에러 모달이 표시됨
- When: [다시 시도] 버튼을 클릭함
- Then: 업로드 영역이 초기화되어 다른 파일을 선택할 수 있는 상태가 되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 에러 인지 후 모달 렌더링까지 레이턴시 ≤ 2,000ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 에러 유형별 명확한 안내 메시지가 구성되었는가?
- [ ] 2초 이내 응답 및 노출 요건을 충족하는가?
- [ ] 디자인 시스템에 맞는 UI로 구현되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-001 (업로드 UI), #API-014 (에러 규약)
- Blocks: #TEST-PARSE-004 (에러 검증 테스트)
