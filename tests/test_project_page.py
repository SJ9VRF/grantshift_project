from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]; self.ids=set(); self.video_sources=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag=='a' and 'href' in a: self.hrefs.append(a['href'])
        if tag=='source' and 'src' in a: self.video_sources.append(a['src'])

def test_project_page_structure_and_links():
    page=ROOT/'project/index.html'
    assert page.exists()
    text=page.read_text()
    parser=LinkParser(); parser.feed(text)
    required_ids={'problem','idea','architecture','contrib','experiments','results','failures','demo','scaling','safety','deep','artifacts','citation'}
    assert required_ids <= parser.ids
    assert 'Aura Yavary' in text
    assert 'GrantShift' in text
    assert 'Paper' in text and 'Code' in text and 'Demo' in text and 'Benchmark' in text and 'Video' in text
    for href in parser.hrefs:
        if href.startswith('#') or '://' in href or href.startswith('mailto:'):
            continue
        target=(page.parent/href.split('#',1)[0]).resolve()
        assert target.exists(), f'broken local link: {href}'
    for src in parser.video_sources:
        target=(page.parent/src).resolve(); assert target.exists(), f'missing video source: {src}'

def test_project_supporting_artifacts_exist():
    required=[
        'paper/grantshift-paper.pdf', 'docs/engineering_report.md', 'docs/blog_post.md',
        'CITATION.bib', 'project/assets/trajectory.json', 'project/assets/project_data.json',
        'project/assets/grantshift-overview.mp4', 'evidence/EXPERIMENT_JOURNAL.md'
    ]
    for rel in required:
        p=ROOT/rel
        assert p.exists() and p.stat().st_size>0, rel


def test_project_page_requested_semantics():
    text=(ROOT/'project/index.html').read_text()
    required_phrases=[
        'Problem','Contribution','Evidence',
        'Agent loop:','Preference-learning / recovery loop:','Training loop:',
        'Operational / recovery view','External inference cost',
        'GitHub / Code','Technical report','Blog post',
        'Irreversible actions','Human escalation','Aura Yavary'
    ]
    for phrase in required_phrases:
        assert phrase in text, phrase
