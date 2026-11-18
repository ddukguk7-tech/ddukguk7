#!/usr/bin/env python3
"""CSV가 변경될 때 Netlify 빌드 중 HTML/JSON을 새로 생성합니다. 표준 라이브러리만 사용."""
from pathlib import Path
from datetime import datetime,timezone
import csv, json, re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUTPUT=ROOT/'dist'
TEMPLATE=ROOT/'site'/'index.template.html'

SCHEMAS={
 '청렴신고_사건데이터.csv':{
    'fields':['사건ID','신고일자','신고유형','지역','처리상태'],
    'numeric':['처리기간_일','위반금액_만원']},
 '청렴교육_현황.csv':{
    'fields':['기관코드','기관명','기관유형','교육이수율','연간교육시간','교육참여자수','청렴우수기관'],
    'numeric':['교육이수율','연간교육시간','교육참여자수']}
}

def load_csv(name):
    p=DATA/name
    if not p.is_file(): raise FileNotFoundError(f'필수 CSV 없음: {p}')
    with p.open('r',encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames: raise ValueError(f'헤더 없는 CSV: {name}')
        required=SCHEMAS[name]['fields']
        missing=[x for x in required if x not in reader.fieldnames]
        if missing: raise ValueError(f'{name} 필수 열 누락: {missing}')
        rows=[]
        for idx,row in enumerate(reader,start=2):
            if None in row: raise ValueError(f'{name}:{idx} 열 개수가 헤더보다 많음')
            item={}
            for k,v in row.items():
                val=(v or '').strip()
                if not val: item[k]=None
                elif k in SCHEMAS[name]['numeric']:
                    try: item[k]=float(val) if '.' in val else int(val)
                    except ValueError: raise ValueError(f'{name}:{idx} {k} 숫자 오류: {val}')
                else:item[k]=val
            rows.append(item)
    if not rows:raise ValueError(f'데이터 행 없음: {name}')
    return rows

def main():
    cases=load_csv('청렴신고_사건데이터.csv')
    education=load_csv('청렴교육_현황.csv')
    meta=json.loads((DATA/'news_snapshot.json').read_text(encoding='utf-8'))
    payload={'cases':cases,'education':education,'news':meta['news']}
    timestamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT/'data.json').write_text(json.dumps({**payload,'built_at_utc':timestamp,'rss_url':meta['rss_url'],'rss_status':meta['rss_status']},ensure_ascii=False,indent=2),encoding='utf-8')
    html=TEMPLATE.read_text(encoding='utf-8')
    placeholder='__BUILD_DATA_JSON__'
    if html.count(placeholder)!=1:raise ValueError('HTML 템플릿의 JSON 삽입 위치를 찾지 못함')
    embedded=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html=html.replace(placeholder,embedded)
    (OUTPUT/'index.html').write_text(html,encoding='utf-8')
    print(f'배포 파일 생성: 신고 {len(cases)}건 / 교육 {len(education)}건')
    print(f'파일: {OUTPUT / "index.html"}, {OUTPUT / "data.json"}')

if __name__=='__main__':main()
