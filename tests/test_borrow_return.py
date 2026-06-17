"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import time
import re
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter,
    login, SCREENSHOT_DIR,
)

def click_confirm_borrow_button(page):
    """Clicks the confirmation 'Mượn' button exactly using a regex match to avoid strictness conflicts with 'Mượn sách này'."""
    confirm_btn = (
        page.locator('flt-semantics[role="button"]')
        .filter(has_text=re.compile(r"^Mượn$"))
        .first
    )
    confirm_btn.click()

def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    ✅ COMPLETED — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
           (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
           (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
           (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
           (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
           (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    """
    # TODO: 
    """TC-08: Borrow an available book and verify status change.

    RIPR Model:
    - [R] Reachability: Access the library system and book list via login.
    - [I] Infection: Select an available book and confirm the borrow action.
    - [P] Propagation: Wait for the system to process and display the success toast.
    - [R✓] Revealability: Verify success message and check that book status is updated.
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Find an Available book and borrow it
    # Wait up to 15s for at least one "Có sẵn" (Available) book card to appear
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=15000)

    # Click the "Mượn sách này" button inside the selected available book card
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    # [P] Propagation: Wait for confirmation dialog to appear
    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)

    # Confirm loan (click "Mượn" in modal dialog strictly)
    click_confirm_borrow_button(page)

    # Wait for success toast/notification
    wait_for_flutter(page, text="thành công", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # [R] Assert: success notification OR book status changed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đang mượn" in sem_text, (
        "Expected 'thành công' or 'Đang mượn' after borrowing — borrow may have failed"
    )
    
def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    ✅ COMPLETED — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
          (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
    """
    # TODO: 
    """TC-09: View borrowed books list in the 'Mượn / Trả' tab.

    RIPR Model:
    - [R] Reachability: Log in and access the system (using ba.nguyen account).
    - [I] Infection: Navigate to the 'Mượn / Trả' tab to update the view state.
    - [P] Propagation: Wait for the borrowed items to appear in the list.
    - [R✓] Revealability: Verify that active loans are visible in the UI.
    """
    # [R] Dùng ba.nguyen (MEM002) đã có sẵn phiếu BR001 [4, 5]
    user_config = test_config.copy()
    user_config.update({"email": "ba.nguyen@email.com"})
    login(page, user_config)
    
    # [I] Chuyển Tab
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').click()
    enable_flutter_semantics(page)

    # [P] Chờ danh sách mượn hiện ra
    wait_for_flutter(page, text="Mã phiếu")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc09_view_list.png"))

    # [R✓] Kiểm tra sự hiện diện của BR001 từ Seed Data [10]
    assert page.locator('flt-semantics[aria-label*="BR001"]').is_visible()

def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    ✅ COMPLETED — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
          (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
          (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
    """
    # TODO: 
    """TC-10: Return a borrowed book and verify status change.

    RIPR Model:
    - [R] Reachability: Log in and navigate to the 'Mượn / Trả' tab.
    - [I] Infection: Trigger the return logic by clicking the 'Trả sách' button.
    - [P] Propagation: Wait for the system to process and display the success feedback.
    - [R✓] Revealability: Verify success message and ensure the book is cleared from the list.
    """
    # [R] Reachability: ba.nguyen đang mượn BOOK003 [5]
    user_config = test_config.copy()
    user_config.update({"email": "ba.nguyen@email.com"})
    login(page, user_config)
    
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').click()
    enable_flutter_semantics(page)

    # [I] Nhấn nút Trả sách
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    # [P] Chờ xác nhận
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc10_return_success.png"))

    # [R✓] Nút trả sách của bản ghi đó phải biến mất (Invariant) [11]
    assert return_btn.count() == 0

# =========================================================================
# BONUS B1: EXTRA TEST CASES (2 cases outside TC-01 to TC-12)
# =========================================================================

def test_borrow_suspended_member(page, test_config):
    """TC-bonus: Suspended member receives suspended-account message

    Expect: Reject borrowing with a message indicating account suspension.
    Actual (BUG-03): Rejects but displays expired-account message instead.
    """
    # [R] Reachability: Login bằng cu.le (MEM004) đang bị Tạm ngưng [1]
    user_config = test_config.copy()
    user_config.update({"email": "cu.le@email.com"})
    login(page, user_config)
    enable_flutter_semantics(page)

    # [I] Infection: Thực hiện mượn một cuốn sách bất kỳ
    page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    enable_flutter_semantics(page) # Thấy Dialog
    
    if page.locator('flt-semantics[role="button"]:has-text("Mượn")').is_visible():
        click_confirm_borrow_button(page)

    # [P] Propagation: NÉ BẪY TIMEOUT
    # Chỉ chờ từ khóa "Thành viên" vì BUG-04 hiển thị sai thành "Thành viên đã hết hạn" [2, 3]
    # Nếu chờ "đang bị tạm ngưng", test sẽ treo 15s và báo lỗi Timeout.
    wait_for_flutter(page, text="Thành viên")
    
    # [R✓] Revealability: Strong Oracle bộc lộ BUG-04 [4]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc16_suspended_rejection.png"))
    
    # Assert này sẽ FAILED và chỉ ra đúng BUG-04 cho bạn làm báo cáo
    expected_msg = "Thành viên đang bị tạm ngưng"
    assert expected_msg in sem_text, f"Bộc lộ BUG-04: Kỳ vọng '{expected_msg}' nhưng thực tế báo sai lý do."

def test_extra_borrow_unavailable_book(page, test_config):
    """B1-2: Verify rejection when a book is already borrowed."""
    login(page, test_config)
    enable_flutter_semantics(page)

    # [R] Find a book card already marked as 'Đang mượn'
    borrowed_book = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]').first
    
    # [I/R✓] Oracle: In this system, the borrow button should be hidden or disabled for borrowed books
    borrow_btn = borrowed_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    assert borrow_btn.count() == 0, "Borrow button should not exist for books already in use"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc17_extra_test_case_unavailable.png"))

# =========================================================================
# BONUS B2: DATA-DRIVEN TESTING (Parameterized Rejections)
# =========================================================================

@pytest.mark.parametrize("email, expected_msg, tc_id", [
    ("cu.le@email.com", "Thành viên đang bị tạm ngưng", "tc16_suspended"),
    ("binh.pham@email.com", "Thành viên đã hết hạn", "tc17_expired"),
])
def test_borrow_rejections_data_driven(page, test_config, email, expected_msg, tc_id):
    """Actual: BUG-04 causes both suspended and expired accounts to show the same 'Thành viên đã hết hạn' message, which is incorrect."""
    user_config = test_config.copy()
    user_config.update({"email": email})
    login(page, user_config)
    enable_flutter_semantics(page)

    page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    enable_flutter_semantics(page)
    if page.locator('flt-semantics[role="button"]:has-text("Mượn")').is_visible():
        click_confirm_borrow_button(page)

    # CHIẾN THUẬT: Chỉ chờ từ "Thành viên" để không bị treo máy 15s khi hệ thống báo sai lý do (BUG-04) [7]
    wait_for_flutter(page, text="Thành viên")
    
    # [R✓] Revealability: Oracle bộc lộ BUG-04 (Tạm ngưng báo nhầm Hết hạn) [8]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"{tc_id}.png"))
    
    assert expected_msg in sem_text, f"Bộc lộ BUG-04: Kỳ vọng '{expected_msg}' nhưng thực tế báo sai lý do."
