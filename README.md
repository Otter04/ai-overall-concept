# AI 입력부터 출력까지

AI 앱에 넣은 질문이 답이 되기까지를 따라가는 입문서입니다. 이 저장소는 책의 원고와, 원고로 웹사이트를 만드는 설정을 담고 있습니다.

## 폴더

- `manuscript/`: 원고(1~10장과 부록 Markdown)와 그림 이미지. 원본은 작성자의 본문 폴더이고, 고친 원고를 여기에 덮어써서 올립니다.
- `docs/index.md`, `docs/stylesheets/extra.css`: 사이트 첫 화면과 모양. 장 페이지(`docs/ch*.md`)는 빌드할 때마다 원고에서 새로 만들어지므로 저장소에 넣지 않습니다.
- `build_docs.py`: 원고를 사이트용으로 바꿉니다. 숨은 주석과 그림 디자인 명세를 빼고, 그림은 제목과 이미지(없으면 텍스트 그림)만 남기고, '이해 확인'은 질문 상자로 바꿉니다.
- `mkdocs.yml`: 사이트 설정(MkDocs Material).
- `.github/workflows/deploy.yml`: main에 올라가면 사이트를 만들어 GitHub Pages에 배포합니다.

## 내 컴퓨터에서 미리 보기

```bash
pip install -r requirements.txt
python3 build_docs.py manuscript docs
mkdocs serve
```
