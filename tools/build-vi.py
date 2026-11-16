# -*- coding: utf-8 -*-
"""
Sinh các bản tiếng Việt từ bản gốc (tiếng Tây Ban Nha) của tác giả Belumoka.

  huevo-dragon.html            -> vi/huevo-dragon.html
  serverhuevo.js               -> vi/serverhuevo.js
  package.json                 -> vi/package.json
  README.md                    -> README.vi.md

Bản gốc KHÔNG BAO GIỜ bị sửa để sau này còn đồng bộ (merge) bản fork từ tác giả.
Chạy lại sau mỗi lần merge upstream:

  python3 tools/build-vi.py

Mỗi phép thay thế đều được kiểm tra: nếu chuỗi gốc không còn trong file thì script
báo lỗi và dừng, nhờ vậy ta biết ngay tác giả đã đổi đoạn nào cần dịch lại.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sub(text, old, new, label, count=1):
    """Thay thế chính xác `old` -> `new`, báo lỗi nếu không tìm thấy."""
    found = text.count(old)
    if found != count:
        raise SystemExit(
            f"[LỖI] '{label}': cần {count} chỗ xuất hiện nhưng thấy {found}.\n"
            f"       Chuỗi gốc: {old[:120]!r}\n"
            f"       Có thể tác giả đã sửa đoạn này, hãy cập nhật tools/build-vi.py"
        )
    return text.replace(old, new)


# ---------------------------------------------------------------------------
# 1) GAME: huevo-dragon.html -> vi/huevo-dragon.html
# ---------------------------------------------------------------------------
html = (ROOT / "huevo-dragon.html").read_text(encoding="utf-8")

HTML_MAP = [
    # <head>
    ('<html lang="es">', '<html lang="vi">', "lang"),
    ("<title>El Huevo Ancestral – Live</title>",
     "<title>Trứng Rồng Cổ Đại – Live</title>", "title"),
    # giao diện trong khung
    ('<span id="st">INCUBANDO</span>', '<span id="st">ĐANG ẤP</span>', "hud st"),
    ('<div class="hint">❤️ LIKES = CALOR · 🎁 REGALOS = ELEMENTO DEL DRAGÓN · ➕ FOLLOW = LUZ</div>',
     '<div class="hint">❤️ LIKE = NHIỆT · 🎁 QUÀ TẶNG = HỆ CỦA RỒNG · ➕ THEO DÕI = ÁNH SÁNG</div>',
     "hint"),
    ('<div class="start" id="start"><h1>EL HUEVO<br>ANCESTRAL</h1><p>TOCA PARA DESPERTARLO</p></div>',
     '<div class="start" id="start"><h1>TRỨNG RỒNG<br>CỔ ĐẠI</h1><p>CHẠM ĐỂ ĐÁNH THỨC</p></div>',
     "start screen"),
    # xuất hiện 2 lần: thẻ HTML và chuỗi trong board() của JS
    ('<h2>👑 PADRES</h2>', '<h2>👑 BẬC SINH THÀNH</h2>', "card padres", 2),
    ('<h2>⚡ EN VIVO</h2>', '<h2>⚡ TRỰC TIẾP</h2>', "card en vivo"),
    ('<h2>📜 COLECCIÓN DE DRAGONES</h2>', '<h2>📜 BỘ SƯU TẬP RỒNG</h2>', "card colección"),
    ('>Aún no ha nacido ninguno…<', '>Chưa có chú rồng nào ra đời…<', "colección vacía"),
    # nút thử nghiệm (?test)
    ('>❤️ LIKES</button>', '>❤️ LIKE</button>', "btn likes"),
    ('>🔥 FUEGO</button>', '>🔥 LỬA</button>', "btn fuego"),
    ('>❄️ HIELO</button>', '>❄️ BĂNG</button>', "btn hielo"),
    ('>⚡ RAYO</button>', '>⚡ SẤM SÉT</button>', "btn rayo"),
    ('>☣️ VENENO</button>', '>☣️ ĐỘC DƯỢC</button>', "btn veneno"),
    ('>✨ LUZ x30</button>', '>✨ ÁNH SÁNG x30</button>', "btn luz"),
    ('>➕ FOLLOW</button>', '>➕ THEO DÕI</button>', "btn follow"),
    ('>🤖 AUTO</button>', '>🤖 TỰ ĐỘNG</button>', "btn auto"),
    ('>🔊 SONIDO</button>', '>🔊 ÂM THANH</button>', "btn sonido"),
    ('<div class="s">❤️ Los likes calientan el huevo · 🎁 Cada regalo añade un elemento y decide qué dragón nace (¡y su rareza!) · ➕ Follow = Luz · Arrastra para girar la cámara, toca para dar calor</div>',
     '<div class="s">❤️ Like làm nóng quả trứng · 🎁 Mỗi món quà thêm một hệ và quyết định chú rồng nào ra đời (kèm độ hiếm!) · ➕ Theo dõi = Ánh sáng · Kéo để xoay camera, chạm để sưởi ấm</div>',
     "dòng trợ giúp dưới cùng"),
    # chú thích JS
    ("// modo directo siempre; con ?test salen los botones de prueba",
     "// luôn ở chế độ phát trực tiếp; thêm ?test để hiện các nút thử nghiệm"),
    ("// en directo la imagen sube un poco para que el huevo no quede detrás del chat de TikTok (ajustable con &y=0.1)",
     "// khi lên sóng, hình được đẩy lên một chút để trứng không bị khung chat TikTok che (chỉnh bằng &y=0.1)"),
    ("// ---------- escena ----------", "// ---------- cảnh ----------"),
    ("// altar y ruinas", "// bàn thờ và phế tích"),
    ("// huevo\nconst eg=new THREE.SphereGeometry", "// quả trứng\nconst eg=new THREE.SphereGeometry"),
    ("// partículas", "// hạt sáng"),
    ("// ---------- estado ----------", "// ---------- trạng thái ----------"),
    ("  // huevo\n  if(egg.visible)", "  // quả trứng\n  if(egg.visible)"),
    ("// ---------- dragón procedural ----------", "// ---------- rồng sinh tự động ----------"),
    ("// ---------- eventos ----------", "// ---------- sự kiện ----------"),
    ("// ---------- máquina de estados ----------", "// ---------- máy trạng thái ----------"),
    ("if(LIVE)startGame(); // en directo arranca solo",
     "if(LIVE)startGame(); // khi lên sóng thì tự chạy"),
    # dữ liệu: hệ nguyên tố, độ hiếm
    ("const E=[{n:'FUEGO'", "const E=[{n:'LỬA'", "E fuego"),
    ("{n:'HIELO'", "{n:'BĂNG'", "E hielo"),
    ("{n:'RAYO'", "{n:'SẤM SÉT'", "E rayo"),
    ("{n:'VENENO'", "{n:'ĐỘC DƯỢC'", "E veneno"),
    ("{n:'LUZ'", "{n:'ÁNH SÁNG'", "E luz"),
    ("{n:'COMÚN'", "{n:'THƯỜNG'", "RAR común"),
    ("{n:'RARO'", "{n:'HIẾM'", "RAR raro"),
    ("{n:'ÉPICO'", "{n:'SỬ THI'", "RAR épico"),
    ("{n:'LEGENDARIO'", "{n:'HUYỀN THOẠI'", "RAR legendario"),
    ("{n:'MÍTICO'", "{n:'THẦN THOẠI'", "RAR mítico"),
    # chuỗi động
    ("$('snd').textContent=mute?'🔇 SONIDO':'🔊 SONIDO'",
     "$('snd').textContent=mute?'🔇 ÂM THANH':'🔊 ÂM THANH'", "toggle sonido"),
    ('<li style="opacity:.5">VACÍO…</li>', '<li style="opacity:.5">TRỐNG…</li>', "bảng trống"),
    ("String(e.user||'Anónimo')", "String(e.user||'Ẩn danh')", "usuario anónimo"),
    ("say(E[el].i+' ESENCIA DE '+E[el].n+' · '+u)",
     "say(E[el].i+' TINH CHẤT '+E[el].n+' · '+u)", "say esencia"),
    ("say('✨ '+u+' AÑADE LUZ')", "say('✨ '+u+' THÊM ÁNH SÁNG')", "say follow"),
    ("log('➕ '+esc(u)+' siguió')", "log('➕ '+esc(u)+' đã theo dõi')", "log follow"),
    ("gift:'Regalo'", "gift:'Quà tặng'", "regalo simulador", 2),
    ("$('auto').textContent='🤖 AUTO'", "$('auto').textContent='🤖 TỰ ĐỘNG'", "auto off"),
    ("$('auto').textContent='⏹ PARAR'", "$('auto').textContent='⏹ DỪNG'", "auto on"),
    ("father:o[0]?o[0][0]:'el Destino'", "father:o[0]?o[0][0]:'Định Mệnh'", "padre destino"),
    ("' · Criado por '+esc(d.father)", "' · Được ấp bởi '+esc(d.father)", "reveal criado por"),
    ("say('🥚 UN NUEVO HUEVO SE FORMA')", "say('🥚 MỘT QUẢ TRỨNG MỚI ĐANG THÀNH HÌNH')",
     "say huevo nuevo"),
    ("st==='egg'?'🥚 INCUBANDO':st==='hatch'?'⚡ ¡ECLOSIÓN!':st==='show'&&G.dragon?'🐉 '+G.dragon.name.toUpperCase():'🥚 PRÓXIMO HUEVO'",
     "st==='egg'?'🥚 ĐANG ẤP':st==='hatch'?'⚡ NỞ RỒI!':st==='show'&&G.dragon?'🐉 '+G.dragon.name.toUpperCase():'🥚 TRỨNG KẾ TIẾP'",
     "hud estados"),
    ("say('✨ EL HUEVO ANCESTRAL DESPIERTA')", "say('✨ TRỨNG RỒNG CỔ ĐẠI THỨC GIẤC')",
     "say despierta"),
    ("log('🟢 Conectado al live')", "log('🟢 Đã kết nối với live')", "log conectado"),
    ("log('🔴 Sin conexión, reintentando…')", "log('🔴 Mất kết nối, đang thử lại…')",
     "log desconectado"),
    ("/* modo directo (TikTok LIVE Studio / OBS): pantalla completa 9:16 y nada que tape las zonas de TikTok */",
     "/* chế độ phát trực tiếp (TikTok LIVE Studio / OBS): toàn màn hình 9:16, không che vùng giao diện của TikTok */",
     "css live"),
    ("/* todo lo demás abajo del todo, para que el huevo se vea entero */",
     "/* mọi thứ khác dồn xuống dưới cùng để nhìn thấy trọn quả trứng */",
     "css abajo"),
]

vi = html
for item in HTML_MAP:
    old, new = item[0], item[1]
    label = item[2] if len(item) > 2 else old[:40]
    times = item[3] if len(item) > 3 else 1
    vi = sub(vi, old, new, label, times)

# ghi chú đầu file cho người đọc biết đây là bản dịch
vi = sub(
    vi,
    '<!DOCTYPE html>\n<html lang="vi">',
    '<!DOCTYPE html>\n<!--\n'
    '  BẢN DỊCH TIẾNG VIỆT – được tạo tự động từ huevo-dragon.html (bản gốc tiếng Tây Ban Nha của Belumoka).\n'
    '  Đừng sửa tay file này: hãy sửa tools/build-vi.py rồi chạy:  python3 tools/build-vi.py\n'
    '  Bản gốc luôn được giữ nguyên để đồng bộ (merge) các bản cập nhật từ tác giả.\n'
    '-->\n<html lang="vi">',
    "chú thích đầu file",
)

# kiểm tra không còn chuỗi tiếng Tây Ban Nha đáng ngờ trong phần giao diện
leftovers = []
for pat in ("INCUBANDO", "PADRES", "Añad", "añad", "siguió", "Criado", "DESPIERTA",
            "HUEVO", "NUEVO", "PARAR", "SONIDO", "VACÍO", "Aún no", "Anónimo",
            "FUEGO", "HIELO", "VENENO", "COMÚN", "ÉPICO", "MÍTICO", "REGALO"):
    for m in re.finditer(re.escape(pat), vi):
        line = vi[: m.start()].count("\n") + 1
        leftovers.append(f"  dòng {line}: {pat}")
if leftovers:
    print("[CẢNH BÁO] còn chuỗi tiếng Tây Ban Nha trong bản dịch:")
    print("\n".join(leftovers))

(ROOT / "vi").mkdir(exist_ok=True)
(ROOT / "vi" / "huevo-dragon.html").write_text(vi, encoding="utf-8")
print("✔ vi/huevo-dragon.html")


# ---------------------------------------------------------------------------
# 2) SERVIDOR: serverhuevo.js -> vi/serverhuevo.js
# ---------------------------------------------------------------------------
js = (ROOT / "serverhuevo.js").read_text(encoding="utf-8")

JS_MAP = [
    ('// SERVIDOR PARA EL JUEGO "EL HUEVO ANCESTRAL" (huevo-dragon.html)',
     '// MÁY CHỦ CHO GAME "TRỨNG RỒNG CỔ ĐẠI" (huevo-dragon.html)\n'
     '// BẢN DỊCH TIẾNG VIỆT – tạo tự động từ serverhuevo.js bằng tools/build-vi.py (đừng sửa tay)'),
    ("// Instalar (una vez):  npm i express cors tiktok-live-connector",
     "// Cài đặt (một lần):    npm i express cors tiktok-live-connector"),
    ("// Ejecutar:            node serverhuevo.js",
     "// Chạy:                 node serverhuevo.js   (hoặc: npm start trong thư mục này)"),
    ("// Juego en directo:    http://localhost:3001/huevo-dragon.html   (con ?test salen los botones de prueba)",
     "// Game khi lên sóng:    http://localhost:3001/huevo-dragon.html   (thêm ?test để hiện nút thử nghiệm)"),
    ("// (usa el puerto 3001 para que pueda funcionar a la vez que server.js de la arena, que usa el 3000)",
     "// (dùng cổng 3001 để có thể chạy song song với server.js của arena, vốn dùng cổng 3000)"),
    ("const USUARIO = 'tu_usuario'; // <- pon aquí el @ de tu live, sin la @",
     "const USUARIO = 'ten_tai_khoan'; // <- điền tên tài khoản TikTok của bạn, KHÔNG kèm dấu @"),
    ("app.use(express.static(__dirname)); // sirve huevo-dragon.html",
     "app.use(express.static(__dirname)); // phục vụ huevo-dragon.html"),
    ("// ---- Canal de eventos para el juego ----",
     "// ---- Kênh sự kiện (SSE) cho game ----"),
    ("res.write(': conectado\\n\\n');", "res.write(': da ket noi\\n\\n');"),
    ("console.log('Juego conectado (' + jugadores.size + ')');",
     "console.log('Game đã kết nối (' + jugadores.size + ')');"),
    ("// ---- Fotos de perfil (pasan por aquí para que el juego pueda pintarlas en la bola) ----",
     "// ---- Ảnh đại diện (đi qua đây để game vẽ được vào quả cầu) ----"),
    ("// ---- Prueba: abre http://localhost:3000/juego-test con el juego abierto ----",
     "// ---- Thử nghiệm: mở http://localhost:3001/juego-test khi game đang mở ----"),
    ("setTimeout(() => enviarJuego({ type: 'gift', user: 'Ana', gift: 'Rosa', diamonds: 1 }), 3200);",
     "setTimeout(() => enviarJuego({ type: 'gift', user: 'Ana', gift: 'Hoa hồng', diamonds: 1 }), 3200);"),
    ("setTimeout(() => enviarJuego({ type: 'gift', user: 'Leo', gift: 'Rosquilla', diamonds: 30 }), 4000);",
     "setTimeout(() => enviarJuego({ type: 'gift', user: 'Leo', gift: 'Bánh vòng', diamonds: 30 }), 4000);"),
    ("res.send('Enviados likes, 2 regalos y un seguidor al huevo. Mira el juego.');",
     "res.send('Đã gửi like, 2 món quà và một người theo dõi tới quả trứng. Xem game đi!');"),
    ("// ---- Conexión con el live de TikTok (se reconecta sola) ----",
     "// ---- Kết nối tới live TikTok (tự động kết nối lại) ----"),
    ("const nombreDe = (d) => d.user?.nickname || d.user?.uniqueId || 'alguien';",
     "const nombreDe = (d) => d.user?.nickname || d.user?.uniqueId || 'ai đó';"),
    ("// Regalos en racha: se cuentan al terminar la racha, con el total de monedas",
     "// Quà tặng liên tiếp (combo): chỉ tính khi combo kết thúc, theo tổng số xu"),
    ("const regalo = d.giftDetails?.giftName || 'regalo';",
     "const regalo = d.giftDetails?.giftName || 'quà tặng';"),
    ("console.log('REGALO:', nombreDe(d), '->', regalo, 'x' + veces, '(' + monedas + ' monedas)');",
     "console.log('QUÀ TẶNG:', nombreDe(d), '->', regalo, 'x' + veces, '(' + monedas + ' xu)');"),
    ("console.log('Desconectado del live, reintento en 10 s');",
     "console.log('Đã ngắt kết nối live, thử lại sau 10 giây');"),
    ("tiktok.on(ControlEvent.ERROR, (e) => console.log('Aviso:', e?.info || e?.exception?.message || e));",
     "tiktok.on(ControlEvent.ERROR, (e) => console.log('Cảnh báo:', e?.info || e?.exception?.message || e));"),
    (".then(() => console.log('Conectado al live de @' + USUARIO))",
     ".then(() => console.log('Đã kết nối tới live của @' + USUARIO))"),
    ("console.log('No se pudo conectar (¿estás en directo?):', err?.message || err, '-> reintento en 10 s');",
     "console.log('Không kết nối được (bạn đã lên sóng chưa?):', err?.message || err, '-> thử lại sau 10 giây');"),
    ("console.log('Huevo en directo: http://localhost:' + PUERTO + '/huevo-dragon.html');",
     "console.log('Trứng Rồng đang lên sóng: http://localhost:' + PUERTO + '/huevo-dragon.html');"),
    ("console.log('Huevo con botones de prueba: http://localhost:' + PUERTO + '/huevo-dragon.html?test');",
     "console.log('Trứng Rồng kèm nút thử nghiệm: http://localhost:' + PUERTO + '/huevo-dragon.html?test');"),
    ("console.log('Prueba eventos:   http://localhost:' + PUERTO + '/juego-test');",
     "console.log('Gửi thử sự kiện:  http://localhost:' + PUERTO + '/juego-test');"),
]

vijs = js
for item in JS_MAP:
    old, new = item[0], item[1]
    label = item[2] if len(item) > 2 else old[:50]
    vijs = sub(vijs, old, new, label)

(ROOT / "vi" / "serverhuevo.js").write_text(vijs, encoding="utf-8")
print("✔ vi/serverhuevo.js")


# ---------------------------------------------------------------------------
# 3) PACKAGE: package.json -> vi/package.json
#    (chỉ dịch phần mô tả, giữ nguyên tên/phiên bản/khai báo phụ thuộc)
# ---------------------------------------------------------------------------
pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
vi_pkg = dict(pkg)
vi_pkg["description"] = (
    "Game tương tác 3D cho TikTok LIVE: khán giả cùng ấp một quả trứng rồng "
    "bằng like và quà tặng. (Bản dịch tiếng Việt, tạo tự động bằng tools/build-vi.py)"
)
vi_pkg["author"] = pkg["author"]  # giữ nguyên tác giả gốc
(ROOT / "vi" / "package.json").write_text(
    json.dumps(vi_pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("✔ vi/package.json")
