// html2frames.mjs: render an HTML animation to deterministic frames with a virtual clock.
//   node html2frames.mjs --src anim.html --out frames --w 1920 --h 1080 [--scale 1] [--fps 30] [--duration 5] [--workers N] [--png]
// Timers, Date, performance.now and requestAnimationFrame are driven by Playwright's fake clock; CSS and Web
// Animations are paused and seeked to each frame's time. The page may set window.DURATION (seconds).
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { pathToFileURL } from "node:url";
import { cpus, homedir } from "node:os";

const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i < 0 ? d : (process.argv[i + 1]?.startsWith("--") || process.argv[i + 1] === undefined ? true : process.argv[i + 1]); };
const modules = process.env.FREE4K_NODE || join(homedir(), ".cache", "free-4k", "node_modules");
const { chromium } = createRequire(join(modules, "x.js"))("playwright-core");
const src = resolve(arg("src")), out = resolve(arg("out", "frames")), W = +arg("w", 1920), H = +arg("h", 1080), scale = +arg("scale", 1), fps = +arg("fps", 30);
const png = !!arg("png", false), workers = Math.max(1, +arg("workers", Math.min(4, cpus().length)));
mkdirSync(out, { recursive: true });

const findChrome = () => { if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  if (existsSync(base)) for (const d of readdirSync(base)) if (/^chromium-\d+$/.test(d)) { const p = join(base, d, "chrome-linux", "chrome"); if (existsSync(p)) return p; }
  return undefined; };
const exe = findChrome();
const browser = await chromium.launch({ executablePath: exe, channel: exe ? undefined : (process.env.CHROME_CHANNEL || undefined), args: ["--no-sandbox", "--force-color-profile=srgb", "--enable-unsafe-swiftshader"] });
const open = async () => { const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: scale });
  await page.clock.install({ time: 0 }); await page.goto(pathToFileURL(src).href, { waitUntil: "load" }); await page.evaluate(() => document.fonts?.ready); return page; };
const probe = await open();
const duration = +arg("duration", 0) || (await probe.evaluate(() => window.DURATION || +document.documentElement.dataset.duration || 0)) || 5;
await probe.close();
const N = Math.round(duration * fps), per = Math.ceil(N / workers), t0 = Date.now(); let done = 0;
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const a = w * per, b = Math.min(N, a + per); if (a >= b) return;
  const page = await open(); let now = 0;
  for (let i = a; i < b; i++) {
    const t = Math.round((i * 1000) / fps);
    if (t > now) { await page.clock.runFor(t - now); now = t; }
    await page.evaluate((ms) => { for (const an of document.getAnimations()) { an.pause(); an.currentTime = ms; } }, t);
    await page.screenshot({ path: join(out, `f${String(i).padStart(6, "0")}.${png ? "png" : "jpg"}`), type: png ? "png" : "jpeg", ...(png ? {} : { quality: 95 }) });
    if (++done % 30 === 0 || done === N) process.stdout.write(`  frame ${done}/${N}  ${((Date.now() - t0) / done).toFixed(0)} ms/frame\n`);
  }
  await page.close();
}));
await browser.close();
console.log(`frames: ${N} at ${W * scale}x${H * scale} -> ${out}`);
