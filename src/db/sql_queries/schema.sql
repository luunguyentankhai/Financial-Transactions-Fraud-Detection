-- Xóa các bảng nếu đã tồn tại (Xóa bảng Fact trước, các bảng Dimension sau)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS devices CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- Xóa các kiểu dữ liệu ENUM nếu đã tồn tại
DROP TYPE IF EXISTS txn_type_enum CASCADE;
DROP TYPE IF EXISTS payment_channel_enum CASCADE;
DROP TYPE IF EXISTS fraud_type_enum CASCADE;
-- ==============================================================================
-- KHỞI TẠO CÁC KIỂU DỮ LIỆU (ENUM)
-- Giúp tiết kiệm dung lượng và tăng tốc độ filter thay vì dùng VARCHAR
-- ==============================================================================

CREATE TYPE txn_type_enum AS ENUM ('deposit', 'payment', 'withdrawal', 'transfer');
CREATE TYPE payment_channel_enum AS ENUM ('USSD', 'Bank Transfer', 'Mobile App', 'Card');
CREATE TYPE fraud_type_enum AS ENUM ('Account Takeover', 'Identity Fraud', 'Impossible Travel Fraud', 'Other'); -- Thêm 'Other' dự phòng

-- ==============================================================================
-- TẠO CÁC BẢNG LƯU TRỮ (DIMENSION TABLES)
-- ==============================================================================

-- 1. Bảng quản lý Tài khoản (Bao gồm cả người gửi và người nhận)
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY,
    bvn_linked BOOLEAN NOT NULL,
    sender_persona VARCHAR(50) NOT NULL,
    user_txn_count_total INT NOT NULL,
    user_avg_txn_amt DOUBLE PRECISION NOT NULL,
    user_std_txn_amt DOUBLE PRECISION NOT NULL,
    user_txn_frequency_24h INT NOT NULL,
    user_top_category VARCHAR(100) NOT NULL,
    persona_fraud_risk DOUBLE PRECISION NOT NULL
);

-- 2. Bảng quản lý Thiết bị
CREATE TABLE devices (
    device_hash VARCHAR(8) PRIMARY KEY,
    device_used VARCHAR(100) NOT NULL,
    device_seen_count INT NOT NULL,
    is_device_shared INT NOT NULL -- Giữ nguyên kiểu INT như data raw thay vì Boolean
);

-- 3. Bảng quản lý Vị trí và IP mạng
CREATE TABLE locations (
    ip_address VARCHAR(15) PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    ip_geo_region VARCHAR(100) NOT NULL,
    ip_seen_count INT NOT NULL,
    is_ip_shared INT NOT NULL,
    location_fraud_risk DOUBLE PRECISION NOT NULL
);

-- ==============================================================================
-- TẠO BẢNG TRUNG TÂM (FACT TABLE)
-- ==============================================================================

-- 4. Bảng Giao dịch (Liên kết với các bảng trên qua Foreign Keys)
CREATE TABLE transactions (
    transaction_id VARCHAR(8) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    
    -- Khóa ngoại
    sender_account BIGINT NOT NULL REFERENCES accounts(account_id),
    receiver_account BIGINT NOT NULL REFERENCES accounts(account_id),
    device_hash VARCHAR(8) NOT NULL REFERENCES devices(device_hash),
    ip_address VARCHAR(15) NOT NULL REFERENCES locations(ip_address),
    
    -- Thông tin giao dịch cơ bản
    transaction_type txn_type_enum NOT NULL,
    payment_channel payment_channel_enum NOT NULL,
    merchant_category VARCHAR(100) NOT NULL,
    amount_ngn DOUBLE PRECISION NOT NULL,
    
    -- Nhãn và Phân loại Gian lận
    is_fraud BOOLEAN NOT NULL,
    fraud_type fraud_type_enum, -- Được phép NULL (như kết quả test: 4.8 triệu dòng Null)
    
    -- Các chỉ số thời gian & rủi ro động của phiên giao dịch
    time_since_last_transaction DOUBLE PRECISION, -- Được phép NULL (như kết quả test: 896,513 dòng Null)
    spending_deviation_score DOUBLE PRECISION NOT NULL,
    velocity_score INT NOT NULL,
    geo_anomaly_score DOUBLE PRECISION NOT NULL,
    new_device_transaction BOOLEAN NOT NULL,
    geospatial_velocity_anomaly BOOLEAN NOT NULL,
    txn_hour INT NOT NULL,
    is_weekend INT NOT NULL,
    is_salary_week INT NOT NULL,
    is_night_txn INT NOT NULL,
    
    -- Các chỉ số thống kê lăn (Rolling stats) tại thời điểm xảy ra giao dịch
    txn_count_last_1h INT NOT NULL,
    txn_count_last_24h INT NOT NULL,
    total_amount_last_1h DOUBLE PRECISION NOT NULL,
    time_since_last DOUBLE PRECISION NOT NULL,
    avg_gap_between_txns DOUBLE PRECISION NOT NULL,
    merchant_fraud_rate DOUBLE PRECISION NOT NULL,
    channel_risk_score DOUBLE PRECISION NOT NULL
);

-- ==============================================================================
-- TẠO CHỈ MỤC (INDEXES) ĐỂ TỐI ƯU TRUY VẤN
-- Hỗ trợ join bảng và trích xuất dữ liệu nhanh hơn khi cần query train model
-- ==============================================================================

CREATE INDEX idx_txn_sender ON transactions(sender_account);
CREATE INDEX idx_txn_receiver ON transactions(receiver_account);
CREATE INDEX idx_txn_device ON transactions(device_hash);
CREATE INDEX idx_txn_ip ON transactions(ip_address);
CREATE INDEX idx_txn_timestamp ON transactions(timestamp);
CREATE INDEX idx_txn_is_fraud ON transactions(is_fraud);
