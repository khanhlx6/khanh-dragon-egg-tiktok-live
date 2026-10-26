// SERVIDOR PARA EL JUEGO "EL HUEVO ANCESTRAL" (huevo-dragon.html)
// Instalar (una vez):  npm i express cors tiktok-live-connector
// Ejecutar:            node serverhuevo.js
// Juego en directo:    http://localhost:3001/huevo-dragon.html   (con ?test salen los botones de prueba)
// (usa el puerto 3001 para que pueda funcionar a la vez que server.js de la arena, que usa el 3000)
const express = require('express');
const cors = require('cors');
const { TikTokLiveConnection, WebcastEvent, ControlEvent } = require('tiktok-live-connector');

const USUARIO = 'tu_usuario'; // <- pon aquí el @ de tu live, sin la @
const PUERTO = 3001;

const app = express();
app.use(cors());
app.use(express.static(__dirname)); // sirve huevo-dragon.html

// ---- Canal de eventos para el juego ----
const jugadores = new Set();
app.get('/juego', (req, res) => {
  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
  res.flushHeaders();
  res.write(': conectado\n\n');
  jugadores.add(res);
  console.log('Juego conectado (' + jugadores.size + ')');
  req.on('close', () => jugadores.delete(res));
});
setInterval(() => jugadores.forEach((c) => c.write(': ping\n\n')), 15000);
function enviarJuego(msg) {
  const data = `data: ${JSON.stringify(msg)}\n\n`;
  jugadores.forEach((c) => c.write(data));
}

// ---- Fotos de perfil (pasan por aquí para que el juego pueda pintarlas en la bola) ----
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

// ---- Prueba: abre http://localhost:3000/juego-test con el juego abierto ----
app.get('/juego-test', (req, res) => {
  for (let i = 0; i < 20; i++) setTimeout(() => enviarJuego({ type: 'like', user: ['Ana', 'Leo', 'Sofi', 'Max', 'Luna'][i % 5], count: 5 }), i * 150);
  setTimeout(() => enviarJuego({ type: 'gift', user: 'Ana', gift: 'Rosa', diamonds: 1 }), 3200);
  setTimeout(() => enviarJuego({ type: 'gift', user: 'Leo', gift: 'Rosquilla', diamonds: 30 }), 4000);
  setTimeout(() => enviarJuego({ type: 'follow', user: 'Sofi' }), 4800);
  res.send('Enviados likes, 2 regalos y un seguidor al huevo. Mira el juego.');
});

// ---- Conexión con el live de TikTok (se reconecta sola) ----
const nombreDe = (d) => d.user?.nickname || d.user?.uniqueId || 'alguien';
const saludados = new Set();
let tiktok = null;

function conectar() {
  tiktok = new TikTokLiveConnection(USUARIO, {});

  tiktok.on(WebcastEvent.CHAT, (d) => {
    enviarJuego({ type: 'chat', user: nombreDe(d), avatar: avatarDe(d.user) });
  });

  // Regalos en racha: se cuentan al terminar la racha, con el total de monedas
  tiktok.on(WebcastEvent.GIFT, (d) => {
    if (d.giftDetails?.giftType === 1 && !d.repeatEnd) return;
    const veces = d.repeatCount || 1;
    const regalo = d.giftDetails?.giftName || 'regalo';
    const monedas = (d.giftDetails?.diamondCount || d.diamondCount || 1) * veces;
    console.log('REGALO:', nombreDe(d), '->', regalo, 'x' + veces, '(' + monedas + ' monedas)');
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
    console.log('Desconectado del live, reintento en 10 s');
    reintentar();
  });
  tiktok.on(ControlEvent.ERROR, (e) => console.log('Aviso:', e?.info || e?.exception?.message || e));

  tiktok.connect()
    .then(() => console.log('Conectado al live de @' + USUARIO))
    .catch((err) => {
      console.log('No se pudo conectar (¿estás en directo?):', err?.message || err, '-> reintento en 10 s');
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
  console.log('Huevo en directo: http://localhost:' + PUERTO + '/huevo-dragon.html');
  console.log('Huevo con botones de prueba: http://localhost:' + PUERTO + '/huevo-dragon.html?test');
  console.log('Prueba eventos:   http://localhost:' + PUERTO + '/juego-test');
});
