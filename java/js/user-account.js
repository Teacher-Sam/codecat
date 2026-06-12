const UserAccount = {
  client: null,
  user: null,
  ready: false,

  isEnabled() {
    return Boolean(CONFIG.SUPABASE_URL && CONFIG.SUPABASE_ANON_KEY);
  },

  requiresLogin() {
    return this.isEnabled() && CONFIG.REQUIRE_LOGIN !== false;
  },

  isLoggedIn() {
    return Boolean(this.user);
  },

  getClient() {
    if (!this.isEnabled()) return null;
    if (!this.client) {
      this.client = supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
    }
    return this.client;
  },

  async init() {
    if (!this.isEnabled()) {
      this.ready = true;
      this.updateHeader();
      return;
    }

    const client = this.getClient();
    const { data } = await client.auth.getSession();
    this.user = data.session?.user ?? null;
    this.ready = true;
    this.updateHeader();

    client.auth.onAuthStateChange((_event, session) => {
      this.user = session?.user ?? null;
      this.updateHeader();
      if (typeof Progress !== "undefined") {
        Progress.onAuthChanged();
      }
    });
  },

  async waitUntilReady() {
    while (!this.ready) {
      await new Promise((r) => setTimeout(r, 20));
    }
  },

  updateHeader() {
    const el = document.getElementById("user-menu");
    if (!el) return;

    if (!this.isEnabled()) {
      el.innerHTML = `<span class="user-guest">本機模式（未連線資料庫）</span>`;
      return;
    }

    if (this.isLoggedIn()) {
      const email = this.escapeHtml(this.user.email || "使用者");
      el.innerHTML = `
        <span class="user-email" title="${email}">${email}</span>
        <button type="button" class="btn btn-sm ghost" id="btn-logout">登出</button>
      `;
      document.getElementById("btn-logout")?.addEventListener("click", () => this.signOut());
    } else {
      el.innerHTML = `<button type="button" class="btn btn-sm primary" id="btn-open-login">登入</button>`;
      document.getElementById("btn-open-login")?.addEventListener("click", () => this.showAuthModal());
    }
  },

  showAuthModal() {
    document.getElementById("user-auth-overlay")?.classList.remove("hidden");
  },

  hideAuthModal() {
    document.getElementById("user-auth-overlay")?.classList.add("hidden");
  },

  getAppBaseUrl() {
    const { origin, pathname } = window.location;
    const dir = pathname.endsWith("/") ? pathname : pathname.replace(/\/[^/]*$/, "/");
    return origin + dir;
  },

  getPasswordResetRedirectUrl() {
    if (CONFIG.PASSWORD_RESET_REDIRECT) {
      return CONFIG.PASSWORD_RESET_REDIRECT;
    }
    return `${this.getAppBaseUrl()}reset-password.html`;
  },

  showAuthPanel(panel) {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const forgotForm = document.getElementById("forgot-form");
    const tabs = document.querySelectorAll("[data-auth-tab]");
    const errorEl = document.getElementById("user-auth-error");
    const successEl = document.getElementById("user-auth-success");

    loginForm?.classList.toggle("hidden", panel !== "login");
    registerForm?.classList.toggle("hidden", panel !== "register");
    forgotForm?.classList.toggle("hidden", panel !== "forgot");
    tabs.forEach((t) => t.classList.toggle("active", t.dataset.authTab === panel));
    errorEl?.classList.add("hidden");
    successEl?.classList.add("hidden");
  },

  bindAuthModal() {
    const overlay = document.getElementById("user-auth-overlay");
    if (!overlay || !this.isEnabled()) return;

    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const forgotForm = document.getElementById("forgot-form");
    const errorEl = document.getElementById("user-auth-error");
    const successEl = document.getElementById("user-auth-success");
    const tabs = overlay.querySelectorAll("[data-auth-tab]");

    const showError = (msg) => {
      errorEl.textContent = msg;
      errorEl.classList.remove("hidden");
      successEl.classList.add("hidden");
    };

    const showSuccess = (msg) => {
      successEl.textContent = msg;
      successEl.classList.remove("hidden");
      errorEl.classList.add("hidden");
    };

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        this.showAuthPanel(tab.dataset.authTab);
      });
    });

    document.getElementById("btn-show-forgot")?.addEventListener("click", () => {
      const loginEmail = document.getElementById("login-email")?.value.trim();
      if (loginEmail) {
        document.getElementById("forgot-email").value = loginEmail;
      }
      this.showAuthPanel("forgot");
    });

    document.getElementById("btn-back-login")?.addEventListener("click", () => {
      this.showAuthPanel("login");
    });

    forgotForm?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("forgot-email").value.trim();
      try {
        await this.requestPasswordReset(email);
        showSuccess("重設連結已寄出，請到信箱查收（也請檢查垃圾郵件）。");
      } catch (err) {
        showError(this.formatError(err));
      }
    });

    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value;
      try {
        await this.signIn(email, password);
        this.hideAuthModal();
        if (typeof App !== "undefined") await App.onUserLoggedIn();
      } catch (err) {
        showError(this.formatError(err));
      }
    });

    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("register-email").value.trim();
      const password = document.getElementById("register-password").value;
      try {
        const { needsEmailConfirmation } = await this.signUp(email, password);
        if (needsEmailConfirmation) {
          showSuccess("註冊成功！請到信箱點擊驗證連結後，再切換到「登入」。");
          this.showAuthPanel("login");
        } else {
          showSuccess("註冊成功！已自動登入。");
          this.hideAuthModal();
          if (typeof App !== "undefined") await App.onUserLoggedIn();
        }
      } catch (err) {
        showError(this.formatError(err));
      }
    });
  },

  async ensureLoggedIn() {
    if (!this.requiresLogin()) return;
    if (this.isLoggedIn()) return;
    this.showAuthModal();
    throw new Error("請先登入");
  },

  async signUp(email, password) {
    const { data, error } = await this.getClient().auth.signUp({ email, password });
    if (error) throw error;

    if (data.session?.user) {
      this.user = data.session.user;
      return { needsEmailConfirmation: false };
    }

    this.user = null;
    return { needsEmailConfirmation: true };
  },

  async requestPasswordReset(email) {
    const { error } = await this.getClient().auth.resetPasswordForEmail(email, {
      redirectTo: this.getPasswordResetRedirectUrl(),
    });
    if (error) throw error;
  },

  async signIn(email, password) {
    const { data, error } = await this.getClient().auth.signInWithPassword({ email, password });
    if (error) throw error;
    this.user = data.user;
    return data;
  },

  async signOut() {
    await this.getClient().auth.signOut();
    this.user = null;
    if (typeof Progress !== "undefined") {
      Progress.clearRemoteCache();
    }
    if (typeof App !== "undefined") {
      App.renderHome();
    }
  },

  formatError(err) {
    const map = {
      "Invalid login credentials": "帳號或密碼錯誤",
      "User already registered": "此 Email 已註冊",
      "Password should be at least 6 characters": "密碼至少 6 個字元",
      "Email not confirmed": "請先到信箱點擊驗證連結（或請管理員關閉 Confirm email）",
    };
    return map[err.message] || err.message || "發生錯誤";
  },

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  },
};
