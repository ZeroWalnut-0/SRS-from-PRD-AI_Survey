# 📐 TASK 의존성 상세 다이어그램 (Per-Task Granularity)

**Document ID:** TASK-DIAG-002 (AI Survey)  
**Revision:** 2.0  
**Date:** 2026-04-26  
**기반 문서:** [`06_TASK_LIST_v2.md`](./06_TASK_LIST_v2.md) (184개 태스크)  

> 본 문서는 `06_TASK_LIST_v2.md`에 정의된 전체 184개 TASK를 **모두 노드로 표현**한 상세 의존성 그래프를 제공합니다. 화살표 `A --> B`는 "A가 완료되어야 B를 시작할 수 있음"을 의미합니다.

---

## 1. 범례 (Legend)

### 1.1 도메인/역할별 색상 코드

| Epic/Domain | 색상 | 클래스 |
|---|---|---|
| E-DB (데이터베이스) | 🟦 파랑 | `cDb` |
| E-API (API 계약) | 🟦 시안 | `cApi` |
| E-MOCK (Mock 데이터) | 🟪 보라 | `cMock` |
| E-BE (백엔드 로직) | 🟥 빨강 | `cBe` |
| E-FE (프론트 로직) | 🟧 주황 | `cFe` |
| E-TEST (테스트 검증) | ⬜ 연회색 | `cTest` |
| E-NFR (인프라/비기능) | 🟫 갈색 | `cNfr` |
| E-UI (UI/UX 퍼블리싱) | 🟩 초록 | `cUi` |

### 1.2 Step(Phase) 흐름

```text
Step 1(계약/데이터) → Step 5(UI) / Step 2(기능 로직) 병렬 → Step 4(인프라/NFR) → Step 3(테스트)
```

---

## 2. 전체 통합 의존성 다이어그램 (184개 노드 요약도)

> 전체 태스크의 흐름을 단일 그래프로 시각화합니다. (가독성을 위해 상세 노드명은 개별 다이어그램에서 확장합니다)

```mermaid
flowchart TB
    subgraph S1["Step 1 — Foundation (계약 및 데이터)"]
        direction TB
        DB_001["DB-001"] ~~~ DB_012["DB-012"]
        API_001["API-001"] ~~~ API_016["API-016"]
        MOCK_001["MOCK-001"] ~~~ MOCK_008["MOCK-008"]
    end

    subgraph S5["Step 5 — UI/UX 컴포넌트"]
        direction TB
        UI_001["UI-001"] ~~~ UI_053["UI-053"]
    end

    subgraph S2["Step 2 — Feature Logic (CQRS)"]
        direction TB
        BE_PARSE_001["BE-PARSE"] ~~~ FE_PARSE_009["FE-PARSE"]
        BE_FORM_001["BE-FORM"] ~~~ FE_FORM_008["FE-FORM"]
        BE_PAY_001["BE-PAY"] ~~~ FE_PAY_004["FE-PAY"]
        BE_QT_001["BE-QT"] ~~~ FE_QT_004["FE-QT"]
        BE_RT_001["BE-RT"] ~~~ FE_RT_002["FE-RT"]
    end

    subgraph S4["Step 4 — Infra & NFR"]
        direction TB
        NFR_INFRA_001["NFR-INFRA"] ~~~ NFR_FB_003["NFR-FB"]
    end

    subgraph S3["Step 3 — 테스트 자동화"]
        direction TB
        TEST_PARSE_001["TEST-PARSE"] ~~~ TEST_ADMIN_001["TEST-ADMIN"]
    end

    S1 --> S2
    S1 --> S5
    S5 --> S2
    S2 --> S4
    S4 --> S3
    S2 --> S3

    %% Epic colors
    classDef cDb   fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A
    classDef cApi  fill:#CFFAFE,stroke:#0891B2,color:#164E63
    classDef cMock fill:#EDE9FE,stroke:#7C3AED,color:#4C1D95
    classDef cBe   fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D
    classDef cFe   fill:#FFEDD5,stroke:#EA580C,color:#7C2D12
    classDef cNfr  fill:#F5F5F4,stroke:#78716C,color:#44403C
    classDef cUi   fill:#D1FAE5,stroke:#059669,color:#064E3B
    classDef cTest fill:#F3F4F6,stroke:#9CA3AF,color:#374151
    
    class S1,DB_001,DB_012 cDb
    class API_001,API_016 cApi
    class MOCK_001,MOCK_008 cMock
    class S2,BE_PARSE_001,BE_FORM_001,BE_PAY_001,BE_QT_001,BE_RT_001 cBe
    class FE_PARSE_009,FE_FORM_008,FE_PAY_004,FE_QT_004,FE_RT_002 cFe
    class S5,UI_001,UI_053 cUi
    class S4,NFR_INFRA_001,NFR_FB_003 cNfr
    class S3,TEST_PARSE_001,TEST_ADMIN_001 cTest
```

---

## 3. Step별 상세 의존성 다이어그램

### 3.1 Step 1 — 계약·데이터 명세 (Foundation)

```mermaid
flowchart LR
    DB_001["DB-001<br/><small>Prisma Init</small>"]
    DB_002["DB-002<br/><small>USER Table</small>"]
    DB_003["DB-003<br/><small>DOCUMENT Table</small>"]
    DB_004["DB-004<br/><small>PARSED_FORM Table</small>"]
    DB_005["DB-005<br/><small>RESPONSE Table</small>"]
    DB_006["DB-006<br/><small>ZIP_DATAMAP Table</small>"]
    DB_007["DB-007<br/><small>QUOTA_SETTING</small>"]
    DB_008["DB-008<br/><small>QUOTA_CELL Table</small>"]
    DB_009["DB-009<br/><small>ROUTING_CONFIG</small>"]
    DB_010["DB-010<br/><small>AUDIT_LOG Table</small>"]
    DB_011["DB-011<br/><small>Enums</small>"]
    DB_012["DB-012<br/><small>Supabase RPC</small>"]

    API_001["API-001<br/><small>Doc Upload</small>"]
    API_002["API-002<br/><small>Status Query</small>"]
    API_003["API-003<br/><small>Form Fetch</small>"]
    API_004["API-004<br/><small>Response Submit</small>"]
    API_005["API-005<br/><small>Form Update</small>"]
    API_006["API-006<br/><small>Form Publish</small>"]
    API_007["API-007<br/><small>Payment Checkout</small>"]
    API_008["API-008<br/><small>Payment Callback</small>"]
    API_009["API-009<br/><small>ZIP Download</small>"]
    API_010["API-010<br/><small>Quota Create</small>"]
    API_011["API-011<br/><small>Quota Status</small>"]
    API_012["API-012<br/><small>Postback URL</small>"]
    API_013["API-013<br/><small>Redirect URL</small>"]
    API_016["API-016<br/><small>Admin Stats</small>"]

    MOCK_001["MOCK-001<br/><small>Upload Mock</small>"]
    MOCK_002["MOCK-002<br/><small>Parsing Mock</small>"]
    MOCK_004["MOCK-004<br/><small>Payment Mock</small>"]
    MOCK_008["MOCK-008<br/><small>Prisma Seed</small>"]

    DB_001 --> DB_002
    DB_001 --> DB_011
    DB_002 --> DB_003
    DB_002 --> DB_010
    DB_003 --> DB_004
    DB_004 --> DB_005
    DB_004 --> DB_006
    DB_004 --> DB_007
    DB_004 --> DB-009
    DB_007 --> DB-008
    DB_008 --> DB_012

    DB_003 --> API_001
    DB_004 --> API_003
    DB_005 --> API_004
    DB_006 --> API_007
    DB_008 --> API_010
    DB_009 --> API_013
    DB_010 --> API_016

    API_001 --> MOCK_001
    API_002 --> MOCK_002
    API_007 --> MOCK_004
    DB_010 --> MOCK_008

    %% Epic colors
    classDef cDb   fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A
    classDef cApi  fill:#CFFAFE,stroke:#0891B2,color:#164E63
    classDef cMock fill:#EDE9FE,stroke:#7C3AED,color:#4C1D95
    class DB_001,DB_002,DB_003,DB_004,DB_005,DB_006,DB_007,DB_008,DB_009,DB_010,DB_011,DB_012 cDb
    class API_001,API_002,API_003,API_004,API_005,API_006,API_007,API_008,API_009,API_010,API_011,API_012,API_013,API_016 cApi
    class MOCK_001,MOCK_002,MOCK_004,MOCK_008 cMock
```

### 3.2 Step 2 & Step 5 — 로직·상태 (CQRS) 및 UI/UX 프론트엔드 연동

```mermaid
flowchart TB
    subgraph UI_Layer["Step 5 (UI/UX)"]
        UI_001["UI-001<br/><small>Design Tokens</small>"]
        UI_002["UI-002<br/><small>Layout Base</small>"]
        UI_010["UI-010<br/><small>Upload Form</small>"]
        UI_020["UI-020<br/><small>Form Editor UI</small>"]
        UI_030["UI-030<br/><small>Mobile Survey UI</small>"]
        UI_041["UI-041<br/><small>Checkout Modal</small>"]
    end

    subgraph Feature_BE["Step 2 (Backend)"]
        BE_PARSE_001["BE-PARSE-001<br/><small>Doc Validate</small>"]
        BE_PARSE_005["BE-PARSE-005<br/><small>Gemini Prompting</small>"]
        BE_FORM_002["BE-FORM-002<br/><small>Form Modify</small>"]
        BE_FORM_004["BE-FORM-004<br/><small>Response Auth</small>"]
        BE_PAY_001["BE-PAY-001<br/><small>Toss Session</small>"]
        BE_QT_003["BE-QT-003<br/><small>RPC Atomic</small>"]
    end

    subgraph Feature_FE["Step 2 (Frontend)"]
        FE_PARSE_001["FE-PARSE-001<br/><small>Upload Logic</small>"]
        FE_FORM_001["FE-FORM-001<br/><small>Editor State</small>"]
        FE_PAY_001["FE-PAY-001<br/><small>PG Modal 연동</small>"]
        FE_QT_003["FE-QT-003<br/><small>Quota Full Gate</small>"]
    end

    subgraph External["선행 (Step 1)"]
        API_001["API-001"]:::ext
        DB_004["DB-004"]:::ext
    end

    UI_001 --> UI_002
    UI_002 --> UI_010
    UI_002 --> UI_020
    
    UI_010 --> FE_PARSE_001
    API_001 --> BE_PARSE_001
    FE_PARSE_001 --> BE_PARSE_001
    BE_PARSE_001 --> BE_PARSE_005

    UI_020 --> FE_FORM_001
    FE_FORM_001 --> BE_FORM_002
    
    UI_030 --> BE_FORM_004
    BE_QT_003 --> FE_QT_003

    UI_041 --> FE_PAY_001
    FE_PAY_001 --> BE_PAY_001

    classDef ext fill:#F9FAFB,stroke:#D1D5DB,color:#6B7280,stroke-dasharray: 3 3
    classDef cBe   fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D
    classDef cFe   fill:#FFEDD5,stroke:#EA580C,color:#7C2D12
    classDef cUi   fill:#D1FAE5,stroke:#059669,color:#064E3B
    class UI_001,UI_002,UI_010,UI_020,UI_030,UI_041 cUi
    class BE_PARSE_001,BE_PARSE_005,BE_FORM_002,BE_FORM_004,BE_PAY_001,BE_QT_003 cBe
    class FE_PARSE_001,FE_FORM_001,FE_PAY_001,FE_QT_003 cFe
```

### 3.3 Step 3 — 테스트 자동화

```mermaid
flowchart TB
    TEST_PARSE_001["TEST-PARSE-001<br/><small>문서 파싱 E2E</small>"]
    TEST_PAY_004["TEST-PAY-004<br/><small>결제 및 ZIP 발급</small>"]
    TEST_QT_002["TEST-QT-002<br/><small>쿼터 오차율 검증</small>"]
    TEST_FORM_002["TEST-FORM-002<br/><small>순환 참조 차단</small>"]
    TEST_ADMIN_001["TEST-ADMIN-001<br/><small>관리자 통계 검증</small>"]

    subgraph External["선행 (Step 2/4)"]
        BE_PARSE_005["BE-PARSE-005"]:::ext
        BE_PAY_001["BE-PAY-001"]:::ext
        BE_QT_003["BE-QT-003"]:::ext
        FE_FORM_001["FE-FORM-001"]:::ext
    end

    BE_PARSE_005 --> TEST_PARSE_001
    BE_PAY_001 --> TEST_PAY_004
    BE_QT_003 --> TEST_QT_002
    FE_FORM_001 --> TEST_FORM_002

    classDef ext fill:#F9FAFB,stroke:#D1D5DB,color:#6B7280,stroke-dasharray: 3 3
    classDef cTest fill:#F3F4F6,stroke:#9CA3AF,color:#374151
    class TEST_PARSE_001,TEST_PAY_004,TEST_QT_002,TEST_FORM_002,TEST_ADMIN_001 cTest
```

### 3.4 Step 4 — 비기능·인프라·보안

```mermaid
flowchart LR
    NFR_INFRA_001["INFRA-001<br/><small>Next.js Init</small>"]
    NFR_INFRA_004["INFRA-004<br/><small>Supabase DB</small>"]
    NFR_INFRA_006["INFRA-006<br/><small>AI SDK 셋업</small>"]
    
    NFR_SEC_001["SEC-001<br/><small>TLS 1.2 강제</small>"]
    NFR_SEC_002["SEC-002<br/><small>At-rest DB 암호화</small>"]

    NFR_MON_001["MON-001<br/><small>Vercel Analytics</small>"]
    NFR_PERF_001["PERF-001<br/><small>응답 부하 테스트</small>"]
    
    subgraph External["선행 태스크"]
        DB_001["DB-001"]:::ext
        BE_FORM_004["BE-FORM-004"]:::ext
    end

    NFR_INFRA_001 --> NFR_INFRA_004
    NFR_INFRA_004 --> NFR_INFRA_006
    DB_001 --> NFR_SEC_001
    NFR_INFRA_004 --> NFR_SEC_002
    BE_FORM_004 --> NFR_PERF_001

    classDef ext fill:#F9FAFB,stroke:#D1D5DB,color:#6B7280,stroke-dasharray: 3 3
    classDef cNfr  fill:#F5F5F4,stroke:#78716C,color:#44403C
    class NFR_INFRA_001,NFR_INFRA_004,NFR_INFRA_006,NFR_SEC_001,NFR_SEC_002,NFR_MON_001,NFR_PERF_001 cNfr
```

---

## 4. Critical Path 분석

### 4.1 핵심 의존성 체인 (Core Pathway)
전체 프로젝트에서 병목을 일으킬 수 있는 가장 깊고 복잡한 연쇄입니다.

> `DB-001(환경 셋업)` → `DB-004(PARSED_FORM)` → `API-003(폼 조회)` → `UI-020(에디터 UI)` → `FE-FORM-001(에디터 상태 관리)` → `BE-FORM-002(폼 수정 API 연동)` → `TEST-FORM-002(순환참조 테스트)`

### 4.2 의존도 높은 핵심 태스크 (Hub 분석)

**최다 후행 영향 (Fan-out) Top 5:**
1. `DB-001`: Prisma 스키마 초기화 (거의 모든 DB 태스크의 진입점)
2. `UI-001`: 디자인 토큰 적용 (모든 프론트엔드 UI의 기반)
3. `DB-004`: `PARSED_FORM` 테이블 생성 (설문 도메인의 중심)
4. `NFR-INFRA-001`: Next.js 라우터 셋업
5. `BE-PARSE-005`: Gemini API 연동 (파싱 결과에 의존하는 기능 다수)

**최다 선행 의존 (Fan-in) Top 5:**
1. `TEST-PARSE-001`: E2E 테스트 (UI, BE, DB 셋업 모두 필요)
2. `BE-PAY-003`: ZIP 데이터맵 생성 (폼 구조, 결제 콜백 등 필요)
3. `NFR-PERF-004`: 대규모 트래픽 부하 테스트
4. `UI-041`: Checkout 모달 (토스트, 레이아웃, 모자이크 UI 등 필요)
5. `BE-QT-003`: 쿼터 Atomic 증가 (DB RPC 함수, 캐싱 등 다중 의존성)

---

## 5. 통계 요약

| 항목 | 수치 |
|---|---|
| **총 노드 (태스크) 수** | 184개 |
| **도메인 분류** | DB(12), API(16), MOCK(8), FE/BE(66), NFR(25), UI(24), TEST(33) |
| **루트 태스크 (선행 없음)** | `DB-001`, `NFR-INFRA-001` 등 |
| **리프 태스크 (후행 없음)** | 테스트 자동화(`TEST-*`) 전반, 인프라 비용/알럿(`NFR-COST-*`) 등 |

> **Notes:** 본 문서의 서브그래프 시각화에서는 브라우저 렌더링 최적화를 위해 일부 독립성이 강하거나 하위 레벨인 태스크(예: 단순 MOCK, 예외 처리 뷰)는 생략 및 축약하여 가장 중요한 줄기를 강조하였습니다. 전체 184개 연결의 논리적 무결성은 마스터 리스트인 `06_TASK_LIST_v2.md`의 `Dependencies` 속성에 의해 보장됩니다.

---
*— End of TASK-DIAG-002 —*
