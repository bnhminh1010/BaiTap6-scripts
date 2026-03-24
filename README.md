# SeleniumTests Base Structure

## Structure

- `conftest.py`: Shared pytest fixtures (`driver`, `wait`, `base_url`)
- `pytest.ini`: Pytest config
- `pages/`: Page Object skeletons (`base_page`, `auth_page`, `catalog_page`, `cart_page`, `wishlist_page`, `checkout_page`)
- `pages/login_page.py`: Login page object sample (already implemented basic methods)
- `tests/test_auth_basic.py`: 2 basic authentication tests (runnable sample)
- `tests/test_auth.py`: Auth skeleton (12 test placeholders)
- `tests/test_catalog.py`: Catalog skeleton (12 test placeholders)
- `tests/test_cart.py`: Cart skeleton (12 test placeholders)
- `tests/test_wishlist.py`: Wishlist skeleton (12 test placeholders)
- `tests/test_checkout.py`: Checkout skeleton (12 test placeholders)
- `requirements.txt`: Python dependencies

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run tests

```bash
pytest -v
```

Or run with a custom base URL:

```bash
pytest -v --base-url http://localhost:5000
```
