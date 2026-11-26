import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','nav','footer'): self.skip+=1
        if tag in ('p','div','li','tr','h1','h2','h3','h4','br','pre','section'): self.out.append('\n')
        if tag=='td': self.out.append(' | ')
    def handle_endtag(self,tag):
        if tag in ('script','style','nav','footer') and self.skip: self.skip-=1
    def handle_data(self,d):
        if not self.skip: self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='ignore').read())
t=html.unescape(''.join(p.out))
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n\n',t)
print(t.strip())
