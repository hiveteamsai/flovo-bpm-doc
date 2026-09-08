#!/usr/bin/env python3
"""bpmEngine/todo.md bakımı — kapanan (`- [x]`) ÜST-DÜZEY maddeleri açık listelerden alır ve dosyanın altındaki
"📦 Tier listelerinden konsolide edilen çözülmüş maddeler" bölümüne taşır. Idempotent; taşınacak madde yoksa sessiz çıkar.
Claude Code hook'u (PostToolUse · SessionStart) olarak çalışır; `--dry-run` ile yalnız önizler."""
import io, json, os, re, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
PATH = os.path.join(ROOT, "bpmEngine", "todo.md")
LOG_HDR = "## ✅ Bu oturumda çözülen tutarsızlıklar (log)"
TARGET_HDR = "### 📦 Tier listelerinden konsolide edilen çözülmüş maddeler"
PLACEHOLDER = "_(açık madde yok — kapananlar alt bölümde: ✅ → 📦 konsolide edilen çözülmüş maddeler)_"
DRY = "--dry-run" in sys.argv

def short_section(title):
    m = re.search(r"Tier \d", title)
    if m: return m.group(0)
    t = re.sub(r"[^\w\sğüşıöçĞÜŞİÖÇ'’/-]", "", title).strip()
    return t[:40]

def fill_empty_sections(lines):
    out, i = [], 0
    while i < len(lines):
        l = lines[i]; out.append(l)
        if l.startswith("## "):
            j = i + 1
            while j < len(lines) and not (lines[j].startswith("## ") or lines[j].startswith("---")): j += 1
            body = lines[i+1:j]
            if not any(b.startswith("- ") for b in body) and not any(PLACEHOLDER in b for b in body):
                k = i + 1
                while k < j and lines[k].strip() == "": k += 1
                out += ["", PLACEHOLDER, ""]; i = k; continue
        i += 1
    return out

def main():
    if not os.path.isfile(PATH): return 0
    payload = {}
    if not sys.stdin.isatty():
        try: payload = json.load(sys.stdin)
        except Exception: payload = {}
    event = payload.get("hook_event_name", "")
    text = io.open(PATH, encoding="utf-8").read()
    lines = text.split("\n")
    log_idx = next((i for i, l in enumerate(lines) if l.startswith(LOG_HDR)), None)
    open_end = log_idx if log_idx is not None else len(lines)
    moved, out, i, section = [], [], 0, ""
    while i < open_end:
        l = lines[i]
        if l.startswith("## "): section = l[3:].strip()
        if l.startswith("- [x]"):
            j = i + 1
            while j < open_end and lines[j].startswith("  "): j += 1
            block = list(lines[i:j])
            first = "- " + block[0][5:].lstrip()
            if "_(← " not in first: first += f" _(← {short_section(section)})_"
            block[0] = first
            moved.append(block); i = j; continue
        out.append(l); i += 1
    if not moved: return 0
    out = fill_empty_sections(out)
    rest = lines[open_end:]
    if log_idx is None:
        rest = ["---", "", LOG_HDR, ""]
    t_idx = next((k for k, l in enumerate(rest) if l.startswith(TARGET_HDR)), None)
    if t_idx is None:
        while rest and rest[-1].strip() == "": rest.pop()
        rest += ["", TARGET_HDR, "> `[x]` işaretlenen üst-düzey maddeler hook ile (`.claude/hooks/todo-archive-closed.py`) otomatik buraya taşınır."]
        t_idx = len(rest) - 2
    t_end = t_idx + 1
    while t_end < len(rest) and not (rest[t_end].startswith("## ") or rest[t_end].startswith("### ") or rest[t_end].startswith("---")): t_end += 1
    ins = t_end
    while ins > t_idx + 1 and rest[ins - 1].strip() == "": ins -= 1
    body = []
    for b in moved: body += b
    tail = rest[ins:]
    rest = rest[:ins] + body + ([""] if tail and tail[0].strip() != "" else []) + tail
    new = "\n".join(out + rest).rstrip("\n") + "\n"
    titles = []
    for b in moved:
        m = re.search(r"\*\*(.+?)\*\*", b[0]); titles.append(m.group(1) if m else b[0][:60])
    msg = f"todo-archive: {len(moved)} kapanan madde alt bölüme (📦) taşındı → " + " · ".join(titles)
    if DRY:
        print("[dry-run] " + msg); return 0
    io.open(PATH, "w", encoding="utf-8").write(new)
    if event:
        print(json.dumps({"systemMessage": msg, "hookSpecificOutput": {"hookEventName": event, "additionalContext": msg}}, ensure_ascii=False))
    else:
        print(msg)
    return 0

if __name__ == "__main__":
    sys.exit(main())
