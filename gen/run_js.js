const vm = require('vm'), util = require('util'), fs = require('fs');
const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
process.on('unhandledRejection', () => {});
(async () => {
  const res = [];
  for (const it of items) {
    const out = []; let err = null;
    const ctx = vm.createContext({ console: { log: (...a) => out.push(util.format(...a)) }, setTimeout, queueMicrotask });
    try { vm.runInContext(it.src, ctx, { timeout: 2000 }); } catch (e) { err = e && e.name ? e.name : 'Error'; }
    await new Promise(r => setTimeout(r, it.wait || 15));
    res.push({ out: out.join('\n'), err });
  }
  process.stdout.write(JSON.stringify(res));
})();
