-- 清除所有 C++ 題目的學習進度（雲端）
-- 在 Supabase SQL Editor 執行一次

DELETE FROM problem_progress
WHERE problem_id LIKE 'cpp-%';

-- 若曾有未加前綴的 C++ 測試資料（極少見），可一併清除本機曾誤存的列：
-- 不建議執行下一行，除非確定要刪除所有語言的舊格式 id
-- DELETE FROM problem_progress WHERE problem_id ~ '^\d+-\d+$';
