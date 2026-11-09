import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const read = (p) => readFile(new URL(`../${p}`, import.meta.url), 'utf8');

test('網站首頁使用繁體中文且有主內容與視窗設定', async () => {
  const page = await read('site/index.html');
  assert.match(page, /lang="zh-Hant"/);
  assert.match(page, /id="main"/);
  assert.match(page, /name="viewport"/);
});

test('示範網站使用相對路徑，適合 GitHub Pages 子路徑', async () => {
  const page = await read('site/index.html');
  assert.match(page, /href="\.\/styles\.css"/);
  assert.match(page, /src="\.\/app\.js"/);
});

test('示範互動有可存取性狀態且不使用本機保存', async () => {
  const page = await read('site/index.html');
  const script = await read('site/app.js');
  assert.match(page, /aria-expanded="false"/);
  assert.match(script, /aria-expanded/);
  assert.doesNotMatch(script, /localStorage|sessionStorage/);
});

test('重要流程文件與交接文件存在', async () => {
  const docs = ['docs/SPEC.md','docs/DESIGN.md','docs/TECH.md','docs/HANDOFF.md','docs/WORKFLOW.md','CLAUDE.md'];
  for (const path of docs) assert.ok((await read(path)).length > 100, path);
});
