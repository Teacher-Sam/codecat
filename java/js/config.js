const CONFIG = {
  PLATFORM_ID: "snakify_practice_platform",
  PLATFORM_NAME: "Snakify Practice Platform",
  SITE_NAME: "Java",
  PROBLEM_ID_PREFIX: "java-",
  EDITOR_MODE: "text/x-java",

  // 選用：全站密碼（實際值請寫在 config.local.js，勿 commit）
  ACCESS_PASSWORD: "",

  // Supabase：填入後啟用帳號與雲端儲存（見 README）
  SUPABASE_URL: "https://fqxbrnvmehickumytzhc.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_91q0wbRqEbSohKFzAE56Mw_LqFnxKof",
  REQUIRE_LOGIN: true,

  // 忘記密碼信中的跳轉網址（留空則自動用目前網址 + reset-password.html）
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
