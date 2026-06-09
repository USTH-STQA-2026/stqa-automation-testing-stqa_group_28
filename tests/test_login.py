"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password (*Đăng nhập thất bại – sai mật khẩu*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)
    
    Description (*Mô tả*):
        Enter correct email but wrong password → system stays on login page
        or shows an error message.
        (*Nhập email đúng nhưng mật khẩu sai → hệ thống không chuyển trang,
        hoặc hiển thị thông báo lỗi.*)

    📖 RIPR — Áp dụng cho test case này:
        [R] page.goto(...) → Chạm tới trang đăng nhập
        [I] flutter_fill(..., "wrongpassword") → Nhiễm trạng thái lỗi
        [P] Hệ thống xử lý login → Lỗi lan truyền ra thông báo
        [R✓] assert ... → Test Oracle kiểm tra thông báo lỗi

    💡 Bonus B2 — Data-Driven Testing:
        TC-02 và TC-03 có cùng pattern (nhập → click → kiểm tra lỗi).
        Bạn có thể gộp bằng @pytest.mark.parametrize:

        @pytest.mark.parametrize("email, password, tc_id", [
            ("valid@email.com", "wrongpass", "TC-02"),
            ("", "", "TC-03"),
        ])
        def test_login_fail(page, test_config, email, password, tc_id):
            ...

        Xem thêm: docs/textbook-concepts.md §3 (Data-Driven Testing)

    Suggested steps (*Gợi ý các bước*):
        1. Navigate to login page (*Truy cập trang đăng nhập*)
        2. Enable Flutter semantics (*Bật Flutter semantics*)
        3. Enter correct Email (from test_config["email"]) (*Nhập Email đúng*)
        4. Enter wrong Password (e.g. "wrongpassword") (*Nhập Mật khẩu sai*)
        5. Click "Đăng nhập" (*Click "Đăng nhập"*)
        6. Assert: URL still on login page OR error message shown
           (*Assert: URL vẫn ở trang đăng nhập HOẶC có thông báo lỗi*)
    """
    # TODO: 
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test [6, 7]
    page.goto(test_config["base_url"], wait_until="networkidle")
    enable_flutter_semantics(page)

    # [I] Infection: Nhập đúng Email nhưng sai Mật khẩu — kích hoạt logic báo lỗi [8, 9]
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrong_password_123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ thông báo lỗi lan truyền ra UI (Smart Wait) [8, 10]
    # Ảnh tc02_failure.png cho thấy text chính xác là "Mật khẩu không đúng." [11]
    wait_for_flutter(page, text="Mật khẩu không đúng.")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc02_test_login_fail_wrong_password.png"))

    # [R✓] Revealability: Strong Oracle (B3) — Kiểm tra thông báo lỗi VÀ trạng thái hệ thống [5, 12]
    # Sử dụng all_text_contents() để lấy toàn bộ văn bản giúp tránh lỗi locator trong Flutter [13, 14]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_found = "Mật khẩu không đúng" in sem_text
    
    # Kiểm tra thêm nút Đăng nhập để chứng minh hệ thống không chuyển trang sai (Invariants) [15, 16]
    login_btn_visible = page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")').is_visible()
    
    assert error_found, "Lỗi: Không tìm thấy thông báo 'Mật khẩu không đúng.' trong Semantics Tree."
    assert login_btn_visible, "Lỗi: Hệ thống không giữ người dùng ở lại trang đăng nhập (Strong Oracle B3)."

def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail – empty fields (*Đăng nhập thất bại – để trống các trường*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Leave all fields empty, click Login → system stays on login page.
        (*Không nhập gì, bấm Đăng nhập → hệ thống không chuyển trang.*)

    Suggested steps (*Gợi ý các bước*):
        1. Navigate to login page (*Truy cập trang đăng nhập*)
        2. Enable Flutter semantics (*Bật Flutter semantics*)
        3. Do NOT enter Email/Password — click "Đăng nhập" immediately
           (*KHÔNG nhập Email/Mật khẩu — click "Đăng nhập" ngay*)
        4. Assert: URL still on login page (*Assert: URL vẫn ở trang đăng nhập*)
    """
    # TODO: 
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle")
    enable_flutter_semantics(page)

    # [I] Infection: Click Đăng nhập ngay lập tức khi chưa điền thông tin [3, 4]
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ UI cập nhật thông báo lỗi (Ảnh tc03_failure.png [5])
    wait_for_flutter(page, text="Vui lòng nhập email và mật khẩu.")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc03_test_login_fail_empty_fields.png"))

    # [R✓] Revealability: Strong Oracle (B3) — Kiểm tra thông báo lỗi VÀ trạng thái UI
    # Quét toàn bộ cây Semantics để tránh lỗi locator thuộc tính [1]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_found = "Vui lòng nhập email và mật khẩu" in sem_text
    
    # Invariant: Ô input Email vẫn phải hiện diện (người dùng vẫn ở trang đăng nhập)
    email_field_visible = page.locator('input[aria-label="Email"]').is_visible()
    
    assert error_found, "Lỗi: Không tìm thấy thông báo 'Vui lòng nhập email và mật khẩu.' trong Semantics Tree."
    assert email_field_visible, "Lỗi: Hệ thống không giữ người dùng ở lại trang đăng nhập (B3)."

@pytest.mark.parametrize("email, password, expected_error, tc_id", [
    ("ba.nguyen@email.com", "wrong_password_123", "Mật khẩu không đúng", "tc02"),
    ("", "", "Vui lòng nhập email và mật khẩu", "tc03"),
])
def test_login_failure(page, test_config, email, password, expected_error, tc_id):
    """
    Combined test for TC-02 and TC-03 using Data-Driven Testing (Bonus B2).
    Uses Strong Oracle (Bonus B3) to verify specific SRS error messages.
    """
     # [R] Reachability: Truy cập trang đăng nhập và bật semantics [6]
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập thông tin để kích hoạt logic báo lỗi [6]
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Đợi thông báo lỗi xuất hiện (Smart Wait cho Flutter) [7]
    wait_for_flutter(page, text=expected_error)

    # [R✓] Revealability: Strong Oracle (B3) kiểm tra text chính xác và trạng thái UI [1, 8]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    login_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")')
    
    # Kiểm tra thông báo lỗi VÀ đảm bảo nút Đăng nhập vẫn còn đó (không bị chuyển trang)
    assert expected_error in sem_text, f"Lỗi: Không tìm thấy '{expected_error}' trên giao diện"
    assert login_btn.is_visible(), "Lỗi: Hệ thống không giữ người dùng ở trang đăng nhập (B3)"

    # Screenshot: Minh chứng cho báo cáo [9]
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"{tc_id}_failure.png"))

def test_extra_login_fail_invalid_email(page, test_config):
    """TC-13 (Bonus B1): Login fail – non-existent email (*Email không tồn tại*)"""
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle")
    enable_flutter_semantics(page)

    # [I] Infection: Nhập email không tồn tại trong hệ thống (Seed Data)
    flutter_fill(page, "Email", "nobody@test.com")
    flutter_fill(page, "Mật khẩu", "123456")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ thông báo lỗi xuất hiện (Dấu chấm cuối câu theo ảnh tc13_failure.png)
    wait_for_flutter(page, text="Không tìm thấy thành viên.")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc13_extra_test_invalid_email.png"))

    # [R✓] Revealability: Strong Oracle (B3) — Kiểm tra thông báo lỗi VÀ trạng thái AppBar
    # Dùng kỹ thuật quét toàn bộ Semantics Tree để tránh lỗi locator [3]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    
    error_found = "Không tìm thấy thành viên" in sem_text
    is_not_logged_in = test_config["display_name"] not in sem_text
    
    assert error_found, "Lỗi: Không tìm thấy thông báo 'Không tìm thấy thành viên.' trong Semantics Tree."
    assert is_not_logged_in, "Lỗi: Hệ thống cho phép đăng nhập trái phép hoặc AppBar hiển thị sai tên (B3)."
