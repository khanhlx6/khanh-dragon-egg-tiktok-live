# 🥚 El Huevo Ancestral – Juego para TikTok LIVE

Juego interactivo en 3D para directos de TikTok: los espectadores calientan entre todos un huevo de dragón con sus **likes**, y con sus **regalos** deciden qué cría nace y lo rara que es.

🌐 Página del juego: **https://belumoka.com/juego-huevo-ancestral-tiktok-live/**

<img width="523" height="801" alt="huevo-ancestral" src="https://github.com/user-attachments/assets/9d70f216-90fd-440b-86cf-08c38fe67dc5" />


## Cómo se juega

| Acción del espectador | Qué pasa en el juego |
| --- | --- |
| ❤️ Like | Calienta el huevo y lanza rayos de luz hacia él. Con el dragón ya nacido, le hace echar fuego. |
| 🎁 Regalo | Añade un elemento al huevo (🔥 fuego, ❄️ hielo, ⚡ rayo, ☣️ veneno o ✨ luz) según el regalo. Cuantas más monedas, más rara será la cría. |
| ➕ Seguir | Añade ✨ luz al huevo. |

Cuando la barra de calor se llena, el huevo se rompe y **nace el dragón**: sale su nombre, su rareza (común, raro, épico, legendario o mítico), sus elementos y quién es el **padre**, el espectador que más ha aportado. Después el dragón vuela un rato, desaparece y se forma un huevo nuevo que necesita algo más de calor.

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| `huevo-dragon.html` | El juego. Es la página que se pone en TikTok LIVE Studio. |
| `serverhuevo.js` | Se conecta a tu live y pasa al juego los likes, regalos y seguidores (puerto 3001). |
| `package.json` | Lista de paquetes que necesita el servidor. |

## Requisitos

- PC con Windows (también funciona en Mac y Linux).
- [Node.js](https://nodejs.org) versión LTS.
- TikTok LIVE Studio (o OBS).
- Conexión a internet.

## Instalación

1. Descarga el proyecto: botón verde **Code → Download ZIP** y descomprímelo.
2. Abre `serverhuevo.js` con el Bloc de notas y pon tu usuario de TikTok, sin la @:
   ```js
   const USUARIO = 'tu_usuario';
   ```
3. Abre PowerShell en la carpeta (escribe `powershell` en la barra de la dirección de la carpeta y pulsa Enter) e instala los paquetes (solo la primera vez):
   ```
   npm install
   ```
4. Arranca el servidor y deja la ventana abierta mientras dure el directo:
   ```
   npm start
   ```
   Cuando estés en directo verás `Conectado al live de @tu_usuario`. Si aún no has empezado, se reintenta solo cada 10 segundos.

## Probarlo

| Dirección | Qué es |
| --- | --- |
| http://localhost:3001/huevo-dragon.html?test | El juego con botones de prueba. Toca para despertar el huevo. |
| http://localhost:3001/juego-test | Manda likes, regalos y un seguidor de prueba al juego. |
| http://localhost:3001/huevo-dragon.html | El juego en modo directo (pantalla completa, sin botones). |

## Ponerlo en TikTok LIVE Studio

1. Arranca `npm start` antes de abrir LIVE Studio.
2. Añade una fuente de tipo **Enlace / Navegador** con `http://localhost:3001/huevo-dragon.html`.
3. Tamaño vertical **1080 × 1920** y activa el audio de la fuente.

La barra de calor sale arriba del todo y los mensajes y el ranking de padres abajo del todo, dejando el huevo libre en el centro.

## Ajustes

| Quiero… | Cómo |
| --- | --- |
| Ver los botones de prueba | Añadir `?test` a la dirección. |
| Subir o bajar el huevo | Añadir `?y=0.12` (más arriba) o `?y=0` (centrado). |
| Cambiar el usuario | `const USUARIO` en `serverhuevo.js`. |
| Cambiar el puerto | `const PUERTO` en `serverhuevo.js` (y en la dirección). |
| Abrir el juego en otro PC | Añadir `?server=http://IP-DEL-PC:3001`. |

## Problemas frecuentes

| Problema | Solución |
| --- | --- |
| `Cannot find module 'express'` | Ejecuta `npm install` en la carpeta. |
| `node no se reconoce como un comando` | Instala Node.js y reinicia el PC. |
| `No se pudo conectar (¿estás en directo?)` | Normal si no has empezado el live. Si ya estás, revisa `USUARIO`. |
| `EADDRINUSE` | Ya hay un servidor abierto en otra ventana: ciérralo. |
| El juego no reacciona | Comprueba que la ventana de `npm start` sigue abierta. |
| Pantalla negra | Hace falta internet para cargar el motor 3D. |

## Consejo para el directo

TikTok puede limitar un directo si cree que es contenido reproducido. Sal en cámara, habla con tus espectadores mientras juegan y no dejes el live solo: el juego es para jugar contigo, no en lugar de ti.

---

Hecho por **[Belumoka](https://belumoka.com)**. Usa la librería no oficial [tiktok-live-connector](https://github.com/zerodytrash/TikTok-Live-Connector); este proyecto no está afiliado a TikTok.
