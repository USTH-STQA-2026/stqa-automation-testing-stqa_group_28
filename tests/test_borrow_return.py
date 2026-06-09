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
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter,
    login, SCREENSHOT_DIR,
)


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    ✅ COMPLETE — Students have implemented this test case.
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
    # [R] Reachability: Log in to the system and ensure semantics are enabled
    # The login helper handles navigation and initial semantics activation [1, 2]
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Perform borrowing actions to trigger logic
    # 1. Locate the first book card marked as "Available" (Có sẵn) [3]
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first

    # 2. Click the 'Borrow' button within that specific card
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    # 3. Handle confirmation dialog (re-enable semantics for the dialog overlay) [4]
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")

    # [P] Propagation: Use Smart Wait for success message to surface in UI
    # Avoid time.sleep() to maintain test stability and speed [4, 5]
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc08_test_borrow_success.png"))

    # [R✓] Revealability: Strong Oracle - Verify evidence of success
    # Check 1: Success toast must match SRS REQ-04 wording [4]
    success_toast = page.locator('flt-semantics[aria-label*="Mượn sách thành công"]')
    assert success_toast.is_visible(), "Borrow success message should be displayed"

    # Check 2: State Change - Verify book status changed to 'Borrowed' (Đang mượn)
    # This confirms the data state propagated correctly to the screen [4]
    borrowed_status = page.locator('flt-semantics[aria-label*="Đang mượn"]').first
    assert borrowed_status.is_visible(), "Book status failed to update to 'Đang mượn'"


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    ✅ COMPLETE — Students have implemented this test case.
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

    # [R] Reachability: Log in to the system
    # ba.nguyen (default in .env) already has BOOK003 in 'Borrowed' status
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Switch to the 'Mượn / Trả' tab
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.click()

    # [P] Propagation: Wait for tab content to render
    # Re-enable semantics is required after tab switching for Flutter Web
    enable_flutter_semantics(page)
    wait_for_flutter(page, text="Đang mượn")
    
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc09_test_view_borrowed_books.png"))

    # [R✓] Revealability: Strong Oracle - Verify borrowed book existence
    # Check for either the 'Borrowed' status label or the 'Return' button
    borrowed_status = page.locator('flt-semantics[aria-label*="Đang mượn"]')
    return_button = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')

    assert borrowed_status.count() > 0 or return_button.count() > 0, \
        "Borrowed books list should display active loans for this member"

def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    ✅ COMPLETE — Students have implemented this test case.
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

    # [R] Reachability: Log in and access the personal borrow records tab
    # ba.nguyen (MEM002) is used as they have an active loan for BOOK003
    login(page, test_config)
    enable_flutter_semantics(page)
    
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.click()
    
    # Re-enable semantics after tab switch to interact with the new view
    enable_flutter_semantics(page)
    wait_for_flutter(page, text="Trả sách")

    # [I] Infection: Perform the return action to trigger logic
    # Click the first 'Trả sách' button found in the list
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    # [P] Propagation: Wait for the UI state to change (Smart Wait)
    # Avoid time.sleep() to follow AI Guidelines for stability
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc10_test_return_success.png"))

    # [R✓] Revealability: Strong Oracle - Verify evidence of success
    # Check 1: Success toast must appear confirming the transaction
    success_toast = page.locator('flt-semantics[aria-label*="Trả sách thành công"]')
    assert success_toast.is_visible(), "Return success notification was not displayed"

    # Check 2: State Change - Verify the 'Return' button is now gone
    # This confirms the book has been successfully moved back to 'Available' status
    return_btn_after = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    assert return_btn_after.count() == 0, "The book record should no longer show the 'Trả sách' button"

# =========================================================================
# BONUS B1: EXTRA TEST CASES (2 cases outside TC-01 to TC-12)
# =========================================================================

def test_extra_borrow_suspended_member(page, test_config):
    """B1-1: Verify that a suspended member (MEM004) cannot borrow books."""
    # [R] Login as cu.le who is 'Tạm ngưng'
    suspended_config = test_config.copy()
    suspended_config.update({"email": "cu.le@email.com"})
    login(page, suspended_config)
    enable_flutter_semantics(page)

    # [I] Attempt to borrow
    page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    enable_flutter_semantics(page)
    if page.locator('flt-semantics[role="button"]:has-text("Mượn")').is_visible():
        flutter_click_button(page, "Mượn")

    # [P] Wait for the specific rejection message defined in REQ-04
    wait_for_flutter(page, text="đang bị tạm ngưng")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc16_extra_test_case_suspended.png"))

    # [R✓] Strong Oracle: Match exact SRS wording for suspended state
    error_msg = page.locator('flt-semantics[aria-label="Thành viên đang bị tạm ngưng"]')
    assert error_msg.is_visible(), "Should show 'Tạm ngưng' message instead of generic error"

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

@pytest.mark.parametrize("email, expected_msg, case_id", [
    ("cu.le@email.com", "Thành viên đang bị tạm ngưng", "DRIVE_Suspended"),
    ("binh.pham@email.com", "Thành viên đã hết hạn", "DRIVE_Expired"),
])
def test_borrow_rejections_data_driven(page, test_config, email, expected_msg, case_id):
    """B2: Using parametrization to verify multiple rejection scenarios from REQ-04."""
    # [R] Arrange environment for each user
    user_config = test_config.copy()
    user_config.update({"email": email})
    login(page, user_config)
    enable_flutter_semantics(page)

    # [I] Act: Trigger rejection
    page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    enable_flutter_semantics(page)
    if page.locator('flt-semantics[role="button"]:has-text("Mượn")').is_visible():
        flutter_click_button(page, "Mượn")

    # [P] Wait for UI response
    wait_for_flutter(page, text=expected_msg)

    # [R✓] Strong Oracle: Verify exact text from SRS [1]
    oracle = page.locator(f'flt-semantics[aria-label="{expected_msg}"]')
    assert oracle.is_visible(), f"Failed to reveal rejection for {case_id}"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"tc18_{case_id}.png"))
