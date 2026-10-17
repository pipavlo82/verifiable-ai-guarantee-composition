"""Read-only bounded HTTP capture. Preserve bytes before any parsing or normalization."""
import argparse,datetime,hashlib,json,urllib.request,urllib.error
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--plan',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    plan=json.loads(Path(a.plan).read_text());out=Path(a.out)
    if out.exists():raise SystemExit('Capture destination must be new; never overwrite evidence')
    out.mkdir(parents=True);rows=[]
    for item in plan['requests']:
        name=item['id'];url=item['url']
        if not name.replace('-','').replace('_','').isalnum() or not url.startswith('https://'):raise ValueError('Unsafe capture name or non-HTTPS URL')
        row={'id':name,'url':url,'method':'GET','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};raw=b''
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'guarantee-composition-research/3'}),timeout=30) as r:
                raw=r.read(4000001);row.update(status=r.status,content_type=r.headers.get('Content-Type'),final_url=r.url)
                if len(raw)>4000000:raise ValueError('Response exceeded capture bound')
        except urllib.error.HTTPError as e:raw=e.read(4000000);row['status']=e.code
        except Exception as e:row['error']=type(e).__name__+': '+str(e)
        path=name+'.raw';(out/path).write_bytes(raw);row.update(file=path,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));rows.append(row)
        print(json.dumps({k:row.get(k) for k in ('id','status','bytes','error')}),flush=True)
    (out/'capture.json').write_text(json.dumps({'schema':'public-capture-v3','requests':rows},indent=2)+'\n',encoding='utf-8',newline='\n')
    return 0 if all(r.get('status')==200 for r in rows) else 2
if __name__=='__main__':raise SystemExit(main())
