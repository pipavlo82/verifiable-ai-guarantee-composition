"""Exploratory descriptor examples only; not an evidence acceptance API."""
EXAMPLES=[
 {'name':'statement_only','DECLARED':True,'DISCRIMINATING':False,'ATTRIBUTION':False,'INDEPENDENT':False,'kind':'synthetic explanatory descriptor'},
 {'name':'anonymous_controlled_experiment','DECLARED':False,'DISCRIMINATING':True,'ATTRIBUTION':False,'INDEPENDENT':False,'kind':'synthetic explanatory descriptor'},
 {'name':'authenticated_untested_statement','DECLARED':True,'DISCRIMINATING':False,'ATTRIBUTION':True,'INDEPENDENT':False,'kind':'synthetic explanatory descriptor'},
 {'name':'independent_anonymous_recomputation','DECLARED':False,'DISCRIMINATING':False,'ATTRIBUTION':False,'INDEPENDENT':True,'kind':'synthetic explanatory descriptor'},
]
CATEGORIES=('DECLARED','DISCRIMINATING','ATTRIBUTION','INDEPENDENT')
def non_implications():
 return [{'from':a,'to':b,'witness':next((e['name'] for e in EXAMPLES if e[a] and not e[b]),None)} for a in CATEGORIES for b in CATEGORIES if a!=b]
