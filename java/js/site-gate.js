/** 選用的全站密碼（與使用者帳號無關，僅擋路人） */
const SiteGate = {
  isEnabled() {
    return Boolean(CONFIG.ACCESS_PASSWORD);
  },

  migrateLegacyAuthKeys() {
    if (sessionStorage.getItem(CONFIG.AUTH_KEY) === "1") return;
    for (const legacyKey of CONFIG.LEGACY_AUTH_KEYS || []) {
      if (legacyKey !== CONFIG.AUTH_KEY && sessionStorage.getItem(legacyKey) === "1") {
        sessionStorage.setItem(CONFIG.AUTH_KEY, "1");
        sessionStorage.removeItem(legacyKey);
        break;
      }
    }
  },

  isAuthenticated() {
    if (!this.isEnabled()) return true;
    this.migrateLegacyAuthKeys();
    return sessionStorage.getItem(CONFIG.AUTH_KEY) === "1";
  },

  login(password) {
    if (password === CONFIG.ACCESS_PASSWORD) {
      sessionStorage.setItem(CONFIG.AUTH_KEY, "1");
      return true;
    }
    return false;
  },

  init() {
    const overlay = document.getElementById("site-gate-overlay");
    if (!overlay) return;

    const input = document.getElementById("site-gate-password");
    const submit = document.getElementById("site-gate-submit");
    const error = document.getElementById("site-gate-error");

    if (!this.isEnabled()) {
      overlay.classList.add("hidden");
      return Promise.resolve();
    }

    if (this.isAuthenticated()) {
      overlay.classList.add("hidden");
      return Promise.resolve();
    }

    overlay.classList.remove("hidden");

    return new Promise((resolve) => {
      const tryLogin = () => {
        if (this.login(input.value)) {
          overlay.classList.add("hidden");
          error.classList.add("hidden");
          resolve();
        } else {
          error.classList.remove("hidden");
        }
      };

      submit.addEventListener("click", tryLogin);
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") tryLogin();
      });
    });
  },
};
