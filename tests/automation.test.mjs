import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const read = (path) => readFile(new URL(`../${path}`, import.meta.url), 'utf8');

test('Pages 只在 main push 或人工重新部署時運作', async () => {
  const text = await read('.github/workflows/pages.yml');
  assert.match(text, /push:\s*\n\s*branches: \[main\]/);
  assert.match(text, /workflow_dispatch:/);
  assert.match(text, /github\.ref == 'refs\/heads\/main'/);
  assert.match(text, /uses: actions\/deploy-pages@v4/);
  assert.match(text, /needs: build/);
  assert.match(text, /npm run check/);
  assert.match(text, /npm test/);
  assert.match(text, /npm run build/);
});

test('Release 不在每次 main push 執行，必須人工批准且有原始碼核驗', async () => {
  const text = await read('.github/workflows/release.yml');
  assert.match(text, /workflow_dispatch:/);
  assert.doesNotMatch(text, /\n\s*push:/);
  assert.match(text, /github\.ref == 'refs\/heads\/main'/);
  assert.match(text, /python3 scripts\/verify_release\.py/);
  assert.match(text, /--expected-commit "\$GITHUB_SHA"/);
  assert.match(text, /gh release create/);
  assert.match(text, /--target "\$GITHUB_SHA"/);
  assert.match(text, /ZIP-SHA256SUMS\.txt/);
});

test('CLAUDE.md 告知不得直接合併 main', async () => {
  const s = await read('CLAUDE.md');
  assert.match(s, /不得直接修改、強制推送或自行合併 `main`/);
  assert.match(s, /release\.yml/);
});
