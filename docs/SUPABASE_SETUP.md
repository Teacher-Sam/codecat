# Supabase 帳號與資料庫設定

專案：**Snakify Practice Platform**（`snakify_practice_platform`）

Java 與 C++ **共用同一 Supabase 專案**。題目進度以 `problem_id` 區分：

| 語言 | problem_id 範例 |
|------|-----------------|
| Java | `java-1-1`、`java-2-3` |
| C++ | `cpp-1-1` |

---

## 1. 建立 Supabase 專案

1. 前往 [https://supabase.com](https://supabase.com) 註冊
2. **New project** → 取名（如 `snakify-practice-platform`）
3. 等待建立完成

## 2. 建立資料表

1. **SQL Editor** → 貼上 `supabase/schema.sql` → **Run**

### 從舊版遷移（曾使用 `1-1` 無前綴）

若已有答題紀錄，再執行一次 `supabase/migrate-java-prefix.sql`。

## 3. 取得 API 金鑰

**Project Settings → API** → 複製 URL 與 **anon public** key。

## 4. 寫入各語言 config

`java/js/config.js` 與 `cpp/js/config.js` 填入相同 Supabase 設定。

```javascript
SUPABASE_URL: "https://xxxxx.supabase.co",
SUPABASE_ANON_KEY: "eyJhbGciOi...",
REQUIRE_LOGIN: true,
ACCESS_PASSWORD: "",
```

## 5. 關閉信箱驗證（建議小班使用）

**Authentication → Sign In / Providers → Email** → 關閉 **Confirm email** → Save

## 6. 忘記密碼（Redirect URLs）

**Authentication → URL Configuration**

**Site URL**（入口頁）：

```text
https://你的帳號.github.io/snakify_practice_platform/
```

**Redirect URLs**（本機 + 線上，Java + C++ 都要加）：

```text
http://localhost:8080/java/reset-password.html
http://localhost:8080/cpp/reset-password.html
https://你的帳號.github.io/snakify_practice_platform/java/reset-password.html
https://你的帳號.github.io/snakify_practice_platform/cpp/reset-password.html
```

或在各語言 `config.js` 設定 `PASSWORD_RESET_REDIRECT`。

## 7. 限制註冊（選用）

**Authentication → Settings** → 關閉 **Enable sign ups**

## 儲存欄位

| 欄位 | 說明 |
|------|------|
| `problem_id` | `java-1-3` 或 `cpp-1-1` |
| `solved` | 是否通過全部測試 |
| `code` | 使用者程式碼 |
| `updated_at` | 最後更新時間 |

## 未設定 Supabase 時

`SUPABASE_URL` 留空 → 進度僅存瀏覽器 localStorage。
