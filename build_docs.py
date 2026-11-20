"""본문 Markdown(AI교재_본문)을 MkDocs용 docs/로 변환한다.
- 숨은 HTML 주석을 뺀다.
- 그림 블록은 제목 + (이미지가 있으면 이미지, 없으면 텍스트 그림)만 남기고 디자인 명세는 뺀다.
- '이해 확인' 상자는 접이식이 아닌 질문 상자로 바꾼다.
사용: python3 build_docs.py <본문 폴더> <출력 docs 폴더>
"""
import re, sys, os, shutil, glob
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def convert_figure(block):
    m = re.search(r'^> \*\*\[그림 (\d+)-(\d+)\]\s*(.*?)\*\*', block, re.M)
    num, title = (f"{m.group(1)}-{m.group(2)}", m.group(3).strip()) if m else ("", "")
    imgs = re.findall(r'^!\[[^\]]*\]\([^)]*\)\s*$', block, re.M)
    code = re.search(r'^```text\n.*?^```', block, re.M | re.S)
    alt = re.search(r'\*\*대체 텍스트:\*\*\s*(.*)$', block, re.M)
    out = ['<figure class="fig" markdown="1">', '']
    if imgs:
        out += imgs
    elif code:
        out.append(code.group(0))
    out += ['', f'<figcaption>그림 {num} {title}</figcaption>', '', '</figure>']
    return '\n' + '\n'.join(out) + '\n'

def convert_check(m):
    lines = [l[2:] if l.startswith('> ') else l[1:] for l in m.group(0).rstrip('\n').split('\n')[1:]]
    return '!!! question "이해 확인"\n\n' + '\n'.join('    ' + l for l in lines) + '\n'

def convert(text):
    # 그림 블록 먼저(주석 표시를 쓰므로)
    text = re.sub(r'<!-- 그림 시작[^>]*-->\n(.*?)<!-- 그림 끝[^>]*-->', lambda m: convert_figure(m.group(1)), text, flags=re.S)
    text = re.sub(r'<!--.*?-->\n?', '', text, flags=re.S)
    text = re.sub(r'^> \*\*이해 확인\*\*\n(?:>.*\n?)+', convert_check, text, flags=re.M)
    # 출처 번호 바로 뒤 괄호([1](작성일 …))가 링크로 읽히지 않게 한다
    text = re.sub(r'(?<![!\\])\[(\d+)\]\((?!https?:)', r'\\[\1\\](', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'

nav = []
for f in sorted(glob.glob(os.path.join(SRC, '[01][0-9]_*.md'))):
    base = os.path.basename(f)
    if base.startswith('11_'):  # 부록은 아직 뼈대
        continue
    n = base[:2]
    s = convert(open(f, encoding='utf-8').read())
    open(os.path.join(OUT, f'ch{n}.md'), 'w', encoding='utf-8').write(s)
    nav.append((n, s.split('\n', 1)[0].lstrip('# ').strip()))
img = os.path.join(SRC, 'images')
if os.path.isdir(img):
    shutil.copytree(img, os.path.join(OUT, 'images'), dirs_exist_ok=True)
for n, t in nav:
    print(n, t)
