#!/usr/bin/env python3
"""Build the C++ theory introductions for Snakify-inspired chapters 5-11."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "cpp" / "data"


def code(value: str) -> str:
    return "<pre><code>" + value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</code></pre>"


INTROS: dict[str, dict[str, str]] = {
    "5": {
        "zh": """
<h3>1. C++ 字串</h3>
<p><code>std::string</code> 用來儲存一串字元。使用前要引入 <code>&lt;string&gt;</code>。<code>cin &gt;&gt; s</code> 只讀到空白前；若內容可能包含空白，請使用 <code>getline(cin, s)</code>。</p>
""" + code('#include <iostream>\n#include <string>\nusing namespace std;\n\nstring name;\ngetline(cin, name);\ncout << "Hello, " << name;') + """
<h3>2. 長度與索引</h3>
<p><code>s.size()</code> 或 <code>s.length()</code> 會回傳字元數。索引從 0 開始，因此第一個字元是 <code>s[0]</code>，最後一個是 <code>s[s.size()-1]</code>。C++ 不支援 Python 的負索引，存取前也要確認索引沒有超出範圍。</p>
""" + code('string s = "Hello";\ncout << s[0] << " " << s[s.size() - 1];  // H o') + """
<h3>3. 子字串與反轉</h3>
<p><code>s.substr(pos, count)</code> 從 <code>pos</code> 取出最多 <code>count</code> 個字元。C++ 沒有 <code>s[a:b]</code> 或步長切片，間隔取字元要用迴圈；反轉可使用 <code>reverse</code>。</p>
""" + code('string part = s.substr(1, 3);\nreverse(s.begin(), s.end());') + """
<h3>4. 搜尋與修改</h3>
<p><code>find()</code> 與 <code>rfind()</code> 分別尋找第一次與最後一次出現的位置；找不到時回傳 <code>string::npos</code>。常用修改方法還有 <code>erase()</code>、<code>insert()</code> 與 <code>replace()</code>。</p>
""" + code('size_t pos = s.find("ll");\nif (pos != string::npos) {\n    s.replace(pos, 2, "XX");\n}') + """
<p><strong>本章重點：</strong>分清楚「字元索引」與「子字串範圍」，並特別留意 <code>size_t</code>、<code>string::npos</code> 和邊界。</p>
""",
        "en": """
<h3>1. C++ strings</h3><p><code>std::string</code> stores a sequence of characters. Use <code>cin &gt;&gt; s</code> for one word and <code>getline(cin, s)</code> when spaces are allowed.</p>
""" + code('string name;\ngetline(cin, name);\ncout << "Hello, " << name;') + """
<h3>2. Length and indexing</h3><p>Use <code>size()</code> or <code>length()</code>. Indexes start at 0. C++ has no negative indexes, so the last character is <code>s[s.size()-1]</code>.</p>
<h3>3. Substrings</h3><p><code>s.substr(pos, count)</code> extracts a substring. Use loops for stepped slices and <code>reverse()</code> to reverse a range.</p>
<h3>4. Search and modification</h3><p>Use <code>find()</code>, <code>rfind()</code>, <code>erase()</code>, <code>insert()</code>, and <code>replace()</code>. A failed search returns <code>string::npos</code>.</p>
""",
    },
    "6": {
        "zh": """
<h3>1. while 迴圈</h3><p>當重複次數無法事先確定時，使用 <code>while</code>。每輪開始前會先檢查條件；條件為 false 時離開迴圈。</p>
""" + code('int i = 1;\nwhile (i <= 10) {\n    cout << i * i << "\\n";\n    i++;\n}') + """
<h3>2. 計數器與狀態更新</h3><p>迴圈內必須讓條件逐漸走向結束，否則會形成無限迴圈。常見狀態包括計數、累加、目前最大值及前一個數字。</p>
<h3>3. 哨兵值輸入</h3><p>有些數列沒有先給長度，而是用 0 表示結束。先讀取，再於條件中判斷；結尾的 0 通常不計入資料。</p>
""" + code('long long sum = 0;\nint x;\ncin >> x;\nwhile (x != 0) {\n    sum += x;\n    cin >> x;\n}') + """
<h3>4. break 與 continue</h3><p><code>break</code> 立即離開最內層迴圈；<code>continue</code> 跳過本輪剩餘程式。可以用清楚的迴圈條件表達時，通常比過度使用它們更容易閱讀。</p>
<h3>5. 同時更新兩個值</h3><p>計算費氏數列時，新值依賴兩個舊值。先存暫存值，或使用 <code>std::tie</code>；交換兩值則可使用 <code>swap(a, b)</code>。</p>
""" + code('long long a = 0, b = 1;\nwhile (b < limit) {\n    long long next = a + b;\n    a = b;\n    b = next;\n}') + """
<p><strong>本章重點：</strong>先寫出「維持什麼狀態、何時停止、每輪如何更新」三件事。</p>
""",
        "en": """
<h3>1. The while loop</h3><p>Use <code>while</code> when the number of repetitions is not known in advance. Its condition is checked before every iteration.</p>
""" + code('int i = 1;\nwhile (i <= 10) {\n    cout << i * i << "\\n";\n    i++;\n}') + """
<h3>2. State and termination</h3><p>Update the counter or state so the loop eventually stops. Typical state includes a count, sum, maximum, or previous value.</p>
<h3>3. Sentinel input</h3><p>A value such as 0 can mark the end of an unknown-length sequence. Do not include the sentinel unless the statement says so.</p>
<h3>4. Loop control</h3><p><code>break</code> exits the innermost loop and <code>continue</code> starts its next iteration. Prefer a clear condition when possible.</p>
""",
    },
    "7": {
        "zh": """
<h3>1. 使用 vector 儲存數列</h3><p>Snakify 的 Python <em>list</em> 在 C++ 中最接近 <code>std::vector</code>。它能在執行時決定大小，元素索引從 0 開始，而且可以修改。</p>
""" + code('#include <vector>\nvector<int> a = {2, 3, 5, 7};\ncout << a[0] << " " << a.size();') + """
<h3>2. 建立與讀取</h3><p>已知元素個數時可先建立大小為 n 的 vector；未知長度時可用 <code>push_back()</code> 加到尾端。</p>
""" + code('int n;\ncin >> n;\nvector<int> a(n);\nfor (int &x : a) cin >> x;') + """
<h3>3. 走訪元素</h3><p>需要索引時使用一般 for 迴圈；只需要值時可使用 range-based for。若要修改元素，迴圈變數必須是參考 <code>int&amp;</code>。</p>
""" + code('for (int i = 0; i < (int)a.size(); i++)\n    cout << i << ": " << a[i] << "\\n";\n\nfor (int &x : a) x *= 2;') + """
<h3>4. 插入、刪除與排序</h3><p><code>insert()</code>、<code>erase()</code> 會使後方元素移動；操作後原本的索引可能失效。排序使用 <code>sort(a.begin(), a.end())</code>。</p>
""" + code('a.insert(a.begin() + pos, value);\na.erase(a.begin() + pos);\nsort(a.begin(), a.end());') + """
<p><strong>本章重點：</strong>先判斷題目要的是元素值還是索引，並小心相鄰元素、首尾元素及修改後的大小。</p>
""",
        "en": """
<h3>1. Storing a sequence</h3><p>C++ <code>std::vector</code> is the closest counterpart of a Python list. It has zero-based indexes, a runtime size, and mutable elements.</p>
""" + code('int n;\ncin >> n;\nvector<int> a(n);\nfor (int &x : a) cin >> x;') + """
<h3>2. Traversal</h3><p>Use an indexed loop when positions matter and a range-based loop when only values matter. Use a reference to modify elements.</p>
<h3>3. Operations</h3><p><code>push_back()</code>, <code>insert()</code>, <code>erase()</code>, and <code>sort()</code> cover the main operations used in this lesson.</p>
""",
    },
    "8": {
        "zh": """
<h3>1. 函式</h3><p>函式把一段工作命名並重複使用。宣告要寫出回傳型別、名稱與參數型別；不回傳值時使用 <code>void</code>。</p>
""" + code('double distance(double x1, double y1, double x2, double y2) {\n    double dx = x1 - x2;\n    double dy = y1 - y2;\n    return sqrt(dx * dx + dy * dy);\n}') + """
<h3>2. 傳值與傳參考</h3><p>一般參數會複製值，函式內修改不影響呼叫端。需要修改原物件或避免大型物件複製時使用參考；唯讀參數通常寫成 <code>const T&amp;</code>。</p>
""" + code('void normalize(vector<int>& a);\nint sum(const vector<int>& a);') + """
<h3>3. 遞迴</h3><p>遞迴函式會呼叫自己。每個遞迴解法都需要：</p><ul><li>可直接回答的基底情況；</li><li>把問題縮小的遞迴步驟；</li><li>確保每次呼叫都更接近基底情況。</li></ul>
""" + code('long long power(long long a, int n) {\n    if (n == 0) return 1;      // 基底情況\n    return a * power(a, n-1); // 規模縮小\n}') + """
<h3>4. 呼叫堆疊</h3><p>每次遞迴呼叫都有自己的區域變數，完成後依相反順序返回。遞迴太深會耗盡堆疊，因此只在題目適合且深度合理時使用。</p>
<p><strong>本章重點：</strong>先定義函式的輸入、輸出與基底情況，再寫遞迴關係。</p>
""",
        "en": """
<h3>1. Functions</h3><p>A function names a reusable operation. Its declaration specifies a return type, name, and typed parameters. Use <code>void</code> when no value is returned.</p>
<h3>2. Values and references</h3><p>Ordinary parameters are copied. Use <code>T&amp;</code> to modify the caller's object and <code>const T&amp;</code> for efficient read-only access.</p>
<h3>3. Recursion</h3><p>A recursive function needs a base case and a recursive step that always makes the problem smaller.</p>
""" + code('long long power(long long a, int n) {\n    if (n == 0) return 1;\n    return a * power(a, n - 1);\n}') + """
<h3>4. The call stack</h3><p>Every call has its own local variables. Excessive recursion depth can overflow the stack.</p>
""",
    },
    "9": {
        "zh": """
<h3>1. 二維資料</h3><p>表格或矩陣具有列與欄。C++ 可用 <code>vector&lt;vector&lt;int&gt;&gt;</code> 表示；<code>a[i][j]</code> 是第 i 列、第 j 欄，索引都從 0 開始。</p>
""" + code('int rows, cols;\ncin >> rows >> cols;\nvector<vector<int>> a(rows, vector<int>(cols));') + """
<h3>2. 輸入與走訪</h3><p>使用雙層迴圈：外層處理列，內層處理欄。列數是 <code>a.size()</code>，非空矩陣的欄數是 <code>a[0].size()</code>。</p>
""" + code('for (int i = 0; i < rows; i++) {\n    for (int j = 0; j < cols; j++) {\n        cin >> a[i][j];\n    }\n}') + """
<h3>3. 對角線</h3><p>方陣主對角線滿足 <code>i == j</code>；副對角線滿足 <code>i + j == n - 1</code>。比較 i、j 還可以判斷元素位於對角線上方或下方。</p>
<h3>4. 建構與轉換矩陣</h3><p>先建立正確尺寸再填值。交換兩欄時要逐列交換；矩陣乘法則以三層迴圈累加共同維度。</p>
""" + code('for (int i = 0; i < rows; i++)\n    swap(a[i][c1], a[i][c2]);') + """
<p><strong>本章重點：</strong>畫出列、欄與索引的對應，避免把 <code>a[row][column]</code> 的順序寫反。</p>
""",
        "en": """
<h3>1. Two-dimensional data</h3><p>Use <code>vector&lt;vector&lt;int&gt;&gt;</code> for a runtime-sized table or matrix. <code>a[i][j]</code> means row i, column j.</p>
""" + code('vector<vector<int>> a(rows, vector<int>(cols));') + """
<h3>2. Traversal</h3><p>Use nested loops: rows outside and columns inside. The main diagonal has <code>i == j</code>; the secondary diagonal has <code>i + j == n - 1</code>.</p>
<h3>3. Transformations</h3><p>Create the required dimensions first. Column swaps work row by row, while matrix multiplication uses three nested loops.</p>
""",
    },
    "10": {
        "zh": """
<h3>1. 集合</h3><p>集合只保存不重複的值。<code>std::set</code> 會自動依遞增順序排列；只要求快速查找而不要求順序時，可考慮 <code>unordered_set</code>。</p>
""" + code('#include <set>\nset<int> values = {3, 1, 3, 2};\n// values 內容為 1, 2, 3') + """
<h3>2. 新增、查找與刪除</h3><p><code>insert(x)</code> 新增元素，<code>count(x)</code> 判斷是否存在，<code>erase(x)</code> 刪除元素，<code>size()</code> 取得不同元素數量。</p>
""" + code('values.insert(x);\nif (values.count(x)) cout << "YES";\nvalues.erase(x);') + """
<h3>3. 走訪與集合運算</h3><p>可以 range-based for 依排序順序走訪。交集、聯集、差集可用兩個 iterator 自行處理，或使用 <code>&lt;algorithm&gt;</code> 中的集合演算法。</p>
""" + code('set_intersection(a.begin(), a.end(),\n                 b.begin(), b.end(),\n                 back_inserter(result));') + """
<h3>4. 選擇資料結構</h3><p>若需要保留重複次數，集合並不合適；請改用 map 計數。若輸出必須排序，<code>set</code> 通常比 <code>unordered_set</code> 方便。</p>
<p><strong>本章重點：</strong>集合回答的是「有哪些不同的值」以及「某值是否存在」。</p>
""",
        "en": """
<h3>1. Sets</h3><p>A set stores unique values. <code>std::set</code> keeps them sorted; <code>unordered_set</code> favors lookup speed without ordering.</p>
<h3>2. Basic operations</h3><p>Use <code>insert()</code>, <code>count()</code>, <code>erase()</code>, and <code>size()</code>.</p>
<h3>3. Set operations</h3><p>Iterate through a set in order. Intersection, union, and difference can be implemented with two iterators or the algorithms in <code>&lt;algorithm&gt;</code>.</p>
<p>Use a map instead when duplicate counts matter.</p>
""",
    },
    "11": {
        "zh": """
<h3>1. 鍵與值</h3><p>字典會把一個鍵對應到一個值。C++ 的 <code>std::map&lt;Key, Value&gt;</code> 依鍵排序；<code>unordered_map</code> 不保證順序，但平均查找速度較快。</p>
""" + code('#include <map>\nmap<string, string> capital;\ncapital["Taiwan"] = "Taipei";') + """
<h3>2. 新增與查找</h3><p><code>m[key]</code> 在鍵不存在時會建立預設值，因此只想查找時應使用 <code>find()</code> 或 <code>count()</code>，避免意外新增資料。</p>
""" + code('auto it = capital.find(country);\nif (it != capital.end())\n    cout << it->second;') + """
<h3>3. 頻率統計</h3><p>map 最常見的用途是計數。整數的預設值為 0，所以可以直接遞增。</p>
""" + code('map<string, int> frequency;\nstring word;\nwhile (cin >> word) frequency[word]++;') + """
<h3>4. 走訪與排序</h3><p>走訪 map 時，每個元素是 <code>pair&lt;const Key, Value&gt;</code>。使用結構化綁定可同時取得鍵和值；<code>map</code> 會自然依鍵的字典序輸出。</p>
""" + code('for (const auto& [key, value] : frequency) {\n    cout << key << " " << value << "\\n";\n}') + """
<h3>5. 一對多資料</h3><p>一個鍵需要保存多個值時，可以使用 <code>map&lt;string, vector&lt;string&gt;&gt;</code> 或 <code>map&lt;string, set&lt;string&gt;&gt;</code>。選擇 vector 或 set 取決於是否允許重複、是否要求排序。</p>
<p><strong>本章重點：</strong>先決定鍵和值各代表什麼，再確認輸出是否要求字典序。</p>
""",
        "en": """
<h3>1. Keys and values</h3><p><code>std::map&lt;Key, Value&gt;</code> associates each key with a value and keeps keys sorted. <code>unordered_map</code> provides average constant-time lookup without ordering.</p>
<h3>2. Lookup</h3><p><code>m[key]</code> creates a default value when the key is absent. Use <code>find()</code> or <code>count()</code> for lookup without insertion.</p>
<h3>3. Frequency counting</h3>
""" + code('map<string, int> frequency;\nstring word;\nwhile (cin >> word) frequency[word]++;') + """
<h3>4. Iteration</h3><p>A map iterates in key order. Structured bindings make the key and value easy to access.</p>
""" + code('for (const auto& [key, value] : frequency)\n    cout << key << " " << value << "\\n";') + """
<p>For one-to-many relationships, combine a map with a vector or set.</p>
""",
    },
}


def main() -> None:
    for chapter, descriptions in INTROS.items():
        path = DATA / f"chapter-{chapter}" / f"cpp-{chapter}-0.json"
        problem = json.loads(path.read_text(encoding="utf-8"))
        problem["description"] = {key: value.strip() for key, value in descriptions.items()}
        problem["source"] = {
            "5": "https://snakify.org/en/lessons/strings_str/",
            "6": "https://snakify.org/en/lessons/while_loop/",
            "7": "https://snakify.org/en/lessons/lists/",
            "8": "https://snakify.org/en/lessons/functions/",
            "9": "https://snakify.org/en/lessons/two_dimensional_lists_arrays/",
            "10": "https://snakify.org/en/lessons/sets/",
            "11": "https://snakify.org/en/lessons/dictionaries_dicts/",
        }[chapter]
        path.write_text(json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated chapter {chapter} intro")


if __name__ == "__main__":
    main()
