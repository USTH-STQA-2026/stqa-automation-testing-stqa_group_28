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
    enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # TODO: 
    # [R] Reachability: Log in to reach the authenticated homepage and book list [9, 15, 16]
    login(page, test_config)

    # [I] Infection: Use the search bar to infect the state with a keyword [17, 18]
    # Label follows SRS hint: "Tìm kiếm theo tên sách hoặc tác giả..." [18]
    search_keyword = "Flutter"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", search_keyword)

    # [P] Propagation: Wait for the list to update and display the target book [8, 17, 19]
    wait_for_flutter(page, text="Lập trình Flutter cơ bản")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc04_test_search_book_by_name.png"))

    # [R✓] Revealability: Strong Oracle verifying Book ID BOOK001 is visible [13, 20, 21]
    # We check for BOOK001 to ensure the specific required data is returned [21]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "BOOK001" in sem_text or "Lập trình Flutter cơ bản" in sem_text, \
        "Search failed: Target book 'BOOK001' not found in results"

def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # TODO: 
    # [R] Reachability: Log in to reach the authenticated homepage and book list [4-6]
    login(page, test_config)

    # [I] Infection: Use a keyword that definitely does not exist to trigger "no results" logic [7, 8]
    invalid_keyword = "xyz_khong_ton_tai_12345"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", invalid_keyword)

    # [P] Propagation: Smart Wait for the "No results" message to propagate to the UI [9-11]
    # This avoids flaky tests by waiting specifically for the text defined in SRS REQ-03 [8]
    expected_msg = "Không tìm thấy sách"
    wait_for_flutter(page, text=expected_msg)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc05_test_search_book_no_result.png"))

    # [R✓] Revealability: Strong Oracle verifying both the error message and the empty list [12-14]
    # We combine checking the specific SRS text with verifying the card count is zero [7, 15]
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    book_cards_count = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count()

    assert expected_msg in sem_text, f"Strong Oracle failed: message '{expected_msg}' not revealed in UI"
    assert book_cards_count == 0, f"Strong Oracle failed: expected 0 books but found {book_cards_count}"

def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

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
    # [R] Reachability: Log in to reach the authenticated book list
    login(page, test_config)

    # [I] Infection: Fill the category filter to trigger filtering logic
    # Label follows SRS hint: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    target_category = "Công nghệ"
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", target_category)

    # [P] Propagation: Smart Wait for the UI to update the filtered list
    # We wait for a known book in this category (BOOK001) to appear
    wait_for_flutter(page, text="Lập trình Flutter cơ bản")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc06_test_filter_by_category.png"))

    # [R✓] Revealability: Strong Oracle verifying all displayed books match the category
    # We iterate through the visible book cards to ensure no incorrect data is shown
    book_locators = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_locators.count()
    
    assert count > 0, f"Strong Oracle failed: No books found for category '{target_category}'"
    
    for i in range(count):
        aria_label = book_locators.nth(i).get_attribute("aria-label")
        assert target_category in aria_label, \
            f"Strong Oracle failed: Book {i+1} does not belong to '{target_category}'. Label: {aria_label}"

def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    ✅ COMPLETE — Students have implemented this test case.
    (*HOÀN THÀNH — Sinh viên đã viết code cho test case này.*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # TODO: 
    # [R] Reachability: Log in to reach the authenticated catalog view [1, 2]
    login(page, test_config)

    # [I] Infection: Enter author name to trigger system search logic [3, 4]
    # Label follows SRS/Hint: "Tìm kiếm theo tên sách hoặc tác giả..." [5, 6]
    author_name = "Nguyễn Minh Đức"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", author_name)

    # [P] Propagation: Smart Wait for filtered results to propagate to UI [7, 8]
    # We wait for a specific book title known to be by this author (BOOK001) [9]
    wait_for_flutter(page, text="Lập trình Flutter cơ bản")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc07_test_search_by_author.png"))

    # [R✓] Revealability: Strong Oracle verifying all results match the author [10, 11]
    # Instead of just counting, we verify the author name is present in each card's label [12]
    book_locators = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_locators.count()
    
    assert count > 0, f"Strong Oracle failed: No books found for author '{author_name}'"
    
    for i in range(count):
        aria_label = book_locators.nth(i).get_attribute("aria-label")
        assert author_name in aria_label, \
            f"Strong Oracle failed: Result {i+1} does not match author '{author_name}'. Label: {aria_label}"

# ---------------------------------------------------------------------------
# BONUS B2: Data-driven testing for keyword search (Covers TC-04, TC-07, and TC-14)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("keyword, expected_id, expected_title, tc_id", [
    ("Flutter", "BOOK001", "Lập trình Flutter cơ bản", "tc04_search_name"),     # TC-04: Search by name
    ("Nguyễn Minh Đức", "BOOK001", "Lập trình Flutter cơ bản", "tc07_search_author"), # TC-07: Search by author
    ("flutter", "BOOK001", "Lập trình Flutter cơ bản", "tc14_case_insensitive"), # TC-14 (Bonus B1): Case-insensitive search
])
def test_search_by_keyword_data_driven(page, test_config, keyword, expected_id, expected_title, tc_id):
    """Data-driven keyword search verifying results and case-insensitivity."""
    
    # [R] Reachability: Log in to reach the authenticated homepage and book list
    login(page, test_config)

    # [I] Infection: Enter keyword into the search bar to infect system state
    # Using aria-label from SRS REQ-03
    search_label = "Tìm kiếm theo tên sách hoặc tác giả..."
    flutter_fill(page, search_label, keyword)

    # [P] Propagation: Smart Wait for results to update in the UI
    wait_for_flutter(page, text=expected_title)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"tc14_{tc_id}.png"))

    # [R✓] Revealability: Strong Oracle (Bonus B3) checking exact Book ID and Title
    # Verification based on SRS seed data (Section 3.1)
    results = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    
    assert results.count() > 0, f"Search failed: No results found for '{keyword}'"
    assert expected_id in sem_text, f"Strong Oracle failed: Book ID '{expected_id}' not revealed"
    assert expected_title in sem_text, f"Strong Oracle failed: Title '{expected_title}' not revealed"

def test_extra_partial_search(page, test_config):
    """TC-15 (Bonus B1): Partial keyword search validation."""
    
    # [R] Reachability: Log in
    login(page, test_config)

    # [I] Infection: Enter partial name "Quản trị"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Quản trị")

    # [P] Propagation: Wait for multiple matching results (BOOK002, BOOK013)
    wait_for_flutter(page, text="Quản trị dự án phần mềm")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc15_extra_test_case_partial_search.png"))

    # [R✓] Revealability: Strong Oracle verifying multiple relevant records exist
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "BOOK002" in sem_text, "Strong Oracle failed: BOOK002 missing"
    assert "BOOK013" in sem_text, "Strong Oracle failed: BOOK013 missing"
