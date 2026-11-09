import { readdir, readFile, rm, mkdir, copyFile, lstat, writeFile } from 'node:fs/promises';
import { join, relative, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const src = fileURLToPath(new URL('../site/', import.meta.url));
const dst = fileURLToPath(new URL('../dist/', import.meta.url));
const allowedExtensions = new Set([
  '.html', '.css', '.js', '.json', '.txt', '.svg', '.png', '.jpg', '.jpeg',
  '.webp', '.avif', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.webmanifest',
  '.pdf', '.mp4', '.webm', '.mp3', '.wav'
]);

async function gather(folder) {
  const entries = await readdir(folder, { withFileTypes: true });
  const found = [];
  for (const entry of entries) {
    const full = join(folder, entry.name);
    const st = await lstat(full);
    if (st.isSymbolicLink()) throw new Error(`不允許符號連結: ${relative(src, full)}`);
    if (entry.name.startsWith('.') || /(?:secret|credential|private|backup|\.env)/i.test(entry.name)) {
      throw new Error(`網站目錄含可疑檔名: ${relative(src, full)}`);
    }
    if (st.isDirectory()) found.push(...await gather(full));
    else if (st.isFile()) {
      if (!allowedExtensions.has(extname(entry.name).toLowerCase())) {
        throw new Error(`網站檔案格式未列入部署清單: ${relative(src, full)}`);
      }
      found.push(full);
    }
  }
  return found;
}

const index = await readFile(join(src, 'index.html'), 'utf8');
if (!index.includes('<html') || !index.includes('</html>')) throw new Error('site/index.html 無效');
const files = await gather(src); // 必須先驗證，再清除 dist/
await rm(dst, { recursive: true, force: true });
await mkdir(dst, { recursive: true });
for (const file of files) {
  const out = join(dst, relative(src, file));
  await mkdir(dirname(out), { recursive: true });
  await copyFile(file, out);
}
// 避免 Pages 使用 Jekyll 處理包含底線的靜態路徑。
await writeFile(join(dst, '.nojekyll'), '', 'utf8');
console.log(`建置完成：${files.length} 個靜態檔案 → dist/`);
