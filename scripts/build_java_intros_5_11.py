#!/usr/bin/env python3
"""Build Java theory introductions for Snakify-inspired chapters 5-11."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "java" / "data"


def code(value: str) -> str:
    return "<pre><code>" + value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</code></pre>"


def both(zh: str, en: str) -> dict[str, str]:
    return {"zh": zh.strip(), "en": en.strip()}


INTROS = {
    "5": both(
        """
<h3>1. Java 字串</h3><p><code>String</code> 儲存一串字元。<code>Scanner.next()</code> 只讀一個單字；內容可能包含空白時使用 <code>nextLine()</code>。</p>
""" + code('Scanner scanner = new Scanner(System.in);\nString s = scanner.nextLine();') + """
<h3>2. 長度與索引</h3><p><code>s.length()</code> 回傳字元數，<code>s.charAt(i)</code> 取得索引 i 的字元。索引從 0 開始，最後一個字元位於 <code>s.length()-1</code>。</p>
""" + code('String s = "Hello";\nSystem.out.println(s.charAt(0));\nSystem.out.println(s.charAt(s.length() - 1));') + """
<h3>3. 子字串與搜尋</h3><p><code>substring(begin, end)</code> 包含 begin、不包含 end。<code>indexOf()</code> 與 <code>lastIndexOf()</code> 找不到時回傳 -1。</p>
""" + code('String part = s.substring(1, 4);\nint first = s.indexOf("ll");\nint last = s.lastIndexOf("l");') + """
<h3>4. 不可變性與 StringBuilder</h3><p>String 建立後不能原地修改；串接、替換都會產生新字串。需要反轉、刪除或大量修改時，使用 <code>StringBuilder</code>。</p>
""" + code('StringBuilder b = new StringBuilder(s);\nb.reverse();\nb.delete(start, end);\nString result = b.toString();') + """
<p><strong>本章重點：</strong>留意索引邊界、substring 的右界不包含，以及 <code>==</code> 不能比較字串內容；請使用 <code>equals()</code>。</p>
""",
        """
<h3>1. Java strings</h3><p><code>String</code> stores characters. Use <code>next()</code> for one token and <code>nextLine()</code> when spaces are allowed.</p>
<h3>2. Length and indexing</h3><p>Use <code>length()</code> and <code>charAt(i)</code>. Indexes start at 0.</p>
<h3>3. Substrings and search</h3><p><code>substring(begin, end)</code> excludes end. <code>indexOf()</code> and <code>lastIndexOf()</code> return -1 when no match exists.</p>
<h3>4. Immutability</h3><p>Strings are immutable. Use <code>StringBuilder</code> for reversal, deletion, insertion, or repeated edits. Compare content with <code>equals()</code>, not <code>==</code>.</p>
""",
    ),
    "6": both(
        """
<h3>1. while 迴圈</h3><p>重複次數無法事先確定時使用 <code>while</code>。每輪開始前先檢查條件；迴圈內必須更新狀態，讓條件最終變成 false。</p>
""" + code('int i = 1;\nwhile (i <= 10) {\n    System.out.println(i * i);\n    i++;\n}') + """
<h3>2. 計數、累加與最大值</h3><p>常見狀態包括計數器、總和、目前最大值及前一個元素。設定初值時要考慮負數及空資料。</p>
<h3>3. 哨兵值輸入</h3><p>數列可能用 0 表示結束。先讀取資料，再判斷是否處理；結尾的 0 通常不計入統計。</p>
""" + code('long sum = 0;\nint x = scanner.nextInt();\nwhile (x != 0) {\n    sum += x;\n    x = scanner.nextInt();\n}') + """
<h3>4. break 與 continue</h3><p><code>break</code> 離開最內層迴圈；<code>continue</code> 跳到下一輪。若可用清楚的條件表達，通常更容易閱讀。</p>
<h3>5. 更新多個狀態</h3><p>Java 沒有 Python 的同時指定；計算費氏數列或交換數值時要使用暫存變數。</p>
""" + code('long next = a + b;\na = b;\nb = next;') + """
<p><strong>本章重點：</strong>先確認停止條件，以及每一輪如何讓程式更接近停止。</p>
""",
        """
<h3>1. The while loop</h3><p>Use <code>while</code> when the number of iterations is unknown. Update state so its condition eventually becomes false.</p>
<h3>2. Sequence state</h3><p>Typical state includes a counter, sum, maximum, and previous value.</p>
<h3>3. Sentinel input</h3><p>A value such as 0 may terminate a sequence and is normally not included in calculations.</p>
<h3>4. Control flow</h3><p><code>break</code> exits the innermost loop and <code>continue</code> proceeds to the next iteration.</p>
""",
    ),
    "7": both(
        """
<h3>1. 陣列與 ArrayList</h3><p>Snakify 的 Python list 在 Java 中可對應陣列或 <code>ArrayList</code>。元素數量固定時使用陣列；需要插入、刪除或動態增長時使用 ArrayList。</p>
""" + code('int[] a = new int[n];\nArrayList<Integer> list = new ArrayList<>();') + """
<h3>2. 讀取與索引</h3><p>陣列大小是 <code>a.length</code>，元素是 <code>a[i]</code>；ArrayList 則使用 <code>size()</code>、<code>get(i)</code> 和 <code>set(i, value)</code>。</p>
""" + code('for (int i = 0; i < a.length; i++) {\n    a[i] = scanner.nextInt();\n}') + """
<h3>3. 走訪</h3><p>需要索引時使用一般 for；只需要元素值時可使用 enhanced for。enhanced for 的變數是值的副本，不能用它替換陣列元素。</p>
<h3>4. 新增、刪除與排序</h3><p>ArrayList 使用 <code>add()</code> 與 <code>remove()</code>。陣列排序使用 <code>Arrays.sort(a)</code>，ArrayList 使用 <code>Collections.sort(list)</code>。</p>
""" + code('list.add(index, value);\nlist.remove(index);\nArrays.sort(a);') + """
<p><strong>本章重點：</strong>分清楚陣列的 <code>length</code>、String 的 <code>length()</code> 與集合的 <code>size()</code>。</p>
""",
        """
<h3>1. Arrays and ArrayList</h3><p>Use an array for fixed-size data and <code>ArrayList</code> for dynamic insertion and removal.</p>
<h3>2. Access</h3><p>Arrays use <code>length</code> and <code>a[i]</code>. ArrayList uses <code>size()</code>, <code>get()</code>, and <code>set()</code>.</p>
<h3>3. Traversal and sorting</h3><p>Use an indexed loop when positions matter. Sort with <code>Arrays.sort()</code> or <code>Collections.sort()</code>.</p>
""",
    ),
    "8": both(
        """
<h3>1. static 方法</h3><p>線上評測的程式從 <code>Main.main</code> 開始。輔助方法通常宣告為 <code>static</code>，並寫出回傳型別、名稱和參數型別。</p>
""" + code('static double distance(double x1, double y1, double x2, double y2) {\n    double dx = x1 - x2;\n    double dy = y1 - y2;\n    return Math.sqrt(dx * dx + dy * dy);\n}') + """
<h3>2. 參數傳遞</h3><p>Java 一律傳值。基本型別會複製數值；物件參數會複製參考，因此方法可以修改物件內容，但不能藉由重新指定參數來替換呼叫端變數。</p>
<h3>3. 遞迴</h3><p>遞迴方法會呼叫自己，必須有可直接回答的基底情況，以及讓問題規模縮小的遞迴步驟。</p>
""" + code('static long power(long a, int n) {\n    if (n == 0) return 1;\n    return a * power(a, n - 1);\n}') + """
<h3>4. 呼叫堆疊</h3><p>每次呼叫都有自己的區域變數；遞迴過深會產生 <code>StackOverflowError</code>。</p>
<p><strong>本章重點：</strong>先定義方法輸入、輸出與基底情況，再寫遞迴關係。</p>
""",
        """
<h3>1. Static methods</h3><p>Execution starts in <code>Main.main</code>. Helper methods are normally static and declare a return type and typed parameters.</p>
<h3>2. Parameters</h3><p>Java is pass-by-value. Object references are copied, so object contents can be changed but the caller's variable cannot be replaced by assigning the parameter.</p>
<h3>3. Recursion</h3><p>A recursive method needs a base case and a step that makes the problem smaller. Excessive depth causes <code>StackOverflowError</code>.</p>
""",
    ),
    "9": both(
        """
<h3>1. 二維陣列</h3><p>表格或矩陣可用 <code>int[][]</code> 表示。<code>a[i][j]</code> 是第 i 列、第 j 欄，索引從 0 開始。</p>
""" + code('int rows = scanner.nextInt();\nint cols = scanner.nextInt();\nint[][] a = new int[rows][cols];') + """
<h3>2. 輸入與走訪</h3><p>使用雙層迴圈。列數為 <code>a.length</code>，第 i 列的欄數為 <code>a[i].length</code>。</p>
""" + code('for (int i = 0; i < a.length; i++)\n    for (int j = 0; j < a[i].length; j++)\n        a[i][j] = scanner.nextInt();') + """
<h3>3. 對角線</h3><p>方陣主對角線滿足 <code>i == j</code>，副對角線滿足 <code>i + j == n - 1</code>。</p>
<h3>4. 矩陣轉換</h3><p>交換兩欄要逐列交換；矩陣乘法用三層迴圈累加共同維度。建立結果陣列前先確認列、欄尺寸。</p>
<p><strong>本章重點：</strong>第一個索引是列，第二個索引是欄。</p>
""",
        """
<h3>1. Two-dimensional arrays</h3><p>Use <code>int[][]</code> for a matrix. <code>a[i][j]</code> means row i, column j.</p>
<h3>2. Traversal</h3><p>Use nested loops. The number of rows is <code>a.length</code>; row i has <code>a[i].length</code> columns.</p>
<h3>3. Diagonals and transformations</h3><p>The main diagonal has <code>i == j</code>, and the secondary diagonal has <code>i + j == n - 1</code>. Column swaps work row by row.</p>
""",
    ),
    "10": both(
        """
<h3>1. Set</h3><p>集合只保存不重複的元素。<code>HashSet</code> 提供快速查找但不保證順序；<code>TreeSet</code> 會依自然順序排列。</p>
""" + code('Set<Integer> values = new HashSet<>();\nvalues.add(3);\nvalues.add(3); // 仍然只有一個 3') + """
<h3>2. 常用操作</h3><p><code>add()</code> 新增、<code>contains()</code> 查找、<code>remove()</code> 刪除、<code>size()</code> 取得不同元素數。</p>
""" + code('if (values.contains(x)) {\n    System.out.println("YES");\n}') + """
<h3>3. 集合運算</h3><p>複製集合後使用 <code>retainAll()</code> 求交集、<code>addAll()</code> 求聯集、<code>removeAll()</code> 求差集，避免意外修改原集合。</p>
""" + code('Set<Integer> intersection = new HashSet<>(a);\nintersection.retainAll(b);') + """
<h3>4. 選擇集合</h3><p>輸出需要排序時使用 TreeSet；要保存重複次數時則應使用 Map 計數。</p>
<p><strong>本章重點：</strong>集合回答「有哪些不同值」與「某值是否存在」。</p>
""",
        """
<h3>1. Sets</h3><p><code>HashSet</code> stores unique values without order. <code>TreeSet</code> keeps values naturally sorted.</p>
<h3>2. Operations</h3><p>Use <code>add()</code>, <code>contains()</code>, <code>remove()</code>, and <code>size()</code>.</p>
<h3>3. Set algebra</h3><p>Use <code>retainAll()</code>, <code>addAll()</code>, and <code>removeAll()</code> on a copy for intersection, union, and difference.</p>
""",
    ),
    "11": both(
        """
<h3>1. Map 的鍵與值</h3><p>Map 將每個鍵對應到一個值。<code>HashMap</code> 不保證順序；<code>TreeMap</code> 會依鍵的自然順序排列。</p>
""" + code('Map<String, String> capital = new HashMap<>();\ncapital.put("Taiwan", "Taipei");') + """
<h3>2. 新增與查找</h3><p>使用 <code>put()</code> 新增或覆蓋，<code>get()</code> 取得值，<code>containsKey()</code> 判斷鍵是否存在。<code>getOrDefault()</code> 很適合計數。</p>
""" + code('int count = frequency.getOrDefault(word, 0);\nfrequency.put(word, count + 1);') + """
<h3>3. merge 計數</h3><p><code>merge()</code> 能把「不存在時設為 1，存在時加 1」寫得更精簡。</p>
""" + code('frequency.merge(word, 1, Integer::sum);') + """
<h3>4. 走訪</h3><p>使用 <code>entrySet()</code> 同時取得鍵和值。若題目要求字典序，使用 TreeMap 或先將鍵排序。</p>
""" + code('for (Map.Entry<String, Integer> e : frequency.entrySet()) {\n    System.out.println(e.getKey() + " " + e.getValue());\n}') + """
<h3>5. 一對多資料</h3><p>一個鍵對應多個值時，可使用 <code>Map&lt;String, List&lt;String&gt;&gt;</code> 或 <code>Map&lt;String, Set&lt;String&gt;&gt;</code>。</p>
<p><strong>本章重點：</strong>先決定鍵和值代表什麼，再確認輸出是否要求排序。</p>
""",
        """
<h3>1. Keys and values</h3><p><code>HashMap</code> associates keys with values without order. <code>TreeMap</code> keeps keys naturally sorted.</p>
<h3>2. Operations</h3><p>Use <code>put()</code>, <code>get()</code>, <code>containsKey()</code>, and <code>getOrDefault()</code>. <code>merge()</code> is convenient for frequency counting.</p>
<h3>3. Iteration</h3><p>Iterate over <code>entrySet()</code> to access keys and values together. Use TreeMap when lexicographic output is required.</p>
<p>For one-to-many relationships, combine a Map with a List or Set.</p>
""",
    ),
}

SOURCES = {
    "5": "https://snakify.org/en/lessons/strings_str/", "6": "https://snakify.org/en/lessons/while_loop/",
    "7": "https://snakify.org/en/lessons/lists/", "8": "https://snakify.org/en/lessons/functions/",
    "9": "https://snakify.org/en/lessons/two_dimensional_lists_arrays/", "10": "https://snakify.org/en/lessons/sets/",
    "11": "https://snakify.org/en/lessons/dictionaries_dicts/",
}


def main() -> None:
    for chapter, description in INTROS.items():
        path = DATA / f"chapter-{chapter}" / f"java-{chapter}-0.json"
        problem = json.loads(path.read_text(encoding="utf-8"))
        problem["description"] = description
        problem["source"] = SOURCES[chapter]
        path.write_text(json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated Java chapter {chapter} intro")


if __name__ == "__main__":
    main()
