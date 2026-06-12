const CONFIG = {
  PLATFORM_ID: "snakify_practice_platform",
  PLATFORM_NAME: "Snakify Practice Platform",
  SITE_NAME: "Java",
  PROBLEM_ID_PREFIX: "java-",
  EDITOR_MODE: "text/x-java",

  // --- 選用：網站密碼（有帳號系統時建議留空）---
  ACCESS_PASSWORD: "",

  // --- Supabase（帳號 + 資料庫）---
  SUPABASE_URL: "https://你的專案.supabase.co",
  SUPABASE_ANON_KEY: "你的-anon-key",
  REQUIRE_LOGIN: true,
  PASSWORD_RESET_REDIRECT: "",

  JUDGE0_URL: "https://ce.judge0.com/submissions?base64_encoded=false&wait=true",
  JAVA_LANGUAGE_ID: 62,
  PISTON_URL: "https://emkc.org/api/v2/piston/execute",
  PISTON_JAVA_VERSION: "15.0.2",

  AUTH_KEY: "snakify_practice_platform_site_gate",
  PROGRESS_KEY: "snakify_practice_platform_java_progress",
  LEGACY_AUTH_KEYS: ["snakify_java_auth"],
  LEGACY_PROGRESS_KEYS: ["snakify_java_progress"],
};
