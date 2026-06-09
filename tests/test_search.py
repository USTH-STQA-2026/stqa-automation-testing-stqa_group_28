"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    ✅ COMPLETED (*HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # TODO: 
    # Arrange: Log in
    login(page, test_config)

    # Act: Input search query
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Smart Wait: wait for the results to load
    wait_for_flutter(page, text="Flutter")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_name_flutter.png"))

    # Assert: at least 1 book containing "Flutter" is displayed
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert results.count() > 0 or "Flutter" in sem_text, (
        "No books found for keyword 'Flutter' — expected at least BOOK001"
    )
    
def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    ✅ COMPLETED (*HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # TODO: 
    # Arrange: Log in
    login(page, test_config)

    # Act: Enter non-existent keyword
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345",
    )

    # Smart Wait: wait for system to process
    wait_for_flutter(page, text="Không tìm thấy")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_no_result.png"))

    # Assert: no book cards shown, or "Không tìm thấy" message is displayed
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_no_books = book_cards.count() == 0
    has_message = "Không tìm thấy" in sem_text
    assert has_no_books or has_message, (
        f"Expected empty result or 'Không tìm thấy' message. "
        f"Book cards found: {book_cards.count()}"
    )

def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    ✅ COMPLETED (*HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
        - Get book list: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
          (*Lấy danh sách sách*)
        - Loop through each book, verify aria-label contains "Công nghệ"
          (*Lặp qua từng sách, kiểm tra aria-label chứa "Công nghệ"*)
    """
    # TODO:     
    # Arrange: Log in
    login(page, test_config)

    # Act: Enter category to filter
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ",
    )

    # Smart Wait: wait for the list to update
    wait_for_flutter(page, text="Công nghệ")
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "filter_by_category_cong_nghe.png")
    )

    # Assert: all displayed book cards belong to "Công nghệ"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()
    assert count > 0, "No books found after filtering by 'Công nghệ'"

    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, (
            f"Book at index {i} does NOT belong to 'Công nghệ'. aria-label: '{label}'"
        )

def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    ✅ COMPLETED (*HOÀN THÀNH*)
    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # TODO: 
    # Arrange: Log in
    login(page, test_config)

    # Act: Search by author name
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức",
    )

    # Smart Wait: wait for results to load
    wait_for_flutter(page, text="Nguyễn Minh Đức")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert: at least 1 book by "Nguyễn Minh Đức" is displayed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0 or "Nguyễn Minh Đức" in sem_text, (
        "No results found for author 'Nguyễn Minh Đức' — expected BOOK001, BOOK009"
    )

# ---------------------------------------------------------------------------
# BONUS B1 — Extra TC: Case-insensitive search
# REQ-03 requires search to be case-insensitive
# ---------------------------------------------------------------------------

def test_search_case_insensitive(page, test_config):
    """BONUS TC-Extra-02: Case-insensitive search

    REQ-03: Search must be case-insensitive.
    Searching for 'FLUTTER' should yield the same results as searching for 'Flutter'.

    Expected: Books containing 'Flutter' are displayed.
    Actual (BUG-AUTO-01): System returns 'Không tìm thấy sách nào' — case-sensitive bug.

    RIPR:
        [R] Log in, navigate to Books tab (books with 'Flutter' exist in system)
        [I] Enter 'FLUTTER' (all uppercase) into the search bar
        [P] System processes the search query
        [R] Assert books containing 'Flutter' are shown (REQ-03 requires case-insensitive)
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Search using ALL UPPERCASE to test case-insensitivity
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "FLUTTER")

    # [P] Smart Wait: wait for the system to respond.
    # If REQ-03 is satisfied: "Flutter" books appear → wait succeeds.
    # If BUG-AUTO-01 exists: "Không tìm thấy sách nào" appears → wait on that instead.
    try:
        page.locator(
            'flt-semantics[aria-label*="Flutter"], flt-semantics:has-text("Không tìm thấy")'
        ).first.wait_for(state="attached", timeout=10000)
    except Exception:
        page.wait_for_timeout(2000)  # fallback wait

    # Always capture screenshot regardless of result (evidence of bug or pass)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_case_insensitive.png"))

    # [R] Assert: books with 'Flutter' must be visible (REQ-03 case-insensitive requirement)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Flutter" in sem_text, (
        "Search 'FLUTTER' (uppercase) should still find 'Flutter' books — "
        "REQ-03 requires case-insensitive search. "
        "BUG-AUTO-01: System is case-sensitive, 'FLUTTER' returns no results."
    )
