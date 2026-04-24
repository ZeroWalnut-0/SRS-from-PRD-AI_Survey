---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PAY-001: ZIP 산출물 생성 및 구조 검증 테스트"
labels: 'test, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PAY-001] ZIP 산출물 생성 및 구조 검증 테스트
- 목적: 결제 완료 후 생성되는 ZIP 패키지 내의 4종 산출물(응답 엑셀, 변수가이드, 코드북, 데이터맵)이 정의된 규격에 맞게 생성되는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-008`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 관련 태스크: #BE-PAY-003 (ZIP 컴파일 로직)

## :white_check_mark: Test Scenarios (검증 시나리오)
- [ ] `tests/integration/zip.compiler.test.ts` 테스트 스크립트 작성
- [ ] 시나리오 1: ZIP 파일 내 4개 파일 존재 여부 확인 (`응답원본.xlsx`, `변수가이드.xlsx`, `코드북.xlsx`, `데이터맵.xlsx`)
- [ ] 시나리오 2: `응답원본.xlsx`의 컬럼 헤더와 데이터 일치성 확인
- [ ] 시나리오 3: `데이터맵.xlsx` 내의 결측치(Missing Value) 0% 여부 전수 검증
- [ ] 시나리오 4: 특수문자가 포함된 문항 제목의 파일 내 정상 인코딩 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 100건의 설문 응답 데이터가 DB에 존재함
- When: ZIP 컴파일 API를 호출함
- Then: 생성된 ZIP 파일의 압축을 해제했을 때, 각 엑셀 파일의 시트 구조가 SRS §4.1.2 명세와 100% 일치해야 한다.

## :gear: Technical & Non-Functional Constraints
- 도구: `adm-zip` 또는 `unzipper` 라이브러리를 활용하여 테스트 코드 내에서 파일 구조 검증
- 성능: 100건 기준 ZIP 생성 및 유효성 검증 시간이 5초 이내여야 함 (REQ-NF-004)

## :checkered_flag: Definition of Done (DoD)
- [ ] 4종 산출물이 모두 포함된 ZIP 파일이 생성되는가?
- [ ] 엑셀 파일 내부의 데이터 정합성이 보장되는가?
- [ ] 비정상적인 데이터(빈 응답 등) 포함 시에도 컴파일이 실패하지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-003 (ZIP 컴파일 로직)
- Blocks: #TEST-PAY-002 (ZIP 생성 성능 테스트)
