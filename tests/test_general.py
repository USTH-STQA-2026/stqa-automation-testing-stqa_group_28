"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter,
    login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click Logout → verify page returns to login screen.
        (*Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "Đăng xuất" button and click (*Tìm nút "Đăng xuất" và click*)
        3. Wait 3s, re-enable semantics (*Đợi 3s, bật lại semantics*)
        4. Assert: "Đăng nhập" button or Email input exists
           (*Assert: có nút "Đăng nhập" hoặc ô input Email*)
    """
    # TODO: 
    """TC-11: Logout success and return to login screen.

    RIPR Model Trace:
    - [R] Reachability: Log in to access the authenticated area.
    - [I] Infection: Click the 'Đăng xuất' (Logout) button to trigger logout logic.
    - [P] Propagation: Wait for the UI to transition back to the login screen.
    - [R✓] Revealability: Verify that login elements are visible again.
    """
    # [R] Reachability: Ensure we are inside the system
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Perform logout action
    flutter_click_button(page, "Đăng xuất")

    # [P] Propagation: Use Smart Wait for the login screen to render (No sleep!)
    # After logout, the "Đăng nhập" button should reappear
    wait_for_flutter(page, text="Đăng nhập")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc11_test_logout.png"))

    # [R✓] Revealability: Strong Oracle - Verify state transition
    # Check for both the Login button and the Email field
    login_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")')
    email_field = page.locator('input[aria-label="Email"]')
    
    assert login_btn.is_visible() and email_field.is_visible(), \
        "Logout failed: System did not return to the login screen"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
        (*Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "EN" button and click (*Tìm nút "EN" và click*)
        3. Wait 2s, re-enable semantics (*Đợi 2s, bật lại semantics*)
        4. Get sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        5. Assert: "Logout" or "Borrow" or "Library" in sem_text
    """
    # TODO: 
    """TC-12: Switch system language to English.

    RIPR Model Trace:
    - [R] Reachability: Log in to the dashboard in the default Vietnamese mode.
    - [I] Infection: Click the 'EN' button to trigger the language toggle logic.
    - [P] Propagation: Wait for the Flutter Semantics Tree to update its labels to English.
    - [R✓] Revealability: Verify that English labels (e.g., 'Logout') are now present.
    """
    # [R] Reachability: Ensure the system is accessed and semantics are enabled
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Click the 'EN' button to change the language
    flutter_click_button(page, "EN")

    # [P] Propagation: Wait for English text to propagate to the UI (Smart Wait)
    # Note: We wait for "Logout" which is the EN translation of "Đăng xuất" per REQ-01
    wait_for_flutter(page, text="Logout")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc12_test_switch_language_to_english.png"))

    # [R✓] Revealability: Strong Oracle - Verify English keywords exist in the Semantics Tree
    # We collect all semantic content to ensure the translation was successful
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    
    # Asserting key English terms defined in the assignment hints
    is_english_active = "Logout" in sem_text or "Borrow" in sem_text or "Library" in sem_text
    
    assert is_english_active, \
        "Language switch failed: UI did not update to English (Logout/Borrow labels not found)"

# -------------------------------------------------------------------------
# BONUS B1: EXTRA TEST CASES (Librarian Specific)
# -------------------------------------------------------------------------

def test_extra_data_reset(page, test_config):
    """B1-1: Verify Librarian's 'Data Reset' functionality (REQ-04/REQ-08)."""
    # [R] Login as Librarian
    lib_config = test_config.copy()
    lib_config.update({"email": "librarian@library.com", "password": "admin123"})
    login(page, lib_config)
    enable_flutter_semantics(page)

    # [I] Action: Click Reset icon 🔄 and confirm
    flutter_click_button(page, "Đặt lại dữ liệu")
    enable_flutter_semantics(page)
    flutter_click_button(page, "Đặt lại")

    # [P] Wait for completion
    wait_for_flutter(page, text="đăng nhập")
    login(page, lib_config)
    enable_flutter_semantics(page)
    wait_for_flutter(page, text="BOOK001")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc19_extra_data_reset.png"))

    # [R✓] Strong Oracle: Check if toast appears and system is at seed state
    seed_state = {
        "Có sẵn": ["BOOK001", "BOOK002", "BOOK005"],
        "Đang mượn": ["BOOK003"],
        }
    for status, book_ids in seed_state.items():
        for book_id in book_ids:
            oracle = page.locator(f'flt-semantics[role= "group"]:has-text("{book_id}"):has-text("{status}")')
            assert oracle.count() > 0, f"{book_id} should have status {status} after  data reset"

def test_extra_overdue_check(page, test_config):
    """B1-2: Verify Librarian's 'Check Overdue' scan (REQ-06)."""
    # [R] Reachability: Login as Librarian
    lib_config = test_config.copy()
    lib_config.update({"email": "librarian@library.com", "password": "admin123"})
    login(page, lib_config)
    enable_flutter_semantics(page)

    # [I] Action: Trigger overdue scan logic
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.click(force= True)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Kiểm tra sách quá hạn")

    # [P] Propagation: Wait for scan confirmation
    wait_for_flutter(page, text="Đã cập nhật")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc20_extra_overdue_check.png"))

    # [R✓] Strong Oracle: Confirm the feedback message
    oracle = page.locator('flt-semantics:has-text("Đã cập nhật")')
    assert oracle.count() > 0, "Check overdue scan confirmation should be displayed"

# -------------------------------------------------------------------------
# BONUS B2: DATA-DRIVEN TESTING (Parameterized Language Labels)
# -------------------------------------------------------------------------

@pytest.mark.parametrize("lang_btn, expected_keyword, case_id", [
    ("EN", "Sign out", "EN_Check"),
    ("VI", "Đăng xuất", "VN_Check"),
])
def test_language_data_driven(page, test_config, lang_btn, expected_keyword, case_id):
    """B2: Verify multiple language transitions using parametrization."""
    # [R] Login
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Act: Switch language based on parameter
    flutter_click_button(page, lang_btn)

    # [P] Wait for specific label
    wait_for_flutter(page, text=expected_keyword)

    # [R✓] Strong Oracle: Verify the keyword exists in the tree
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_keyword in sem_text, f"Label {expected_keyword} not found for {case_id}"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"tc21_{case_id}.png"))
