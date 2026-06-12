const App = {
  data: null,
  editor: null,
  currentChapter: null,
  currentProblem: null,
  testStates: [],
  activeTestIndex: null,
  isRunningTests: false,
  saveCodeTimer: null,

  /** @param {{zh?: string, en?: string} | string | null | undefined} value */
  text(value) {
    if (value == null) return "";
    if (typeof value === "string") return value;
    return value.zh || value.en || "";
  },

  /** @param {{zh?: string, en?: string} | string | null | undefined} value */
  bilingualTitle(value) {
    if (typeof value === "string") return value;
    return `${value.zh} <span class="title-en">/ ${value.en}</span>`;
  },

  /** @param {{ type?: string } | null | undefined} problem */
  isIntro(problem) {
    return problem?.type === "intro";
  },

  /** @param {{ problems: Array<{ type?: string }> }} chapter */
  codingProblems(chapter) {
    return chapter.problems.filter((p) => !this.isIntro(p));
  },

  /** @param {{ id: string, title: unknown, type?: string }} problem */
  problemNo(problem) {
    if (this.isIntro(problem)) return "Intro";
    const prefix = CONFIG.PROBLEM_ID_PREFIX || "";
    if (prefix && problem.id.startsWith(prefix)) {
      return problem.id.slice(prefix.length);
    }
    return problem.id;
  },

  /** @param {{ id: string, title: unknown }} problem */
  bilingualProblemTitle(problem) {
    return `<span class="problem-no">${this.escapeHtml(this.problemNo(problem))}</span>${this.bilingualTitle(problem.title)}`;
  },

  /** @param {{zh?: string, en?: string} | string | null | undefined} value */
  bilingualHtml(value) {
    if (typeof value === "string") return value;
    return `
      <div class="bilingual">
        <div class="lang-block lang-zh">
          <span class="lang-label">中文</span>
          <div class="lang-content">${value.zh || ""}</div>
        </div>
        <div class="lang-block lang-en">
          <span class="lang-label">English</span>
          <div class="lang-content">${value.en || ""}</div>
        </div>
      </div>`;
  },

  async loadData() {
    const indexResponse = await fetch("data/index.json");
    if (!indexResponse.ok) {
      throw new Error("無法載入 data/index.json");
    }
    const index = await indexResponse.json();
    const chapters = [];

    for (const entry of index.chapters) {
      const base = `data/${entry.dir}`;
      const chapterResponse = await fetch(`${base}/chapter.json`);
      if (!chapterResponse.ok) {
        throw new Error(`無法載入 ${base}/chapter.json`);
      }
      const chapterMeta = await chapterResponse.json();
      const problems = [];

      for (const problemId of chapterMeta.problemIds) {
        const problemResponse = await fetch(`${base}/${problemId}.json`);
        if (!problemResponse.ok) {
          throw new Error(`無法載入 ${base}/${problemId}.json`);
        }
        problems.push(await problemResponse.json());
      }

      chapters.push({ ...chapterMeta, problems });
    }

    return { chapters };
  },

  async init() {
    await SiteGate.init();
    await UserAccount.init();
    UserAccount.bindAuthModal();
    Progress.init();

    if (UserAccount.requiresLogin() && !UserAccount.isLoggedIn()) {
      UserAccount.showAuthModal();
    } else if (UserAccount.isLoggedIn()) {
      await Progress.loadRemote();
    }

    this.data = await this.loadData();

    this.bindNavigation();
    this.renderHome();
    this.handleRoute();
    window.addEventListener("hashchange", () => this.handleRoute());
  },

  async onUserLoggedIn() {
    await Progress.loadRemote();
    this.renderHome();
    this.handleRoute();
  },

  bindNavigation() {
    document.addEventListener("click", (e) => {
      const nav = e.target.closest("[data-nav]");
      if (nav) {
        e.preventDefault();
        if (nav.dataset.nav === "home") {
          location.hash = "";
        }
      }
    });
  },

  isSolved(problemId) {
    return Progress.isSolved(problemId);
  },

  scheduleSaveCode(problemId) {
    if (!this.editor || this._suppressCodeSave) return;
    clearTimeout(this.saveCodeTimer);
    this.saveCodeTimer = setTimeout(() => {
      if (this._suppressCodeSave) return;
      Progress.saveCode(problemId, this.editor.getValue());
    }, 1500);
  },

  showView(name) {
    document.querySelectorAll(".view").forEach((el) => el.classList.add("hidden"));
    document.getElementById(`view-${name}`).classList.remove("hidden");
  },

  renderHome() {
    const container = document.getElementById("chapter-list");
    container.innerHTML = this.data.chapters
      .map((chapter) => {
        const coding = this.codingProblems(chapter);
        const total = coding.length;
        const solved = coding.filter((p) => this.isSolved(p.id)).length;
        return `
          <div class="card" data-chapter="${chapter.id}">
            <h3>第 ${chapter.id} 章 · ${this.bilingualTitle(chapter.title)}</h3>
            <p>${this.text(chapter.description)}</p>
            <p style="margin-top:0.5rem;font-size:0.85rem;">${solved} / ${total} 題完成</p>
          </div>
        `;
      })
      .join("");

    container.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("click", () => {
        location.hash = `#/chapter/${card.dataset.chapter}`;
      });
    });
  },

  renderChapter(chapterId) {
    const chapter = this.data.chapters.find((c) => c.id === chapterId);
    if (!chapter) {
      location.hash = "";
      return;
    }

    this.currentChapter = chapter;
    document.getElementById("chapter-title").innerHTML = this.bilingualTitle(chapter.title);

    const container = document.getElementById("problem-list");
    container.innerHTML = chapter.problems
      .map((problem, index) => {
        if (this.isIntro(problem)) {
          return `
          <div class="card card-intro" data-problem="${problem.id}">
            <h3>
              ${this.bilingualProblemTitle(problem)}
              <span class="status-badge intro">閱讀</span>
            </h3>
            <p class="problem-meta">章節介紹 · 先閱讀再開始寫程式</p>
          </div>
        `;
        }

        const codingIndex = chapter.problems.slice(0, index).filter((p) => !this.isIntro(p)).length + 1;
        const done = this.isSolved(problem.id);
        return `
          <div class="card" data-problem="${problem.id}">
            <h3>
              ${this.bilingualProblemTitle(problem)}
              <span class="status-badge ${done ? "done" : "todo"}">${done ? "已完成" : "未完成"}</span>
            </h3>
            <p class="problem-meta">第 ${codingIndex} 題 · ${problem.tests.length} 個測試案例</p>
          </div>
        `;
      })
      .join("");

    container.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("click", () => {
        location.hash = `#/problem/${chapterId}/${card.dataset.problem}`;
      });
    });

    this.showView("chapter");
  },

  initEditor(code) {
    const wrapper = document.getElementById("editor");
    wrapper.innerHTML = "";

    this._suppressCodeSave = false;

    this.editor = CodeMirror(wrapper, {
      value: code,
      mode: CONFIG.EDITOR_MODE || "text/x-java",
      theme: "material-darker",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      lineWrapping: true,
    });

    this.editor.on("cursorActivity", () => this.scrollEditorCursorIntoView());
    this.bindEditorWheelScroll();

    this.fitEditorHeight();
    if (!this._editorResizeBound) {
      this._editorResizeBound = true;
      window.addEventListener("resize", () => this.fitEditorHeight());
    }

    this.editor.on("change", (_, change) => {
      if (change.origin !== "setValue") {
        this._suppressCodeSave = false;
      }
      if (this.currentProblem && !this._suppressCodeSave) {
        this.scheduleSaveCode(this.currentProblem.id);
      }
      this.scheduleEditorResize();
    });
  },

  bindEditorWheelScroll() {
    if (this._editorWheelBound) return;
    this._editorWheelBound = true;

    document.addEventListener(
      "wheel",
      (e) => {
        const wrap = e.target.closest?.(".editor-wrap");
        if (!wrap || wrap.scrollHeight <= wrap.clientHeight) return;

        wrap.scrollTop += e.deltaY;
        e.preventDefault();
      },
      { passive: false, capture: true }
    );
  },

  scrollEditorCursorIntoView() {
    if (!this.editor) return;
    const wrap = document.querySelector(".editor-wrap");
    if (!wrap || wrap.scrollHeight <= wrap.clientHeight) return;

    const coords = this.editor.charCoords(this.editor.getCursor(), "local");
    const padding = 28;
    const viewTop = wrap.scrollTop;
    const viewBottom = viewTop + wrap.clientHeight;

    if (coords.top < viewTop + padding) {
      wrap.scrollTop = Math.max(0, coords.top - padding);
    } else if (coords.bottom > viewBottom - padding) {
      wrap.scrollTop = coords.bottom - wrap.clientHeight + padding;
    }
  },

  fitEditorHeight() {
    if (!this.editor) return;
    const wrap = document.querySelector(".editor-wrap");
    if (!wrap) return;

    const prevScrollTop = wrap.scrollTop;

    const rootStyles = getComputedStyle(document.documentElement);
    const minH = parseInt(rootStyles.getPropertyValue("--editor-min-height"), 10) || 260;
    const maxH = parseInt(getComputedStyle(wrap).maxHeight, 10) || Math.min(window.innerHeight * 0.5, 600);

    this.editor.setSize("100%", maxH);
    this.editor.refresh();
    const contentH = this.editor.getScrollInfo().height;
    const viewportH = Math.min(maxH, Math.max(minH, contentH));

    this.editor.setSize("100%", contentH);
    wrap.style.height = `${viewportH}px`;
    this.editor.refresh();

    const maxScroll = Math.max(0, wrap.scrollHeight - wrap.clientHeight);
    wrap.scrollTop = Math.min(prevScrollTop, maxScroll);
  },

  /** 等版面完成後再量一次（載入已存程式碼、切換題目時需要） */
  remeasureEditorHeight() {
    this.fitEditorHeight();
    requestAnimationFrame(() => {
      requestAnimationFrame(() => this.fitEditorHeight());
    });
  },

  scheduleEditorResize() {
    clearTimeout(this.editorResizeTimer);
    this.editorResizeTimer = setTimeout(() => {
      this.fitEditorHeight();
      this.scrollEditorCursorIntoView();
    }, 50);
  },

  setOutput(text, type) {
    const el = document.getElementById("output-content");
    el.textContent = text;
    el.className = "output-content" + (type ? ` ${type}` : "");
  },

  /** 單一測試執行後，組出應顯示在輸出區的程式結果 */
  formatProgramOutput(result) {
    const stdout = result.actual != null ? result.actual : "";
    const isWrongAnswer = result.error === "輸出與預期不符";
    const hasRuntimeError = result.error && !isWrongAnswer;

    if (hasRuntimeError) {
      if (stdout) {
        return `${stdout}\n\n--- 錯誤訊息 ---\n${result.error}`;
      }
      return result.error;
    }

    if (stdout) return stdout;
    return "(無輸出)";
  },

  formatTestData(text) {
    if (!text) return "(無 / empty)";
    return text;
  },

  initTestStates(count) {
    this.testStates = Array.from({ length: count }, () => ({
      status: "pending",
      result: null,
    }));
    this.activeTestIndex = null;
  },

  updateTestsSummary() {
    const el = document.getElementById("tests-summary");
    if (!el || !this.testStates.length) {
      if (el) el.textContent = "";
      return;
    }
    const passed = this.testStates.filter((t) => t.status === "pass").length;
    const total = this.testStates.length;
    el.textContent = `(${passed}/${total} 通過)`;
  },

  statusLabel(status) {
    switch (status) {
      case "pass":
        return { icon: "✓", text: "通過", className: "pass" };
      case "fail":
        return { icon: "✗", text: "失敗", className: "fail" };
      case "running":
        return { icon: "…", text: "執行中", className: "running" };
      default:
        return { icon: "○", text: "未測試", className: "pending" };
    }
  },

  renderTestList(problem) {
    const container = document.getElementById("test-list");
    container.innerHTML = problem.tests
      .map((test, index) => {
        const state = this.testStates[index];
        const status = this.statusLabel(state.status);
        const result = state.result;
        let resultHtml = "";

        if (state.status === "running") {
          resultHtml = `<div class="test-item-result running">執行中…</div>`;
        } else if (result && (result.pass || result.actual || result.error)) {
          const outputText = this.formatProgramOutput(result);
          const resultClass = result.pass ? "pass" : "fail";
          const resultLabel = result.pass ? "程式輸出 Output" : "程式輸出 Output";
          resultHtml = `
            <div class="test-item-result ${resultClass}">
              <div><strong>${resultLabel}</strong></div>
              <pre>${this.escapeHtml(outputText)}</pre>
            </div>`;
        }

        return `
          <div class="test-item ${status.className} ${this.activeTestIndex === index ? "active" : ""}" data-test-index="${index}">
            <div class="test-item-top">
              <span class="test-item-status" title="${status.text}">${status.icon}</span>
              <span class="test-item-title">測試 ${index + 1} / Test ${index + 1}</span>
              <button type="button" class="btn-test-run" data-test-run="${index}" title="執行此測試">▶</button>
            </div>
            <div class="test-item-data">
              <div class="test-data-block">
                <span class="test-data-label">輸入 Input</span>
                <pre>${this.escapeHtml(this.formatTestData(test.input))}</pre>
              </div>
              <div class="test-data-block">
                <span class="test-data-label">預期輸出 Expected</span>
                <pre>${this.escapeHtml(this.formatTestData(test.output))}</pre>
              </div>
            </div>
            ${resultHtml}
          </div>
        `;
      })
      .join("");

    container.querySelectorAll(".test-item").forEach((item) => {
      item.addEventListener("click", (e) => {
        if (e.target.closest(".btn-test-run")) return;
        const index = Number(item.dataset.testIndex);
        this.runTestAtIndex(index);
      });
    });

    container.querySelectorAll(".btn-test-run").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.runTestAtIndex(Number(btn.dataset.testRun));
      });
    });

    this.updateTestsSummary();
  },

  setTestBusy(busy) {
    this.isRunningTests = busy;
    const btnSubmit = document.getElementById("btn-submit");
    const btnRun = document.getElementById("btn-run");
    if (btnSubmit) btnSubmit.disabled = busy;
    if (btnRun) btnRun.disabled = busy;
    document.querySelectorAll(".btn-test-run").forEach((btn) => {
      btn.disabled = busy;
    });
  },

  applyTestResult(index, result) {
    this.testStates[index] = {
      status: result.pass ? "pass" : "fail",
      result,
    };
    this.activeTestIndex = index;
    this.renderTestList(this.currentProblem);
  },

  async runTestAtIndex(index) {
    if (this.isRunningTests || !this.currentProblem) return;

    const problem = this.currentProblem;
    const test = problem.tests[index];
    if (!test) return;

    this.setTestBusy(true);
    this.testStates[index] = { status: "running", result: null };
    this.activeTestIndex = index;
    this.renderTestList(problem);
    this.setOutput(`正在執行測試 ${index + 1}…`);

    try {
      const code = this.editor.getValue();
      const result = await Runner.runOneTest(code, test, index);
      this.applyTestResult(index, result);
      this.setOutput(this.formatProgramOutput(result), result.pass ? "success" : "error");
    } catch (error) {
      this.applyTestResult(index, {
        index: index + 1,
        pass: false,
        input: test.input || "",
        expected: Runner.normalizeOutput(test.output),
        actual: "",
        error: error.message,
      });
      this.setOutput(error.message, "error");
    } finally {
      this.setTestBusy(false);
    }
  },

  async runAllTests() {
    if (this.isRunningTests || !this.currentProblem) return;

    const problem = this.currentProblem;
    this.setTestBusy(true);
    this.setOutput("正在驗證全部測試…");
    this.initTestStates(problem.tests.length);
    this.renderTestList(problem);

    try {
      const code = this.editor.getValue();
      const results = [];

      for (let i = 0; i < problem.tests.length; i++) {
        this.testStates[i] = { status: "running", result: null };
        this.activeTestIndex = i;
        this.renderTestList(problem);

        const result = await Runner.runOneTest(code, problem.tests[i], i);
        results.push(result);
        this.applyTestResult(i, result);
      }

      const allPass = results.every((r) => r.pass);
      if (allPass) {
        await Progress.markSolved(problem.id, code);
        this.setOutput("全部測試通過！題目已完成。", "success");
        this.renderHome();
      } else {
        const failed = results.filter((r) => !r.pass).map((r) => r.index);
        this.setOutput(`部分測試未通過：${failed.join(", ")}`, "error");
      }
    } catch (error) {
      this.setOutput(error.message, "error");
    } finally {
      this.setTestBusy(false);
    }
  },

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  },

  renderProblem(chapterId, problemId) {
    const chapter = this.data.chapters.find((c) => c.id === chapterId);
    const problem = chapter?.problems.find((p) => p.id === problemId);

    if (!problem) {
      location.hash = "";
      return;
    }

    this.currentChapter = chapter;
    this.currentProblem = problem;

    const isIntro = this.isIntro(problem);
    const layout = document.querySelector(".problem-layout");
    const editorPanel = document.querySelector(".editor-panel");
    const hintBox = document.querySelector(".hint-box");
    const introNav = document.getElementById("intro-nav");
    const btnNext = document.getElementById("btn-next-problem");

    document.getElementById("problem-title").innerHTML = this.bilingualProblemTitle(problem);
    document.getElementById("problem-heading").innerHTML = this.bilingualProblemTitle(problem);
    document.getElementById("breadcrumb-chapter").innerHTML = this.bilingualTitle(chapter.title);
    document.getElementById("breadcrumb-chapter").onclick = (e) => {
      e.preventDefault();
      location.hash = `#/chapter/${chapterId}`;
    };
    document.getElementById("problem-description").innerHTML = this.bilingualHtml(problem.description);

    if (isIntro) {
      layout?.classList.add("intro-only");
      editorPanel?.classList.add("hidden");
      hintBox?.classList.add("hidden");
      introNav?.classList.remove("hidden");

      const nextProblem = chapter.problems.find((p) => !this.isIntro(p));
      if (btnNext) {
        btnNext.onclick = () => {
          if (nextProblem) {
            location.hash = `#/problem/${chapterId}/${nextProblem.id}`;
          }
        };
        btnNext.disabled = !nextProblem;
      }

      this.showView("problem");
      return;
    }

    layout?.classList.remove("intro-only");
    editorPanel?.classList.remove("hidden");
    hintBox?.classList.remove("hidden");
    introNav?.classList.add("hidden");

    document.getElementById("problem-hint").innerHTML = this.bilingualHtml(problem.hint);

    this.showView("problem");

    const savedCode = Progress.getCode(problem.id);
    this.initEditor(savedCode || problem.starterCode);
    this.remeasureEditorHeight();
    document.getElementById("stdin-input").value = "";
    this.setOutput("尚未執行");
    this.initTestStates(problem.tests.length);
    this.renderTestList(problem);

    const btnRun = document.getElementById("btn-run");
    const btnSubmit = document.getElementById("btn-submit");
    const btnReset = document.getElementById("btn-reset");

    btnRun.onclick = async () => {
      if (this.isRunningTests) return;
      this.setTestBusy(true);
      this.setOutput("執行中…");
      try {
        const code = this.editor.getValue();
        const stdin = document.getElementById("stdin-input").value;
        const result = await Runner.run(code, stdin);

        if (result.ok) {
          const out = result.stdout || "(無輸出)";
          const extra = result.via === "piston" ? "\n\n（經 Piston 備用 API 執行）" : "";
          this.setOutput(out + extra, "success");
        } else {
          this.setOutput(result.stderr || "執行失敗", "error");
        }
      } catch (error) {
        this.setOutput(error.message, "error");
      } finally {
        this.setTestBusy(false);
      }
    };

    btnSubmit.onclick = () => this.runAllTests();

    btnReset.onclick = () => {
      const solved = this.isSolved(problem.id);
      const msg = solved
        ? "確定要重設為初始程式碼嗎？\n\n僅影響目前畫面，不會覆蓋已儲存的答對程式。重新整理或再次進入此題會還原。"
        : "確定要重設為初始程式碼嗎？\n\n僅影響目前畫面，重新整理或再次進入此題會還原已儲存的程式。";
      if (confirm(msg)) {
        clearTimeout(this.saveCodeTimer);
        this._suppressCodeSave = true;
        this.editor.setValue(problem.starterCode);
        this.initTestStates(problem.tests.length);
        this.renderTestList(problem);
        this.fitEditorHeight();
        this.setOutput("已重設為初始程式碼（僅本次編輯）");
      }
    };

  },

  handleRoute() {
    const hash = location.hash.slice(1);

    if (!hash || hash === "/") {
      this.renderHome();
      this.showView("home");
      return;
    }

    const chapterMatch = hash.match(/^\/chapter\/([^/]+)$/);
    if (chapterMatch) {
      this.renderChapter(chapterMatch[1]);
      return;
    }

    const problemMatch = hash.match(/^\/problem\/([^/]+)\/([^/]+)$/);
    if (problemMatch) {
      this.renderProblem(problemMatch[1], problemMatch[2]);
      return;
    }

    location.hash = "";
  },
};

document.addEventListener("DOMContentLoaded", () => App.init());
