# 🔗 태스크 의존성 상세 다이어그램 (Dependency Graph)

**문서 ID:** DEP-001  
**원천 문서:** 06_TASK_LIST_v2.md (166개 태스크)  
**작성일:** 2026-04-24  

---

## 1. 전체 파이프라인 개요 (Epic 수준)

```mermaid
flowchart TD
    subgraph S0["Phase 0: Infrastructure"]
        INFRA["NFR-INFRA\n001~007"]
    end

    subgraph S1["Step 1: Foundation Layer"]
        DB["DB-001~012\n스키마 & RPC"]
        API["API-001~016\nDTO 계약"]
        MOCK["MOCK-001~008\nMock 데이터"]
        DB --> API --> MOCK
    end

    subgraph S2["Step 2: Feature Layer"]
        PARSE["Parser\nBE 10 + FE 6"]
        FORM["Form\nBE 4 + FE 7"]
        PAY["Payment\nBE 6 + FE 4"]
        WM["Watermark\nBE 2 + FE 2"]
        QT["Quota\nBE 5 + FE 3"]
        RT["Routing\nBE 3 + FE 2"]
        RL["RateLimit\nBE 2 + FE 1"]
        RET["Retention\nBE 2"]
        DASH["Dashboard\nBE 2 + FE 3"]
        AUTH["Auth\nBE 2 + FE 3"]
        ADM["Admin\nBE 1 + FE 2"]
    end

    subgraph S3["Step 3: Test Layer"]
        TEST["TEST 33개"]
    end

    subgraph S4["Step 4: NFR Layer"]
        PERF["NFR-PERF 4"]
        SEC["NFR-SEC 4"]
        MON["NFR-MON 5"]
        COST["NFR-COST 2"]
        FB["NFR-FB 3"]
    end

    INFRA --> DB
    INFRA --> AUTH
    DB --> PARSE & FORM & PAY & QT & RT
    MOCK --> PARSE & FORM
    PARSE --> QT
    FORM --> PAY
    QT --> RT
    PARSE & FORM & PAY & QT & RT --> TEST
    PARSE --> PERF & MON
    PAY --> FB & MON
    QT --> PERF
    RL --> ADM
```

---

## 2. Foundation Layer 상세 (DB → API → MOCK)

```mermaid
flowchart TD
    subgraph DB["DB 스키마"]
        DB001["DB-001\nPrisma 초기화"]
        DB002["DB-002\nUSER"] --> DB001
        DB003["DB-003\nDOCUMENT"] --> DB002
        DB004["DB-004\nPARSED_FORM"] --> DB003
        DB005["DB-005\nRESPONSE"] --> DB004
        DB006["DB-006\nZIP_DATAMAP"] --> DB004
        DB007["DB-007\nQUOTA_SETTING"] --> DB004
        DB008["DB-008\nQUOTA_CELL"] --> DB007
        DB009["DB-009\nROUTING_CONFIG"] --> DB004
        DB010["DB-010\nAUDIT_LOG"] --> DB002
        DB011["DB-011\nEnum 정의"] --> DB001
        DB012["DB-012\nRPC 함수"] --> DB008
    end

    subgraph API["API 계약"]
        API001["API-001\nUpload DTO"] --> DB003
        API002["API-002\nStatus DTO"] --> DB003
        API003["API-003\nForm DTO"] --> DB004
        API004["API-004\nResponse DTO"] --> DB005
        API005["API-005\nForm Edit DTO"] --> DB004
        API006["API-006\nPublish DTO"] --> DB004
        API007["API-007\nPayment DTO"] --> DB006
        API008["API-008\nCallback DTO"] --> DB006
        API009["API-009\nDownload DTO"] --> DB006
        API010["API-010\nQuota Setup DTO"] --> DB007 & DB008
        API011["API-011\nQuota Status DTO"] --> DB007 & DB008
        API012["API-012\nRouting Post DTO"] --> DB009
        API013["API-013\nRouting Redir DTO"] --> DB009
        API014["API-014\nError Schema"]
        API015["API-015\nVersioning"]
        API016["API-016\nAdmin Stats DTO"] --> DB010
    end

    subgraph MOCK["Mock 데이터"]
        MOCK001["MOCK-001\nUpload Mock"] --> API001
        MOCK002["MOCK-002\nParsing Mock"] --> API002 & API003
        MOCK003["MOCK-003\nResponse Mock"] --> API004
        MOCK004["MOCK-004\nPayment Mock"] --> API007 & API008
        MOCK005["MOCK-005\nDownload Mock"] --> API009
        MOCK006["MOCK-006\nQuota Mock"] --> API010 & API011
        MOCK007["MOCK-007\nRouting Mock"] --> API012 & API013
        MOCK008["MOCK-008\nPrisma Seed"] --> DB002
    end
```

---

## 3. Document Parser 도메인 상세

```mermaid
flowchart TD
    subgraph EXT["외부 의존"]
        DB003e["DB-003"]
        DB004e["DB-004"]
        API001e["API-001"]
        API002e["API-002"]
        MOCK001e["MOCK-001"]
        MOCK002e["MOCK-002"]
    end

    subgraph BE_PARSE["Backend Parser"]
        BP001["BE-PARSE-001\n서버 검증"] --> DB003e & API001e
        BP002["BE-PARSE-002\nHWPX 전처리"] --> BP001
        BP003["BE-PARSE-003\nWord 전처리"] --> BP001
        BP004["BE-PARSE-004\nPDF 전처리"] --> BP001
        BP005["BE-PARSE-005\nAI SDK+Gemini"] --> BP002 & BP003 & BP004 & DB004e
        BP006["BE-PARSE-006\n스킵 요소"] --> BP005
        BP007["BE-PARSE-007\n상태 갱신"] --> BP005
        BP008["BE-PARSE-008\n상태 조회"] --> DB003e & API002e
        BP009["BE-PARSE-009\nFallback 경로"] --> BP005
        BP010["BE-PARSE-010\n해시 캐시"] --> BP001 & DB003e
    end

    subgraph FE_PARSE["Frontend Parser"]
        FP001["FE-PARSE-001\n업로드 UI"] --> MOCK001e
        FP002["FE-PARSE-002\n로딩 스켈레톤"] --> FP001
        FP003["FE-PARSE-003\nHWPX 안내 모달"] --> FP001
        FP004["FE-PARSE-004\n정확도 안내"] --> FP001
        FP005["FE-PARSE-005\n에러 모달"] --> FP001
        FP006["FE-PARSE-006\n미리보기"] --> MOCK002e
    end

    subgraph TEST_PARSE["Parser Tests"]
        TP001["TEST-PARSE-001\n정확도 테스트"] --> BP005
        TP002["TEST-PARSE-002\n유효성 테스트"] --> BP001
        TP003["TEST-PARSE-003\nHWPX 전환 테스트"] --> FP003 & BP001
        TP004["TEST-PARSE-004\n레이턴시 테스트"] --> BP005
        TP005["TEST-PARSE-005\nFallback 테스트"] --> BP002 & BP003 & BP004
        TP006["TEST-PARSE-006\n스킵 요소 테스트"] --> BP006
        TP007["TEST-PARSE-007\nHWP 가이드 테스트"] --> FP003 & BP001
        TP008["TEST-PARSE-008\nRate Limit 테스트"] -.-> RL001e["BE-RL-001"]
        TP009["TEST-PARSE-009\n해시 캐시 테스트"] --> BP010
    end
```

---

## 4. Form Management 도메인 상세

```mermaid
flowchart TD
    subgraph EXT["외부 의존"]
        DB004f["DB-004"]
        DB005f["DB-005"]
        API003f["API-003"]
        API004f["API-004"]
        API005f["API-005"]
        API006f["API-006"]
        MOCK002f["MOCK-002"]
        MOCK003f["MOCK-003"]
    end

    subgraph BE_FORM["Backend Form"]
        BF001["BE-FORM-001\n폼 조회"] --> DB004f & API003f
        BF002["BE-FORM-002\n폼 수정"] --> DB004f & API005f
        BF003["BE-FORM-003\n폼 배포"] --> DB004f & API006f
        BF004["BE-FORM-004\n응답 제출"] --> DB005f & API004f
    end

    subgraph FE_FORM["Frontend Form"]
        FF001["FE-FORM-001\n에디터 레이아웃"] --> MOCK002f
        FF002["FE-FORM-002\n문항 유형 편집"] --> FF001
        FF003["FE-FORM-003\n문항 추가/삭제"] --> FF001
        FF004["FE-FORM-004\n스킵 로직 설정"] --> FF001
        FF005["FE-FORM-005\n모바일 미리보기"] --> FF001
        FF006["FE-FORM-006\n배포/공유 화면"] --> FF001
        FF007["FE-FORM-007\n모바일 설문 폼"] --> MOCK002f & MOCK003f
    end

    subgraph TEST_FORM["Form Tests"]
        TF001["TEST-FORM-001\nDnD 테스트"] --> FF001
        TF002["TEST-FORM-002\n분기 로직 테스트"] --> FF004 & BF002
        TF003["TEST-FORM-003\n모바일 렌더링 테스트"] --> FF007
        TF004["TEST-FORM-004\n제출 무결성 테스트"] --> BF004
    end
```

---

## 5. DataMap & Paywall 도메인 상세

```mermaid
flowchart TD
    subgraph EXT["외부 의존"]
        DB005p["DB-005"]
        DB006p["DB-006"]
        DB010p["DB-010"]
        API007p["API-007"]
        API008p["API-008"]
        API009p["API-009"]
        MOCK004p["MOCK-004"]
    end

    subgraph BE_PAY["Backend Payment"]
        BPAY001["BE-PAY-001\n결제 요청"] --> DB006p & API007p
        BPAY002["BE-PAY-002\n결제 콜백"] --> DB006p & DB010p & API008p
        BPAY003["BE-PAY-003\nZIP 컴파일"] --> DB005p & DB006p & BPAY002
        BPAY004["BE-PAY-004\nStorage URL"] --> BPAY003
        BPAY005["BE-PAY-005\n다운로드 핸들러"] --> DB006p & API009p & BPAY002
        BPAY006["BE-PAY-006\n결측치 검증"] --> BPAY003
    end

    subgraph FE_PAY["Frontend Payment"]
        FPAY001["FE-PAY-001\nPaywall UI"] --> MOCK004p
        FPAY002["FE-PAY-002\nPG SDK 연동"] --> FPAY001
        FPAY003["FE-PAY-003\n성공 화면"] --> FPAY001
        FPAY004["FE-PAY-004\nZIP 다운로드 UI"] --> FPAY002
    end

    subgraph TEST_PAY["Payment Tests"]
        TPAY001["TEST-PAY-001\nZIP 구조 검증"] --> BPAY003
        TPAY002["TEST-PAY-002\nZIP 성능 테스트"] --> BPAY003
        TPAY003["TEST-PAY-003\n다운로드 보안"] --> BPAY004 & BPAY005
        TPAY004["TEST-PAY-004\n콜백 흐름"] --> BPAY002 & BPAY004
        TPAY005["TEST-PAY-005\n실패 차단"] --> BPAY002 & BPAY005
        TPAY006["TEST-PAY-006\n결측치 0%"] --> BPAY006
        TPAY007["TEST-PAY-007\n미리보기 자산"] --> FPAY003
    end
```

---

## 6. Quota & Panel Routing 도메인 상세

```mermaid
flowchart TD
    subgraph EXT["외부 의존"]
        DB007q["DB-007"]
        DB008q["DB-008"]
        DB009q["DB-009"]
        DB005q["DB-005"]
        DB010q["DB-010"]
        DB012q["DB-012"]
        API010q["API-010"]
        API011q["API-011"]
        API012q["API-012"]
        API013q["API-013"]
        MOCK006q["MOCK-006"]
        MOCK007q["MOCK-007"]
        BF004q["BE-FORM-004"]
    end

    subgraph BE_QT["Backend Quota"]
        BQT001["BE-QT-001\n쿼터 설정"] --> DB007q & DB008q & API010q
        BQT002["BE-QT-002\n쿼터 조회"] --> DB008q & API011q
        BQT003["BE-QT-003\n원자적 증가"] --> DB012q & BF004q
        BQT004["BE-QT-004\nSlack 알림"] --> BQT003
        BQT005["BE-QT-005\n레이턴시 감시"] --> BQT003 & DB010q
    end

    subgraph FE_QT["Frontend Quota"]
        FQT001["FE-QT-001\n매트릭스 에디터"] --> MOCK006q
        FQT002["FE-QT-002\n상태 대시보드"] --> MOCK006q
        FQT003["FE-QT-003\n마감 안내 화면"] -.-> FF007q["FE-FORM-007"]
    end

    subgraph BE_RT["Backend Routing"]
        BRT001["BE-RT-001\n포스트백 등록"] --> DB009q & API012q
        BRT002["BE-RT-002\n리다이렉트"] --> DB009q & DB005q & API013q & BQT003
        BRT003["BE-RT-003\n재시도 큐"] --> BRT002
    end

    subgraph FE_RT["Frontend Routing"]
        FRT001["FE-RT-001\n라우팅 설정 UI"] --> MOCK007q
        FRT002["FE-RT-002\n리다이렉트 로딩"] --> FRT001
    end

    subgraph TEST_QR["Quota & Routing Tests"]
        TQT001["TEST-QT-001\n매트릭스 테스트"] --> BQT001
        TQT002["TEST-QT-002\n오차율 테스트"] --> BQT003
        TQT003["TEST-QT-003\n동시성 테스트"] --> BQT003 & DB012q
        TQT004["TEST-QT-004\n레이턴시 알림"] --> BQT005
        TQT005["TEST-QT-005\nSlack 알림"] --> BQT004
        TRT001["TEST-RT-001\n포스트백 테스트"] --> BRT001
        TRT002["TEST-RT-002\n리다이렉트 테스트"] --> BRT002
        TRT003["TEST-RT-003\n재시도 신뢰성"] --> BRT003
    end
```

---

## 7. Watermark · Auth · Dashboard · Admin · Retention 상세

```mermaid
flowchart TD
    subgraph WM["Watermark"]
        BWM001["BE-WM-001\nURL 생성"] -.-> BP005w["BE-PARSE-005"]
        BWM002["BE-WM-002\n클릭 로깅"] -.-> DB010w["DB-010"]
        FWM001["FE-WM-001\n배너 렌더링"] -.-> FF007w["FE-FORM-007"]
        FWM002["FE-WM-002\n리다이렉션"] --> FWM001
        TWM001["TEST-WM-001\n렌더링 테스트"] --> FWM001
        TWM002["TEST-WM-002\n바이럴 테스트"] --> FWM002
    end

    subgraph AUTH["Authentication"]
        FAUTH001["FE-AUTH-001\n로그인 UI"] -.-> INFRA004a["NFR-INFRA-004"]
        FAUTH002["FE-AUTH-002\n프로필 설정"] --> FAUTH001
        FAUTH003["FE-AUTH-003\nAuth Guard"] --> FAUTH001
        BAUTH001["BE-AUTH-001\nSupabase Auth"] -.-> INFRA004a
        BAUTH002["BE-AUTH-002\n세션 핸들러"] --> BAUTH001
    end

    subgraph DASH["Dashboard"]
        FDASH001["FE-DASH-001\n설문 목록 UI"] -.-> MOCK002d["MOCK-002"]
        FDASH002["FE-DASH-002\n통계 차트"] --> FDASH001
        FDASH003["FE-DASH-003\n데이터 테이블"] --> FDASH001
        BDASH001["BE-DASH-001\n통계 집계"] -.-> DB005d["DB-005"]
        BDASH002["BE-DASH-002\n대시보드 조회"] -.-> DB004d["DB-004"]
    end

    subgraph ADMIN["Admin"]
        FADM001["FE-ADMIN-001\n관리자 레이아웃"] -.-> BRL002a["BE-RL-002"]
        FADM002["FE-ADMIN-002\n통계 화면"] --> FADM001
        BADM001["BE-ADMIN-001\n통계 집계 로직"] -.-> DB010a["DB-010"]
        TADM001["TEST-ADMIN-001\n접근 제어"] --> BRL002a & FADM001
    end

    subgraph RL["Rate Limit & Auth"]
        BRL001["BE-RL-001\nRate Limit"] -.-> DB002r["DB-002"]
        BRL002["BE-RL-002\nRBAC"] -.-> DB002r
        FRL001["FE-RL-001\n한도 초과 안내"] -.-> FP001r["FE-PARSE-001"]
    end

    subgraph RET["Data Retention"]
        BRET001["BE-RET-001\n삭제 스케줄러"] -.-> DB003r["DB-003"] & DB010r["DB-010"]
        BRET002["BE-RET-002\nCron 설정"] --> BRET001
        TRET001["TEST-RET-001\n자동 삭제 테스트"] --> BRET001
        TRET002["TEST-RET-002\n암호화 테스트"] --> BRET001
    end
```

---

## 8. NFR & Infrastructure 도메인 상세

```mermaid
flowchart TD
    subgraph INFRA["Infrastructure Setup"]
        NI001["NFR-INFRA-001\nNext.js 초기 셋업"]
        NI002["NFR-INFRA-002\nTailwind/shadcn"] --> NI001
        NI003["NFR-INFRA-003\nVercel CI/CD"] --> NI001
        NI004["NFR-INFRA-004\nSupabase 초기화"] --> NI001
        NI005["NFR-INFRA-005\n환경 변수 관리"] --> NI003 & NI004
        NI006["NFR-INFRA-006\nAI SDK 설정"] --> NI005
        NI007["NFR-INFRA-007\n순환 의존성 체크"] --> NI001
    end

    subgraph PERF["Performance"]
        NP001["NFR-PERF-001\np95 부하 테스트"] -.-> BF004p["BE-FORM-004"]
        NP002["NFR-PERF-002\n파싱 벤치마크"] -.-> BP005p["BE-PARSE-005"]
        NP003["NFR-PERF-003\n쿼터 벤치마크"] -.-> BQT003p["BE-QT-003"]
        NP004["NFR-PERF-004\n동시접속 스트레스"] --> NP001
    end

    subgraph SEC["Security"]
        NS001["NFR-SEC-001\nTLS/HTTPS 강제"] -.-> DB001s["DB-001"]
        NS002["NFR-SEC-002\nPostgreSQL 암호화"] -.-> DB001s & NI004
        NS003["NFR-SEC-003\n결제 감사 로그 0%"] -.-> BPAY002s["BE-PAY-002"]
        NS004["NFR-SEC-004\nIP 해싱"] -.-> BF004s["BE-FORM-004"]
    end

    subgraph MON["Monitoring"]
        NM001["NFR-MON-001\nVercel Analytics"] -.-> BP005m["BE-PARSE-005"]
        NM002["NFR-MON-002\nSlack 통합 알림"] -.-> NI005
        NM003["NFR-MON-003\nKPI 대시보드 집계"] -.-> BPAY002m["BE-PAY-002"]
        NM004["NFR-MON-004\nGA4 워터마크 퍼널"] -.-> FWM002m["FE-WM-002"]
        NM005["NFR-MON-005\n운영자 대시보드"] --> NM003
    end

    subgraph COST["Cost"]
        NC001["NFR-COST-001\n파싱 원가 검증"] -.-> BP005c["BE-PARSE-005"]
        NC002["NFR-COST-002\n예산 초과 알림"] --> NI003 & NI004
    end

    subgraph FB["Fallback"]
        NF001["NFR-FB-001\nPG 장애 폴백"] -.-> BPAY001f["BE-PAY-001"]
        NF002["NFR-FB-002\nStorage 장애 폴백"] -.-> BPAY004f["BE-PAY-004"]
        NF003["NFR-FB-003\nAnalytics 장애 폴백"] -.-> NM001
    end

    NI001 -.-> DB001s
```

---

## 9. Critical Path (핵심 경로)

> 프로젝트의 **최장 의존 체인**을 나타냅니다. 이 경로상의 태스크가 지연되면 전체 일정에 직접 영향을 줍니다.

```mermaid
flowchart LR
    CP01["NFR-INFRA-001\nNext.js 셋업"] --> CP02["DB-001\nPrisma 초기화"]
    CP02 --> CP03["DB-002\nUSER"]
    CP03 --> CP04["DB-003\nDOCUMENT"]
    CP04 --> CP05["DB-004\nPARSED_FORM"]
    CP05 --> CP06["DB-005\nRESPONSE"]
    CP04 --> CP07["API-001\nUpload DTO"]
    CP07 --> CP08["MOCK-001\nUpload Mock"]
    CP04 --> CP09["BE-PARSE-001\n서버 검증"]
    CP09 --> CP10["BE-PARSE-002\nHWPX 전처리"]
    CP10 --> CP11["BE-PARSE-005\nAI SDK + Gemini"]
    CP11 --> CP12["BE-PARSE-006\n스킵 요소"]
    CP06 --> CP13["BE-FORM-004\n응답 제출"]
    CP05 --> CP14["DB-008\nQUOTA_CELL"]
    CP14 --> CP15["DB-012\nRPC 함수"]
    CP15 --> CP16["BE-QT-003\n원자적 쿼터 증가"]
    CP13 --> CP16
    CP16 --> CP17["TEST-QT-002\n오차율 테스트"]
    CP06 --> CP18["BE-PAY-002\n결제 콜백"]
    CP18 --> CP19["BE-PAY-003\nZIP 컴파일"]
    CP19 --> CP20["TEST-PAY-001\nZIP 구조 검증"]

    style CP01 fill:#4CAF50,color:#fff
    style CP11 fill:#FF9800,color:#fff
    style CP16 fill:#F44336,color:#fff
    style CP19 fill:#F44336,color:#fff
```

---

## 범례

| 선 유형 | 의미 |
|---|---|
| `A --> B` | B는 A에 의존 (A가 완료되어야 B 시작 가능) |
| `A -.-> B` | B는 A에 약한 의존 (A의 일부만 필요하거나 Mock으로 대체 가능) |

| 색상 (Critical Path) | 의미 |
|---|---|
| 🟢 초록 | 시작점 (의존성 없음) |
| 🟠 주황 | 핵심 기술 의존 (AI SDK) |
| 🔴 빨강 | 최고 리스크 노드 (동시성/결제) |

---

*End of Document — DEP-001*
