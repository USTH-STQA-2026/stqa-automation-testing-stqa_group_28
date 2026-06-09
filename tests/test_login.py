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
    # [R] Reachability: Navigate to login page and enable semantics for Flutter interaction [4, 5]
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter correct email but an incorrect password to trigger error logic [6, 7]
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrong_password_123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the specific error message to propagate to the UI [8, 9]
    # (Smart Wait used to avoid non-deterministic time.sleep errors [3, 10])
    expected_error = "Mật khẩu không đúng"
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc02_test_login_fail_wrong_password.png"))

    # [R✓] Revealability: Strong Oracle verifying the exact error string from SRS REQ-01 [6, 8, 11]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, f"Expected error '{expected_error}' not found in UI"

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
    # [R] Reachability: Access the system entry point [5, 9]
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Click Login immediately without providing credentials [8, 12]
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the system to display the mandatory field warning [6, 8]
    expected_error = "Vui lòng nhập email và mật khẩu"
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc03_test_login_fail_empty_fields.png"))

    # [R✓] Revealability: Verify the error message matches the SRS exactly [8, 13]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, f"Expected validation message '{expected_error}' not found"

@pytest.mark.parametrize("email, password, expected_error, tc_id", [
    ("ba.nguyen@email.com", "wrong_password_123", "Mật khẩu không đúng", "tc02"),
    ("", "", "Vui lòng nhập email và mật khẩu", "tc03"),
])
def test_login_failure(page, test_config, email, password, expected_error, tc_id):
    """
    Combined test for TC-02 and TC-03 using Data-Driven Testing (Bonus B2).
    Uses Strong Oracle (Bonus B3) to verify specific SRS error messages.
    """
    # [R] Reachability: Navigate to login page and enable semantics for Flutter interaction
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Input credentials (valid/invalid/empty) to trigger system logic
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Smart Wait for the specific error message to appear in the UI
    # This avoids flaky tests and is required for Flutter Web [2]
    wait_for_flutter(page, text=expected_error)

    # [R✓] Revealability: Strong Oracle verifying the exact text defined in REQ-01 [3]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, f"Expected error '{expected_error}' not found in UI"

    # Screenshot: Automatic evidence for the report [4]
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"{tc_id}_failure.png"))

def test_extra_login_fail_invalid_email(page, test_config):
    """TC-13 (Bonus B1): Login fail – non-existent email (*Email không tồn tại*)"""
    # [R] Reachability: Reach the login UI [5, 9]
    page.goto(test_config["base_url"])
    enable_flutter_semantics(page)

    # [I] Infection: Input an email that does not exist in the seed data [7]
    flutter_fill(page, "Email", "nobody@test.com")
    flutter_fill(page, "Mật khẩu", "any_pass")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for error state to surface at UI level [6, 8]
    expected_error = "Không tìm thấy thành viên"
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc13_extra_test_login_fail_invalid_email.png"))

    # [R✓] Revealability: Assert the specific rejection reason is revealed [6, 14]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, f"Expected error '{expected_error}' was not revealed"