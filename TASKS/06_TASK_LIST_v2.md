# 📋 개발 태스크 목록 명세서 v2 (Task Breakdown from SRS_v1)

**문서 ID:** TASK-001 Rev 2  
**원천 문서:** SRS-001 Rev 1.2 (SRS_v1.md)  
**작성일:** 2026-04-21 (v1) / 2026-04-23 (v2 최신화)  
**작성 방법론:** Contract-First → CQRS → TDD → NFR 순차 추출  
**v2 변경사항:** Dashboard·Auth·Admin 도메인 추가, TEST-FORM·TEST-ADMIN 추가, Step 5 UI/UX 컴포넌트 추가 (141 → 184개)  

---

## 목차

1. [Step 1. 계약·데이터 명세 Task (Foundation Layer)](#step-1-계약데이터-명세-task-foundation-layer)
2. [Step 2. 로직·상태 변경 Task (Feature Layer — CQRS 분해)](#step-2-로직상태-변경-task-feature-layer--cqrs-분해)
3. [Step 3. 테스트 Task (AC 기반 자동화 검증)](#step-3-테스트-task-ac-기반-자동화-검증)
4. [Step 4. 비기능 제약(NFR) 및 인프라 Task](#step-4-비기능-제약nfr-및-인프라-task)
5. [Step 5. UI/UX 프론트엔드 태스크](#step-5--uiux-프론트엔드-태스크)
6. [전체 태스크 의존성 맵 (Dependency Graph)](#전체-태스크-의존성-맵-dependency-graph)
7. [전체 태스크 요약 통계](#전체-태스크-요약-통계)

---

## Step 1. 계약·데이터 명세 Task (Foundation Layer)

> **목표:** 백엔드·프론트엔드가 공유할 **단일 진실 공급원(SSOT)** 구축.  
> DB 스키마, API DTO, Mock 데이터를 가장 먼저 확정하여 후속 모든 태스크의 기반으로 삼는다.

### 1-A. 데이터베이스(DB) 스키마 및 마이그레이션 Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| DB-001 | Foundation | Prisma 스키마 초기화 및 개발 환경 구성 (SQLite 로컬 / Supabase PostgreSQL 배포) | §1.2.3 C-TEC-003 | None | M |
| DB-002 | Foundation | USER 테이블 스키마 및 마이그레이션 작성 (user_id, email, name, is_paid_user, created_at) | §6.2.9 ERD | DB-001 | L |
| DB-003 | Foundation | DOCUMENT 테이블 스키마 및 마이그레이션 작성 (doc_id, user_id FK, file_type ENUM, file_hash, status ENUM, expires_at 등) | §6.2.1 | DB-002 | M |
| DB-004 | Foundation | PARSED_FORM 테이블 스키마 및 마이그레이션 작성 (form_id, doc_id FK, structure_schema JSON, viral_watermark_url, is_paid_user 등) | §6.2.2 | DB-003 | M |
| DB-005 | Foundation | RESPONSE 테이블 스키마 및 마이그레이션 작성 (resp_id, form_id FK, raw_record JSON, quota_status ENUM, routing_status ENUM, ip_hash 등) | §6.2.3 | DB-004 | M |
| DB-006 | Foundation | ZIP_DATAMAP 테이블 스키마 및 마이그레이션 작성 (package_id, form_id FK, payment_cleared, pg_transaction_id, download_url, download_count 등) | §6.2.4 | DB-004 | M |
| DB-007 | Foundation | QUOTA_SETTING 테이블 스키마 및 마이그레이션 작성 (quota_id, form_id FK, quota_matrix JSON, is_active 등) | §6.2.5 | DB-004 | L |
| DB-008 | Foundation | QUOTA_CELL 테이블 스키마 및 마이그레이션 작성 (cell_id, quota_id FK, group_key, gender ENUM, target_count, current_count, is_full 등) | §6.2.6 | DB-007 | M |
| DB-009 | Foundation | ROUTING_CONFIG 테이블 스키마 및 마이그레이션 작성 (routing_id, form_id FK, success_url, screenout_url, quotafull_url 등) | §6.2.7 | DB-004 | L |
| DB-010 | Foundation | AUDIT_LOG 테이블 스키마 및 마이그레이션 작성 (log_id, user_id FK, action, resource_type, resource_id, details JSON 등) | §6.2.8 | DB-002 | L |
| DB-011 | Foundation | Enum 타입 정의 (FileType, DocumentStatus, QuotaStatus, RoutingStatus, Gender) 및 Prisma enum 매핑 | §6.2.10 | DB-001 | L |
| DB-012 | Foundation | 쿼터 카운트 원자적 증가를 위한 Supabase RPC(PL/pgSQL) 함수 작성 (`increment_quota_cell`) | §6.2.6, §3.6.3 | DB-008 | H |

### 1-B. API 통신 계약(Contract) 및 DTO 정의 Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| API-001 | Foundation | Document 도메인 API 계약 정의: `POST /api/v1/documents/upload` Request(multipart/form-data) / Response DTO (`{ doc_id, status }`) 및 에러 코드(400, 429) | §6.1 #1 | DB-003 | M |
| API-002 | Foundation | Document 도메인 API 계약 정의: `GET /api/v1/documents/{doc_id}/status` Response DTO (`{ doc_id, parsed_success, form_id, error_code }`) 및 에러 코드(404) | §6.1 #2 | DB-003 | L |
| API-003 | Foundation | Form 도메인 API 계약 정의: `GET /api/v1/forms/{form_id}` Response DTO (`{ form_id, structure_schema, viral_watermark_url }`) 및 에러 코드(404) | §6.1 #3 | DB-004 | L |
| API-004 | Foundation | Form 도메인 API 계약 정의: `POST /api/v1/forms/{form_id}/responses` Request DTO (`{ resp_id, user_agent, raw_record, quota_group }`) / Response DTO (`{ resp_id, status }`) 및 에러 코드(400, 429) | §6.1 #4 | DB-005 | M |
| API-005 | Foundation | Form 커스텀 빌드 API 계약 정의: `PUT /api/v1/forms/{form_id}` Request DTO (수정된 structure_schema) / Response DTO 및 에러 코드(400) | §6.3.6 | DB-004 | M |
| API-006 | Foundation | Form 배포 API 계약 정의: `POST /api/v1/forms/{form_id}/publish` Response DTO (`{ survey_url, qr_code }`) | §6.3.6 | DB-004 | L |
| API-007 | Foundation | Package/Payment 도메인 API 계약 정의: `POST /api/v1/packages/{form_id}/payment` Request/Response DTO 및 에러 코드(400, 500) | §6.1 #5 | DB-006 | M |
| API-008 | Foundation | Package/Payment 도메인 API 계약 정의: `POST /api/v1/payments/callback` Request DTO (`{ session_id, status, pg_transaction_id }`) / Response DTO 및 에러 코드(400) | §6.1 #6 | DB-006 | M |
| API-009 | Foundation | Package 도메인 API 계약 정의: `GET /api/v1/packages/{package_id}/download` Response DTO (`{ presigned_url }`) 및 에러 코드(403 미결제, 404) | §6.1 #7 | DB-006 | L |
| API-010 | Foundation | Quota 도메인 API 계약 정의: `POST /api/v1/quotas` Request DTO (`{ form_id, quota_matrix }`) / Response DTO 및 에러 코드(400) | §6.1 #8 | DB-007, DB-008 | M |
| API-011 | Foundation | Quota 도메인 API 계약 정의: `GET /api/v1/quotas/{quota_id}/status` Response DTO (`{ quota_id, cells: [...] }`) 및 에러 코드(404) | §6.1 #9 | DB-007, DB-008 | L |
| API-012 | Foundation | Routing 도메인 API 계약 정의: `POST /api/v1/routing/postback` Request DTO (`{ form_id, success_url, screenout_url, quotafull_url }`) / Response DTO 및 에러 코드(400) | §6.1 #10 | DB-009 | L |
| API-013 | Foundation | Routing 도메인 API 계약 정의: `GET /api/v1/routing/redirect/{resp_id}` Response(HTTP 302) 및 에러 코드(404, 500) | §6.1 #11 | DB-009 | L |
| API-014 | Foundation | 공통 에러 응답 형식(Error Response Schema) 및 HTTP 상태 코드 규약 정의 (400, 403, 404, 429, 500 통합) | §6.1 전체 | None | L |
| API-015 | Foundation | API 버전 관리 체계 (`/api/v{N}/`) Route Handler 디렉토리 구조 설계 | §4.2.7 REQ-NF-031 | None | L |
| API-016 | Foundation | Admin 도메인 API 계약 정의: `GET /api/v1/admin/stats` 통계 집계 Response DTO 및 권한 검증 | §4.2.8 REQ-NF-033 | DB-010 | L |

### 1-C. Mock 데이터 및 프론트엔드 독립 개발 지원 Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| MOCK-001 | Foundation | 문서 업로드 성공/실패 Mock API 엔드포인트 및 시드 데이터 작성 (HWPX/Word/PDF 샘플, 에러 응답 포함) | §6.1 #1, §4.1.1 | API-001 | M |
| MOCK-002 | Foundation | 파싱 완료 상태 조회 Mock API 및 structure_schema 샘플 JSON 작성 | §6.1 #2, #3 | API-002, API-003 | M |
| MOCK-003 | Foundation | 설문 응답 수집 Mock API 및 raw_record 샘플 데이터 작성 | §6.1 #4 | API-004 | L |
| MOCK-004 | Foundation | 결제 요청/콜백 Mock API 및 PG 응답 시뮬레이션 데이터 작성 (성공/실패 케이스) | §6.1 #5, #6 | API-007, API-008 | M |
| MOCK-005 | Foundation | ZIP 다운로드 Mock API 및 서명 URL 시뮬레이션 데이터 작성 | §6.1 #7 | API-009 | L |
| MOCK-006 | Foundation | 쿼터 설정/조회 Mock API 및 교차 쿼터 매트릭스 샘플 데이터 작성 | §6.1 #8, #9 | API-010, API-011 | M |
| MOCK-007 | Foundation | 패널 라우팅 포스트백 등록/리다이렉트 Mock API 및 시뮬레이션 데이터 작성 | §6.1 #10, #11 | API-012, API-013 | L |
| MOCK-008 | Foundation | Prisma DB Seed 스크립트 작성 (전체 테이블 초기 데이터 일괄 인서트) | §6.2 전체 | DB-002 ~ DB-010 | M |

---

## Step 2. 로직·상태 변경 Task (Feature Layer — CQRS 분해)

> **목표:** 기능적 요구사항을 **Read(Query)** 와 **Write(Command)** 로 철저히 분리.  
> 에이전트가 오직 하나의 데이터 흐름에만 집중하도록 격리(Isolation) 한다.

### 2-A. Epic: AI Document Parser (문서 파싱)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-PARSE-001 | Document Parser | [Client Logic] 문서 업로드 이벤트 처리 및 클라이언트 측 파일 검증 로직 연결 | §4.1.1 REQ-FUNC-001 | UI-010, MOCK-001 | M |
| FE-PARSE-002 | Document Parser | [Client Logic] 파싱 대기 스켈레톤 상태 연동 및 폴링/타임아웃(10초) 처리 | §4.2.1 REQ-NF-003 | UI-011 | L |
| FE-PARSE-003 | Document Parser | [Client Logic] HWPX 전환 안내 모달 트리거 상태 제어 (.hwp 확장자 감지 시) | §4.1.1 REQ-FUNC-031 | UI-010 | L |
| FE-PARSE-004 | Document Parser | [Client Logic] 정확도 한계 안내 모달 표시 및 템플릿 다운로드 이벤트 연동 | §4.1.6 REQ-FUNC-027 | UI-010 | L |
| FE-PARSE-005 | Document Parser | [Client Logic] 파일 검증 에러 상태 연동 및 에러 모달 트리거 | §4.1.1 REQ-FUNC-005 | UI-010 | L |
| FE-PARSE-006 | Document Parser | [Client Logic] 파싱 결과 JSON 데이터 폼 미리보기 바인딩 및 상태 렌더링 | §4.1.1 REQ-FUNC-007 | UI-004, MOCK-002 | M |
| FE-PARSE-007 | Document Parser | [Client Logic] AI 주치의 제안 Alert 데이터 수신 및 수락 시 자동 교정 로직 적용 | §4.1.1 REQ-FUNC-032 | UI-022, MOCK-002 | M |
| FE-PARSE-008 | Document Parser | [Client Logic] 커스텀 에디터 모드 전역 상태 연동 및 인라인 AI 명령 전송 로직 | §4.1.1 REQ-FUNC-033 | UI-020, MOCK-002 | H |
| FE-PARSE-009 | Document Parser | [Client Logic] 멀티턴 대화형 설문 설계 챗봇 API 연동 및 상태 업데이트 | §4.1.1 REQ-FUNC-034 | UI-002, MOCK-002 | H |
| BE-PARSE-001 | Document Parser | [Command] 문서 파일 서버 측 검증 로직 구현 (확장자·크기·암호화·손상 체크) → DOCUMENT 레코드 생성 (status=FAILED 또는 PARSING) | §4.1.1 REQ-FUNC-001, 005 | DB-003, API-001 | M |
| BE-PARSE-002 | Document Parser | [Command] HWPX 문서 전처리 구현: jszip 압축 해제 → section0.xml 텍스트 노드 추출 | §4.1.1 REQ-FUNC-006 | BE-PARSE-001 | H |
| BE-PARSE-003 | Document Parser | [Command] Word(.docx) 문서 전처리 구현: mammoth 라이브러리 텍스트 추출 | §4.1.1 REQ-FUNC-006 | BE-PARSE-001 | M |
| BE-PARSE-004 | Document Parser | [Command] PDF 문서 전처리 구현: pdf-parse 라이브러리 텍스트 추출 | §4.1.1 REQ-FUNC-006 | BE-PARSE-001 | M |
| BE-PARSE-005 | Document Parser | [Command] Vercel AI SDK + Gemini API 연동: generateObject()로 structure_schema JSON 생성 및 AI 주치의(문항 논리 교정 가이드) 생성 + PARSED_FORM 레코드 저장 | §4.1.1 REQ-FUNC-002, §3.6.1 | BE-PARSE-002, BE-PARSE-003, BE-PARSE-004, DB-004 | H |
| BE-PARSE-006 | Document Parser | [Command] 이미지/수식 요소 스킵 처리 및 skipped_elements 목록 기록 로직 구현 | §4.1.1 REQ-FUNC-007 | BE-PARSE-005 | M |
| BE-PARSE-007 | Document Parser | [Command] 파싱 완료 후 DOCUMENT.parsed_success = true 갱신 및 DOCUMENT.status = COMPLETED 처리 | §3.6.1 | BE-PARSE-005 | L |
| BE-PARSE-008 | Document Parser | [Query] GET /api/v1/documents/{doc_id}/status 파싱 상태 조회 Route Handler 구현 | §4.1.1 REQ-FUNC-004, §6.1 #2 | DB-003, API-002 | L |
| BE-PARSE-009 | Document Parser | [Command] Gemini API Fallback: JS 텍스트 추출 라이브러리(pdf-parse, mammoth, hwp.js)로 대체 파싱 경로 구현 | §3.1 EXT-07 | BE-PARSE-005 | H |
| BE-PARSE-010 | Document Parser | [Command] 파일 해시(SHA-256) 기반 캐시 조회: Supabase DB에서 동일 해시 파싱 결과 존재 시 재사용 | §4.1.6 REQ-FUNC-028 | BE-PARSE-001, DB-003 | M |
| BE-PARSE-011 | Document Parser | [Command] AI 주치의 진단 로직: 파싱 완료된 JSON을 LLM으로 검수하여 편향성/오류 등 수정 가이드 Alert 객체 반환 | §4.1.1 REQ-FUNC-032 | BE-PARSE-005 | H |
| BE-PARSE-012 | Document Parser | [Command] 대화형 챗봇 API 연동: Vercel AI SDK (streamText) 기반으로 사용자 대화에 맞춰 structure_schema 동적 갱신 | §4.1.1 REQ-FUNC-034 | BE-PARSE-005 | H |

### 2-B. Epic: Form Management (설문 폼 관리)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-FORM-001 | Form Management | [Client Logic] 폼 에디터 문항 배열 전역 상태 관리 및 순서 변경(D&D) 로직 연동 | §6.3.6 | UI-020, MOCK-002 | H |
| FE-FORM-002 | Form Management | [Client Logic] 문항 유형 변경 이벤트 처리 및 객체 속성(보기 등) 동적 업데이트 | §6.3.6 | UI-021, FE-FORM-001 | H |
| FE-FORM-003 | Form Management | [Client Logic] 새 문항 추가 로직 및 폼 스키마 전역 상태 동기화 | §6.3.6 | UI-021, FE-FORM-001 | M |
| FE-FORM-004 | Form Management | [Client Logic] 스킵 로직(조건부 분기) 상태 저장 및 클라이언트 측 순환 참조 검증 | §6.3.6 | UI-023, FE-FORM-001 | H |
| FE-FORM-005 | Form Management | [Client Logic] 모바일 미리보기 창 데이터 바인딩 및 실시간 렌더링 동기화 | §6.3.6 | UI-030, FE-FORM-001 | M |
| FE-FORM-006 | Form Management | [Client Logic] 폼 배포 API 호출 및 배포 결과(URL, QR) 클라이언트 렌더링 | §6.3.6 | UI-020, FE-FORM-001 | M |
| FE-FORM-007 | Form Management | [Client Logic] 모바일 설문 응답 폼 동적 렌더링 및 사용자 입력 상태(응답 데이터) 수집 로직 | §3.2 CLI-02, §6.3.2 | UI-030, MOCK-003 | H |
| FE-FORM-008 | Form Management | [Client Logic] 의심 응답 데이터 패치 및 상태 복원(ACTIVE) API 연동 처리 | §4.1.8 REQ-FUNC-037 | UI-051, FE-FORM-007 | M |
| BE-FORM-001 | Form Management | [Query] GET /api/v1/forms/{form_id} 설문 폼 조회 Route Handler 구현 (structure_schema + viral_watermark_url 반환) | §4.1.1 REQ-FUNC-006, §6.1 #3 | DB-004, API-003 | L |
| BE-FORM-002 | Form Management | [Command] PUT /api/v1/forms/{form_id} 폼 수정(커스텀 빌드) Route Handler 구현: structure_schema 서버 측 유효성 검증 + DB 갱신 (question_count 재계산) | §6.3.6 | DB-004, API-005 | H |
| BE-FORM-003 | Form Management | [Command] POST /api/v1/forms/{form_id}/publish 폼 배포 Route Handler 구현: status='PUBLISHED' 갱신 + 응답 수집용 고유 URL 생성 | §6.3.6 | DB-004, API-006 | M |
| BE-FORM-004 | Form Management | [Command] POST /api/v1/forms/{form_id}/responses 설문 응답 제출 Route Handler 구현: AI Data Bouncer를 통한 500ms 이내 실시간 불성실 응답(매크로/찍기) 무효 처리 후 RESPONSE 레코드 저장 (raw_record, user_agent, ip_hash) | §4.1.2 REQ-FUNC-008, §6.1 #4 | DB-005, API-004 | M |

### 2-C. Epic: DataMap Compiler & Paywall (ZIP 산출물 및 결제)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-PAY-001 | DataMap & Paywall | [Client Logic] 결제 대기 상태 관리 및 Paywall 모달 트리거 처리 | §4.1.2 REQ-FUNC-010 | UI-041, MOCK-004 | M |
| FE-PAY-002 | DataMap & Paywall | [Client Logic] 토스페이먼츠 JS SDK 연동 및 결제 요청/콜백 상태 제어 | §4.1.2 REQ-FUNC-010, §3.6.2 | UI-041, FE-PAY-001 | H |
| FE-PAY-003 | DataMap & Paywall | [Client Logic] 모자이크 이미지 및 더미 스키마 다운로드 이벤트 핸들러 | §4.1.2 REQ-FUNC-015 | UI-040, FE-PAY-001 | M |
| FE-PAY-004 | DataMap & Paywall | [Client Logic] 결제 성공/실패 응답 상태에 따른 UI 분기 및 ZIP 다운로드 트리거 | §4.1.2 REQ-FUNC-013, §3.6.2 | UI-041, FE-PAY-002 | L |
| BE-PAY-001 | DataMap & Paywall | [Command] POST /api/v1/packages/{form_id}/payment 결제 요청 Route Handler 구현: PG사 결제 세션 생성 및 결제 모듈 URL 반환 | §4.1.2 REQ-FUNC-010, §6.1 #5 | DB-006, API-007 | H |
| BE-PAY-002 | DataMap & Paywall | [Command] POST /api/v1/payments/callback PG 결제 콜백 Route Handler 구현: payment_cleared 상태 갱신 + AUDIT_LOG KPI 이벤트 기록 | §4.1.2 REQ-FUNC-012, §6.1 #6 | DB-006, DB-010, API-008 | H |
| BE-PAY-003 | DataMap & Paywall | [Command] ZIP 5종 산출물 컴파일 로직 구현: JSZip + exceljs 기반 응답 원본 엑셀, 변수가이드, 코드북, 데이터맵, 할당표, AI 내러티브 리포트 자동 생성 | §4.1.2 REQ-FUNC-008, 009 | DB-005, DB-006, BE-PAY-002 | H |
| BE-PAY-004 | DataMap & Paywall | [Command] 생성된 ZIP 파일 Supabase Storage 업로드 + 서명 Download URL 발급 및 DB 저장 | §4.1.2 REQ-FUNC-011, §3.6.2 | BE-PAY-003 | M |
| BE-PAY-005 | DataMap & Paywall | [Query] GET /api/v1/packages/{package_id}/download ZIP 다운로드 Route Handler 구현: 결제 상태 검증(payment_cleared=true) 후 서명 URL 반환, 미결제 시 403 차단 | §4.1.2 REQ-FUNC-011, 013, §6.1 #7 | DB-006, API-009, BE-PAY-002 | M |
| BE-PAY-006 | DataMap & Paywall | [Command] 데이터맵 결측치(Missing Value) 검증 로직 구현: ZIP 컴파일 시 전체 응답자 레코드 결측치 0% 보장 | §4.1.2 REQ-FUNC-014 | BE-PAY-003 | H |
| BE-PAY-007 | DataMap & Paywall | [Command] AI 내러티브 리포트 산출 로직 구현: 응답 통계 데이터를 Vercel AI SDK(generateText)로 분석하여 마크다운(.md) 요약 작성 | §4.1.2 REQ-FUNC-035 | BE-PAY-003 | H |

### 2-D. Epic: Watermark & Viral (워터마크 바이럴)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-WM-001 | Watermark & Viral | [Client Logic] 뷰포트 내 워터마크 노출 조건 검증 및 렌더링 상태 제어 | §4.1.3 REQ-FUNC-016 | UI-031, FE-FORM-007 | M |
| FE-WM-002 | Watermark & Viral | [Client Logic] 워터마크 클릭 이벤트 로깅 및 UTM 파라미터 포함 리다이렉션 | §4.1.3 REQ-FUNC-017 | UI-031, FE-WM-001 | L |
| BE-WM-001 | Watermark & Viral | [Command] PARSED_FORM 생성 시 viral_watermark_url 자동 생성(utm_source=watermark 파라미터 포함) | §4.1.3 REQ-FUNC-017, §6.2.2 | BE-PARSE-005 | L |
| BE-WM-002 | Watermark & Viral | [Command] 워터마크 클릭 이벤트 AUDIT_LOG 기록 (action=WATERMARK_CLICK) — GA4 장애 시 Fallback | §3.1 EXT-06 | DB-010 | L |

### 2-E. Epic: Quota Management (쿼터 관리)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-QT-001 | Quota Management | [Client Logic] 교차 쿼터 엑셀 데이터 파싱 및 매트릭스 상태 바인딩 | §4.1.4 REQ-FUNC-018 | UI-052, MOCK-006 | H |
| FE-QT-002 | Quota Management | [Client Logic] 쿼터 진행률 데이터 실시간 폴링 및 차트/게이지 데이터 매핑 | §4.1.4 REQ-FUNC-019, 022 | UI-052, MOCK-006 | H |
| FE-QT-004 | Quota Management | [Client Logic] 자연어 프롬프트 API 호출 및 할당표 자동 생성 결과 상태 반영 | §4.1.4 REQ-FUNC-038 | UI-052, FE-QT-001 | M |
| FE-QT-003 | Quota Management | [Client Logic] 쿼터 풀 상태 감지 시 진입 차단 및 안내 모달 렌더링 제어 | §4.1.4 REQ-FUNC-020 | UI-052, FE-FORM-007 | M |
| BE-QT-001 | Quota Management | [Command] POST /api/v1/quotas 쿼터 설정 생성 Route Handler 구현: 엑셀 파일 파싱 → QUOTA_SETTING + QUOTA_CELL 레코드 일괄 생성 | §4.1.4 REQ-FUNC-018, §6.1 #8 | DB-007, DB-008, API-010 | H |
| BE-QT-002 | Quota Management | [Query] GET /api/v1/quotas/{quota_id}/status 쿼터 상태 조회 Route Handler 구현 (셀별 target/current/is_full 반환) | §4.1.4 REQ-FUNC-019, §6.1 #9 | DB-008, API-011 | M |
| BE-QT-003 | Quota Management | [Command] 응답 제출 시 쿼터 카운트 원자적 증가 로직 구현: Supabase RPC 호출 → Over-quota 시 즉시 QUOTAFULL 리다이렉션 (오차율 1% 이내) | §4.1.4 REQ-FUNC-019, 020 | DB-012, BE-FORM-004 | H |
| BE-QT-004 | Quota Management | [Command] 쿼터 100% 도달 감지 시 QUOTA_CELL.is_full=true 갱신 + Slack Webhook 발송 | §4.1.4 REQ-FUNC-022 | BE-QT-003 | M |
| BE-QT-005 | Quota Management | [Command] 쿼터 연산 레이턴시 > 1초 시 AUDIT_LOG 기록 + Slack Webhook 경고 발송 | §4.1.4 REQ-FUNC-021 | BE-QT-003, DB-010 | M |
| BE-QT-006 | Quota Management | [Command] 자연어 기반 쿼터 자동 연산 API: 통계청 인구 데이터 비례 배분 로직(LLM JSON 반환)을 적용한 QUOTA_MATRIX 생성 | §4.1.4 REQ-FUNC-038 | API-010 | H |

### 2-F. Epic: Panel Routing (패널사 라우팅)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-RT-001 | Panel Routing | [Client Logic] 패널 연동 상태 폼 데이터 검증 및 포스트백 URL 저장 API 연동 | §4.1.5 REQ-FUNC-023 | UI-020, MOCK-007 | M |
| FE-RT-002 | Panel Routing | [Client Logic] 리다이렉트 지연 시간(안내 메시지 표시) 상태 제어 및 외부 라우팅 실행 | §4.1.5 REQ-FUNC-024 | UI-030, FE-RT-001 | L |
| BE-RT-001 | Panel Routing | [Command] POST /api/v1/routing/postback 포스트백 URL 등록 Route Handler 구현: ROUTING_CONFIG 레코드 생성/수정 | §4.1.5 REQ-FUNC-023, §6.1 #10 | DB-009, API-012 | M |
| BE-RT-002 | Panel Routing | [Command] GET /api/v1/routing/redirect/{resp_id} 패널 리다이렉트 Route Handler 구현: 응답 상태(SUCCESS/SCREENOUT/QUOTAFULL)에 따른 HTTP 302 리다이렉트 | §4.1.5 REQ-FUNC-024, §6.1 #11 | DB-009, DB-005, API-013, BE-QT-003 | H |
| BE-RT-003 | Panel Routing | [Command] 라우팅 실패 시 재시도 큐 등록(3회 재시도) + 3회 실패 시 Slack 알림 + 응답자 안내 페이지 렌더링 | §3.1 EXT-03 | BE-RT-002 | H |

### 2-G. Epic: Rate Limit & Auth (인증 및 제한)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-RL-001 | Rate Limit & Auth | [Client Logic] API 429 에러 코드 인터셉트 및 파싱 한도 초과 안내 모달 트리거 | §4.1.6 REQ-FUNC-026 | UI-003, FE-PARSE-001 | L |
| BE-RL-001 | Rate Limit & Auth | [Command] middleware.ts 인증·Rate Limit 미들웨어 구현: Supabase DB 기반 무료 계정 일일 파싱 3회 제한 (IP 체크 또는 유저별 카운트) | §4.1.6 REQ-FUNC-026, §3.4 | DB-002, DB-010 | H |
| BE-RL-002 | Rate Limit & Auth | [Command] RBAC(역할 기반 접근 제어) 미들웨어 구현: 사용자 권한 분리 (일반/유료/운영자) | §4.2.3 REQ-NF-019 | DB-002 | H |

### 2-H. Epic: Data Retention (데이터 삭제)

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| BE-RET-001 | Data Retention | [Command] Vercel Cron 기반 Zero-Retention 삭제 스케줄러 구현: expires_at ≤ NOW() 문서 조회 → Storage 파일 삭제 → DB 레코드 삭제/비식별화 → AUDIT_LOG 기록 | §4.1.7 REQ-FUNC-029, §6.3.4 | DB-003, DB-010 | H |
| BE-RET-002 | Data Retention | [Command] vercel.json cron 설정 작성 (매시간 실행) + 수동 삭제 npm script Fallback 구현 | §3.1 EXT-09 | BE-RET-001 | M |

### 2-I. Epic: Dashboard (대시보드 통계) — v2 추가

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-DASH-001 | Dashboard | [Client Logic] 설문 목록 API 연동 및 클라이언트 측 상태 필터링/검색 로직 | §6.3.5 | UI-050, MOCK-002 | M |
| FE-DASH-002 | Dashboard | [Client Logic] 응답 수 및 완료율 집계 데이터 차트 라이브러리(Recharts) 바인딩 | §4.2.8 REQ-NF-035 | UI-053, FE-DASH-001 | M |
| FE-DASH-003 | Dashboard | [Client Logic] 테이블 페이지네이션, 정렬 상태 관리 및 CSV 내보내기 다운로드 핸들러 | §4.2.8 REQ-NF-036 | UI-050, FE-DASH-001 | M |
| BE-DASH-001 | Dashboard | [Query] 설문별 응답 통계 집계 Route Handler: 일별/주별 응답 수, 완료율, 평균 소요 시간 등 | §4.2.8 REQ-NF-035 | DB-005, DB-004 | M |
| BE-DASH-002 | Dashboard | [Query] 사용자별 대시보드 데이터 조회: 내 설문 목록 + 각 설문 요약 정보 반환 | §6.3.5 | DB-004, DB-002 | M |

### 2-J. Epic: Authentication (인증 체계) — v2 추가

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-AUTH-001 | Authentication | [Client Logic] Supabase Auth SDK 연동 및 이메일/소셜 로그인/가입 상태 관리 | §4.2.3 REQ-NF-018 | UI-050, NFR-INFRA-004 | M |
| FE-AUTH-002 | Authentication | [Client Logic] 프로필/비밀번호 수정 폼 검증 및 계정 삭제 API 연동 | §4.2.3 REQ-NF-018 | UI-050, FE-AUTH-001 | M |
| FE-AUTH-003 | Authentication | [Client Logic] Auth Guard 미들웨어 상태 연동 및 세션 만료 시 리다이렉션 제어 | §4.2.3 REQ-NF-019 | UI-002, FE-AUTH-001 | M |
| BE-AUTH-001 | Authentication | [Command] Supabase Auth 통합: 이메일 가입/로그인 서버 측 검증 + JWT 토큰 발급/갱신 처리 | §4.2.3 REQ-NF-018, §3.1 EXT-08 | NFR-INFRA-004 | M |
| BE-AUTH-002 | Authentication | [Command] 사용자 세션 핸들러: 서버 컴포넌트/미들웨어에서 Supabase 세션 검증 + 세션 갱신 로직 구현 | §4.2.3 REQ-NF-019 | BE-AUTH-001, DB-002 | M |

### 2-K. Epic: Admin (관리자 기능) — v2 추가

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| FE-ADMIN-001 | Admin | [Client Logic] 관리자 라우트 접근 권한 검증 및 네비게이션 전역 상태 동기화 | §4.2.8 REQ-NF-033 | UI-050, BE-RL-002 | M |
| FE-ADMIN-002 | Admin | [Client Logic] 전체 통계 API 연동 및 KPI 대시보드 데이터 바인딩 | §4.2.8 REQ-NF-037 | UI-053, API-016 | M |
| BE-ADMIN-001 | Admin | [Query] 관리자 통계 집계 로직: 전체 서비스 KPI 데이터 수집 및 가공 (Prisma groupBy 활용) | §4.2.8 REQ-NF-033 | DB-010, BE-RL-002 | M |

---

## Step 3. 테스트 Task (AC 기반 자동화 검증)

> **목표:** SRS의 Acceptance Criteria를 **실행 가능한 테스트 코드**로 변환.  
> "이 테스트가 통과할 때까지 비즈니스 로직을 수정하라"는 명령이 가능한 수준으로 작성한다.

### 3-A. Document Parser 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-PARSE-001 | Document Parser | [Test] 유효한 HWPX/Word/PDF 파일 업로드 시 PARSED_FORM 생성 성공 GWT 시나리오 테스트 (TC-FUNC-001, TC-FUNC-002) | §4.1.1 REQ-FUNC-001, 002 | BE-PARSE-005 | M |
| TEST-PARSE-002 | Document Parser | [Test] 파싱 완료 레이턴시 ≤ 10초 성능 검증 테스트 (TC-FUNC-003, TC-NF-003) | §4.1.1 REQ-FUNC-003, §4.2.1 REQ-NF-003 | BE-PARSE-005 | M |
| TEST-PARSE-003 | Document Parser | [Test] 파싱 데이터 손실률 < 1% 검증 테스트: 원본 문항 수 vs structure_schema 문항 수 비교 (TC-FUNC-004) | §4.1.1 REQ-FUNC-004 | BE-PARSE-005 | M |
| TEST-PARSE-004 | Document Parser | [Test] 유효하지 않은 파일(암호화/손상/지원외 확장자) 업로드 시 400 에러 + 2초 이내 응답 검증 테스트 (TC-FUNC-005, TC-NF-007) | §4.1.1 REQ-FUNC-005 | BE-PARSE-001 | M |
| TEST-PARSE-005 | Document Parser | [Test] HWPX jszip 전처리 → PDF pdf-parse 전처리 → Word mammoth 전처리 분기 정상 동작 테스트 (TC-FUNC-006) | §4.1.1 REQ-FUNC-006 | BE-PARSE-002, 003, 004 | M |
| TEST-PARSE-006 | Document Parser | [Test] 이미지/수식 포함 문서 파싱 시 해당 요소 스킵 + skipped_elements 기록 + 알림 메시지 생성 테스트 (TC-FUNC-007) | §4.1.1 REQ-FUNC-007 | BE-PARSE-006 | M |
| TEST-PARSE-007 | Document Parser | [Test] .hwp 파일 업로드 시 HWPX 전환 안내 모달 1초 이내 표시 및 업로드 중단 테스트 (TC-FUNC-031) | §4.1.1 REQ-FUNC-031 | FE-PARSE-003, BE-PARSE-001 | L |
| TEST-PARSE-008 | Document Parser | [Test] Rate Limit 초과(무료 계정 4번째 파싱) 시 429 에러 반환 테스트 (TC-FUNC-026) | §4.1.6 REQ-FUNC-026 | BE-RL-001 | M |
| TEST-PARSE-009 | Document Parser | [Test] 동일 파일 해시 중복 요청 시 캐시 결과 반환(파이프라인 미재실행) 테스트 (TC-FUNC-028) | §4.1.6 REQ-FUNC-028 | BE-PARSE-010 | M |

### 3-B. DataMap & Paywall 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-PAY-001 | DataMap & Paywall | [Test] 조사 종료 후 ZIP 5종 산출물(응답 원본 엑셀, 변수가이드, 코드북, 데이터맵, 할당표, AI 내러티브 리포트) 정상 생성 검증 테스트 (TC-FUNC-008) | §4.1.2 REQ-FUNC-008 | BE-PAY-003 | H |
| TEST-PAY-002 | DataMap & Paywall | [Test] ZIP 패키지 생성 ≤ 5초 성능 검증 테스트 (TC-FUNC-009, TC-NF-004) | §4.1.2 REQ-FUNC-009, §4.2.1 REQ-NF-004 | BE-PAY-003 | M |
| TEST-PAY-003 | DataMap & Paywall | [Test] PG 결제 모듈 프레임 팝업 3초 이내 로드 검증 테스트 (TC-FUNC-010, TC-NF-005) | §4.1.2 REQ-FUNC-010, §4.2.1 REQ-NF-005 | FE-PAY-002, BE-PAY-001 | M |
| TEST-PAY-004 | DataMap & Paywall | [Test] 결제 성공 콜백 수신 → payment_cleared=true 갱신 + 서명 URL 발급 정상 흐름 테스트 (TC-FUNC-011, TC-FUNC-012) | §4.1.2 REQ-FUNC-011, 012 | BE-PAY-002, BE-PAY-004 | M |
| TEST-PAY-005 | DataMap & Paywall | [Test] 결제 실패/이탈 시 payment_cleared=false 유지 + 403 Forbidden 다운로드 차단 테스트 (TC-FUNC-013) | §4.1.2 REQ-FUNC-013 | BE-PAY-002, BE-PAY-005 | M |
| TEST-PAY-006 | DataMap & Paywall | [Test] 데이터맵 결측치(Missing Value) 처리 실패율 0% 검증 테스트 (TC-FUNC-014, TC-NF-011) | §4.1.2 REQ-FUNC-014 | BE-PAY-006 | H |
| TEST-PAY-007 | DataMap & Paywall | [Test] Paywall 팝업 내 모자이크 샘플 이미지 + 더미 스키마 엑셀 다운로드 링크 정상 제공 테스트 (TC-FUNC-015) | §4.1.2 REQ-FUNC-015 | FE-PAY-003 | L |

### 3-C. Watermark & Viral 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-WM-001 | Watermark & Viral | [Test] 무료 사용자 폼 하단 뷰포트 워터마크 배너 100% 렌더링 검증 테스트 (TC-FUNC-016) | §4.1.3 REQ-FUNC-016 | FE-WM-001 | L |
| TEST-WM-002 | Watermark & Viral | [Test] 워터마크 클릭 시 utm_source=watermark 파라미터 포함 URL 랜딩 검증 테스트 (TC-FUNC-017) | §4.1.3 REQ-FUNC-017 | FE-WM-002 | L |

### 3-D. Quota Management 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-QT-001 | Quota Management | [Test] 엑셀 업로드 기반 교차 쿼터(성별×연령×지역) 자동 반영 정상 동작 테스트 (TC-FUNC-018) | §4.1.4 REQ-FUNC-018 | BE-QT-001 | M |
| TEST-QT-002 | Quota Management | [Test] Over-quota 수용 오차율 ≤ 1% 검증: 목표 도달 후 초과 응답자 QUOTAFULL 리다이렉트 테스트 (TC-FUNC-019) | §4.1.4 REQ-FUNC-019 | BE-QT-003 | H |
| TEST-QT-003 | Quota Management | [Test] 동시 접속 시나리오에서 DB 데드락 미발생 검증 테스트: Supabase RPC Atomic Update (TC-FUNC-020) | §4.1.4 REQ-FUNC-020 | BE-QT-003, DB-012 | H |
| TEST-QT-004 | Quota Management | [Test] 쿼터 연산 레이턴시 > 1초 시 AUDIT_LOG + Slack Webhook 경고 발송 검증 테스트 (TC-FUNC-021) | §4.1.4 REQ-FUNC-021 | BE-QT-005 | M |
| TEST-QT-005 | Quota Management | [Test] 쿼터 100% 도달 시 Slack Alert 즉시 발송 검증 테스트 (TC-FUNC-022) | §4.1.4 REQ-FUNC-022 | BE-QT-004 | M |

### 3-E. Panel Routing 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-RT-001 | Panel Routing | [Test] 포스트백 링크(성공/스크린아웃/쿼터풀) 입력 → DB 저장 + 라우팅 정상 적용 테스트 (TC-FUNC-023) | §4.1.5 REQ-FUNC-023 | BE-RT-001 | M |
| TEST-RT-002 | Panel Routing | [Test] 패널 응답 완료/스크린아웃/쿼터풀 조건별 HTTP 302 리다이렉트 정상 동작 테스트 (TC-FUNC-024) | §4.1.5 REQ-FUNC-024 | BE-RT-002 | M |
| TEST-RT-003 | Panel Routing | [Test] 라우팅 실패 이탈률 < 0.1% 검증: 타임아웃/잘못된 URL 시나리오 통합 테스트 (TC-FUNC-025, TC-NF-012) | §4.1.5 REQ-FUNC-025 | BE-RT-002, BE-RT-003 | H |

### 3-F. Data Retention 테스트

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-RET-001 | Data Retention | [Test] 작업 종료 24시간 후 원본 문서 + 파편 데이터 영구 삭제 + 삭제 로그 기록 검증 테스트 (TC-FUNC-029) | §4.1.7 REQ-FUNC-029 | BE-RET-001 | M |
| TEST-RET-002 | Data Retention | [Test] 디스크 저장 데이터 Supabase at-rest encryption + HTTPS TLS 1.2+ 적용 검증 테스트 (TC-FUNC-030) | §4.1.7 REQ-FUNC-030 | BE-RET-001 | M |

### 3-G. Form Management 테스트 — v2 추가

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-FORM-001 | Form Management | [Test] 폼 에디터 드래그 앤 드롭 문항 순서 변경 정상 동작 검증 테스트 | §6.3.6 | FE-FORM-001 | M |
| TEST-FORM-002 | Form Management | [Test] 스킵 로직(조건부 분기) 순환 참조 감지 및 분기 정상 작동 검증 테스트 | §6.3.6 | FE-FORM-004, BE-FORM-002 | M |
| TEST-FORM-003 | Form Management | [Test] 모바일 웹 설문 폼 반응형 렌더링 및 터치 인터랙션 검증 테스트 | §3.2 CLI-02 | FE-FORM-007 | M |
| TEST-FORM-004 | Form Management | [Test] 설문 응답 제출 데이터 무결성 검증: raw_record 구조 일치 + DB 정합성 테스트 | §4.1.2 REQ-FUNC-008 | BE-FORM-004 | M |

### 3-H. Admin 테스트 — v2 추가

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| TEST-ADMIN-001 | Admin | [Test] 관리자 권한 접근 제어: 일반 사용자 /admin 경로 403 차단 + 관리자 정상 접근 검증 테스트 | §4.2.3 REQ-NF-019 | BE-RL-002, FE-ADMIN-001 | M |

---

## Step 4. 비기능 제약(NFR) 및 인프라 Task

> **목표:** 성능·보안·모니터링·인프라 관련 비기능 요구사항을 독립 태스크로 도출하고,  
> 전체 태스크 간 의존성을 명시한다.

### 4-A. 성능(Performance) Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-PERF-001 | Infra & NFR | [Perf] 설문 응답 패킷 p95 응답 시간 ≤ 1,000ms 부하 테스트 스크립트 작성 (k6 또는 Artillery) | §4.2.1 REQ-NF-001 | BE-FORM-004 | H |
| NFR-PERF-002 | Infra & NFR | [Perf] 문서 파싱 레이턴시 ≤ 15초 벤치마크 테스트 스크립트 작성 | §4.2.1 REQ-NF-002 | BE-PARSE-005 | M |
| NFR-PERF-003 | Infra & NFR | [Perf] 쿼터 카운트 연산 레이턴시 ≤ 1초 벤치마크 테스트 스크립트 작성 | §4.2.1 REQ-NF-006 | BE-QT-003 | M |
| NFR-PERF-004 | Infra & NFR | [Perf] 동시 접속 50~100명 부하 테스트 시나리오 작성 및 Vercel Serverless 스케일링 검증 | §4.2.6 REQ-NF-029, 030 | NFR-PERF-001 | H |

### 4-B. 보안(Security) Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-SEC-001 | Infra & NFR | [Sec] 전체 클라이언트-서버 통신 TLS 1.2+ 적용 확인 및 Vercel HTTPS 강제 설정 검증 | §4.2.3 REQ-NF-016 | DB-001 | L |
| NFR-SEC-002 | Infra & NFR | [Sec] Supabase PostgreSQL at-rest encryption 설정 확인 + 암호화 미적용 데이터 0 검증 | §4.2.3 REQ-NF-017 | DB-001 | L |
| NFR-SEC-003 | Infra & NFR | [Sec] 결제 트랜잭션 Audit Log 누락률 0% 검증 파이프라인 구축 | §4.2.3 REQ-NF-020 | BE-PAY-002, DB-010 | M |
| NFR-SEC-004 | Infra & NFR | [Sec] 응답자 IP 해싱(비식별화) 처리 로직 구현 및 검증 | §6.2.3 RESPONSE.ip_hash | BE-FORM-004 | M |

### 4-C. 모니터링·운영(Monitoring) Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-MON-001 | Infra & NFR | [Mon] Vercel Analytics 연동 설정 + 파싱 파이프라인 전 단계 trace 커버리지 100% 구현 | §4.2.5 REQ-NF-026 | BE-PARSE-005 | M |
| NFR-MON-002 | Infra & NFR | [Mon] Slack Webhook 통합 알림 모듈 구현: 결제 실패, 쿼터 도달, 레이턴시 초과, 라우팅 실패 통합 | §4.2.5 REQ-NF-024, 025 | DB-010 | M |
| NFR-MON-003 | Infra & NFR | [Mon] 북극성 KPI(유료 ZIP 다운로드 완료 건수) DB AUDIT_LOG 기록 + Prisma 쿼리 대시보드 집계 구현 | §4.2.5 REQ-NF-027 | BE-PAY-002, DB-010 | M |
| NFR-MON-004 | Infra & NFR | [Mon] GA4 연동: Next.js Script 태그 + utm 파라미터 트래킹 + 워터마크 퍼널 분석 설정 | §4.2.5 REQ-NF-028 | FE-WM-002 | M |
| NFR-MON-005 | Infra & NFR | [Mon] 운영자 대시보드: 파싱 완료율, 결제 전환율, 쿼터 상태 일간/주간 KPI 집계 화면 구현 | §4.2.8 REQ-NF-033~037 | NFR-MON-003 | H |

### 4-D. 인프라·배포(Infra & DevOps) Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-INFRA-001 | Infra & NFR | [Infra] Next.js App Router 프로젝트 초기 셋업: /app/(dashboard)/ + /app/(survey)/ 라우트 그룹 구조 생성 | §3.2, §3.4, C-TEC-001 | None | M |
| NFR-INFRA-002 | Infra & NFR | [Infra] Tailwind CSS + shadcn/ui 초기 설정 및 디자인 시스템 토큰 정의 | §1.2.3 C-TEC-004 | NFR-INFRA-001 | M |
| NFR-INFRA-003 | Infra & NFR | [Infra] Vercel 프로젝트 연결 + Git Push 자동 배포(CI/CD) 설정 | §1.2.3 C-TEC-007 | NFR-INFRA-001 | L |
| NFR-INFRA-004 | Infra & NFR | [Infra] Supabase 프로젝트 생성 + PostgreSQL 연결 + Storage 버킷 설정 | §1.2.3 C-TEC-003 | NFR-INFRA-001 | M |
| NFR-INFRA-005 | Infra & NFR | [Infra] 환경 변수 관리: Gemini API Key, Supabase URL/Anon Key, PG 시크릿 키, Slack Webhook URL 등 | §1.2.3 C-TEC-005, 006 | NFR-INFRA-003, NFR-INFRA-004 | L |
| NFR-INFRA-006 | Infra & NFR | [Infra] Vercel AI SDK + Google Gemini API 연동 초기 설정 확인 (환경 변수만으로 모델 교체 가능 검증) | §1.2.3 C-TEC-005, 006, CON-05 | NFR-INFRA-005 | M |
| NFR-INFRA-007 | Infra & NFR | [Infra] 모듈 간 순환 의존성 검증 도구 설정 (eslint-plugin-import 또는 madge) | §4.2.7 REQ-NF-032 | NFR-INFRA-001 | L |

### 4-E. 비용·예산(Cost) Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-COST-001 | Infra & NFR | [Cost] 단건 파싱 원가 ≤ 20원(KRW) 검증: Gemini API 호출 비용 모니터링 및 측정 스크립트 작성 | §4.2.4 REQ-NF-021 | BE-PARSE-005 | M |
| NFR-COST-002 | Infra & NFR | [Cost] 클라우드 예산 초과 자동 알람 설정: Vercel Usage Alert + Supabase Usage Alert + Gemini API 쿼터 모니터링 | §4.2.4 REQ-NF-023 | NFR-INFRA-003, NFR-INFRA-004 | M |

### 4-F. Fallback & 장애 대응 Task

| Task ID | Epic (도메인) | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 (H/M/L) |
|---|---|---|---|---|---|
| NFR-FB-001 | Infra & NFR | [Fallback] PG사 장애 시 payment_pending 상태 DB 기록 + 복구 시 재검증 처리 + '결제 시스템 점검 중' 안내 모달 구현 | §3.1 EXT-01 Fallback | BE-PAY-001, BE-PAY-002 | H |
| NFR-FB-002 | Infra & NFR | [Fallback] Supabase Storage 장애 시 Vercel /tmp ZIP 임시 저장 + Route Handler 직접 스트리밍 Fallback 구현 | §3.1 EXT-02 Fallback | BE-PAY-004 | H |
| NFR-FB-003 | Infra & NFR | [Fallback] Vercel Analytics 장애 시 AUDIT_LOG 테이블 직접 Structured JSON 기록 + 대시보드 UI 배너 알림 표시 | §3.1 EXT-04 Fallback | DB-010, NFR-MON-001 | M |

---

## Step 5 — UI/UX 프론트엔드 태스크

> **목적:** 백엔드 로직과 분리된 순수 프론트엔드 UI 컴포넌트 및 페이지 조립 태스크를 추출하여 디자인 시스템을 코드로 구현한다.

### 5.1 공통 UI 인프라

| Task ID | Epic | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 |
|---|---|---|---|---|---|
| **UI-001** | UI | shadcn/ui + Tailwind 디자인 시스템 토큰 적용 및 기반 환경 세팅 | NFR-INFRA | NFR-INFRA-002 | M |
| **UI-002** | UI | 공통 레이아웃 컴포넌트 (GNB 헤더, 모바일 하단 네비게이션, 셸) | §6.3 | UI-001 | M |
| **UI-003** | UI | 글로벌 토스트 알림 컴포넌트 (저장 완료, 에러 발생, AI 주치의 알림) | §6.3 | UI-001 | L |
| **UI-004** | UI | 글로벌 로딩 스켈레톤 및 파싱 프로그레스 바 컴포넌트 | §6.3.1 | UI-001 | M |

### 5.2 도메인별 페이지·컴포넌트

| Task ID | Epic | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 |
|---|---|---|---|---|---|
| **UI-010** | Document Parser | 랜딩 페이지 — HWPX/Word/PDF 파일 드래그 앤 드롭 업로드 영역 UI | §4.1.1 | UI-002 | M |
| **UI-011** | Document Parser | 문서 파싱 대기 화면 — Lottie 애니메이션 및 AI 진행률 상태 표시 UI | §4.1.1 | UI-010 | M |
| **UI-020** | Form Editor | 폼 에디터 메인 화면 — 3단 레이아웃 (좌측 패널, 중앙 에디터, 우측 속성) | §6.3.6 | UI-002 | H |
| **UI-021** | Form Editor | 문항 카드 컴포넌트 (질문, 보기, 드래그 핸들, 타입 변경 셀렉트박스) | §6.3.6 | UI-020 | H |
| **UI-022** | Form Editor | AI 주치의 제안 배지 및 상세 수락/거절 팝업 모달 UI | §4.1.1 | UI-021 | M |
| **UI-023** | Form Editor | 스킵 로직(조건부 분기) 설정 시각화 컴포넌트 | §6.3.6 | UI-020 | H |
| **UI-030** | Survey Response | 모바일 최적화 설문 응답 폼 렌더러 (페이지네이션, 터치 버튼) | §6.3.2 | UI-001 | H |
| **UI-031** | Survey Response | 바이럴 워터마크 푸터 컴포넌트 ("나도 10초만에 설문지 만들기") | §4.1.5 | UI-030 | L |
| **UI-040** | DataMap & Paywall | 설문 종료 후 데이터맵 샘플 미리보기(모자이크 처리) UI | §4.1.2 | UI-030 | M |
| **UI-041** | DataMap & Paywall | Paywall 결제 유도 모달 및 PG사 연동 로딩 화면 UI | §3.6.2 | UI-040 | M |

### 5.3 관리자 백오피스 UI

| Task ID | Epic | Feature (기능명) | 관련 SRS 섹션 | 선행 태스크 (Dependencies) | 복잡도 |
|---|---|---|---|---|---|
| **UI-050** | Admin | 관리자 로그인 및 대시보드 공통 레이아웃 (LNB) | §1.3 | UI-002 | M |
| **UI-051** | Admin | AI Data Bouncer (휴지통) 대시보드 — 의심 응답 목록 테이블 및 상세 사유 뷰어 | §4.1.8 | UI-050 | H |
| **UI-052** | Admin | 쿼터 모니터링 대시보드 — 성별/연령별 달성률 프로그레스 게이지 UI | §4.1.4 | UI-050 | M |
| **UI-053** | Admin | 수익/결제 현황 대시보드 — ZIP 패키지 다운로드 수 및 전환율 차트 UI | §4.2.8 | UI-050 | M |

---

## 전체 태스크 의존성 맵 (Dependency Graph)

```mermaid
flowchart TD
    subgraph S1["Step 1: Foundation Layer"]
        subgraph DB["DB 스키마"]
            DB001[DB-001: Prisma 초기화]
            DB002[DB-002: USER] --> DB001
            DB003[DB-003: DOCUMENT] --> DB002
            DB004[DB-004: PARSED_FORM] --> DB003
            DB005[DB-005: RESPONSE] --> DB004
            DB006[DB-006: ZIP_DATAMAP] --> DB004
            DB007[DB-007: QUOTA_SETTING] --> DB004
            DB008[DB-008: QUOTA_CELL] --> DB007
            DB009[DB-009: ROUTING_CONFIG] --> DB004
            DB010[DB-010: AUDIT_LOG] --> DB002
            DB011[DB-011: Enum 정의] --> DB001
            DB012[DB-012: RPC 함수] --> DB008
        end

        subgraph API["API 계약"]
            API001[API-001~015: DTO 및 에러 코드] --> DB003
        end

        subgraph MOCK["Mock 데이터"]
            MOCK001[MOCK-001~008: Mock API 및 Seed] --> API001
        end
    end

    subgraph S2["Step 2: Feature Layer"]
        subgraph PARSE["Document Parser"]
            BEPARSE[BE-PARSE-001~010]
            FEPARSE[FE-PARSE-001~006]
        end
        subgraph FORM["Form Management"]
            BEFORM[BE-FORM-001~004]
            FEFORM[FE-FORM-001~007]
        end
        subgraph PAY["DataMap and Paywall"]
            BEPAY[BE-PAY-001~006]
            FEPAY[FE-PAY-001~004]
        end
        subgraph WM["Watermark"]
            BEWM[BE-WM-001~002]
            FEWM[FE-WM-001~002]
        end
        subgraph QT["Quota"]
            BEQT[BE-QT-001~005]
            FEQT[FE-QT-001~002]
        end
        subgraph RT["Routing"]
            BERT[BE-RT-001~003]
            FERT[FE-RT-001]
        end
        subgraph RL["Auth and RateLimit"]
            BERL[BE-RL-001~002]
        end
        subgraph RET["Retention"]
            BERET[BE-RET-001~002]
        end
        subgraph DASH["Dashboard"]
            BEDASH[BE-DASH-001~002]
            FEDASH[FE-DASH-001~003]
        end
        subgraph AUTH["Authentication"]
            BEAUTH[BE-AUTH-001~002]
            FEAUTH[FE-AUTH-001~003]
        end
        subgraph ADMIN["Admin"]
            BEADMIN[BE-ADMIN-001]
            FEADMIN[FE-ADMIN-001~002]
        end
    end

    subgraph S3["Step 3: Test Layer"]
        TEST[TEST-PARSE / TEST-PAY / TEST-WM / TEST-QT / TEST-RT / TEST-RET / TEST-FORM / TEST-ADMIN]
    end

    subgraph S4["Step 4: NFR and Infra"]
        INFRA[NFR-INFRA-001~007]
        PERF[NFR-PERF-001~004]
        SEC[NFR-SEC-001~004]
        MON[NFR-MON-001~005]
        COST[NFR-COST-001~002]
        FB[NFR-FB-001~003]
    end

    subgraph S5["Step 5: UI Component Layer"]
        UICORE[UI-001~004: Core UI]
        UIPARSE[UI-010~011: Parser UI]
        UIFORM[UI-020~023: Form UI]
        UIRES[UI-030~031: Response UI]
        UIPAY[UI-040~041: Paywall UI]
        UIADMIN[UI-050~053: Admin UI]
    end

    INFRA --> UICORE
    UICORE --> UIPARSE
    UICORE --> UIFORM
    UICORE --> UIRES
    UICORE --> UIPAY
    UICORE --> UIADMIN

    UIPARSE --> FEPARSE
    UIFORM --> FEFORM
    UIRES --> FEFORM
    UIPAY --> FEPAY
    UIADMIN --> FEADMIN

    DB002 --> BEPARSE
    DB003 --> BEPARSE
    DB004 --> BEFORM
    DB005 --> BEPAY
    DB007 --> BEQT
    DB009 --> BERT
    DB012 --> BEQT

    MOCK001 --> FEPARSE
    MOCK001 --> FEFORM
    MOCK001 --> UIPARSE
    MOCK001 --> UIFORM

    BEPARSE --> TEST
    BEFORM --> TEST
    BEPAY --> TEST
    BEQT --> TEST
    BERT --> TEST

    BEPARSE --> PERF
    BEPAY --> MON
    BEQT --> PERF

    BEPAY --> FB
```

---

## 전체 태스크 요약 통계

| Step | 카테고리 | 태스크 수 | 복잡도 분포 (H/M/L) |
|---|---|---|---|
| **Step 1** | DB 스키마 | 12 | 1H / 6M / 5L |
| **Step 1** | API 계약 | 16 | 0H / 6M / 10L |
| **Step 1** | Mock 데이터 | 8 | 0H / 5M / 3L |
| **Step 2** | Document Parser (BE) | 10 | 3H / 5M / 2L |
| **Step 2** | Document Parser (FE) | 6 | 0H / 2M / 4L |
| **Step 2** | Form Management (BE) | 4 | 1H / 2M / 1L |
| **Step 2** | Form Management (FE) | 7 | 3H / 3M / 1L |
| **Step 2** | DataMap & Paywall (BE) | 6 | 3H / 2M / 1L |
| **Step 2** | DataMap & Paywall (FE) | 4 | 1H / 2M / 1L |
| **Step 2** | Watermark (BE+FE) | 4 | 0H / 1M / 3L |
| **Step 2** | Quota Management (BE) | 5 | 2H / 3M / 0L |
| **Step 2** | Quota Management (FE) | 3 | 2H / 1M / 0L |
| **Step 2** | Panel Routing (BE+FE) | 5 | 2H / 2M / 1L |
| **Step 2** | Rate Limit & Auth (BE+FE) | 3 | 2H / 0M / 1L |
| **Step 2** | Data Retention | 2 | 1H / 1M / 0L |
| **Step 2** | Dashboard (BE+FE) — *v2 추가* | 5 | 0H / 5M / 0L |
| **Step 2** | Authentication (BE+FE) — *v2 추가* | 5 | 0H / 5M / 0L |
| **Step 2** | Admin (BE+FE) — *v2 추가* | 3 | 0H / 3M / 0L |
| **Step 3** | 테스트 (전체) | 33 | 4H / 23M / 6L |
| **Step 4** | NFR (성능/보안/모니터링/인프라/비용/Fallback) | 25 | 5H / 14M / 6L |
| **Step 5** | UI/UX 프론트엔드 공통 컴포넌트 | 4 | 0H / 2M / 2L |
| **Step 5** | UI/UX 도메인 페이지 및 모달 | 10 | 4H / 5M / 1L |
| **Step 5** | UI/UX 관리자 백오피스 | 4 | 1H / 3M / 0L |
| | **합계** | **184** | **35H / 101M / 48L** |

---

### 개발 착수 순서 (권장)

> **NFR-INFRA (프로젝트 셋업) → [병렬 1] Step 5 UI (퍼블리싱) & [병렬 2] Step 1 DB/API/MOCK (계약) → Step 2 BE/FE Feature (로직 연동) → Step 3 TEST (검증) → Step 4 NFR (비기능)**

### 병렬화 가능 구간

> **Contract & UI First:** Mock 데이터(MOCK-*)와 UI 컴포넌트(UI-*)가 선행되면, 프론트엔드 로직(FE-*)은 백엔드 로직(BE-*) 완성을 기다리지 않고 곧바로 **데이터 바인딩 및 상태 연동** 개발이 가능합니다. 이는 1인 개발 1순위 병목을 해소하는 핵심 이점입니다.

### 주의 사항

> **REQ-FUNC-028 (캐시):** SRS 원문에는 "Vercel KV 기반 캐시"로 명시되어 있으나, CON-03 및 ADR-02에서 "별도 캐시 서버 불가"로 제약하고 있어, Supabase DB 기반 파일 해시 캐시로 대체 구현합니다 (BE-PARSE-010 참조).

---

*End of Document — TASK-001*