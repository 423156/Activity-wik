"""Read-only checks. Run with Python containing pypdf; no network or installs."""
from pathlib import Path
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
results = []

def check(name, ok, detail):
    results.append({'check': name, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})

def readable(p):
    try:
        if p.suffix.lower() == '.pdf':
            from pypdf import PdfReader
            return any((page.extract_text() or '').strip() for page in PdfReader(p).pages)
        if p.suffix.lower() in ('.docx', '.pptx'):
            with zipfile.ZipFile(p) as z:
                names = [n for n in z.namelist() if n == 'word/document.xml' or re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]
                return any(any((e.text or '').strip() for e in ET.fromstring(z.read(n)).iter() if e.tag.endswith('}t')) for n in names)
        if p.suffix.lower() in ('.txt', '.md', '.csv', '.html'):
            return bool(p.read_text(encoding='utf-8-sig').strip())
    except Exception:
        return False
    return False

class Deck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.current = None
        self.tags = []
        self.errors = []
        self.doctype = False
        self.counts = {}
        self.capture = None
    def handle_decl(self, decl):
        self.doctype = decl.lower() == 'doctype html'
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if tag not in {'meta','link','br','hr','img','input','source','wbr','area','base','embed','param','track','col'}:
            self.tags.append(tag)
        if tag == 'section' and 'slide' in a.get('class','').split():
            self.current = {'id':a.get('id'), 'title':[], 'stage':[], 'points':[], 'takeaway':[], 'sources':[], 'all':[]}
            self.slides.append(self.current)
        if self.current is not None:
            key = 'title' if tag == 'h2' else ('points' if tag == 'li' else a.get('class'))
            if key in {'title','stage','points','takeaway','sources'}:
                self.capture = [tag, key, []]
    def handle_data(self, data):
        if self.current is not None:
            self.current['all'].append(data)
            if self.capture:
                self.capture[2].append(data)
    def handle_endtag(self, tag):
        if not self.tags or self.tags[-1] != tag:
            self.errors.append('unbalanced '+tag)
        else:
            self.tags.pop()
        if self.capture and self.capture[0] == tag:
            self.current[self.capture[1]].append(''.join(self.capture[2]).strip())
            self.capture = None
        if tag == 'section':
            self.current = None

required = ['AGENTS.md','wiki/index.md','wiki/log.md','workflow/sources.md','workflow/evidence.md','workflow/outline.md','workflow/draft.md','workflow/deck.html','workflow/report.md','checks/validate.py','submission.md']
missing = [p for p in required if not (ROOT/p).is_file() or not (ROOT/p).stat().st_size]
check('required_files', not missing, {'missing':missing})
raw = sorted(p for p in (ROOT/'raw').rglob('*') if p.is_file())
good = [p for p in raw if readable(p)]
check('raw_readable_count', len(good)>=5, {'files':len(raw),'readable':len(good),'unreadable':[p.name for p in raw if p not in good]})
source_text = (ROOT/'workflow/sources.md').read_text(encoding='utf-8')
entries = re.findall(r'^\| (S\d{2,}) \| ([^|]+) \| [^|]+ \| 是 \|$', source_text, re.M)
ids = {sid for sid, name in entries}
check('source_manifest', len(ids)==len(entries)==len(raw) and all((ROOT/'raw'/name.strip()).is_file() for sid,name in entries), {'ids':sorted(ids),'entries':len(entries)})
hashes = dict(re.findall(r'^\| (S\d{2,}) \| `([a-f0-9]{64})` \|$',source_text,re.M))
hash_bad = [sid for sid,name in entries if hashes.get(sid)!=hashlib.sha256((ROOT/'raw'/name.strip()).read_bytes()).hexdigest()]
check('source_hashes',not hash_bad,{'mismatch':hash_bad})
unknown = {}
for folder in ['wiki','workflow']:
    for p in (ROOT/folder).glob('*'):
        if p.suffix not in {'.md','.html'}: continue
        bad = sorted(set(re.findall(r'\bS\d{2,}\b',p.read_text(encoding='utf-8')))-ids)
        if bad: unknown[str(p.relative_to(ROOT))]=bad
if (ROOT/'submission.md').exists():
    bad=sorted(set(re.findall(r'\bS\d{2,}\b',(ROOT/'submission.md').read_text(encoding='utf-8')))-ids)
    if bad: unknown['submission.md']=bad
check('all_source_ids_exist',not unknown,unknown)

html_path = ROOT/'workflow/deck.html'
if html_path.exists():
    text=html_path.read_text(encoding='utf-8'); deck=Deck(); deck.feed(text)
    check('html_structure',deck.doctype and not deck.errors and not deck.tags and all(deck.counts.get(t)==1 for t in ['html','head','body','main','title']),{'errors':deck.errors,'unclosed':deck.tags})
    check('slide_count',10<=len(deck.slides)<=15,{'actual':len(deck.slides),'min':10,'max':15})
    check('unique_slide_ids',len({s['id'] for s in deck.slides})==len(deck.slides) and all(s['id'] for s in deck.slides),{'ids':[s['id'] for s in deck.slides]})
    empty=[s['id'] for s in deck.slides if not s['title'] or not any(t.strip() for t in s['points'])]
    check('no_blank_slides',not empty,{'empty':empty})
    no_refs=[s['id'] for s in deck.slides if not (set(re.findall(r'\bS\d{2,}\b',' '.join(s['sources']))) & ids)]
    check('content_slide_sources',not no_refs,{'missing':no_refs,'scope':'all slides, including cover and sources'})
    draft=(ROOT/'workflow/draft.md').read_text(encoding='utf-8')
    chunks=re.split(r'^## \d{2} ',draft,flags=re.M)[1:]
    mismatches=[]
    for i,chunk in enumerate(chunks):
        lines=chunk.splitlines()
        expected={'title':[lines[0]],'stage':[x.removeprefix('階段：') for x in lines if x.startswith('階段：')],'sources':[x.removeprefix('來源：') for x in lines if x.startswith('來源：')],'points':[x[2:] for x in lines if x.startswith('- ')],'takeaway':[x[2:] for x in lines if x.startswith('> ')]}
        if i>=len(deck.slides) or any(deck.slides[i][k]!=v for k,v in expected.items()): mismatches.append(i+1)
    check('draft_html_exact_content',not mismatches and len(chunks)==len(deck.slides),{'different_pages':mismatches,'draft_pages':len(chunks)})
else:
    check('html_available',False,'deck.html missing')

print(json.dumps({'results':results,'passed':sum(r['result']=='PASS' for r in results),'failed':sum(r['result']=='FAIL' for r in results),'limits':['Source ID existence does not prove semantic fidelity.','Browser rendering and human usability are separate checks.','Readable means extractable text, not complete image ingestion.']},ensure_ascii=False,indent=2))
sys.exit(1 if any(r['result']=='FAIL' for r in results) else 0)
