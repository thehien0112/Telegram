# Hướng Dẫn Kích Hoạt Tự Động Hóa Online ☁️

Để code trên GitHub có thể tự động gửi tin nhắn cho chị mỗi ngày, chị cần cung cấp "chìa khóa" (Token & Chat ID) cho nó.

## Bước 1: Vào Cài Đặt trên GitHub
1.  Truy cập Repository của chị: **[https://github.com/thehien0112/Telegram](https://github.com/thehien0112/Telegram)**
2.  Bấm vào tab **Settings** (trên cùng bên phải).
3.  Ở menu bên trái, tìm mục **Security** -> chọn **Secrets and variables** -> chọn **Actions**.

## Bước 2: Thêm "Chìa Khóa" (Secrets)
Chị bấm nút **New repository secret** (màu xanh lá) và thêm 2 cái sau:

### Secret 1
*   **Name:** `TELEGRAM_TOKEN`
*   **Secret:** `7447180914:AAHr9VvFPGVR7mtr2VMwPc1mJLYAx-6KIpE`
*   Bấm **Add secret**.

### Secret 2
*   **Name:** `TELEGRAM_CHAT_ID`
*   **Secret:** `5395100907`
*   Bấm **Add secret**.

## Bước 3: Kiểm Tra
Sau khi thêm xong, ngày mai (tầm 8h sáng), Bot sẽ tự động gửi bài.
Nếu chị muốn test ngay:
1.  Vào tab **Actions** trên GitHub.
2.  Chọn **Daily Telegram Sender** ở bên trái.
3.  Bấm **Run workflow** (nút màu xám bên phải) -> **Run workflow**.
4.  Đợi 1-2 phút, nếu thấy tick xanh ✅ và tin nhắn về máy là thành công!
