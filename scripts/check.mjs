import { readFile, readdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = [
  'README.md','QUICKSTART.md','CLAUDE.md','docs/SPEC.md','docs/DESIGN.md',
  'docs/TECH.md','docs/HANDOFF.md','docs/WORKFLOW.md','docs/DATA_SAFETY.md',
  'templates/CHATGPT_TO_CLAUDE.md','templates/CLAUDE_TO_CHATGPT.md',
  'templates/CLAUDE_GITHUB_TASK.md','docs/RELEASE_AUTOMATION.md',
  'docs/CODE_REVIEW.md','docs/RISK_POLICY.md','docs/REVIEW_LOG.md',
  'templates/CHATGPT_CODE_REVIEW.md','templates/CHATGPT_REVIEW_REQUEST.md',
  'templates/REVIEW_FIX_HANDOFF.md','templates/CLAUDE_REVIEW_RESPONSE.md',
  'scripts/export_review_packet.py',
  '.github/workflows/ci.yml','.github/workflows/pages.yml','.github/workflows/release.yml',
  'site/index.html','site/styles.css','site/app.js'
];
for (const f of required) await readFile(join(root, f));
const html = await readFile(join(root, 'site/index.html'), 'utf8');
if (!html.includes('lang="zh-Hant"')) throw new Error('HTML 請設定 lang="zh-Hant"');
if (!html.includes('name="viewport"')) throw new Error('HTML 缺少 viewport');
if (/\b(?:src|href)\s*=\s*["']\/(?!\/)/i.test(html)) {
  throw new Error('偵測到根路徑資源，可能破壞 GitHub Pages 子路徑部署');
}
const blocked = /\b(?:localStorage|sessionStorage)\b/;
const js = await readFile(join(root, 'site/app.js'), 'utf8');
if (blocked.test(js)) throw new Error('示範網站不應儲存本機資料');
const siteFiles = await readdir(join(root,'site'));
if (siteFiles.some(f => /^\.env(?:\.|$)|secret|credential/i.test(f))) {
  throw new Error('site/ 不可包含機密檔名');
}
console.log(`檢查通過：${required.length} 個必要檔案、HTML 設定與示範網站儲存策略。`);
console.log('注意：這是基礎結構檢查，不是完整安全稽核。');
