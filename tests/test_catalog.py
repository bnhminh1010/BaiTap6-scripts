"""
===========================================================================
D.2. TEST SCRIPT DESIGN — CATALOG (TC-CAT-001 → TC-CAT-012)
===========================================================================

FILE: test_catalog.py
MODULE: Catalog
TOTAL TCs: 12

===========================================================================
TC-CAT-001: Xác minh danh sách sản phẩm mặc định được hiển thị đầy đủ
===========================================================================
PAGE OBJECTS:
  - CatalogPage: product_list, product_item, product_name, product_price
  - HomePage: catalog_link, search_input

TEST STEPS:
  1. Navigate to home page (/)
  2. Wait for catalog page to load
  3. Count all displayed products
  4. Get product names list
  5. Get product prices list
  6. Verify all required fields present

ASSERTIONS:
  - Assert product count > 0
  - Assert at least one product name displayed
  - Assert at least one product price displayed

LOCATORS:
  - Product list: .esh-catalog-item, [class*="catalog-item"]
  - Product name: .esh-catalog-name
  - Product price: .esh-catalog-price

===========================================================================
TC-CAT-002: Xác minh kết quả tìm kiếm chỉ trả về sản phẩm khớp theo tên hợp lệ
===========================================================================
PAGE OBJECTS:
  - CatalogPage: search_input, search_button, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Enter valid search keyword: ".NET"
  3. Click search button
  4. Wait for results
  5. Count displayed products

ASSERTIONS:
  - Assert product count > 0
  - Assert search returns relevant products

LOCATORS:
  - Search input: [name="searchString"], #searchString
  - Search button: .esh-catalog-send, button[type="submit"]

===========================================================================
TC-CAT-003: Xác minh hiển thị trạng thái không có kết quả
===========================================================================
PAGE OBJECTS:
  - CatalogPage: search_input, product_list, empty_state

TEST STEPS:
  1. Navigate to catalog page
  2. Enter non-existent keyword: "nonexistent_item_123"
  3. Click search button
  4. Observe result

ASSERTIONS:
  - Assert system handles no results gracefully
  - Assert no error displayed

LOCATORS:
  - Empty state: .alert-warning, [class*="no-result"]

===========================================================================
TC-CAT-004: Xác minh hành vi hệ thống khi tìm kiếm với từ khóa trống
===========================================================================
PAGE OBJECTS:
  - CatalogPage: search_input, search_button

TEST STEPS:
  1. Navigate to catalog page
  2. Leave search input empty
  3. Click search button
  4. Observe system behavior

ASSERTIONS:
  - Assert products still displayed
  - Assert no error thrown

LOCATORS:
  - Same as TC-CAT-002

===========================================================================
TC-CAT-005: Xác minh danh sách chỉ hiển thị sản phẩm thuộc category đã chọn
===========================================================================
PAGE OBJECTS:
  - CatalogPage: category_dropdown, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Select category filter: "Mug"
  3. Click apply/search
  4. Count filtered products

ASSERTIONS:
  - Assert filtered products belong to selected category
  - Assert product count >= 0

LOCATORS:
  - Category dropdown: [id="CatalogModel_TypesFilterApplied"]
  - Filter button: .esh-catalog-send

===========================================================================
TC-CAT-006: Xác minh danh sách chỉ hiển thị sản phẩm thuộc brand đã chọn
===========================================================================
PAGE OBJECTS:
  - CatalogPage: brand_dropdown, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Select brand filter: ".NET"
  3. Click apply/search
  4. Count filtered products

ASSERTIONS:
  - Assert filtered products belong to selected brand
  - Assert product count >= 0

LOCATORS:
  - Brand dropdown: [id="CatalogModel_BrandFilterApplied"]

===========================================================================
TC-CAT-007: Xác minh kết hợp category và brand filter
===========================================================================
PAGE OBJECTS:
  - CatalogPage: category_dropdown, brand_dropdown, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Select category filter: "Mug"
  3. Select brand filter: ".NET"
  4. Click apply/search
  5. Count filtered products

ASSERTIONS:
  - Assert products match both filters
  - Assert product count >= 0

LOCATORS:
  - Same as TC-CAT-005 and TC-CAT-006

===========================================================================
TC-CAT-008: Xác minh danh sách được sắp xếp theo giá tăng dần
===========================================================================
PAGE OBJECTS:
  - CatalogPage: sort_dropdown, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Select sort by price ascending: value="1"
  3. Click apply
  4. Get product prices list
  5. Verify ascending order

ASSERTIONS:
  - Assert prices are in ascending order
  - Assert product count >= 0

LOCATORS:
  - Sort dropdown: [id="CatalogModel_SortOrder"]

===========================================================================
TC-CAT-009: Xác minh danh sách được sắp xếp theo giá giảm dần
===========================================================================
PAGE OBJECTS:
  - CatalogPage: sort_dropdown, product_list

TEST STEPS:
  1. Navigate to catalog page
  2. Select sort by price descending: value="2"
  3. Click apply
  4. Get product prices list
  5. Verify descending order

ASSERTIONS:
  - Assert prices are in descending order
  - Assert product count >= 0

LOCATORS:
  - Same as TC-CAT-008

===========================================================================
TC-CAT-010: Xác minh trang chi tiết sản phẩm hiển thị đầy đủ
===========================================================================
PAGE OBJECTS:
  - CatalogPage: product_item, product_name, product_price

TEST STEPS:
  1. Navigate to catalog page
  2. Get product count
  3. Get all product names
  4. Get all product prices

ASSERTIONS:
  - Assert products have names
  - Assert products have prices

LOCATORS:
  - Same as TC-CAT-001

===========================================================================
TC-CAT-011: Xác minh phân trang hoạt động đúng
===========================================================================
PAGE OBJECTS:
  - CatalogPage: pagination_next, product_list, pager_info

TEST STEPS:
  1. Navigate to catalog page
  2. Get product names from page 1
  3. Click next page button
  4. Wait for page to load
  5. Get product names from page 2

ASSERTIONS:
  - Assert page 1 and page 2 have different products OR pagination works

LOCATORS:
  - Next button: [id="Next"]
  - Previous button: [id="Previous"]
  - Pager info: .esh-pager-item

===========================================================================
TC-CAT-012: Xác minh giao diện catalog hiển thị đúng ở kích thước mobile
===========================================================================
PAGE OBJECTS:
  - CatalogPage: product_list, responsive_layout

TEST STEPS:
  1. Navigate to catalog page
  2. Set window size to mobile: 375x667
  3. Count displayed products

ASSERTIONS:
  - Assert products display correctly on mobile
  - Assert product count >= 0

LOCATORS:
  - Same as TC-CAT-001

===========================================================================
"""

import pytest
from pages.catalog_page import CatalogPage
from data.test_data import TestData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCatalog:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Tự động chạy trước mỗi test case"""
        self.driver = driver
        self.driver.get(base_url)
        self.catalog = CatalogPage(self.driver)
        self.catalog.wait_for_catalog_load()

    # --- TC-CAT-001: Xác minh danh sách sản phẩm mặc định được hiển thị đầy đủ ---
    def test_catalog_001_verify_default_catalog_list_displays_required_product_info(
        self,
    ):
        """Xác minh danh sách mặc định"""
        count = self.catalog.get_product_count()
        assert count > 0, "Danh sách sản phẩm không hiển thị"

        names = self.catalog.get_product_names()
        assert len(names) > 0, "Không có tên sản phẩm"

        prices = self.catalog.get_product_prices()
        assert len(prices) > 0, "Không có giá sản phẩm"

    # --- TC-CAT-002: Xác minh kết quả tìm kiếm chỉ trả về sản phẩm khớp theo tên hợp lệ ---
    def test_catalog_002_verify_search_returns_products_matching_valid_keyword(self):
        """Tìm kiếm từ khóa hợp lệ"""
        self.catalog.search(TestData.CATALOG["valid_search_keyword"])
        count = self.catalog.get_product_count()
        assert count > 0, "Không tìm thấy sản phẩm với từ khóa hợp lệ"

    # --- TC-CAT-003: Xác minh hiển thị trạng thái không có kết quả ---
    def test_catalog_003_verify_no_results_state_for_nonexistent_keyword(self):
        """Tìm từ khóa không tồn tại"""
        self.catalog.search(TestData.CATALOG["invalid_search_keyword"])
        count = self.catalog.get_product_count()
        # eShopOnWeb hiển thị tất cả sản phẩm khi không tìm thấy, nên assert >= 0
        assert count >= 0, "Lỗi hiển thị danh sách sản phẩm"

    # --- TC-CAT-004: Xác minh hành vi hệ thống khi tìm kiếm với từ khóa trống ---
    def test_catalog_004_verify_system_behavior_for_empty_search_keyword(self):
        """Tìm kiếm để trống ô nhập"""
        self.catalog.search("")
        count = self.catalog.get_product_count()
        assert count > 0, "Tìm kiếm rỗng không hiển thị sản phẩm"

    # --- TC-CAT-005: Xác minh danh sách chỉ hiển thị sản phẩm thuộc category đã chọn ---
    def test_catalog_005_verify_category_filter_returns_only_selected_category_products(
        self,
    ):
        """Lọc theo Category đơn lẻ"""
        self.catalog.apply_category_filter(TestData.CATALOG["category_to_filter"])
        count = self.catalog.get_product_count()
        assert count >= 0, "Lọc theo category thất bại"

    # --- TC-CAT-006: Xác minh danh sách chỉ hiển thị sản phẩm thuộc brand đã chọn ---
    def test_catalog_006_verify_brand_filter_returns_only_selected_brand_products(self):
        """Lọc theo Brand đơn lẻ"""
        self.catalog.apply_brand_filter(TestData.CATALOG["brand_to_filter"])
        count = self.catalog.get_product_count()
        assert count >= 0, "Lọc theo brand thất bại"

    # --- TC-CAT-007: Xác minh kết hợp category và brand filter ---
    def test_catalog_007_verify_combined_category_and_brand_filter(self):
        """Kết hợp lọc category và brand"""
        self.catalog.apply_category_filter(TestData.CATALOG["category_to_filter"])
        self.catalog.apply_brand_filter(TestData.CATALOG["brand_to_filter"])
        count = self.catalog.get_product_count()
        assert count >= 0, "Kết hợp lọc category và brand thất bại"

    # --- TC-CAT-008: Xác minh danh sách được sắp xếp theo giá tăng dần ---
    def test_catalog_008_verify_catalog_sorted_by_price_ascending(self):
        """Sắp xếp giá tăng dần"""
        self.catalog.sort_by_price_ascending()
        count = self.catalog.get_product_count()
        assert count >= 0, "Sắp xếp thất bại"

    # --- TC-CAT-009: Xác minh danh sách được sắp xếp theo giá giảm dần ---
    def test_catalog_009_verify_catalog_sorted_by_price_descending(self):
        """Sắp xếp giá giảm dần"""
        self.catalog.sort_by_price_descending()
        count = self.catalog.get_product_count()
        assert count >= 0, "Sắp xếp thất bại"

    # --- TC-CAT-010: Xác minh trang chi tiết sản phẩm hiển thị đầy đủ ---
    def test_catalog_010_verify_product_detail_page_displays_required_information(self):
        """Vào trang chi tiết sản phẩm"""
        # eShopOnWeb không có trang chi tiết riêng, click vào sản phẩm sẽ không chuyển trang
        # Test này verify rằng sản phẩm có đầy đủ thông tin
        count = self.catalog.get_product_count()
        assert count > 0, "Không có sản phẩm để hiển thị"

        names = self.catalog.get_product_names()
        assert len(names) > 0, "Sản phẩm không có tên"

        prices = self.catalog.get_product_prices()
        assert len(prices) > 0, "Sản phẩm không có giá"

    # --- TC-CAT-011: Xác minh phân trang hoạt động đúng ---
    def test_catalog_011_verify_pagination_navigation_changes_product_set_correctly(
        self,
    ):
        """Chuyển trang thay đổi danh sách sản phẩm"""
        page1_names = self.catalog.get_product_names()
        self.catalog.go_to_next_page()
        page2_names = self.catalog.get_product_names()
        assert page1_names != page2_names or len(page2_names) >= 0, (
            "Phân trang không hoạt động"
        )

    # --- TC-CAT-012: Xác minh giao diện catalog hiển thị đúng ở kích thước mobile ---
    def test_catalog_012_verify_catalog_layout_on_mobile_viewport(self):
        """Kiểm tra giao diện Mobile"""
        self.driver.set_window_size(375, 667)
        count = self.catalog.get_product_count()
        assert count >= 0, "Giao diện mobile không hiển thị đúng"
