class Config:
    # URL của ứng dụng Web đang chạy
    BASE_URL = "http://localhost:5001"

    # Thời gian chờ mặc định cho Explicit Wait
    TIMEOUT = 10

    # Cấu hình trình duyệt (có thể thêm 'firefox', 'edge')
    BROWSER = "chrome"

    # Chế độ chạy ẩn danh hoặc không hiện trình duyệt (Headless)
    HEADLESS = False
