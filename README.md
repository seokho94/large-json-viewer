# 📊 OTEL JSON Viewer

OpenTelemetry Collector가 생성한 대용량 JSON 파일을 웹 기반으로 시각화하는 Python Streamlit 프로젝트입니다.  
중첩된 `resourceMetrics → metrics → dataPoints` 계층을 평탄화하여 직관적인 표 형태로 확인할 수 있습니다.

---

## ✅ 가상 환경 구성 및 실행

### 1. 가상 환경(venv) 생성

```bash
python -m venv viewer-venv
```

### 2. 가상 환경(venv) 실행

#### (1) Windows
```bash
viewer-venv\Scripts\activate
```

#### (2) macOS/Linux
```bash
source viewer-venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. Streamlit 앱 실행
```bash
streamlit run viewer/app.py
```

```bash
streamlit 실행 시 이메일은 스킵 가능
```

### 5. 프로젝트 구조
```bash
json-viewer/
├── viewer/
│   ├── app.py            # Streamlit 웹앱 실행 코드
│   └── parser.py         # JSON 파싱 및 평탄화 로직
├── requirements.txt      # 필요 패키지 목록
├── README.md             # 설명 문서
└── viewer-venv/          # 가상환경 폴더 (git 제외 대상)
```