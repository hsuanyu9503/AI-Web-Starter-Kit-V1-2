import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const read=(name)=>readFile(new URL(`../${name}`,import.meta.url),'utf8');

test('V1.2 三級風險審查政策存在並禁止無證據核准', async()=>{
  const [risk, review,claude]=await Promise.all([
    read('docs/RISK_POLICY.md'),read('docs/CODE_REVIEW.md'),read('CLAUDE.md')
  ]);
  for(const name of ['L1','L2','L3','BLOCKER','HIGH']) assert.match(risk,new RegExp(name));
  assert.match(review,/Head SHA/);
  assert.match(review,/不能.*GitHub/);
  assert.match(claude,/claude\/\*/);
});

test('V1.2 PR 模板要求風險、實際證據及使用者決策', async()=>{
  const p=await read('.github/pull_request_template.md');
  assert.match(p,/初評風險等級/);
  assert.match(p,/Head SHA/);
  assert.match(p,/使用者的合併決定/);
  assert.match(await read('templates/CLAUDE_REVIEW_RESPONSE.md'),/REV-001/);
});

test('V1.2 預設不把審查紀錄當作自動 GitHub approve',async()=>{
  const [r,w]=await Promise.all([read('docs/CODE_REVIEW.md'),read('.github/workflows/ci.yml')]);
  assert.match(r,/不會自行強制/);
  assert.match(w,/validate:/);
});
