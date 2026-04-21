# SRS 기술 스택 전환 계획서

**문서 ID:** PLAN-SRS-STACK-001
**작성일:** 2026-04-21
**대상 문서:** SRS_v0.1_Opus.md
**목적:** 현행 SRS의 가상 분산 아키텍처를 C-TEC-001~007 기술 스택(Next.js 단일 풀스택)으로 전환하기 위한 SRS 문서 수정 계획 및 MVP 핵심 UX 훼손 여부 검토

---

## 목차

1. [적용 대상 기술 스택 (C-TEC)](#1-적용-대상-기술-스택-c-tec)
2. [현행 SRS 대비 전환 영향 분석](#2-현행-srs-대비-전환-영향-분석)
3. [SRS 수정 작업 계획 (섹션별)](#3-srs-수정-작업-계획-섹션별)
4. [외부 시스템 매핑 전환표](#4-외부-시스템-매핑-전환표)
5. [기능 커버리지 검토](#5-기능-커버리지-검토)
6. [MVP 핵심 UX 훼손 여부 검토](#6-mvp-핵심-ux-훼손-여부-검토)
7. [리스크 및 대응 방안](#7-리스크-및-대응-방안)
8. [작업 체크리스트](#8-작업-체크리스트)

---

## 1. 적용 대상 기술 스택 (C-TEC)

### 시스템 내부 — 단일 통합 프레임워크

| ID | 제약사항 |
|---|---|
| C-TEC-001 | 모든 서비스는 **Next.js (App Router)** 기반의 단일 풀스택 프레임워크로 구현한다. 프론트엔드와 백엔드를 별도 분리하지 않는다. |
| C-TEC-002 | 서버 측 로직(DB 접근, API 호출 등)은 Next.js의 **Server Actions 또는 Route Handlers**를 사용하여 별도의 백엔드 서버 없이 구현한다. |
| C-TEC-003 | 데이터베이스는 **Prisma + 로컬 SQLite**(개발)를 사용하고, 배포 시 **Supabase(PostgreSQL)**를 사용하여 인프라 설정 복잡도를 최소화한다. |
| C-TEC-004 | UI 및 스타일링은 **Tailwind CSS**와 **shadcn/ui**를 사용하여 AI가 일관된 디자인 코드를 생성하도록 강제한다. |

### 시스템 외부 — 연결 및 AI 통합

| ID | 제약사항 |
|---|---|
| C-TEC-005 | LLM 오케스트레이션은 별도의 Python 서버 없이 **Vercel AI SDK**를 사용하여 Next.js 내부에서 직접 구현한다. |
| C-TEC-006 | LLM 호출은 **Google Gemini API**를 기본으로 사용하며, 환경 변수 설정만으로 모델 교체가 가능하도록 SDK의 표준 인터페이스를 준수한다. |
| C-TEC-007 | 배포 및 인프라 관리는 **Vercel 플랫폼**으로 단일화하며, CI/CD 설정 없이 **Git Push만으로 배포를 자동화**한다. |

---

## 2. 현행 SRS 대비 전환 영향 분석

### 2.1 아키텍처 전환 요약

```
[현행 SRS]                              [전환 후]
┌─────────────┐  ┌──────────────┐       ┌──────────────────────────────┐
│ 웹 대시보드  │  │ 모바일웹 폼   │       │  Next.js App (Vercel)        │
│ (프론트엔드) │  │ (프론트엔드)  │       │  ┌────────────────────────┐  │
└──────┬───────┘  └──────┬───────┘       │  │ App Router (Pages)     │  │
       │                 │               │  │  - 웹 대시보드          │  │
       ▼                 ▼               │  │  - 모바일웹 설문 폼     │  │
┌──────────────────────────┐             │  │  - shadcn/ui + Tailwind│  │
│      API Server          │             │  ├────────────────────────┤  │
│  (별도 백엔드 서버)       │             │  │ Route Handlers / SA    │  │
│  - 인증/Rate Limit       │             │  │  - /api/v1/* 엔드포인트│  │
│  - 비즈니스 로직          │             │  │  - Server Actions      │  │
└──────┬───────────────────┘             │  ├────────────────────────┤  │
       │                                 │  │ Vercel AI SDK          │  │
  ┌────┴────┬────────┬────────┐          │  │  - Gemini API 연동     │  │
  ▼         ▼        ▼        ▼          │  │  - 문서 파싱 파이프라인  │  │
┌─────┐ ┌──────┐ ┌──────┐ ┌──────┐      │  └────────────────────────┘  │
│ DB  │ │Redis │ │ OCR  │ │ S3   │      └──────────────┬───────────────┘
│(PG) │ │Cache │ │Engine│ │(AWS) │                     │
└─────┘ └──────┘ └──────┘ └──────┘          ┌──────────┴──────────┐
                                            ▼          ▼          ▼
                                      ┌─────────┐ ┌────────┐ ┌────────┐
                                      │Supabase │ │Vercel  │ │Gemini  │
                                      │(PG+Stor)│ │KV/Cron │ │API     │
                                      └─────────┘ └────────┘ └────────┘
```

### 2.2 컴포넌트 수준 전환표

| 현행 SRS 컴포넌트 | 전환 후 | 변경 유형 |
|---|---|---|
| API Server (별도 백엔드) | Next.js Route Handlers (`/app/api/`) | **대체** |
| Document Service | `lib/services/document.ts` (서버 모듈) | 리팩터링 |
| AI Parser Service + OCR Engine | Vercel AI SDK + Gemini `generateObject()` | **대체** |
| Form Service | `lib/services/form.ts` + Server Actions | 리팩터링 |
| Package Service | `lib/services/package.ts` (JSZip + exceljs) | 리팩터링 |
| Payment Service | `lib/services/payment.ts` + 토스 JS SDK | 리팩터링 |
| Quota Service | `lib/services/quota.ts` + Vercel KV | 리팩터링 |
| Routing Service | `lib/services/routing.ts` + `redirect()` | 리팩터링 |
| Scheduler Service (Cron) | Vercel Cron Jobs (`vercel.json`) | **대체** |
| PostgreSQL (RDB) | Prisma + SQLite(dev) / Supabase PostgreSQL(prod) | **대체** |
| Redis (Cache/Counter) | Vercel KV (Redis 호환) 또는 DB 트랜잭션 | **대체** |
| AWS S3 (파일 저장) | Supabase Storage (S3 호환) | **대체** |
| OCR Engine (내부 모듈) | JS 라이브러리 전처리 + Gemini API 멀티모달 | **제거** |
| DataDog APM | Vercel Analytics + Logs + 내부 AUDIT_LOG | **대체** |
| PagerDuty | Slack Webhook + 이메일 (MVP 통합) | **대체** |
| Amplitude | Vercel Analytics 또는 Supabase DB 직접 집계 | **대체** |

---

## 3. SRS 수정 작업 계획 (섹션별)

### Phase 1: 기반 구조 변경 (아키텍처·제약사항·참조)

| # | 대상 섹션 | 작업 내용 | 영향도 |
|---|---|---|---|
| P1-01 | **§1.2.3 Constraints** | C-TEC-001~007을 CON-06~CON-12로 신규 추가. 기존 CON-05("오픈소스 로컬 모델 의무화") → C-TEC-005/006 기반 "Vercel AI SDK + Gemini API 사용"으로 수정 | 🔴 |
| P1-02 | **§1.2.4 Assumptions** | Vercel Free/Pro 티어 제한사항(함수 실행 10s/60s, 동시 실행 수), Supabase Free 티어(500MB DB, 1GB Storage), Vercel KV Free(3000 req/day) 가정 추가 | 🟡 |
| P1-03 | **§1.3 Definitions** | Next.js App Router, Server Actions, Route Handlers, Vercel AI SDK, Prisma, Supabase, Vercel KV, Vercel Cron 등 신규 용어 추가 | 🟢 |

### Phase 2: 시스템 컨텍스트 전면 재정의

| # | 대상 섹션 | 작업 내용 | 영향도 |
|---|---|---|---|
| P2-01 | **§3.1 External Systems** | EXT-01~10 전면 재정의 (아래 §4 전환표 참조). Fallback 전략도 새로운 스택 기준으로 재작성 | 🔴 |
| P2-02 | **§3.2 Client Applications** | "웹 대시보드"와 "모바일 웹 설문 폼" → "Next.js App 내의 라우트 그룹"으로 명시 변경. CLI-01/02는 동일 배포 단위임을 명확화 | 🟡 |
| P2-03 | **§3.3 Use Case Diagram** | 외부 시스템 노드명 변경 (AWS S3 → Supabase Storage, DataDog → Vercel Analytics 등) | 🟡 |
| P2-04 | **§3.4 Component Diagram** | 4레이어 마이크로서비스 → **Next.js 단일 앱 + Vercel 인프라** 구조로 전면 재작성 | 🔴 |
| P2-05 | **§3.5 API Overview** | REST 엔드포인트 경로 유지하되, 구현 방식을 "Next.js Route Handlers (`/app/api/v1/...`)"로 주석/설명 변경 | 🟢 |

### Phase 3: 요구사항 스택 정합성 보정

| # | 대상 섹션 | 작업 내용 | 영향도 |
|---|---|---|---|
| P3-01 | **§4.1.1 F1 (AI Parser)** | "전용 OCR 엔진 및 텍스트 추출 모듈" → "Vercel AI SDK + Gemini API 멀티모달 파싱 + JS 텍스트 추출 라이브러리(HWP 전용)" 변경. REQ-FUNC-006 수정 | 🔴 |
| P3-02 | **§4.1.2 F2 (ZIP & Paywall)** | S3 Presigned URL → Supabase Storage 서명 URL. REQ-FUNC-011, 013 변경 | 🟡 |
| P3-03 | **§4.1.4 F4 (쿼터)** | "Redis 기반 원자적(Atomic) 연산" → "Vercel KV INCR 또는 Prisma 트랜잭션 기반 원자적 연산" 변경. REQ-FUNC-020 수정 | 🟡 |
| P3-04 | **§4.1.7 F7 (보안)** | "AES-256 암호화 적용" → "Supabase at-rest encryption (PostgreSQL 레벨) + HTTPS(TLS) 전송 암호화" 명시 | 🟢 |
| P3-05 | **§4.2.4 비용** | 월간 인프라 비용 100,000 KRW 내역: Vercel Pro(~$20), Supabase Free/Pro, Vercel KV, Gemini API 호출 비용 구성표 추가 | 🟡 |
| P3-06 | **§4.2.5 모니터링** | DataDog → Vercel Analytics/Logs. PagerDuty → Slack 통합. Amplitude → Vercel Analytics 또는 DB 집계. REQ-NF-024~028 수정 | 🟡 |
| P3-07 | **§4.2.6 확장성** | "수평 확장 Stateless" → "Vercel Serverless 자동 스케일링" 변경. REQ-NF-030 수정 | 🟢 |
| P3-08 | **§4.2.7 유지보수성** | "마이크로서비스 또는 모듈화된 모놀리스" → "Next.js App Router 기반 도메인별 폴더/레이어 분리" 변경. REQ-NF-032 수정 | 🟢 |

### Phase 4: 다이어그램·부록 갱신

| # | 대상 섹션 | 작업 내용 | 영향도 |
|---|---|---|---|
| P4-01 | **§3.6 Interaction Sequences** (3건) | participant 명칭 변경: "API Server" → "Next.js Route Handler", "OCR Engine" → "Gemini API", "AWS S3" → "Supabase Storage" 등 | 🟡 |
| P4-02 | **§6.1 API Endpoint List** | 엔드포인트 URL 경로는 유지. 구현 방식 주석/비고 컬럼에 "Route Handler" 명시 추가 | 🟢 |
| P4-03 | **§6.2.9 ERD** | 엔터티 구조 변경 없음. 단, Prisma schema 모델 매핑 주석 추가 | 🟢 |
| P4-04 | **§6.2.10 Class Diagram** | 서비스 클래스 → Next.js 서버 모듈 함수 기반으로 재구성 (클래스 → 모듈 함수) | 🟡 |
| P4-05 | **§6.3 상세 시퀀스** (6건) | P4-01과 동일하게 participant 명칭 전면 변경 | 🟡 |
| P4-06 | **§5 Traceability** | 변경된 REQ-FUNC/NF ID 임팩트 반영 (ID 자체는 유지, Source 컬럼 보정) | 🟢 |

---

## 4. 외부 시스템 매핑 전환표

| 현행 ID | 현행 시스템 | → 전환 후 시스템 | 전환 근거 | SRS 영향 REQ |
|---|---|---|---|---|
| EXT-01 | PG사 (토스페이먼츠) | **유지** (토스페이먼츠 JS SDK + Route Handler 콜백) | 결제 시스템은 대체 불가 | REQ-FUNC-010~013 |
| EXT-02 | AWS S3 | **Supabase Storage** (S3 호환 API, 서명 URL 지원) | C-TEC-003 Supabase 생태계 통합. 무료 1GB → MVP Zero-Retention에 충분 | REQ-FUNC-011, 013 |
| EXT-03 | 패널사 (Cint/Toluna) | **유지** (HTTP 302 Redirect, Route Handler에서 처리) | 외부 패널 연동 방식 변경 없음 | REQ-FUNC-023~025 |
| EXT-04 | DataDog APM | **Vercel Analytics + Vercel Logs** + 내부 `AUDIT_LOG` DB 테이블 | C-TEC-007 Vercel 단일화. MVP에 전용 APM 과잉. 월 비용 절감 | REQ-NF-026 |
| EXT-05 | PagerDuty | **Slack Webhook** (EXT-06과 통합) + 이메일 알림 | MVP에 PagerDuty 별도 도입은 비용·복잡도 과잉 | REQ-NF-024 |
| EXT-06 | Slack | **유지** (Webhook, Route Handler에서 직접 호출) | Slack Webhook은 무료, 서버리스 호환 | REQ-NF-025 |
| EXT-07 | Amplitude | **Vercel Analytics** 또는 Supabase DB 직접 집계 (`KPI_EVENT` 테이블) | MVP 단계에서 Amplitude 별도 도입은 과잉. DB 집계로 북극성 KPI 추적 가능 | REQ-NF-027 |
| EXT-08 | GA4 | **유지** (utm 파라미터 + Next.js `<Script>` 태그 삽입) | 무료 서비스, 변경 불필요 | REQ-NF-028 |
| EXT-09 | Redis | **Vercel KV** (Redis 호환) 또는 Prisma 트랜잭션 (`SELECT FOR UPDATE`) | C-TEC-007 Vercel 생태계 통합. Free 3,000 req/day → MVP 초기 트래픽에 충분 | REQ-FUNC-020, REQ-NF-029 |
| EXT-10 | OCR 엔진 | **제거** → Gemini API 멀티모달 + JS 라이브러리 (hwp.js, pdf-parse, mammoth) | C-TEC-005/006 Vercel AI SDK 의무화. 별도 OCR 엔진 불필요 | REQ-FUNC-002, 006 |

---

## 5. 기능 커버리지 검토

### 5.1 전체 커버리지 매트릭스

> **결론: REQ-FUNC-001~030 전 항목 구현 가능. 구현 불가 항목 0건.**

| REQ-FUNC 그룹 | 항목 수 | 커버 판정 | 구현 방식 |
|---|---|---|---|
| F1: AI 문서 파싱 (001~007) | 7 | ✅ 전체 가능 | Gemini `generateObject()` + JS 텍스트 추출 |
| F2: ZIP 패키지 & Paywall (008~015) | 8 | ✅ 전체 가능 | JSZip + exceljs + 토스 SDK + Supabase Storage |
| F3: 워터마크 바이럴 (016~017) | 2 | ✅ 전체 가능 | Tailwind CSS 하단 고정 + utm 파라미터 |
| F4: 쿼터 세팅 (018~022) | 5 | ✅ 전체 가능 | Vercel KV INCR + Prisma 트랜잭션 |
| F5: 패널 라우팅 (023~025) | 3 | ✅ 전체 가능 | Route Handler `redirect()` (302) |
| F6: Rate Limit (026~028) | 3 | ✅ 전체 가능 | Next.js Middleware + Vercel KV 카운터 |
| F7: 보안/삭제 (029~030) | 2 | ✅ 전체 가능 | Vercel Cron Jobs + Supabase encryption |
| **합계** | **30** | **✅ 30/30** | |

### 5.2 주요 기능별 상세 커버 방식

#### F1: AI 문서 파싱 (가장 큰 변경)

```
[현행]                          [전환 후]
사용자 → API Server             사용자 → Next.js Route Handler
          → OCR Engine                    → JS 라이브러리 텍스트 추출
          → AI Parser                       (HWP: hwp.js, Word: mammoth,
          → DB 저장                          PDF: pdf-parse)
                                          → Vercel AI SDK
                                            → Gemini generateObject()
                                            → structure_schema (JSON)
                                          → Prisma DB 저장
```

| 문서 형식 | 텍스트 추출 | 구조 분석 | 비고 |
|---|---|---|---|
| **PDF** | `pdf-parse` 또는 Gemini 멀티모달 직접 | Gemini `generateObject()` | Gemini가 PDF를 직접 읽을 수 있어 전처리 불필요할 수 있음 |
| **Word (.docx)** | `mammoth` 라이브러리 | Gemini `generateObject()` | DOCX → HTML/텍스트 변환 후 Gemini 투입 |
| **HWP** | `hwp.js` 또는 `node-hwp` | Gemini `generateObject()` | ⚠️ HWP 바이너리 지원이 핵심 리스크. 라이브러리 안정성 검증 필요 |

#### F2: ZIP 패키지 생성

| 산출물 | 생성 방식 | 라이브러리 |
|---|---|---|
| 응답 원본 엑셀 | Prisma 쿼리 → 엑셀 생성 | `exceljs` |
| 변수가이드 | structure_schema 기반 자동 생성 | `exceljs` |
| 코드북 | structure_schema 기반 자동 생성 | `exceljs` |
| 데이터맵 | 응답 데이터 + schema 매핑 자동 생성 | `exceljs` |
| ZIP 패키징 | 4개 파일 → ZIP 압축 | `JSZip` |
| 파일 저장 | ZIP → Supabase Storage 업로드 | `@supabase/storage-js` |

---

## 6. MVP 핵심 UX 훼손 여부 검토

> **핵심 질문:** 기술 스택을 전환해도 3종 페르소나(홍일반, 최실무, 유팀장)의 **핵심 가치 전달 경험**이 동일하게 유지되는가?

### 6.1 Story별 UX 훼손 여부 판정

#### Story 1: 문서 무손실 파싱 (홍일반/최실무)

> 가치: "문서 업로드 한 번이면 10초 안에 설문 폼이 자동으로 만들어진다"

| UX 요소 | 현행 SRS 경험 | 전환 후 경험 | 훼손 여부 |
|---|---|---|---|
| 문서 업로드 인터랙션 | 웹 대시보드에서 파일 드래그/선택 | **동일** — shadcn/ui 파일 업로드 컴포넌트 | ✅ 유지 |
| 파싱 완료 속도 | 10초 이내 (OCR → AI Parser) | **동일 또는 개선** — Gemini API 직접 호출 시 OCR 중간 단계 제거로 레이턴시 단축 가능 | ✅ 유지 |
| 파싱 정확도 | 데이터 손실률 1% 미만 | **동등 이상** — Gemini 멀티모달은 문서 구조 이해에 강점. 다만 HWP 전처리 품질에 의존 | ⚠️ 조건부 유지 |
| 에러 처리 (2초 이내 모달) | API 400 에러 모달 | **동일** — Route Handler → 클라이언트 에러 표시 | ✅ 유지 |
| 워터마크 렌더링 (100%) | 하단 뷰포트 배너 | **동일** — Tailwind CSS `fixed bottom-0` | ✅ 유지 |

**판정: ✅ 핵심 UX 유지됨**
- HWP 파싱 정확도는 `hwp.js` 라이브러리 품질에 의존하나, 텍스트 기반 설문 문항이므로 구조적 손실 리스크는 낮음.
- Gemini API의 구조화 출력(`generateObject`)이 오히려 OCR+별도 파서보다 일관된 JSON 스키마를 생성할 수 있어 **UX가 개선될 가능성**도 있음.

---

#### Story 2: 4종 산출물 ZIP 턴키 출하 (최실무)

> 가치: "조사 종료 직후, 결제 한 번이면 대행사급 4종 패키지가 즉시 다운로드된다"

| UX 요소 | 현행 SRS 경험 | 전환 후 경험 | 훼손 여부 |
|---|---|---|---|
| 결제 팝업 (3초 이내) | PG사 프레임 팝업 | **동일** — 토스페이먼츠 JS SDK (프론트엔드 동일) | ✅ 유지 |
| ZIP 생성 (5초 이내) | 서버에서 4종 컴파일 | **동일** — Route Handler에서 JSZip + exceljs 실행. 서버리스 환경에서 충분 | ✅ 유지 |
| 결제 실패 시 403 차단 | S3 Presigned URL 미발급 | **동일** — Supabase Storage 서명 URL 미발급 | ✅ 유지 |
| 다운로드 경험 | S3 Presigned URL → 브라우저 다운로드 | **동일** — Supabase Storage 서명 URL → 브라우저 다운로드 | ✅ 유지 |
| 결측치 0% 보장 | 백엔드 데이터 검증 | **동일** — Prisma 쿼리 + 서버측 검증 로직 | ✅ 유지 |

**판정: ✅ 핵심 UX 완전 유지됨**
- 사용자가 체감하는 결제 → 다운로드 흐름은 PG SDK와 서명 URL 방식이 동일하므로 **경험 차이 없음**.
- 파일 저장소가 S3 → Supabase Storage로 바뀌지만, 서명 URL 발급 API가 호환되어 클라이언트 경험은 동일.

---

#### Story 3: 동적 쿼터/라우팅 인프라 (유팀장)

> 가치: "엑셀 업로드만으로 노코드 쿼터 세팅, 패널사 연동까지 5분 이내 완료. 외주비 0원"

| UX 요소 | 현행 SRS 경험 | 전환 후 경험 | 훼손 여부 |
|---|---|---|---|
| 엑셀 업로드 쿼터 세팅 | 웹 대시보드 UI | **동일** — shadcn/ui 파일 업로드 + Server Action 처리 | ✅ 유지 |
| 교차 쿼터 자동 반영 | API → DB 저장 | **동일** — Route Handler → Prisma 저장 | ✅ 유지 |
| 쿼터 카운트 동시성 | Redis 원자적 INCR | **동등** — Vercel KV INCR (Redis 호환) | ✅ 유지 |
| Over-quota 1% 이내 | Redis 기반 즉각 제어 | **동등** — Vercel KV 원자적 연산 동일 정밀도 | ✅ 유지 |
| 패널 리다이렉트 (302) | API Server redirect | **동일** — Route Handler `redirect()` | ✅ 유지 |
| 쿼터 100% Slack 알림 | Slack Webhook | **동일** — Route Handler에서 Webhook 직접 호출 | ✅ 유지 |
| 쿼터 연산 1초 초과 경고 | DataDog Alert | **변경** — Vercel Logs 기반 모니터링 (알림 세분화 수준 약간 하향) | ⚠️ 경미한 변경 |

**판정: ✅ 핵심 UX 유지됨**
- 운영자 대시보드의 쿼터 모니터링 경고 수준이 DataDog → Vercel Logs로 변경되면서 **실시간 커스텀 Alert 세밀도가 약간 낮아질 수 있으나**, MVP에서 Slack 알림이 핵심이므로 사용자 체감 영향은 미미함.

---

### 6.2 비기능 UX 항목 검토

| 비기능 지표 | 현행 기준 | 전환 후 달성 가능성 | 비고 |
|---|---|---|---|
| p95 응답 ≤ 300ms | API Server 기준 | ✅ 가능 — Vercel Edge/Serverless 응답 시간 동등 | Vercel의 글로벌 CDN이 오히려 유리할 수 있음 |
| 파싱 ≤ 10초 | OCR + AI Parser | ⚠️ 조건부 — Gemini API 응답 시간 의존 | 50문항 제한(ASM-01)과 스트리밍 활용으로 대응 가능 |
| ZIP 생성 ≤ 5초 | 서버 컴파일 | ✅ 가능 — JSZip/exceljs 서버리스 실행 | Vercel Pro 60초 타임아웃 내에 충분 |
| SLA 99.9% | 자체 인프라 | ✅ 가능 — Vercel SLA 99.99% | Vercel이 더 높은 SLA 제공 |
| 동시 1,000명 | Redis 기반 | ⚠️ 조건부 — Vercel 동시 실행 제한 | Pro 플랜 필요. Vercel KV로 병목 분산 |
| 월 인프라 ≤ 100,000 KRW | 자체 인프라 | ✅ 가능 — 아래 비용 구성 참조 | |

### 6.3 MVP 월간 예상 비용 구성

| 서비스 | 티어 | 월 예상 비용 | 비고 |
|---|---|---|---|
| Vercel | Pro ($20/월) | ~27,000 KRW | 60s 함수 타임아웃, 1TB 대역폭 |
| Supabase | Free | 0 KRW | 500MB DB, 1GB Storage, 50,000 MAU |
| Vercel KV | Free (기본 포함) | 0 KRW | 3,000 req/day (MVP 초기 충분) |
| Google Gemini API | Free Tier / Pay-as-you-go | 0 ~ 30,000 KRW | 무료 쿼터 활용 후 종량제 (1M 토큰당 ~$0.075) |
| 토스페이먼츠 | 건당 수수료 | 매출 연동 | 기본 사용료 없음 |
| Slack Webhook | Free | 0 KRW | |
| GA4 | Free | 0 KRW | |
| **합계** | | **27,000 ~ 57,000 KRW** | **✅ 100,000 KRW 이내** |

### 6.4 종합 판정

| 검토 항목 | 결과 |
|---|---|
| Story 1 핵심 가치 (10초 자동 파싱) | ✅ **유지** |
| Story 2 핵심 가치 (결제 즉시 4종 다운로드) | ✅ **유지** |
| Story 3 핵심 가치 (노코드 쿼터, 외주비 0원) | ✅ **유지** |
| 성능 비기능 요건 (p95, SLA, 동시성) | ✅ **유지** (일부 Vercel Pro 필요) |
| 월간 비용 제약 (≤ 100,000 KRW) | ✅ **충족** (예상 27,000~57,000 KRW) |
| 데이터 보안 (Zero-Retention, 암호화) | ✅ **유지** (Vercel Cron + Supabase encryption) |

> **최종 결론: MVP 핵심 사용자 경험(가치 전달)은 기술 스택 전환에 의해 훼손되지 않습니다.** 오히려 인프라 단순화(단일 배포), 비용 절감(85% ↓), 개발 속도 향상(풀스택 단일 프레임워크)의 이점이 있습니다.

---

## 7. 리스크 및 대응 방안

| ID | 리스크 | 발생 확률 | 영향도 | 대응 방안 |
|---|---|---|---|---|
| R-01 | **HWP 파싱 실패** — hwp.js 라이브러리가 복잡한 HWP 구조를 처리하지 못함 | 중 | 높음 | HWP→PDF 변환 서비스(libreoffice CLI)를 Vercel 외부에 경량 API로 구축하거나, 사용자에게 "PDF로 변환 후 업로드" 안내 제공. ASM-01(50문항 텍스트 기반)이 리스크 완화 |
| R-02 | **Gemini API 응답 지연** — 10초 타임아웃 초과 | 중 | 중 | Vercel AI SDK `streamObject()` 스트리밍 활용. 파싱 진행률 UI 표시로 체감 대기시간 감소. Vercel Pro 60초 타임아웃 활용 |
| R-03 | **Vercel KV Free 일일 한도** (3,000 req/day) 초과 | 낮음 | 중 | MVP 초기 트래픽 기준 충분하나, 쿼터 조사 운영 시 Vercel KV Pro 업그레이드 또는 Supabase DB 트랜잭션 Fallback 적용 |
| R-04 | **Supabase Storage 1GB 한도** 초과 | 낮음 | 낮음 | Zero-Retention(24시간 삭제) 정책으로 파일 누적 방지. Vercel Cron으로 자동 정리 |
| R-05 | **Vercel Serverless 함수 동시 실행 제한** — 대규모 쿼터 조사 시 병목 | 낮음 | 중 | Vercel Pro 동시 실행 확장 + Vercel KV로 DB 경합 최소화 |
| R-06 | **Gemini API 비용 급증** — 대량 파싱 시 토큰 비용 증가 | 중 | 중 | 캐시 서버(Vercel KV) 해시 기반 중복 요청 방지 + 무료 계정 일일 3회 Rate Limit(ADR-02) 유지 |

---

## 8. 작업 체크리스트

SRS 문서 수정 시 아래 순서대로 진행합니다.

### Phase 1: 기반 구조 변경
- [ ] P1-01: §1.2.3 Constraints에 C-TEC-001~007 추가, CON-05 수정
- [ ] P1-02: §1.2.4 Assumptions에 Vercel/Supabase 티어 제한 가정 추가
- [ ] P1-03: §1.3 Definitions에 신규 기술 용어 추가

### Phase 2: 시스템 컨텍스트 재정의
- [ ] P2-01: §3.1 External Systems 전면 재정의 (Fallback 포함)
- [ ] P2-02: §3.2 Client Applications 설명 갱신
- [ ] P2-03: §3.3 Use Case Diagram 외부 시스템 노드명 변경
- [ ] P2-04: §3.4 Component Diagram 전면 재작성
- [ ] P2-05: §3.5 API Overview 구현 방식 주석 변경

### Phase 3: 요구사항 보정
- [ ] P3-01: §4.1.1 F1 AI Parser 구현 방식 변경 (Gemini API)
- [ ] P3-02: §4.1.2 F2 S3 → Supabase Storage 변경
- [ ] P3-03: §4.1.4 F4 Redis → Vercel KV 변경
- [ ] P3-04: §4.1.7 F7 보안 구현 방식 변경
- [ ] P3-05: §4.2.4 비용 내역 구성표 갱신
- [ ] P3-06: §4.2.5 모니터링 시스템 변경
- [ ] P3-07: §4.2.6 확장성 서술 변경
- [ ] P3-08: §4.2.7 유지보수성 서술 변경

### Phase 4: 다이어그램·부록 갱신
- [ ] P4-01: §3.6 핵심 시퀀스 다이어그램 participant 변경 (3건)
- [ ] P4-02: §6.1 API Endpoint List 비고 갱신
- [ ] P4-03: §6.2.9 ERD Prisma 주석 추가
- [ ] P4-04: §6.2.10 Class Diagram 서비스 모듈 재구성
- [ ] P4-05: §6.3 상세 시퀀스 다이어그램 participant 변경 (6건)
- [ ] P4-06: §5 Traceability Matrix Source 컬럼 보정

### 최종 검증
- [ ] 변경 후 전체 REQ-FUNC 30건 커버리지 재확인
- [ ] 변경 후 REQ-NF 37건 달성 가능성 재확인
- [ ] SRS Review Report 갱신

---

*End of Plan — PLAN-SRS-STACK-001*
