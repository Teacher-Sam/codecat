# Snakify Practice Platform

互動式程式練題平台（Monorepo），支援 **Java** 與 **C++**，可在瀏覽器寫程式、執行並自動測試。

專案 ID：`snakify_practice_platform`

適合小團體教學，**不需付費主機**（GitHub Pages + Judge0 / Piston + Supabase 免費方案）。

---

## 網站結構

```text
snakify_practice_platform/
├── index.html                  ← 語言選擇入口
├── java/                       ← Java 練題（第 1～4 章）
│   ├── index.html
│   ├── data/                   ← 題目 id：java-1-1、java-2-3、java-3-5 …
│   └── js/config.js
├── cpp/                        ← C++ 練題（第 1～11 章）
│   ├── index.html
│   ├── data/                   ← 題目 id：cpp-1-1 …
│   └── js/config.js
├── supabase/
│   ├── schema.sql
│   └── migrate-java-prefix.sql
├── scripts/
└── docs/SUPABASE_SETUP.md
```

**Supabase**：Java 與 C++ **共用同一專案、同一帳號**，但進度以 `problem_id` 前綴分開（`java-*` / `cpp-*`），互不干擾。

---

## 本機預覽

```powershell
cd d:\Project\snakify_practice_platform
python -m http.server 8080
```

| 頁面 | 網址 |
|------|------|
| 語言選擇 | http://localhost:8080/ |
| Java | http://localhost:8080/java/ |
| C++ | http://localhost:8080/cpp/ |

請用本地伺服器開啟，不要直接雙擊 `index.html`。

---

## 部署 GitHub Pages

1. Push 到 `main` 分支（見下方指令）
2. **Settings → Secrets and variables → Actions** → 新增 Secret：
   - Name: `ACCESS_PASSWORD`
   - Value: 你的全站密碼（例如 `codecat`）
3. **Settings → Pages** → **Source** 選 **GitHub Actions**（不要選 Deploy from branch）
4. 每次 push 到 `main` 會自動部署；也可在 **Actions** 分頁手動執行 **Deploy GitHub Pages**

網址範例：

| 頁面 | 網址 |
|------|------|
| 入口 | `https://你的帳號.github.io/snakify_practice_platform/` |
| Java | `https://你的帳號.github.io/snakify_practice_platform/java/` |
| C++ | `https://你的帳號.github.io/snakify_practice_platform/cpp/` |

部署時 workflow 會用 Secret 產生 `config.local.js`（不進 git），線上版也會有全站密碼。若未設定 Secret，線上版僅靠 Supabase 登入。

```powershell
cd d:\Project\snakify_java
git add .
git commit -m "你的提交訊息"
git push -u origin main
```

### Supabase 網址設定

見 [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)。Redirect URLs 需包含 **java** 與 **cpp** 兩邊的 `reset-password.html`。

### 若已有舊版 Java 進度（problem_id 為 `1-1`）

1. 在 Supabase 執行 `supabase/migrate-java-prefix.sql`
2. 本機 localStorage 會在開啟 Java 頁時自動遷移為 `java-1-1` 格式

### 重置 C++ 全部進度

1. **雲端**：Supabase SQL Editor 執行 `supabase/reset-cpp-progress.sql`
2. **本機**：重新整理 C++ 頁面（見 `cpp/js/config.js` 的 `PROGRESS_RESET_VERSION`）

---

## 設定

各語言目錄各有 `js/config.js`（可從 `config.example.js` 複製）：

| 設定 | 說明 |
|------|------|
| `PLATFORM_ID` | `snakify_practice_platform` |
| `PLATFORM_NAME` | 顯示名稱 |
| `PROGRESS_KEY` | `snakify_practice_platform_java_progress` / `_cpp_progress` |
| `AUTH_KEY` | `snakify_practice_platform_site_gate`（Java/C++ 共用全站密碼） |

**全站密碼**（`ACCESS_PASSWORD`）請寫在 `js/config.local.js`（從 `config.local.example.js` 複製），此檔已在 `.gitignore`，不會 push 到 GitHub。

---

## 匯入 / 轉換題目

```powershell
python scripts/import_chapter1.py
python scripts/import_chapter2.py
python scripts/import_chapter3.py
python scripts/migrate_problem_ids.py java java
python scripts/convert_java_to_cpp.py
python scripts/import_cpp_chapters_5_11.py
python scripts/translate_cpp_chapters_5_11.py
python scripts/build_cpp_intros_5_11.py
```

---

## 授權

題目內容參考 [Snakify / vpavlenko/content](https://github.com/vpavlenko/content)（CC BY-NC-SA）。
