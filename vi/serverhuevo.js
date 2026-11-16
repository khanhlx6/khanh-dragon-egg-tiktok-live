// MÁY CHỦ CHO GAME "TRỨNG RỒNG CỔ ĐẠI" (huevo-dragon.html)
// BẢN DỊCH TIẾNG VIỆT – tạo tự động từ serverhuevo.js bằng tools/build-vi.py (đừng sửa tay)
// Cài đặt (một lần):    npm i express cors tiktok-live-connector
// Chạy:                 node serverhuevo.js   (hoặc: npm start trong thư mục này)
// Game khi lên sóng:    http://localhost:3001/huevo-dragon.html   (thêm ?test để hiện nút thử nghiệm)
// (dùng cổng 3001 để có thể chạy song song với server.js của arena, vốn dùng cổng 3000)
const express = require('express');
const cors = require('cors');
const { TikTokLiveConnection, WebcastEvent, ControlEvent } = require('tiktok-live-connector');

const USUARIO = 'ten_tai_khoan'; // <- điền tên tài khoản TikTok của bạn, KHÔNG kèm dấu @
const PUERTO = 3001;

const app = express();
app.use(cors());
app.use(express.static(__dirname)); // phục vụ huevo-dragon.html

// ---- Kênh sự kiện (SSE) cho game ----
const jugadores = new Set();
app.get('/juego', (req, res) => {
  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
  res.flushHeaders();
  res.write(': da ket noi\n\n');
  jugadores.add(res);
  console.log('Game đã kết nối (' + jugadores.size + ')');
  req.on('close', () => jugadores.delete(res));
});
setInterval(() => jugadores.forEach((c) => c.write(': ping\n\n')), 15000);
function enviarJuego(msg) {
  const data = `data: ${JSON.stringify(msg)}\n\n`;
  jugadores.forEach((c) => c.write(data));
}

// ---- Ảnh đại diện (đi qua đây để game vẽ được vào quả cầu) ----
function avatarDe(u) {
  const url = u?.profilePictureUrl || u?.profilePicture?.url?.[0] || u?.profilePicture?.urls?.[0]
    || u?.avatarThumb?.urlList?.[0] || u?.avatarThumb?.url?.[0] || '';
  return url ? '/avatar?u=' + encodeURIComponent(url) : '';
}
app.get('/avatar', async (req, res) => {
  try {
    const u = new URL(String(req.query.u || ''));
    if (u.protocol !== 'https:' || !/(tiktokcdn|ibyteimg|byteimg|muscdn)/.test(u.hostname)) return res.sendStatus(400);
    const r = await fetch(u, { signal: AbortSignal.timeout(5000) });
    if (!r.ok) return res.sendStatus(502);
    res.set('Content-Type', r.headers.get('content-type') || 'image/jpeg');
    res.set('Cache-Control', 'public, max-age=86400');
    res.send(Buffer.from(await r.arrayBuffer()));
  } catch { res.sendStatus(404); }
});

// ---- Thử nghiệm: mở http://localhost:3001/juego-test khi game đang mở ----
app.get('/juego-test', (req, res) => {
  for (let i = 0; i < 20; i++) setTimeout(() => enviarJuego({ type: 'like', user: ['Ana', 'Leo', 'Sofi', 'Max', 'Luna'][i % 5], count: 5 }), i * 150);
  setTimeout(() => enviarJuego({ type: 'gift', user: 'Ana', gift: 'Hoa hồng', diamonds: 1 }), 3200);
  setTimeout(() => enviarJuego({ type: 'gift', user: 'Leo', gift: 'Bánh vòng', diamonds: 30 }), 4000);
  setTimeout(() => enviarJuego({ type: 'follow', user: 'Sofi' }), 4800);
  res.send('Đã gửi like, 2 món quà và một người theo dõi tới quả trứng. Xem game đi!');
});

// ---- Kết nối tới live TikTok (tự động kết nối lại) ----
const nombreDe = (d) => d.user?.nickname || d.user?.uniqueId || 'ai đó';
const saludados = new Set();
let tiktok = null;

function conectar() {
  tiktok = new TikTokLiveConnection(USUARIO, {});

  tiktok.on(WebcastEvent.CHAT, (d) => {
    enviarJuego({ type: 'chat', user: nombreDe(d), avatar: avatarDe(d.user) });
  });

  // Quà tặng liên tiếp (combo): chỉ tính khi combo kết thúc, theo tổng số xu
  tiktok.on(WebcastEvent.GIFT, (d) => {
    if (d.giftDetails?.giftType === 1 && !d.repeatEnd) return;
    const veces = d.repeatCount || 1;
    const regalo = d.giftDetails?.giftName || 'quà tặng';
    const monedas = (d.giftDetails?.diamondCount || d.diamondCount || 1) * veces;
    console.log('QUÀ TẶNG:', nombreDe(d), '->', regalo, 'x' + veces, '(' + monedas + ' xu)');
    enviarJuego({ type: 'gift', user: nombreDe(d), gift: regalo, diamonds: monedas, avatar: avatarDe(d.user) });
  });

  tiktok.on(WebcastEvent.LIKE, (d) => {
    enviarJuego({ type: 'like', user: nombreDe(d), count: d.likeCount || 1, avatar: avatarDe(d.user) });
  });

  tiktok.on(WebcastEvent.MEMBER, (d) => {
    const id = d.user?.uniqueId || d.user?.nickname;
    if (!id || saludados.has(id)) return;
    saludados.add(id);
    enviarJuego({ type: 'join', user: nombreDe(d), avatar: avatarDe(d.user) });
  });

  tiktok.on(WebcastEvent.FOLLOW, (d) => {
    enviarJuego({ type: 'follow', user: nombreDe(d), avatar: avatarDe(d.user) });
  });

  if (WebcastEvent.SHARE) {
    tiktok.on(WebcastEvent.SHARE, (d) => {
      enviarJuego({ type: 'share', user: nombreDe(d), avatar: avatarDe(d.user) });
    });
  }

  tiktok.on(ControlEvent.DISCONNECTED, () => {
    console.log('Đã ngắt kết nối live, thử lại sau 10 giây');
    reintentar();
  });
  tiktok.on(ControlEvent.ERROR, (e) => console.log('Cảnh báo:', e?.info || e?.exception?.message || e));

  tiktok.connect()
    .then(() => console.log('Đã kết nối tới live của @' + USUARIO))
    .catch((err) => {
      console.log('Không kết nối được (bạn đã lên sóng chưa?):', err?.message || err, '-> thử lại sau 10 giây');
      reintentar();
    });
}

let esperando = false;
function reintentar() {
  if (esperando) return;
  esperando = true;
  try { tiktok.removeAllListeners(); tiktok.disconnect(); } catch {}
  setTimeout(() => { esperando = false; conectar(); }, 10000);
}

conectar();

app.listen(PUERTO, () => {
  console.log('Trứng Rồng đang lên sóng: http://localhost:' + PUERTO + '/huevo-dragon.html');
  console.log('Trứng Rồng kèm nút thử nghiệm: http://localhost:' + PUERTO + '/huevo-dragon.html?test');
  console.log('Gửi thử sự kiện:  http://localhost:' + PUERTO + '/juego-test');
});
