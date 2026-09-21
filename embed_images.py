import base64, os, re, sys

MIME = {'.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png',
        '.gif':'image/gif', '.webp':'image/webp', '.svg':'image/svg+xml'}

def embed(html_path):
    base = os.path.dirname(os.path.abspath(html_path))
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    def repl(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        if src.startswith(('http://','https://','data:','#','//')):
            return m.group(0)
        img_path = os.path.normpath(os.path.join(base, src))
        if not os.path.isfile(img_path):
            print(f"  ! missing: {src}")
            return m.group(0)
        ext = os.path.splitext(img_path)[1].lower()
        mime = MIME.get(ext, 'image/jpeg')
        with open(img_path, 'rb') as im:
            b64 = base64.b64encode(im.read()).decode('ascii')
        print(f"  embedded {src} ({os.path.getsize(img_path)}B -> {len(b64)}B base64)")
        return f'{pre}data:{mime};base64,{b64}{post}'

    pat = re.compile(r'(<img\b[^>]*?\ssrc=")([^"]+)(")')
    new_html, n = pat.subn(repl, html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"=> {html_path}: {n} image(s) embedded, new size {os.path.getsize(html_path)}B")

for p in sys.argv[1:]:
    print(f"[processing {p}]")
    embed(p)
