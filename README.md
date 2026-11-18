# 청렴 신고 시민 포털 — CSV 자동 배포 버전

## 동작 원리

GitHub 저장소의 `data/청렴신고_사건데이터.csv` 또는 `data/청렴교육_현황.csv`를 동일한 이름으로 교체하고 **Commit changes** 하면 Netlify가 빌드 명령 `python3 scripts/build.py`를 실행합니다. 결과물은 `dist/`에 만들어져 자동 배포됩니다. 표준 Python만 사용하며 외부 라이브러리는 필요 없습니다.

- 원본 페이지 디자인과 카드·검색·유형/상태/지역 필터, 교육 목록 유지
- 뉴스 5건은 `data/news_snapshot.json`에 고정된 기존 목록이며, 지정된 정책브리핑 RSS 제공 중단으로 자동 갱신하지 않음
- 원본 CSV 헤더(필수 컬럼)는 유지해야 함. 열 순서는 바꿔도 됨
- 파일 인코딩: UTF-8 또는 UTF-8 BOM, CSV 구분자 쉼표
- 시민에게 공개되는 데이터만 업로드. **GitHub 공개 저장소에는 개인식별/신고자 정보가 포함된 실데이터를 올리지 말 것**

## 처음 연결하기

1. GitHub에서 새 저장소를 만들고 이 압축 파일의 **폴더 안 파일 전체**를 저장소 루트에 업로드하여 커밋합니다 (`data/`, `site/`, `scripts/`, `netlify.toml`).
2. Netlify에서 **Add new project → Import an existing project** 선택 → GitHub 연결 → 저장소 선택.
3. Production branch `main`, Base directory 비움, Build command `python3 scripts/build.py`, Publish directory `dist`인지 확인하고 Deploy.
4. 배포 성공 후 `https://발급주소.netlify.app`에서 검색 기능을 점검합니다.
5. GitHub 저장소의 `data/청렴신고_사건데이터.csv`를 열어 **Upload files** 또는 파일 교체 후 **Commit changes**. Netlify가 자동 빌드·배포합니다.

> 기존에 Netlify Drop으로 올렸던 사이트가 있다면 자동배포 Git 연결을 새 프로젝트로 시작하는 것이 가장 간단합니다. 기존 사이트 주소를 유지하려면 해당 사이트의 Git 연결/도메인 설정을 별도로 조정해야 합니다.

## 로컬 테스트 (Windows)

프로젝트 폴더에서 명령 프롬프트 실행:

```cmd
python scripts\build.py
```

`dist/index.html`을 열어 보세요. CSV 값 하나를 바꾼 뒤 다시 위 명령을 실행하면 `dist/index.html`과 `dist/data.json`이 새 값으로 만들어집니다.

## 업데이트 확인

1. GitHub 파일 변경사항 커밋
2. Netlify Deploys에서 새 배포의 상태가 **Published**인지 확인
3. 배포 주소 뒤 `/data.json`으로 들어가 변경된 사건 정보를 검색하거나 `built_at_utc`를 확인
4. 페이지를 새로고침 (필요하면 강력 새로고침 Ctrl+F5)

**주의:** 사용자 PC에 내려받아 보관한 과거 HTML은 갱신되지 않습니다. Netlify 사이트에 새로 접속하는 방문자가 최신 배포본을 받습니다.
