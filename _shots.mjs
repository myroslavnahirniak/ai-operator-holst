// Скрины холста одним headless Chrome.
// usage: URL=http://127.0.0.1:8781/site/ W=1440 H=900 MOBILE=0 OUT=shots NAME=d AT="svodka,u1,u1-more,hunt:0.3" node _shots.mjs
// AT: id элемента (скролл к нему), id:доля — для #hunt доля прокрутки сцены, y=число — абсолютный скролл, js:выражение.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9336, W = +process.env.W || 1440, H = +process.env.H || 900, mobile = process.env.MOBILE === '1';
const chrome = spawn(CH, ['--headless=new', '--hide-scrollbars', '--mute-audio', '--no-first-run', '--autoplay-policy=no-user-gesture-required', `--remote-debugging-port=${port}`, `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function getWs(){ for (let i = 0; i < 40; i++){ try { const l = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); const p = l.find(t => t.type === 'page'); if (p) return p.webSocketDebuggerUrl; } catch(e){} await sleep(250); } throw new Error('no chrome'); }
const ws = new WebSocket(await getWs()); let id = 0; const pending = new Map(); const logs = [];
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)){ pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === 'Runtime.consoleAPICalled' && /error|warn/.test(m.params.type)) logs.push(m.params.type + ': ' + m.params.args.map(a => a.value || a.description).join(' '));
  if (m.method === 'Runtime.exceptionThrown') logs.push('EXC: ' + (m.params.exceptionDetails.exception && m.params.exceptionDetails.exception.description || m.params.exceptionDetails.text));
  if (m.method === 'Network.loadingFailed' && !/net::ERR_ABORTED/.test(m.params.errorText)) logs.push('NET: ' + m.params.errorText + ' ' + (reqs.get(m.params.requestId) || ''));
  if (m.method === 'Network.requestWillBeSent') reqs.set(m.params.requestId, m.params.request.url);
  if (m.method === 'Network.responseReceived' && m.params.response.status >= 400) logs.push('HTTP ' + m.params.response.status + ' ' + m.params.response.url); };
const reqs = new Map();
await new Promise(r => ws.onopen = r);
const send = (method, params = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); return r.result && r.result.result && r.result.result.value; };
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: mobile ? 2 : 1, mobile });
if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true });
await send('Page.navigate', { url: process.env.URL || 'http://127.0.0.1:8781/site/' });
await sleep(+process.env.FIRST || 3500);
await ev("document.documentElement.style.scrollBehavior='auto'");
const out = process.env.OUT || 'shots'; mkdirSync(out, { recursive: true }); const name = process.env.NAME || 's';
const shot = async k => { const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); writeFileSync(`${out}/${name}-${k}.jpg`, Buffer.from(s.result.data, 'base64')); };
const at = (process.env.AT || 'top').split(',').filter(Boolean);
let k = 0;
for (const a of at){
  if (a === 'top') await ev('scrollTo(0,0)');
  else if (a.startsWith('y=')) await ev(`scrollTo(0,${+a.slice(2)})`);
  else if (a.startsWith('js:')) await ev(a.slice(3));
  else if (a.includes(':')){ const [el, f] = a.split(':'); await ev(`(()=>{const w=document.getElementById('${el}');const t=w.getBoundingClientRect().top+scrollY;scrollTo(0,t+(w.offsetHeight-innerHeight)*${+f});})()`); }
  else await ev(`(()=>{const e=document.getElementById('${a}');scrollTo(0,e.getBoundingClientRect().top+scrollY-${mobile ? 48 : 52});})()`);
  await sleep(+process.env.DELAY || 1600);
  await shot(k++);
}
if (process.env.EVAL) console.log('eval:', JSON.stringify(await ev(process.env.EVAL)));
console.log('console:', logs.length ? [...new Set(logs)].join('\n') : 'clean');
ws.close(); chrome.kill();
