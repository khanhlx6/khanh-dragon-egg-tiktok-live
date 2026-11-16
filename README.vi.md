# 🥚 Trứng Rồng Cổ Đại – Game cho TikTok LIVE

> 🇻🇳 **Đây là bản dịch tiếng Việt của [`README.md`](README.md).** Tệp gốc (tiếng Tây Ban Nha) được giữ nguyên để sau này còn đồng bộ với bản của tác giả. Nếu hai bản khác nhau, bản gốc có quyền ưu tiên.

Trò chơi 3D tương tác dành cho livestream TikTok: khán giả cùng nhau sưởi ấm một quả trứng rồng bằng **like**, và bằng **quà tặng** quyết định chú rồng con nào sẽ ra đời cùng độ hiếm của nó.

🌐 Trang web của game (tác giả): **https://belumoka.com/juego-huevo-ancestral-tiktok-live/**

🎮 Bản deploy trên GitHub Pages: **https://khanhlx6.github.io/khanh-dragon-egg-tiktok-live/**

<img width="523" height="801" alt="huevo-ancestral" src="https://github.com/user-attachments/assets/9d70f216-90fd-440b-86cf-08c38fe67dc5" />

## Cách chơi

| Hành động của khán giả | Điều gì xảy ra trong game |
| --- | --- |
| ❤️ Like | Làm nóng quả trứng và bắn những tia sáng về phía nó. Khi rồng đã nở, like khiến rồng phun lửa. |
| 🎁 Quà tặng | Thêm một hệ cho quả trứng (🔥 lửa, ❄️ băng, ⚡ sấm sét, ☣️ độc dược hoặc ✨ ánh sáng) tùy theo món quà. Càng nhiều xu thì rồng càng hiếm. |
| ➕ Theo dõi | Thêm ✨ ánh sáng cho quả trứng. |

Khi thanh nhiệt đầy, quả trứng nứt ra và **rồng ra đời**: hiện tên, độ hiếm (thường, hiếm, sử thi, huyền thoại hoặc thần thoại), các hệ nguyên tố, và ai là **bậc sinh thành** — khán giả đã đóng góp nhiều nhất. Sau đó rồng bay một lúc, biến mất và một quả trứng mới thành hình, cần thêm một chút nhiệt nữa.

## Các tệp trong dự án

| Tệp | Dùng để làm gì |
| --- | --- |
| `huevo-dragon.html` | Game. Đây là trang được đưa vào TikTok LIVE Studio. |
| `serverhuevo.js` | Kết nối tới live của bạn và chuyển like, quà tặng, người theo dõi vào game (cổng 3001). |
| `package.json` | Danh sách các gói mà máy chủ cần. |
| `index.html` | Trang chủ trên GitHub Pages, chỉ để điều hướng cho nhanh (không bắt buộc). |
| `vi/` | Bản dịch tiếng Việt: game (`vi/huevo-dragon.html`), máy chủ (`vi/serverhuevo.js`), `vi/package.json`. |
| `tools/build-vi.py` | Script tự sinh bản dịch tiếng Việt từ bản gốc. Chạy lại sau mỗi lần đồng bộ với upstream. |
| `tools/check-vi.py` | Kiểm tra nhanh bản dịch (JSON hợp lệ, cú pháp JS, còn sót chuỗi tiếng Tây Ban Nha hay không). |
| `.github/workflows/vi-sync.yml` | CI: tự chạy `build-vi.py` sau mỗi lần merge và tự commit bản dịch mới. |
| `.github/workflows/static.yml` | CI: deploy game lên GitHub Pages. |
| `README.vi.md` | Tệp hướng dẫn này (bản dịch viết tay, không do script sinh). |

## Yêu cầu

- PC chạy Windows (Mac và Linux cũng dùng được).
- [Node.js](https://nodejs.org) bản LTS.
- TikTok LIVE Studio (hoặc OBS).
- Kết nối internet.

## Cài đặt

1. Tải dự án về: bấm nút xanh **Code → Download ZIP** rồi giải nén.
2. Mở `serverhuevo.js` bằng Notepad và điền tên tài khoản TikTok của bạn, **không** kèm dấu @:
   ```js
   const USUARIO = 'ten_tai_khoan_cua_ban';
   ```
   (Muốn dùng bản dịch tiếng Việt thì mở `vi/serverhuevo.js`; tên biến vẫn giữ nguyên là `USUARIO`.)
3. Mở PowerShell ngay trong thư mục dự án (gõ `powershell` vào thanh địa chỉ của thư mục rồi nhấn Enter) và cài các gói (chỉ cần làm lần đầu):
   ```
   npm install
   ```
4. Khởi động máy chủ và để cửa sổ này mở trong suốt buổi live:
   ```
   npm start
   ```
   Khi bạn đang lên sóng, bạn sẽ thấy `Đã kết nối tới live của @ten_tai_khoan`. Nếu chưa bắt đầu live, chương trình tự thử lại sau mỗi 10 giây.

## Thử nghiệm

| Địa chỉ | Đó là gì |
| --- | --- |
| http://localhost:3001/huevo-dragon.html?test | Game kèm các nút thử nghiệm. Chạm để đánh thức quả trứng. |
| http://localhost:3001/juego-test | Gửi like, quà tặng và một người theo dõi thử vào game. |
| http://localhost:3001/huevo-dragon.html | Game ở chế độ lên sóng (toàn màn hình, không có nút). |

Nếu chạy máy chủ từ thư mục `vi/` (`cd vi`, `npm install`, `npm start`) thì địa chỉ vẫn như trên và game sẽ là **bản tiếng Việt**.

## Đưa game vào TikTok LIVE Studio

1. Chạy `npm start` trước khi mở LIVE Studio.
2. Thêm một nguồn loại **Link / Browser** với địa chỉ `http://localhost:3001/huevo-dragon.html`.
3. Kích thước dọc **1080 × 1920** và bật âm thanh cho nguồn đó.

Thanh nhiệt nằm ở sát phía trên, còn tin nhắn và bảng xếp hạng bậc sinh thành ở sát phía dưới, nhờ vậy quả trứng luôn trống trải ở giữa.

## Tùy chỉnh

| Tôi muốn… | Cách làm |
| --- | --- |
| Xem các nút thử nghiệm | Thêm `?test` vào cuối địa chỉ. |
| Nâng hoặc hạ quả trứng | Thêm `?y=0.12` (cao hơn) hoặc `?y=0` (căn giữa). |
| Đổi tài khoản TikTok | Sửa `const USUARIO` trong `serverhuevo.js`. |
| Đổi cổng | Sửa `const PUERTO` trong `serverhuevo.js` (và trong địa chỉ). |
| Mở game trên máy khác | Thêm `?server=http://IP-CUA-MAY:3001`. |

## Sự cố thường gặp

| Vấn đề | Cách xử lý |
| --- | --- |
| `Cannot find module 'express'` | Chạy `npm install` trong thư mục dự án. |
| `node no se reconoce como un comando` (Windows không nhận lệnh `node`) | Cài Node.js rồi khởi động lại máy. |
| `Không kết nối được (bạn đã lên sóng chưa?)` | Bình thường nếu bạn chưa live. Nếu đang live rồi, kiểm tra lại `USUARIO`. |
| `EADDRINUSE` | Đã có một máy chủ khác mở ở cửa sổ khác: hãy đóng nó đi. |
| Game không phản ứng | Kiểm tra cửa sổ `npm start` vẫn còn mở. |
| Màn hình đen | Cần internet để tải engine 3D. |

## Về bản deploy trên GitHub Pages

- Địa chỉ: **https://khanhlx6.github.io/khanh-dragon-egg-tiktok-live/**
- Bản tiếng Việt: `…/vi/huevo-dragon.html` · Bản gốc: `…/huevo-dragon.html`
- Workflow `.github/workflows/static.yml` tự deploy mỗi khi push lên nhánh `main` (hoặc bấm chạy tay trong tab **Actions**).
- **Lưu ý:** GitHub Pages chỉ chạy phần giao diện game (hiệu ứng 3D). Nó **không** chạy được Node.js, nên không nhận được like/quà thật từ TikTok. Muốn chơi thật, hãy chạy `npm start` trên máy của bạn và mở `http://localhost:3001/huevo-dragon.html`.

## Mẹo cho buổi live

TikTok có thể hạn chế một buổi live nếu cho rằng đó là nội dung phát lại. Hãy xuất hiện trước camera, trò chuyện với khán giả trong khi họ chơi, và đừng để live chạy một mình: game sinh ra để chơi **cùng** bạn, chứ không phải thay bạn.

## Đồng bộ với bản gốc của tác giả

Repo gốc: **https://github.com/belumokasl-hub/juego-huevo-ancestral-tiktok-live**

Bản gốc tiếng Tây Ban Nha (`huevo-dragon.html`, `serverhuevo.js`, `package.json`, `README.md`) **không bao giờ bị sửa** trong repo này, nên bạn có thể merge thẳng các cập nhật từ tác giả:

```bash
# thêm remote upstream (chỉ lần đầu)
git remote add upstream https://github.com/belumokasl-hub/juego-huevo-ancestral-tiktok-live.git

# lấy và merge bản mới của tác giả vào nhánh main của bạn
git fetch upstream
git checkout main
git merge upstream/main

# dịch lại các chuỗi mới (script sẽ báo lỗi nếu tác giả đổi câu chữ cần dịch)
python3 tools/build-vi.py
```

`tools/build-vi.py` sinh ra `vi/huevo-dragon.html`, `vi/serverhuevo.js` và `vi/package.json` từ bản gốc. Script kiểm tra từng chuỗi cần dịch: nếu tác giả đã đổi câu chữ, nó dừng lại và liệt kê **tất cả** vị trí cần cập nhật trong script, nhờ vậy bản dịch không bao giờ bị lệch một cách âm thầm.

### CI tự động (`.github/workflows/vi-sync.yml`)

Workflow **Sync Vietnamese translation** chạy tự động, không cần làm gì thủ công:

| Khi nào | Workflow làm gì |
| --- | --- |
| Có **push lên `main`** (kể cả commit merge) | Chạy `build-vi.py` → nếu bản gốc đổi phần không cần dịch (màu, thông số, logic…) thì **tự commit & push** bản dịch mới vào `vi/`, rồi deploy lại Pages. Không có gì đổi thì không tạo commit rỗng. |
| Có **PR** hoặc **bấm tay** trong tab Actions | Chỉ kiểm tra: chạy `build-vi.py` + `check-vi.py`, báo lỗi nếu `vi/` đang lệch bản gốc (nhờ vậy không merge PR có bản dịch sai). |
| Tác giả **đổi câu chữ cần dịch** | CI **đỏ** và ghi rõ trong phần *Summary*: nhãn chuỗi, chuỗi gốc, và cách sửa `tools/build-vi.py`. CI **không tự đoán** bản dịch mới. |

> Commit do bot tạo ra bằng `GITHUB_TOKEN` không tự kích hoạt các workflow khác, nên job `sync` gọi lại `static.yml` để Pages phục vụ bản dịch mới nhất.

Muốn chạy kiểm tra tương tự ngay trên máy:

```bash
python3 tools/build-vi.py    # sinh lại bản dịch
python3 tools/check-vi.py    # kiểm tra (cần node để check cú pháp JS)
```

---

Thực hiện bởi **[Belumoka](https://belumoka.com)**. Sử dụng thư viện không chính thức [tiktok-live-connector](https://github.com/zerodytrash/TikTok-Live-Connector); dự án này không liên kết với TikTok.
