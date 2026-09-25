/* Validate the complete offline file before replacing browser data. */
window.validateRSIBackup=function(b){
 const fail=()=>{throw Error('Backup inválido ou incompleto. Os dados atuais foram preservados.');};
 const obj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
 const str=(x,k)=>k.every(v=>typeof x[v]==='string');
 if(!obj(b)||b.schema!==1||!['pessoal','autonomo','empresa'].includes(b.profile)||typeof b.active!=='string')fail();
 const fields={tasks:['id','title','due','status','profile','created'],memories:['id','title','body','profile','created'],versions:['id','name','prompt','created'],runs:['id','prompt','profile','version','created'],candidates:['id','name','prompt','rationale','base','created','profile'],experiments:['id','candidate','base','created','mode','profile'],routines:['id','name','prompt','profile','next'],audit:['id','at','event','detail'],usage:['id','at','status']};
 for(const [key,required] of Object.entries(fields)){if(!Array.isArray(b[key])||b[key].length>10000)fail();const ids=new Set();for(const row of b[key]){if(!obj(row)||!str(row,required)||ids.has(row.id))fail();ids.add(row.id);if('profile' in row&&!['pessoal','autonomo','empresa','todos'].includes(row.profile))fail();}}
 if(!b.versions.some(v=>v.id===b.active))fail();
 const output=o=>{if(!obj(o)||!str(o,['title','answer']))fail();for(const k of ['assumptions','sources','actions'])if(!Array.isArray(o[k])||o[k].length>12||o[k].some(x=>typeof x!=='string'||x.length>1600))fail();if(!o.actions.length||o.actions.length>8)fail();};
 for(const r of b.runs){output(r.output);if(!obj(r.meta)||typeof r.meta.model!=='string'||!Array.isArray(r.context)||r.context.some(x=>!obj(x)||!str(x,['id','title']))||typeof r.applied!=='boolean')fail();if(r.feedback!==null&&(!obj(r.feedback)||!str(r.feedback,['note'])||!Number.isInteger(r.feedback.rating)||r.feedback.rating<1||r.feedback.rating>5))fail();}
 for(const t of b.tasks)if(!['open','done'].includes(t.status)||(t.due&&!/^\d{4}-\d{2}-\d{2}$/.test(t.due)))fail();
 for(const r of b.routines)if(typeof r.enabled!=='boolean'||Number.isNaN(Date.parse(r.next)))fail();
 for(const e of b.experiments){if(!obj(e.scores)||!Array.isArray(e.cases)||e.cases.length!==3)fail();if(e.review!==null&&(!obj(e.review)||typeof e.review.note!=='string'))fail();for(const k of ['baseline','candidate'])if(typeof e.scores[k]!=='number'||!Number.isFinite(e.scores[k])||e.scores[k]<0||e.scores[k]>100)fail();for(const c of e.cases){if(!obj(c)||typeof c.input!=='string')fail();for(const k of ['baseline','candidate']){if(!obj(c[k]))fail();output(c[k].output);if(!obj(c[k].metrics)||!obj(c[k].metrics.checks)||Object.values(c[k].metrics.checks).some(v=>typeof v!=='boolean'))fail();}}}
 const missions=b.missions??[];const statuses=['plan','ready','review','manual','paused','completed','cancelled'];
 if(!Array.isArray(missions)||missions.length>1000)fail();const mids=new Set();
 for(const m of missions){if(!obj(m)||!str(m,['id','title','goal','profile','created','version','instruction'])||mids.has(m.id)||!['pessoal','autonomo','empresa'].includes(m.profile)||!statuses.includes(m.status)||!Number.isInteger(m.revision)||m.revision<0)fail();mids.add(m.id);
 if(!Array.isArray(m.steps)||m.steps.length<1||m.steps.length>5||!Number.isInteger(m.current)||m.current<0||m.current>m.steps.length)fail();
 if(m.current===m.steps.length&&!['completed','cancelled'].includes(m.status))fail();if(m.status==='completed'&&m.current!==m.steps.length)fail();
 if(m.error!==null&&typeof m.error!=='string')fail();if(![null,'plan','ready','review','manual'].includes(m.resume)||(m.status==='paused'&&m.resume===null))fail();
 for(const [i,x] of m.steps.entries()){if(!obj(x)||!str(x,['id','title','instruction','feedback'])||!['draft','manual'].includes(x.kind)||!['pending','review','manual','approved'].includes(x.status)||!Array.isArray(x.attempts)||x.attempts.length>10)fail();if(i<m.current&&x.status!=='approved')fail();if(x.review!==null&&(!obj(x.review)||typeof x.review.note!=='string'||!Number.isInteger(x.review.rating)||x.review.rating<1||x.review.rating>5))fail();if(x.status==='approved'&&x.review===null)fail();if(x.status==='review'&&!x.attempts.length)fail();for(const a of x.attempts){if(!obj(a)||!str(a,['run','created'])||!Array.isArray(a.context)||a.context.some(c=>!obj(c)||!str(c,['id','title']))||!b.runs.some(r=>r.id===a.run))fail();output(a.output);}}
 if(['review','manual'].includes(m.status)&&(m.steps[m.current].status!==m.status||(m.status==='manual'&&m.steps[m.current].kind!=='manual')))fail();}
 return {...structuredClone(b),missions:structuredClone(missions),version:'1.1.0'};
};
