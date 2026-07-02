# Exploratory Data Analysis (EDA) Report

# Phiên bản Tiếng Việt

## 1. Tổng quan Dataset

Dataset gồm:

- 5,000,000 giao dịch
- 45 thuộc tính

Kiểu dữ liệu:

| Kiểu dữ liệu | Số lượng |
| ------------ | -------: |
| Integer      |       19 |
| Float        |       13 |
| Category     |       10 |
| Datetime     |        1 |
| String       |        2 |

### Missing Values

Có 2 cột chứa giá trị thiếu:

| Feature                     | Ghi chú                               |
| --------------------------- | ------------------------------------- |
| fraud_type                  | Chỉ có giá trị khi giao dịch là Fraud |
| time_since_last_transaction | Có missing values                     |

---

## 2. Fraud Distribution

Tổng số giao dịch Fraud:

- **179,553** giao dịch
- **3.5911%**

Tổng số giao dịch Non-Fraud:

- **4,820,447** giao dịch
- **96.4089%**

Dataset gồm **3 loại Fraud**:

- Account Takeover
- Identity Fraud
- Impossible Travel Fraud

Dataset bị mất cân bằng (imbalanced), với tỷ lệ Fraud chỉ khoảng **3.6%**.

---

## 3. Phân bố dữ liệu

### Transaction Type

Có 4 loại giao dịch.

| Transaction Type | Non-Fraud |  Fraud |
| ---------------- | --------: | -----: |
| Transfer         | 1,205,006 | 45,328 |
| Withdrawal       | 1,203,761 | 44,874 |
| Deposit          | 1,205,807 | 44,786 |
| Payment          | 1,205,873 | 44,565 |

Deposit là loại giao dịch xuất hiện nhiều nhất với **1,250,593** giao dịch.

Phân bố Fraud giữa các transaction type gần như đồng đều.

---

### Payment Channel

Có 4 phương thức thanh toán.

| Payment Channel | Non-Fraud |  Fraud |
| --------------- | --------: | -----: |
| USSD            | 1,204,447 | 45,108 |
| Mobile App      | 1,205,965 | 44,882 |
| Card            | 1,203,600 | 44,834 |
| Bank Transfer   | 1,206,435 | 44,729 |

Bank Transfer là phương thức xuất hiện nhiều nhất (**1,251,164** giao dịch).

Fraud phân bố tương đối đồng đều giữa các payment channel.

---

### Device Used

| Device | Non-Fraud |  Fraud |
| ------ | --------: | -----: |
| ATM    | 1,204,423 | 45,217 |
| POS    | 1,204,306 | 44,852 |
| Web    | 1,205,264 | 44,807 |
| Mobile | 1,206,454 | 44,677 |

Fraud không tập trung vào một thiết bị cụ thể.

---

### Sender Persona

Có 3 nhóm người gửi:

| Persona       |  Fraud |
| ------------- | -----: |
| Student       | 60,083 |
| Trader        | 59,856 |
| Salary Earner | 59,614 |

Số lượng Fraud của ba nhóm gần như tương đương.

---

### Merchant Category

Dataset có 21 Merchant Category.

Merchant xuất hiện nhiều nhất là:

- Other Transaction: **1,251,802**

Các merchant tiếp theo:

- Bet9ja Stake
- Arik Air Flight
- SPAR Purchase
- POS Withdrawal
- ABC Transport Ticket
- SportyBet Deposit
- Shoprite Purchase
- Bolt Ride
- Local Market Purchase

Mỗi merchant này đều có khoảng **208 nghìn** giao dịch.

---

### Location

Dataset gồm 10 địa điểm.

Top Location có nhiều Fraud nhất:

| Location      |  Fraud |
| ------------- | -----: |
| Kaduna        | 18,256 |
| Abuja         | 18,163 |
| Kano          | 18,037 |
| Onitsha       | 18,033 |
| Benin City    | 17,994 |
| Lagos         | 17,895 |
| Ibadan        | 17,859 |
| Enugu         | 17,825 |
| Aba           | 17,771 |
| Port Harcourt | 17,720 |

Số lượng Fraud giữa các địa điểm khá đồng đều.

---

## 4. Phân tích theo thời gian

Số lượng giao dịch tập trung nhiều nhất trong khoảng:

- **09:00 - 17:00**

Trung bình khoảng:

- **388,500 giao dịch mỗi giờ**

Ngoài khoảng thời gian này, số lượng giao dịch dao động quanh **100,000 giao dịch mỗi giờ**.

Fraud cũng xuất hiện nhiều hơn trong khoảng thời gian từ **09:00 đến 17:00**, phù hợp với thời điểm có nhiều giao dịch hơn.

---

## 5. Địa chỉ IP

Địa chỉ IP có số lượng Fraud cao nhất ghi nhận:

- **24 giao dịch Fraud**

Không có IP nào chiếm tỷ lệ Fraud vượt trội.

---

## 6. Phân bố Amount

Biến **amount_ngn** có phân phối lệch phải (right-skewed).

| Statistic |          Value |
| --------- | -------------: |
| Mean      | 748,292.44 NGN |
| Median    | 163,810.03 NGN |

Mean lớn hơn nhiều so với Median, cho thấy tồn tại một số giao dịch có giá trị rất lớn.

---

## 7. Correlation với is_fraud

Hầu hết các biến số có hệ số tương quan Pearson rất thấp với biến mục tiêu.

Feature có tương quan lớn nhất:

| Feature                | Correlation |
| ---------------------- | ----------: |
| new_device_transaction |       0.090 |
| user_txn_count_total   |       0.018 |
| txn_count_last_1h      |       0.009 |
| user_txn_frequency_24h |       0.009 |
| txn_count_last_24h     |       0.009 |

Các feature còn lại đều có hệ số tương quan gần bằng 0.

Điều này cho thấy không có một biến số đơn lẻ nào có mối quan hệ tuyến tính mạnh với Fraud.

---

## 8. Correlation theo Fraud Type

Phân tích theo từng loại Fraud cho thấy:

### Account Takeover

Feature có tương quan cao nhất:

- new_device_transaction (0.09)

Các feature như:

- user_txn_count_total
- txn_count_last_1h
- txn_count_last_24h
- user_txn_frequency_24h

đều có tương quan dương nhưng nhỏ.

---

### Identity Fraud

Feature nổi bật:

- bvn_linked (-0.19)

Ngoài ra không có feature nào có tương quan đáng kể.

---

### Impossible Travel Fraud

Feature nổi bật:

- geospatial_velocity_anomaly (0.18)

Các feature còn lại đều có tương quan gần bằng 0.

---

## 9. Một số nhận xét

- Dataset có tỷ lệ Fraud thấp (3.59%).
- Fraud phân bố khá đồng đều giữa transaction type, payment channel, device và sender persona.
- Fraud xảy ra nhiều hơn trong khung giờ có nhiều giao dịch (09:00–17:00).
- amount_ngn có phân phối lệch phải.
- Không có feature đơn lẻ nào có tương quan tuyến tính mạnh với is_fraud.
- Một số feature có liên hệ rõ hơn với từng Fraud Type, bao gồm:
  - new_device_transaction đối với Account Takeover.
  - bvn_linked đối với Identity Fraud.
  - geospatial_velocity_anomaly đối với Impossible Travel Fraud.

---

# Exploratory Data Analysis (EDA) Report

# English version

## 1. Dataset Overview

The dataset contains:

- 5,000,000 transactions
- 45 features

Data types:

| Data Type | Count |
| --------- | ----: |
| Integer   |    19 |
| Float     |    13 |
| Category  |    10 |
| Datetime  |     1 |
| String    |     2 |

### Missing Values

Two columns contain missing values:

| Feature                     | Description                        |
| --------------------------- | ---------------------------------- |
| fraud_type                  | Missing for Non-Fraud transactions |
| time_since_last_transaction | Contains missing values            |

---

## 2. Fraud Distribution

Total Fraud transactions:

- **179,553**
- **3.5911%**

Total Non-Fraud transactions:

- **4,820,447**
- **96.4089%**

The dataset contains three fraud categories:

- Account Takeover
- Identity Fraud
- Impossible Travel Fraud

The dataset is imbalanced, with Fraud accounting for only **3.59%** of all transactions.

---

## 3. Data Distribution

### Transaction Type

There are four transaction types.

| Transaction Type | Non-Fraud |  Fraud |
| ---------------- | --------: | -----: |
| Transfer         | 1,205,006 | 45,328 |
| Withdrawal       | 1,203,761 | 44,874 |
| Deposit          | 1,205,807 | 44,786 |
| Payment          | 1,205,873 | 44,565 |

Deposit is the most common transaction type with **1,250,593** transactions.

Fraud cases are distributed relatively evenly across transaction types.

---

### Payment Channel

Four payment channels are included.

| Payment Channel | Non-Fraud |  Fraud |
| --------------- | --------: | -----: |
| USSD            | 1,204,447 | 45,108 |
| Mobile App      | 1,205,965 | 44,882 |
| Card            | 1,203,600 | 44,834 |
| Bank Transfer   | 1,206,435 | 44,729 |

Bank Transfer is the most frequently used payment channel (**1,251,164** transactions).

Fraud is evenly distributed across payment channels.

---

### Device Used

| Device | Non-Fraud |  Fraud |
| ------ | --------: | -----: |
| ATM    | 1,204,423 | 45,217 |
| POS    | 1,204,306 | 44,852 |
| Web    | 1,205,264 | 44,807 |
| Mobile | 1,206,454 | 44,677 |

No device shows a significantly higher fraud frequency than the others.

---

### Sender Persona

Three sender personas are included.

| Persona       |  Fraud |
| ------------- | -----: |
| Student       | 60,083 |
| Trader        | 59,856 |
| Salary Earner | 59,614 |

Fraud counts are nearly identical across all sender personas.

---

### Merchant Category

The dataset contains 21 merchant categories.

The largest category is:

- Other Transaction: **1,251,802** transactions

Other major merchants include:

- Bet9ja Stake
- Arik Air Flight
- SPAR Purchase
- POS Withdrawal
- ABC Transport Ticket
- SportyBet Deposit
- Shoprite Purchase
- Bolt Ride
- Local Market Purchase

Each records approximately **208 thousand** transactions.

---

### Location

Ten locations are included.

Top locations with the highest fraud counts:

| Location      |  Fraud |
| ------------- | -----: |
| Kaduna        | 18,256 |
| Abuja         | 18,163 |
| Kano          | 18,037 |
| Onitsha       | 18,033 |
| Benin City    | 17,994 |
| Lagos         | 17,895 |
| Ibadan        | 17,859 |
| Enugu         | 17,825 |
| Aba           | 17,771 |
| Port Harcourt | 17,720 |

Fraud counts are relatively balanced across all locations.

---

## 4. Transaction Time

Transaction activity is highest between:

- **09:00 and 17:00**

with an average of approximately:

- **388,500 transactions per hour**

Outside this period, hourly transaction counts remain relatively stable at around **100,000 transactions**.

Fraud transactions also occur more frequently during the same period due to the higher transaction volume.

---

## 5. IP Address

The highest fraud count recorded for a single IP address is:

- **24 fraud transactions**

No individual IP address dominates fraud activity.

---

## 6. Transaction Amount Distribution

The **amount_ngn** variable is right-skewed.

| Statistic |          Value |
| --------- | -------------: |
| Mean      | 748,292.44 NGN |
| Median    | 163,810.03 NGN |

The mean is substantially larger than the median, indicating the presence of high-value transactions.

---

## 7. Correlation with is_fraud

Most numerical features have very weak Pearson correlations with the target variable.

Top correlated features include:

| Feature                | Correlation |
| ---------------------- | ----------: |
| new_device_transaction |       0.090 |
| user_txn_count_total   |       0.018 |
| txn_count_last_1h      |       0.009 |
| user_txn_frequency_24h |       0.009 |
| txn_count_last_24h     |       0.009 |

All remaining numerical features have correlations close to zero.

This indicates that no single feature has a strong linear relationship with fraud.

---

## 8. Correlation by Fraud Type

### Account Takeover

The strongest numerical feature is:

- new_device_transaction (0.09)

Small positive correlations are also observed for:

- user_txn_count_total
- txn_count_last_1h
- txn_count_last_24h
- user_txn_frequency_24h

---

### Identity Fraud

The most notable feature is:

- bvn_linked (-0.19)

Other numerical features show negligible correlations.

---

### Impossible Travel Fraud

The strongest feature is:

- geospatial_velocity_anomaly (0.18)

All remaining numerical features have correlations close to zero.

---

## 9. Summary

- The dataset is highly imbalanced, with only **3.59%** Fraud transactions.
- Fraud is evenly distributed across transaction types, payment channels, devices, and sender personas.
- Most fraud occurs during peak transaction hours (09:00–17:00).
- Transaction amounts exhibit a right-skewed distribution.
- No numerical feature has a strong linear correlation with **is_fraud**.
- Different fraud types are associated with different features:
  - **new_device_transaction** for Account Takeover.
  - **bvn_linked** for Identity Fraud.
  - **geospatial_velocity_anomaly** for Impossible Travel Fraud.
