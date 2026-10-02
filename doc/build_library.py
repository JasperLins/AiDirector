# -*- coding: utf-8 -*-
"""
build_library.py — AiDirector 源码文库生成器（方案④：零依赖单文件文库）
扫描 kb_library/、skills/、AGENTS.md、memory/global/ 下的 Markdown，
内联进一个独立的 library.html：双击即开，无需服务器、无需安装任何包。
左侧文档树 + 右侧"在此页面"目录 + 复制页面按钮 + 明暗双主题（与 doc.html 同色系）。

用法：python build_library.py   （每次改动 md 后重跑一次即可）
"""
import json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # 项目根（脚本在 doc/ 下）
OUT  = ROOT / "doc" / "library.html"

GROUPS = [
    ("总控路由",                  ["AGENTS.md"]),
    ("KB 工具书 · 12 册",         sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"kb_library").glob("*.md"))),
    ("技能索引",                  ["skills/SKILL_INDEX.md"]),
    ("✍️ 编剧叙事",               sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/01_narrative_skills").glob("*.md"))),
    ("🎬 导演·美术·场记",         sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/02_visual_director_skills").glob("*.md"))),
    ("🖼️ 生图技法",               sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/03_image_gen_skills").glob("*.md"))),
    ("🎥 生视频技法",             sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/04_video_gen_skills").glob("*.md"))),
    ("🔌 平台语法插件",           sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/05_platform_plugins").glob("*.md"))),
    ("⚖️ 评分·配音·剪辑·自进化",  sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT/"skills/06_audio_edit_qc_skills").glob("*.md"))),
    ("全局记忆",                  ["memory/global/权威工作流与影视知识库.md", "memory/global/全局复盘避坑黑名单.md"]),
]

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)
DESC_RE = re.compile(r'^description:\s*["\']?(.+?)["\']?\s*$', re.M)

def parse_doc(rel_path):
    p = ROOT / rel_path
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    fm, desc = "", ""
    m = FM_RE.match(text)
    if m:
        fm = m.group(1)
        text = text[m.end():]
        dm = DESC_RE.search(fm)
        if dm:
            desc = dm.group(1).strip()
    tm = re.search(r"^#\s+(.+)$", text, re.M)
    title = tm.group(1).strip() if tm else Path(rel_path).stem
    return {"p": rel_path, "t": title, "d": desc, "raw": text.strip()}

def build():
    docs = []
    for label, paths in GROUPS:
        items = [d for d in (parse_doc(p) for p in paths) if d]
        if items:
            docs.append({"g": label, "items": items})
    total = sum(len(g["items"]) for g in docs)
    kb = sum(len(d["raw"]) for g in docs for d in g["items"])
    payload = json.dumps(docs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    stamp = time.strftime("%Y-%m-%d %H:%M")
    html = TEMPLATE.replace("__DATA__", payload).replace("__STAMP__", stamp).replace(
        "__STATS__", f"{total} 篇 · {kb//1024} KB")
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ 已生成 {OUT.name}：{total} 篇文档，{kb//1024} KB 内容，文件 {(OUT.stat().st_size)//1024} KB")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AiDirector · 源码文库（Skills × KB）</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
<style>
:root{
  --bg:#0E0E0D;--panel:#141413;--panel2:#181817;--line:rgba(255,255,255,.12);--line2:rgba(255,255,255,.26);
  --accent:#F2FF59;--txt:#A0A0A2;--txt2:#8B8B8D;--txt3:#66666A;--title:#E0E0E2;
  --code-bg:#161614;--well:#080d18;
  --mono:'SF Pro',Menlo,Consolas,monospace;
  --sans:'SF Pro','PingFang SC','HarmonyOS Sans SC','Microsoft YaHei',system-ui,sans-serif;
}
html[data-theme="light"]{
  --bg:#ffffff;--panel:#f7f6f4;--panel2:#f1eff7;--line:rgba(83,67,66,.14);--line2:rgba(83,67,66,.3);
  --accent:#49378B;--txt:#534342;--txt2:#7d6b68;--txt3:#a19490;--title:#49378B;
  --code-bg:#2b2735;--well:#f1eff7;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font:15px/1.8 var(--sans)}
::selection{background:var(--accent);color:var(--bg)}
*{scrollbar-width:thin;scrollbar-color:rgba(140,140,140,.3) transparent}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:rgba(140,140,140,.3);border-radius:99px}
::-webkit-scrollbar-track{background:transparent}

/* ===== 三栏骨架 ===== */
.frame{display:grid;grid-template-columns:296px minmax(0,1fr) 232px;min-height:100vh}

/* ===== 顶栏（仅移动端） ===== */
.m-topbar{display:none;position:fixed;top:0;left:0;right:0;z-index:30;height:52px;align-items:center;gap:12px;
  padding:0 16px;background:var(--panel);border-bottom:1px solid var(--line)}
.m-topbar button{width:34px;height:34px;border-radius:50%;border:1px solid var(--line2);background:var(--panel2);color:var(--title);font-size:15px;cursor:pointer}
.m-topbar .tt{font-weight:800;color:var(--title);font-size:15px}

/* ===== 左侧文库树 ===== */
.sidebar{background:var(--panel);border-right:1px solid var(--line);padding:18px 14px 26px;overflow-y:auto;height:100vh;position:sticky;top:0}
.brand{display:flex;align-items:center;gap:10px;padding:2px 6px 14px}
.brand b{color:var(--title);font-size:15.5px;letter-spacing:.02em}
.brand small{color:var(--txt3);font-size:10.5px;display:block;font-family:var(--mono)}
.tbtn{margin-left:auto;width:32px;height:32px;flex:none;border-radius:50%;border:1px solid var(--line2);background:var(--panel2);color:var(--accent);font-size:15px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .25s}
.tbtn:hover{transform:rotate(24deg);background:var(--line)}
.search{width:100%;padding:9px 12px;border-radius:9px;border:1px solid var(--line2);background:var(--bg);color:var(--txt);font:13px var(--sans);outline:none;margin-bottom:12px}
.search:focus{border-color:var(--accent)}
.search::placeholder{color:var(--txt3)}
.group{margin-bottom:6px}
.group>.gl{font:700 11px var(--mono);color:var(--txt3);letter-spacing:.08em;padding:12px 8px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.item{display:block;width:100%;text-align:left;padding:7px 10px;border:0;border-radius:8px;background:transparent;color:var(--txt);font:13.5px/1.5 var(--sans);cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:.15s}
.item:hover{background:var(--panel2);color:var(--title)}
.item.on{background:var(--accent);color:var(--bg);font-weight:700}
.item .hint{color:var(--txt3);font-size:11px}
.item.on .hint{color:var(--bg);opacity:.7}
.side-foot{margin-top:16px;padding:10px 8px 0;border-top:1px solid var(--line);color:var(--txt3);font:10.5px/1.7 var(--mono)}

/* ===== 中栏正文 ===== */
.main{padding:34px clamp(18px,4vw,52px) 90px;min-width:0}
.crumbs{font:11.5px var(--mono);color:var(--txt3);letter-spacing:.06em;margin-bottom:10px;word-break:break-all}
.art-head{border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:26px}
.art-actions{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.cat{font:700 11px var(--mono);color:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:2px 12px;letter-spacing:.06em}
.copy-btn{margin-left:auto;background:var(--accent);border:0;color:var(--bg);font:700 12.5px var(--sans);border-radius:999px;padding:8px 18px;cursor:pointer;transition:.2s}
.copy-btn:hover{opacity:.86}
.copy-btn.okd{background:var(--txt2)}
h1.art-title{font-size:29px;font-weight:900;color:var(--title);line-height:1.35;letter-spacing:.01em}
.art-desc{margin-top:10px;font-size:13px;color:var(--txt2);line-height:1.7;border-left:3px solid var(--accent);padding:2px 0 2px 12px}

/* ===== Markdown 渲染 ===== */
.md{max-width:860px}
.md h2{font-size:21px;font-weight:800;color:var(--title);margin:38px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line);scroll-margin-top:20px}
.md h3{font-size:17px;font-weight:800;color:var(--title);margin:28px 0 12px;scroll-margin-top:20px}
.md h4{font-size:15px;font-weight:700;color:var(--title);margin:20px 0 10px;scroll-margin-top:20px}
.md p{margin:10px 0}
.md ul,.md ol{padding-left:26px;margin:10px 0}
.md li{margin:4px 0}
.md li::marker{color:var(--accent)}
.md a{color:var(--accent);text-decoration:none;border-bottom:1px dashed var(--accent)}
.md blockquote{margin:14px 0;padding:10px 16px;border-left:3px solid var(--accent);background:var(--panel);border-radius:0 10px 10px 0;color:var(--txt2);font-size:13.5px}
.md blockquote p{margin:4px 0}
.md hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.md code{font-family:var(--mono);font-size:.88em;background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:1px 6px;color:var(--title)}
.md pre{background:var(--code-bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px;overflow-x:auto;margin:14px 0;line-height:1.7}
.md pre code{background:transparent;border:0;padding:0;font-size:12.8px;color:#c9ccd6;white-space:pre-wrap;word-break:break-word}
.md table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13px;display:block;overflow-x:auto}
.md th{background:var(--panel2);color:var(--title);font-weight:700;text-align:left}
.md th,.md td{border:1px solid var(--line);padding:7px 12px;vertical-align:top}
.md tr:nth-child(even) td{background:var(--panel)}
.md img{max-width:100%;border-radius:10px}
.md strong{color:var(--title)}

/* ===== 右栏：在此页面 ===== */
.toc{padding:34px 18px;position:sticky;top:0;height:100vh;overflow-y:auto}
.toc .tl{font:700 11.5px var(--mono);color:var(--txt3);letter-spacing:.1em;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.toc a{display:block;color:var(--txt2);text-decoration:none;font-size:12.5px;line-height:1.55;padding:4px 10px;border-left:2px solid var(--line);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:.15s}
.toc a:hover{color:var(--title)}
.toc a.lv3{padding-left:22px}
.toc a.lv4{padding-left:34px;font-size:12px}
.toc a.on{color:var(--accent);border-left-color:var(--accent);font-weight:700}

/* ===== Toast ===== */
#toast{position:fixed;left:50%;bottom:34px;transform:translateX(-50%) translateY(16px);z-index:60;background:var(--title);color:var(--bg);font:600 13px var(--sans);padding:9px 20px;border-radius:999px;opacity:0;pointer-events:none;transition:.25s}
#toast.show{opacity:1;transform:translateX(-50%)}
.raw-fallback{white-space:pre-wrap;font-family:var(--mono);font-size:13px}

/* ===== 响应式（置于末尾确保覆盖基础样式） ===== */
@media(max-width:1180px){
  .frame{grid-template-columns:280px minmax(0,1fr)}
  .toc{display:none}
}
@media(max-width:900px){
  .frame{grid-template-columns:1fr}
  .sidebar{position:fixed;left:0;top:0;bottom:0;z-index:40;width:300px;transform:translateX(-102%);transition:transform .28s}
  .sidebar.open{transform:none}
  .toc{display:none}
  .m-topbar{display:flex}
  .main{padding-top:52px}
  .backdrop{display:none;position:fixed;inset:0;z-index:35;background:rgba(0,0,0,.45)}
  .backdrop.show{display:block}
}
</style>
</head>
<body>
<script id="library-data" type="application/json">__DATA__</script>

<div class="m-topbar">
  <button id="mMenu" type="button" aria-label="打开文库目录">☰</button>
  <span class="tt">📚 AiDirector 文库</span>
  <button class="tbtn" id="themeToggleM" type="button" title="切换白天/黑夜模式" style="margin-left:auto">🌙</button>
</div>
<div class="backdrop" id="backdrop"></div>

<div class="frame">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div><b>📚 AiDirector 文库</b><small>SKILLS × KB · 本地单文件</small></div>
      <button class="tbtn" id="themeToggle" type="button" title="切换白天/黑夜模式">🌙</button>
    </div>
    <input class="search" id="search" type="search" placeholder="筛选文档标题 / 关键词…">
    <nav id="docTree"></nav>
    <div class="side-foot">__STATS__<br>生成于 __STAMP__ · 改 md 后重跑 build_library.py</div>
  </aside>

  <main class="main">
    <div class="crumbs" id="crumbs"></div>
    <div class="art-head">
      <div class="art-actions">
        <span class="cat" id="artCat"></span>
        <button class="copy-btn" id="copyPage" type="button">📋 复制页面</button>
      </div>
      <h1 class="art-title" id="artTitle"></h1>
      <div class="art-desc" id="artDesc" style="display:none"></div>
    </div>
    <div class="md" id="article"></div>
  </main>

  <aside class="toc">
    <div class="tl">☰ 在此页面</div>
    <nav id="tocList"></nav>
  </aside>
</div>
<div id="toast"></div>

<script>
const GROUPS=JSON.parse(document.getElementById('library-data').textContent);
const $=id=>document.getElementById(id);
let cur=null;

/* ---------- 主题（与 doc.html 同色系，独立记忆键） ---------- */
function applyTheme(t){document.documentElement.dataset.theme=t;
  const icon=t==='light'?'🌙':'☀️';
  $('themeToggle').textContent=icon;$('themeToggleM').textContent=icon;
  try{localStorage.setItem('aidoc-lib-theme',t);}catch(e){}}
$('themeToggle').onclick=$('themeToggleM').onclick=()=>applyTheme(document.documentElement.dataset.theme==='light'?'dark':'light');
applyTheme(localStorage.getItem('aidoc-lib-theme')||'dark');

/* ---------- 侧栏文库树 ---------- */
function renderTree(filter){
  const q=(filter||'').trim().toLowerCase();
  const tree=$('docTree');tree.innerHTML='';
  GROUPS.forEach((g,gi)=>{
    const items=g.items.filter(d=>!q||(d.t+' '+d.d+' '+d.p).toLowerCase().includes(q));
    if(!items.length)return;
    const wrap=document.createElement('div');wrap.className='group';
    wrap.innerHTML=`<div class="gl">${g.g}</div>`;
    items.forEach(d=>{
      const b=document.createElement('button');b.className='item'+(cur===d.p?' on':'');b.type='button';
      b.innerHTML=d.t+`<span class="hint">　${d.p.split('/').pop()}</span>`;
      b.title=d.t+'\n'+d.p;
      b.onclick=()=>{openDoc(d.p);closeMobile();};
      wrap.appendChild(b);});
    tree.appendChild(wrap);});
}
$('search').addEventListener('input',e=>renderTree(e.target.value));

/* ---------- Markdown 渲染 ---------- */
function renderMarkdown(d){
  const box=$('article');
  if(typeof marked==='undefined'){box.innerHTML='<div class="raw-fallback"></div>';
    box.firstChild.textContent=d.raw;return [];}
  box.innerHTML=marked.parse(d.raw,{gfm:true,breaks:false});
  const h1=box.querySelector('h1');if(h1)h1.remove();          /* 标题已在文章头展示 */
  box.querySelectorAll('img').forEach(im=>im.onerror=()=>{
    const s=document.createElement('span');s.style.cssText='color:var(--txt3);font-size:12px;font-family:var(--mono)';
    s.textContent='［图片未随文库内联：'+im.getAttribute('src')+'］';im.replaceWith(s);});
  if(window.hljs)box.querySelectorAll('pre code').forEach(c=>{try{hljs.highlightElement(c);}catch(e){}});
  const heads=[];
  box.querySelectorAll('h2,h3,h4').forEach((h,i)=>{
    h.id='sec-'+i;heads.push({level:+h.tagName[1],text:h.textContent,id:h.id});});
  return heads;
}

/* ---------- 打开文档 ---------- */
function openDoc(path,keepHash){
  const d=GROUPS.flatMap(g=>g.items).find(x=>x.p===path);
  if(!d){toast('文库中未收录：'+path);return;}
  cur=path;
  $('crumbs').textContent=path;
  $('artCat').textContent=GROUPS.find(g=>g.items.includes(d)).g;
  $('artTitle').textContent=d.t;
  const de=$('artDesc');
  if(d.d){de.style.display='';de.textContent=d.d;}else de.style.display='none';
  const heads=renderMarkdown(d);
  const tl=$('tocList');tl.innerHTML=heads.map(h=>
    `<a href="#${h.id}" class="lv${h.level}" data-id="${h.id}">${h.text}</a>`).join('');
  renderTree($('search').value);
  if(!keepHash){try{location.hash='#/p='+encodeURIComponent(path);}catch(e){}}
  window.scrollTo({top:0,behavior:'auto'});
}

/* ---------- 滚动高亮"在此页面" ---------- */
let spyLock=false;
function spy(){
  if(spyLock)return;
  const heads=document.querySelectorAll('#article h2[id],#article h3[id],#article h4[id]');
  let curId='';
  heads.forEach(h=>{if(h.getBoundingClientRect().top<=120)curId=h.id;});
  document.querySelectorAll('#tocList a').forEach(a=>a.classList.toggle('on',a.dataset.id===curId));
}
addEventListener('scroll',()=>{spy();clearTimeout(window.__spyT);window.__spyT=setTimeout(spy,140);},{passive:true});
$('tocList').addEventListener('click',e=>{
  const a=e.target.closest('a');if(!a)return;e.preventDefault();spyLock=true;
  const el=document.getElementById(a.dataset.id);
  if(el)el.scrollIntoView({behavior:'smooth',block:'start'});
  setTimeout(()=>spyLock=false,800);});

/* ---------- 复制页面（原文 Markdown） ---------- */
function copyText(txt,btn){
  const done=()=>{if(btn){const o=btn.textContent;btn.textContent='✓ 已复制';
    setTimeout(()=>btn.textContent=o,1500);}toast('已复制整页 Markdown');};
  if(navigator.clipboard&&navigator.clipboard.writeText)
    navigator.clipboard.writeText(txt).then(done,()=>fallback());
  else fallback();
  function fallback(){const ta=document.createElement('textarea');ta.value=txt;
    document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done();}catch(e){toast('复制失败，请手动选择');}
    ta.remove();}
}
$('copyPage').onclick=()=>{const d=GROUPS.flatMap(g=>g.items).find(x=>x.p===cur);
  if(d)copyText(d.raw,$('copyPage'));};

/* ---------- 文库内 .md 互链跳转 ---------- */
document.addEventListener('click',e=>{
  const a=e.target.closest('.md a[href]');if(!a)return;
  const href=a.getAttribute('href');
  if(/^(https?:|#|mailto:)/i.test(href))return;
  e.preventDefault();
  const all=GROUPS.flatMap(g=>g.items).map(x=>x.p);
  const hit=all.find(p=>p.endsWith(href.split('/').pop()))||
             all.find(p=>p.replace(/\\/g,'/').endsWith(href));
  if(hit)openDoc(hit);else toast('文库内未收录该链接：'+href);
});

/* ---------- 移动端侧栏 ---------- */
function closeMobile(){$('sidebar').classList.remove('open');$('backdrop').classList.remove('show');}
$('mMenu').onclick=()=>{$('sidebar').classList.add('open');$('backdrop').classList.add('show');};
$('backdrop').onclick=closeMobile;

/* ---------- Toast ---------- */
let toastTimer;
function toast(msg){const t=$('toast');t.textContent=msg;t.classList.add('show');
  clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),1800);}

/* ---------- 启动（支持 #/p=<路径> 深链） ---------- */
(function(){
  let target=GROUPS[0].items[0].p;
  const m=location.hash.match(/^#\/p=(.+)$/);
  if(m){const want=decodeURIComponent(m[1]);
    if(GROUPS.some(g=>g.items.some(x=>x.p===want)))target=want;}
  openDoc(target,true);
  addEventListener('hashchange',()=>{
    const mm=location.hash.match(/^#\/p=(.+)$/);
    if(mm){const want=decodeURIComponent(mm[1]);
      if(want!==cur&&GROUPS.some(g=>g.items.some(x=>x.p===want)))openDoc(want,true);}});
  spy();
})();
</script>
</body>
</html>
"""
if __name__ == "__main__":
    build()
