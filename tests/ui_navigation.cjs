const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1220, height: 780 } });
  const errors = [];
  page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
  await page.goto('file:///' + path.resolve(__dirname, '../assets/index.html').replaceAll('\\', '/'));
  async function menuClick(id) {
    const item = page.locator(id);
    await item.locator('xpath=ancestor::details/summary').click();
    await item.click();
    assert.equal(await page.locator('.menu[open]').count(), 0);
  }
  assert.equal(await page.locator('#toolbar > button').count(), 2);
  await page.getByText('视图', { exact: true }).click();
  await page.getByText('设置', { exact: true }).click();
  assert.equal(await page.locator('.menu[open]').count(), 1);
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('.menu[open]').count(), 0);
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
  await menuClick('#editModeBtn');
  assert.equal(await page.locator('#preview mark').count(), 3);
  await page.locator('#findNext').click();
  assert.equal(await page.locator('#preview mark.current').innerText(), 'needle');
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#preview mark').count(), 0);
  await menuClick('#editModeBtn');
  const handle = await page.locator('.splitter').boundingBox();
  await page.mouse.move(handle.x + 3, handle.y + 100);
  await page.mouse.down();
  await page.mouse.move(850, handle.y + 100);
  await page.mouse.up();
  assert.ok((await page.locator('#editorPane').boundingBox()).width > 800);
  await menuClick('#outlineBtn');
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
  await menuClick('#syntaxBtn');
  const syntax = await page.locator('#syntaxPane').boundingBox();
  const outline = await page.locator('#outline').boundingBox();
  assert.ok(syntax.x > outline.x);
  await menuClick('#readerModeBtn');
  assert.equal(await page.locator('#outline').isVisible(), false);
  assert.equal(await page.locator('#syntaxPane').isVisible(), true);
  await menuClick('#editModeBtn');
  assert.equal(await page.locator('#editorPane').isVisible(), true);
  await menuClick('#syntaxBtn');
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
  await page.evaluate(() => {
    window.appState.path = 'C:/example.md';
    window.pywebview.api.insert_image = async () => ({ ok: true, markdown: '![图片](example.assets/image.png)' });
    window.pywebview.api.paste_clipboard = async () => ({ ok: true, text: '普通粘贴' });
  });
  await page.locator('#editor').fill('原文');
  await page.locator('#editor').press('Control+End');
  await menuClick('#imageBtn');
  await page.waitForFunction(() => editor.value.includes('![图片]'));
  assert.equal(await page.locator('#editor').inputValue(), '原文![图片](example.assets/image.png)');
  await page.locator('#editor').press('Control+z');
  assert.equal(await page.locator('#editor').inputValue(), '原文');
  await page.locator('#editor').press('Control+v');
  await page.waitForFunction(() => editor.value.includes('普通粘贴'));
  assert.equal(await page.locator('#editor').inputValue(), '原文普通粘贴');
  assert.deepEqual(errors, []);
  await page.evaluate(() => { window.print = () => { window.printCalled = true; }; });
  await menuClick('#printBtn');
  await page.waitForFunction(() => window.printCalled);
  await page.emulateMedia({ media: 'print' });
  assert.equal(await page.locator('#toolbar').isVisible(), false);
  assert.equal(await page.locator('#editorPane').isVisible(), false);
  assert.equal(await page.locator('#syntaxPane').isVisible(), false);
  assert.equal(await page.locator('#previewPane').isVisible(), true);
  const pdf = await page.pdf();
  assert.ok(pdf.length > 1000);
  await browser.close();
  console.log('PASS: search/count/wrap/scroll, reader highlights, splitter drag, outline jump, narrow layout, unchanged document');
})().catch(error => { console.error(error); process.exitCode = 1; });
