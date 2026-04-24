---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PAY-002: ZIP 산출물 패키징 정합성 및 압축 상태 테스트"
labels: 'test, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PAY-002] ZIP 산출물 패키징 정합성 및 압축 상태 테스트
- 목적: 생성된 ZIP 파일 내에 4종의 산출물이 모두 포함되어 있는지, 그리고 각 파일의 내용이 실제 설문 데이터와 일치하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PAY-003 (ZIP 컴파일러)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: ZIP 파일 압축 해제 후 파일 목록(4종) 확인
- [ ] 시나리오 2: 엑셀 파일 내 응답자 수와 DB 응답자 수 대조
- [ ] 시나리오 3: 코드북 엑셀 내 문항 번호와 실제 문항 일치 여부 확인
- [ ] 시나리오 4: 원본 PDF 파일이 손상 없이 포함되었는지 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 50건의 응답이 완료된 설문
- When: ZIP 패키징을 수행하고 파일을 다운로드함
- Then: 압축 파일 내에 `raw_data.xlsx`, `codebook.xlsx`, `original_doc.pdf`, `clean_data.csv`가 존재해야 한다.

## :gear: Technical Constraints
- 도구: Node.js `adm-zip` 라이브러리를 이용한 자동 검증 스크립트

## :checkered_flag: Definition of Done (DoD)
- [ ] 생성된 ZIP 파일의 구조가 명세와 일치하는가?
- [ ] 각 파일 내부의 데이터 정합성이 100%인가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-003 (ZIP 컴파일 로직)
- Blocks: None
