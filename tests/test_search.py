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
    # [R] Reachability: Đăng nhập và truy cập danh sách sách [3, 4]
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập từ khóa "Flutter" vào ô tìm kiếm [5, 6]
    search_keyword = "Flutter"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", search_keyword)

    # [P] Propagation: Đợi kết quả lan truyền ra UI (Smart Wait) [5, 7]
    # Chờ cho đến khi sách mục tiêu xuất hiện trên CanvasKit
    wait_for_flutter(page, text="Lập trình Flutter cơ bản")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc04_search_success.png"))

    # [R✓] Revealability: Strong Oracle (B3) kiểm tra cả Mã sách và Trạng thái [1, 8]
    # Dùng locator nhắm thẳng vào card sách qua aria-label để lấy thông tin chính xác
    book_card = page.locator('flt-semantics[role="group"][aria-label*="BOOK001"]')
    
    assert book_card.is_visible(), "Lỗi: Không tìm thấy card sách mã 'BOOK001'"
    
    # Kiểm tra Oracle mạnh: Card phải chứa cả tiêu đề và trạng thái 'Có sẵn' (theo ảnh 497)
    card_info = book_card.get_attribute("aria-label")
    assert "Lập trình Flutter cơ bản" in card_info, "Lỗi: Tiêu đề sách không khớp"
    assert "Có sẵn" in card_info or "Available" in card_info, "Lỗi: Trạng thái sách hiển thị sai"

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
    
    # [R] Reachability: Đăng nhập và bật semantics tree cho Flutter
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập từ khóa vào ô tìm kiếm theo REQ-03
    search_label = "Tìm kiếm theo tên sách hoặc tác giả..."
    flutter_fill(page, search_label, keyword)

    # [P] Propagation: Chờ kết quả cập nhật trên UI (Smart Wait)
    wait_for_flutter(page, text=expected_title)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"tc14_{tc_id}.png"))

    # [R✓] Revealability: Strong Oracle (B3) — Kiểm tra chính xác card sách qua aria-label
    # Không dùng all_text_contents() vì Flutter không render text vào DOM thông thường [2]
    book_card = page.locator(f'flt-semantics[role="group"][aria-label*="{expected_id}"]')
    
    # Kiểm tra sự hiện diện của card sách mục tiêu
    assert book_card.is_visible(), f"Lỗi: Không tìm thấy card sách có mã '{expected_id}'"
    
    # Oracle mạnh: Đọc thuộc tính aria-label để xác nhận cả ID và Tiêu đề trên cùng 1 card [4]
    card_info = book_card.get_attribute("aria-label")
    assert expected_title in card_info, f"Lỗi: Tiêu đề '{expected_title}' không khớp trong card '{expected_id}'"
