const Runner = {
  normalizeOutput(text) {
    if (text == null) return "";
    return String(text).replace(/\r\n/g, "\n").trimEnd();
  },

  utf8ToBase64(text) {
    if (!text) return "";
    const bytes = new TextEncoder().encode(text);
    let binary = "";
    for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
  },

  base64ToUtf8(b64) {
    if (!b64) return "";
    const binary = atob(b64);
    const bytes = Uint8Array.from(binary, (c) => c.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  },

  async runWithJudge0(sourceCode, stdin) {
    const response = await fetch(CONFIG.JUDGE0_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source_code: this.utf8ToBase64(sourceCode),
        language_id: CONFIG.CPP_LANGUAGE_ID,
        stdin: this.utf8ToBase64(stdin || ""),
      }),
    });

    let result;
    try {
      result = await response.json();
    } catch {
      throw new Error(`Judge0 回應錯誤 (${response.status})`);
    }

    if (!response.ok) {
      throw new Error(result.error || result.message || `Judge0 回應錯誤 (${response.status})`);
    }

    const stdout = this.base64ToUtf8(result.stdout);
    const stderr = this.base64ToUtf8(result.stderr);
    const compileOutput = this.base64ToUtf8(result.compile_output);
    const statusId = result.status?.id;

    if (statusId === 3) {
      return { ok: true, stdout, stderr };
    }

    const message =
      compileOutput ||
      stderr ||
      result.message ||
      result.status?.description ||
      "執行失敗";

    return { ok: false, stdout, stderr: message };
  },

  async runWithPiston(sourceCode, stdin) {
    const response = await fetch(CONFIG.PISTON_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        language: "c++",
        version: CONFIG.PISTON_CPP_VERSION,
        files: [{ name: "main.cpp", content: sourceCode }],
        stdin: stdin || "",
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error("Piston 需要授權（備援 API 不可用）");
      }
      throw new Error(`Piston 回應錯誤 (${response.status})`);
    }

    const result = await response.json();
    const run = result.run || {};
    const compile = result.compile || {};

    if (compile.code !== 0 && compile.code != null) {
      return { ok: false, stdout: run.stdout || "", stderr: compile.stderr || compile.output || "編譯失敗" };
    }

    if (run.code !== 0 && run.code != null) {
      return { ok: false, stdout: run.stdout || "", stderr: run.stderr || "執行失敗" };
    }

    return { ok: true, stdout: run.stdout || "", stderr: run.stderr || "" };
  },

  async run(sourceCode, stdin) {
    try {
      return await this.runWithJudge0(sourceCode, stdin);
    } catch (judge0Error) {
      try {
        const fallback = await this.runWithPiston(sourceCode, stdin);
        fallback.via = "piston";
        return fallback;
      } catch (pistonError) {
        throw new Error(
          `無法執行程式。Judge0: ${judge0Error.message}；Piston: ${pistonError.message}`
        );
      }
    }
  },

  async evaluateTest(sourceCode, test, index) {
    const expected = this.normalizeOutput(test.output);
    const input = test.input || "";

    try {
      const result = await this.run(sourceCode, input);
      const actual = this.normalizeOutput(result.stdout);

      if (!result.ok) {
        return {
          index: index + 1,
          pass: false,
          input,
          expected,
          actual,
          error: result.stderr,
        };
      }

      return {
        index: index + 1,
        pass: actual === expected,
        input,
        expected,
        actual,
        error: actual === expected ? "" : "輸出與預期不符",
      };
    } catch (error) {
      return {
        index: index + 1,
        pass: false,
        input,
        expected,
        actual: "",
        error: error.message,
      };
    }
  },

  async runOneTest(sourceCode, test, index) {
    return this.evaluateTest(sourceCode, test, index);
  },

  async runTests(sourceCode, tests) {
    const results = [];
    for (let i = 0; i < tests.length; i++) {
      results.push(await this.evaluateTest(sourceCode, tests[i], i));
    }
    return results;
  },
};
