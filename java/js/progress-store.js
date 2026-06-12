/** 學習進度與程式碼：本機快取 + Supabase 同步（依 PROBLEM_ID_PREFIX 與 Java/C++ 分開） */
const Progress = {
  cache: {},

  init() {
    this.applyProgressResetIfNeeded();
    this.migrateLegacyStorageKeys();
    this.loadLocal();
  },

  migrateLegacyStorageKeys() {
    const current = CONFIG.PROGRESS_KEY;
    if (!current) return;
    if (!localStorage.getItem(current)) {
      for (const legacyKey of CONFIG.LEGACY_PROGRESS_KEYS || []) {
        const raw = localStorage.getItem(legacyKey);
        if (raw) {
          localStorage.setItem(current, raw);
          break;
        }
      }
    }
    for (const legacyKey of CONFIG.LEGACY_PROGRESS_KEYS || []) {
      if (legacyKey !== current) {
        localStorage.removeItem(legacyKey);
      }
    }
  },

  applyProgressResetIfNeeded() {
    const version = CONFIG.PROGRESS_RESET_VERSION || 0;
    if (!version) return;
    const flagKey = `${CONFIG.PROGRESS_KEY}_reset_v`;
    if (localStorage.getItem(flagKey) !== String(version)) {
      localStorage.removeItem(CONFIG.PROGRESS_KEY);
      localStorage.setItem(flagKey, String(version));
    }
  },

  belongsToThisLanguage(problemId) {
    const prefix = CONFIG.PROBLEM_ID_PREFIX || "";
    if (!prefix) return true;
    return problemId.startsWith(prefix);
  },

  normalizeProblemId(problemId) {
    const prefix = CONFIG.PROBLEM_ID_PREFIX || "";
    const bareId = /^\d+-\d+$/;
    if (prefix && bareId.test(problemId)) {
      return `${prefix}${problemId}`;
    }
    return problemId;
  },

  loadLocal() {
    try {
      const raw = localStorage.getItem(CONFIG.PROGRESS_KEY);
      const legacy = raw ? JSON.parse(raw) : {};
      this.cache = {};
      Object.entries(legacy).forEach(([problemId, value]) => {
        const id = this.normalizeProblemId(problemId);
        if (!this.belongsToThisLanguage(id)) return;

        if (value === true) {
          this.cache[id] = { solved: true, code: null };
        } else if (value && typeof value === "object") {
          this.cache[id] = {
            solved: Boolean(value.solved),
            code: value.code ?? null,
          };
        }
      });
      this.saveLocal();
    } catch {
      this.cache = {};
    }
  },

  saveLocal() {
    const payload = {};
    Object.entries(this.cache).forEach(([id, row]) => {
      if (this.belongsToThisLanguage(id)) {
        payload[id] = row;
      }
    });
    localStorage.setItem(CONFIG.PROGRESS_KEY, JSON.stringify(payload));
  },

  isSolved(problemId) {
    return Boolean(this.cache[problemId]?.solved);
  },

  getCode(problemId) {
    return this.cache[problemId]?.code ?? null;
  },

  async markSolved(problemId, code) {
    const existing = this.cache[problemId] || { solved: false, code: null };
    this.cache[problemId] = {
      solved: true,
      code: code ?? existing.code,
    };
    this.saveLocal();
    await this.syncToRemote(problemId);
  },

  async saveCode(problemId, code) {
    const existing = this.cache[problemId] || { solved: false, code: null };
    this.cache[problemId] = {
      solved: existing.solved,
      code,
    };
    this.saveLocal();
    await this.syncToRemote(problemId);
  },

  async loadRemote() {
    if (!UserAccount.isLoggedIn()) return;

    const prefix = CONFIG.PROBLEM_ID_PREFIX || "";
    let query = UserAccount.getClient()
      .from("problem_progress")
      .select("problem_id, solved, code, updated_at");

    if (prefix) {
      query = query.like("problem_id", `${prefix}%`);
    }

    const { data, error } = await query;

    if (error) {
      console.warn("載入雲端進度失敗:", error.message);
      return;
    }

    (data || []).forEach((row) => {
      const problemId = this.normalizeProblemId(row.problem_id);
      if (!this.belongsToThisLanguage(problemId)) return;

      const local = this.cache[problemId];
      const remoteTime = row.updated_at ? new Date(row.updated_at).getTime() : 0;
      const useRemote = !local || remoteTime >= (local._updatedAt || 0);

      if (useRemote) {
        this.cache[problemId] = {
          solved: row.solved,
          code: row.code,
          _updatedAt: remoteTime,
        };
      }
    });

    Object.keys(this.cache).forEach((id) => {
      if (!this.belongsToThisLanguage(id)) {
        delete this.cache[id];
      }
    });

    this.saveLocal();
  },

  async syncToRemote(problemId) {
    if (!UserAccount.isLoggedIn()) return;
    if (!this.belongsToThisLanguage(problemId)) return;

    const row = this.cache[problemId];
    if (!row) return;

    const { error } = await UserAccount.getClient().from("problem_progress").upsert(
      {
        user_id: UserAccount.user.id,
        problem_id: problemId,
        solved: row.solved,
        code: row.code,
        updated_at: new Date().toISOString(),
      },
      { onConflict: "user_id,problem_id" }
    );

    if (error) {
      console.warn("同步雲端失敗:", error.message);
    }
  },

  clearRemoteCache() {
    this.loadLocal();
  },

  async onAuthChanged() {
    if (UserAccount.isLoggedIn()) {
      await this.loadRemote();
      if (typeof App !== "undefined") {
        App.renderHome();
        App.handleRoute();
      }
    }
  },
};
