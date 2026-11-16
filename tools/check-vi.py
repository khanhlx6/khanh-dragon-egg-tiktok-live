# -*- coding: utf-8 -*-
"""
Kiểm tra nhanh các file tiếng Việt trong vi/ (dùng trong CI và khi làm việc local).

  python3 tools/check-vi.py

Kiểm tra:
  1. vi/package.json là JSON hợp lệ và giữ đúng tên / phụ thuộc của bản gốc.
  2. JS trong vi/huevo-dragon.html và vi/serverhuevo.js không lỗi cú pháp
     (dùng `node --check` nếu máy có Node.js).
  3. vi/huevo-dragon.html khai báo <html lang="vi">.
  4. Không còn sót chuỗi giao diện tiếng Tây Ban Nha trong bản dịch
     (dấu hiệu ai đó sửa tay file vi/ thay vì chạy tools/build-vi.py).

Trả về mã 0 nếu mọi thứ ổn, 1 nếu có lỗi.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VI = ROOT / "vi"

loi = []
ok = []


def bao_ok(msg):
    ok.append(msg)


def bao_loi(msg):
    loi.append(msg)


# --- 1) package.json --------------------------------------------------------
try:
    goc = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    vi = json.loads((VI / "package.json").read_text(encoding="utf-8"))
    for khoa in ("name", "version", "main", "dependencies", "scripts"):
        if goc.get(khoa) != vi.get(khoa):
            bao_loi(f"vi/package.json: mục '{khoa}' khác bản gốc "
                    f"({vi.get(khoa)!r} != {goc.get(khoa)!r})")
    else:
        bao_ok("vi/package.json: JSON hợp lệ, khớp name/version/main/dependencies")
except json.JSONDecodeError as e:
    bao_loi(f"vi/package.json: JSON không hợp lệ ({e})")
except OSError as e:
    bao_loi(f"Không đọc được package.json ({e})")


# --- 2) cú pháp JS ----------------------------------------------------------
def check_js(ten, ma):
    if not shutil.which("node"):
        bao_ok(f"{ten}: bỏ qua kiểm tra cú pháp (máy không có node)")
        return
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "check.js"
        f.write_text(ma, encoding="utf-8")
        r = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
        if r.returncode == 0:
            bao_ok(f"{ten}: cú pháp JS hợp lệ")
        else:
            chi_tiet = (r.stderr or r.stdout).strip().splitlines()
            bao_loi(f"{ten}: lỗi cú pháp JS -> {chi_tiet[0] if chi_tiet else 'không rõ'}")


html = VI / "huevo-dragon.html"
if html.exists():
    noi_dung = html.read_text(encoding="utf-8")
    khoi = re.findall(r"<script>(.*?)</script>", noi_dung, re.S)
    if not khoi:
        bao_loi("vi/huevo-dragon.html: không tìm thấy thẻ <script> nào")
    else:
        check_js("vi/huevo-dragon.html", khoi[-1])

    # --- 3) ngôn ngữ --------------------------------------------------------
    if '<html lang="vi">' in noi_dung:
        bao_ok('vi/huevo-dragon.html: khai báo <html lang="vi">')
    else:
        bao_loi('vi/huevo-dragon.html: thiếu <html lang="vi">')

    # --- 4) chuỗi tiếng Tây Ban Nha còn sót ---------------------------------
    SOT = [
        "INCUBANDO", "ECLOSIÓN", "¡ECLOSIÓN!", "PRÓXIMO HUEVO", "NUEVO HUEVO",
        "EL HUEVO ANCESTRAL DESPIERTA", "AÑADE LUZ", "Criado por", "siguió",
        "VACÍO", "Aún no ha nacido", "Anónimo", "ESENCIA DE", "PADRES",
        "COLECCIÓN DE DRAGONES", "TOCA PARA DESPERTARLO", "SONIDO", "PARAR",
        "Los likes calientan", "Los likes", "EN VIVO", "COLLECTION",
        "FUEGO", "HIELO", "VENENO", "COMÚN", "ÉPICO", "LEGENDARIO", "MÍTICO",
        "ESENCIA", "Criado",
    ]
    con_lai = []
    for tu in SOT:
        for m in re.finditer(re.escape(tu), noi_dung):
            dong = noi_dung[: m.start()].count("\n") + 1
            con_lai.append(f"dòng {dong}: {tu}")
    if con_lai:
        bao_loi("vi/huevo-dragon.html: còn chuỗi tiếng Tây Ban Nha -> "
                + "; ".join(con_lai[:8]))
    else:
        bao_ok("vi/huevo-dragon.html: không còn chuỗi giao diện tiếng Tây Ban Nha")
else:
    bao_loi("Thiếu file vi/huevo-dragon.html")

# --- server ---------------------------------------------------------------
server = VI / "serverhuevo.js"
if server.exists():
    check_js("vi/serverhuevo.js", server.read_text(encoding="utf-8"))
else:
    bao_loi("Thiếu file vi/serverhuevo.js")

# --- in kết quả -----------------------------------------------------------
for d in ok:
    print(f"✔ {d}")
for d in loi:
    print(f"✘ {d}", file=sys.stderr)

print()
if loi:
    print(f"THẤT BẠI: {len(loi)} lỗi. Chạy lại: python3 tools/build-vi.py", file=sys.stderr)
    sys.exit(1)
print(f"TẤT CẢ ĐỀU ỔN ({len(ok)} mục kiểm tra).")
