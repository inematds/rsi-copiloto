"""Check multilingual guide structure, local asset links and static app files."""
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
import re
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):super().__init__();self.counts=Counter();self.links=[];self.ids=set();self.lang=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.counts[tag]+=1
        if tag=='html':self.lang=d.get('lang')
        if 'id' in d:self.ids.add(d['id'])
        if tag in ['a','link','img','script']:
            key='src' if tag in ['img','script'] else 'href'
            if d.get(key):self.links.append(d[key])
base=None
for locale,path in [('pt-BR','guia/index.html'),('en','guia/en/index.html'),('es','guia/es/index.html')]:
    file=ROOT/path;src=file.read_text();p=Page();p.feed(src)
    assert p.lang==locale,(path,p.lang)
    assert not re.search(r'\{\{[A-Z_]+\}\}',src),path
    if base is None:base=p
    assert all(base.counts[t]==p.counts[t] for t in ['div','section','li','figure']),path
    assert p.ids==base.ids,path
    for url in p.links:
        if '://' in url or url.startswith('mailto:'):continue
        if url.startswith('#'):assert url[1:] in p.ids,(path,url);continue
        clean=url.split('#')[0].split('?')[0]
        target=(file.parent/clean).resolve()
        assert target.is_relative_to(ROOT) and target.exists(),(path,url)
    print(path,'OK',p.counts['section'],'sections')
for file in ['app/index.html','app/style.css','app/app.js','app/demo.js','app/backup.js','app/catalog.json','README.md','README.en.md','README.es.md']:
    assert (ROOT/file).is_file(),file
print('Static files and multilingual links OK')
