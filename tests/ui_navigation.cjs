const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1220, height: 780 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('file:///' + path.resolve(__dirname, '../assets/index.html').replaceAll('\\', '/'));
  await page.evaluate(() => {
    window.pywebview = { api: {
      render: async () => ({ ok: true, html: '<h1>标题</h1><p>needle NEEDLE</p>' + '<p>正文</p>'.repeat(100) + '<h2>末尾</h2><p>needle</p>' }),
      set_dirty: async () => {},
    } };
    applyDocument({ content: '# 标题\nneedle NEEDLE\n' + '正文\n'.repeat(100) + '## 末尾\nneedle', name: 'sample.md' });
  });
  await page.locator('#preview h2').waitFor();
  await page.evaluate(async () => {
    editor.scrollTop = editor.scrollHeight;
    previewPane.scrollTop = previewPane.scrollHeight;
    applyDocument({ content: '# 标题\nneedle NEEDLE\n' + '正文\n'.repeat(100) + '## 末尾\nneedle', name: 'another.md' });
    await new Promise(requestAnimationFrame);
    editor.focus();
  });
  assert.deepEqual(await page.evaluate(() => [editor.scrollTop, previewPane.scrollTop, editor.selectionStart]), [0, 0, 0]);
  await page.evaluate(async () => {
    editor.scrollTop = 100;
    previewPane.scrollTop = 100;
    await renderPreview();
  });
  assert.deepEqual(await page.evaluate(() => [editor.scrollTop, previewPane.scrollTop]), [100, 100]);
  await page.keyboard.press('Control+f');
  await page.locator('#findInput').fill('needle');
  assert.equal(await page.locator('#findCount').innerText(), '0 / 3');
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('#findCount').innerText(), '1 / 3');
  assert.equal(await page.locator('#editor').evaluate(el => el.value.slice(el.selectionStart, el.selectionEnd)), 'needle');
  await page.locator('#findPrev').click();
  assert.equal(await page.locator('#findCount').innerText(), '3 / 3');
  assert.ok(await page.locator('#editor').evaluate(el => el.scrollTop) > 0);
  await page.locator('#editModeBtn').click();
  assert.equal(await page.locator('#preview mark').count(), 3);
  await page.locator('#findNext').click();
  assert.equal(await page.locator('#preview mark.current').innerText(), 'needle');
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#preview mark').count(), 0);
  await page.locator('#editModeBtn').click();
  const handle = await page.locator('.splitter').boundingBox();
  await page.mouse.move(handle.x + 3, handle.y + 100);
  await page.mouse.down();
  await page.mouse.move(850, handle.y + 100);
  await page.mouse.up();
  assert.ok((await page.locator('#editorPane').boundingBox()).width > 800);
  await page.locator('#outlineBtn').click();
  const outlineBounds = await page.locator('#outline').boundingBox();
  const previewBounds = await page.locator('#previewPane').boundingBox();
  assert.ok(outlineBounds.x >= previewBounds.x + previewBounds.width - 1);
  assert.equal(await page.locator('#outline button').count(), 2);
  await page.locator('#outline button').last().click();
  assert.ok(await page.locator('#previewPane').evaluate(el => el.scrollTop) > 0);
  await page.setViewportSize({ width: 820, height: 560 });
  await page.locator('#outline button').last().click();
  assert.equal(await page.locator('#previewPane').isVisible(), true);
  assert.equal(await page.evaluate(() => window.appState.dirty), false);
  await page.locator('#syntaxBtn').click();
  const syntax = await page.locator('#syntaxPane').boundingBox();
  const outline = await page.locator('#outline').boundingBox();
  assert.ok(syntax.x > outline.x);
  await page.locator('#readerModeBtn').click();
  assert.equal(await page.locator('#outline').isVisible(), false);
  assert.equal(await page.locator('#syntaxPane').isVisible(), true);
  await page.locator('#editModeBtn').click();
  assert.equal(await page.locator('#editorPane').isVisible(), true);
  await page.locator('#syntaxBtn').click();
  assert.equal(await page.locator('#editor').inputValue(), '# 标题\nneedle NEEDLE\n' + '正文\n'.repeat(100) + '## 末尾\nneedle');
  for (const [source, expected] of [
    ['1. 项目', '1. 项目\n2. '], ['- 项目', '- 项目\n- '],
    ['    + 项目', '    + 项目\n    + '], ['- [x] 完成', '- [x] 完成\n- [ ] '],
    ['2) 项目', '2) 项目\n3) '], ['- ', ''], ['    1. ', ''],
    ['普通正文', '普通正文\n'], ['```\n- 代码', '```\n- 代码\n'],
  ]) {
    await page.locator('#editor').fill(source);
    await page.locator('#editor').press('Control+End');
    await page.locator('#editor').press('Enter');
    assert.equal(await page.locator('#editor').inputValue(), expected);
    if (expected !== source + '\n') {
      await page.locator('#editor').press('Control+z');
      assert.equal(await page.locator('#editor').inputValue(), source);
    }
  }
  await page.locator('#editor').fill('- 项目');
  await page.locator('#editor').press('Control+End');
  await page.locator('#editor').press('Shift+Enter');
  assert.equal(await page.locator('#editor').inputValue(), '- 项目\n');
  assert.equal(await page.evaluate(() => window.appState.dirty), true);
  assert.deepEqual(errors, []);
  await browser.close();
  console.log('PASS: search/count/wrap/scroll, reader highlights, splitter drag, outline jump, narrow layout, unchanged document');
})().catch(error => { console.error(error); process.exitCode = 1; });
