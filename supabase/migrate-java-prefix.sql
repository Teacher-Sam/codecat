-- 將舊版 problem_id（如 1-1、2-3）加上 java- 前綴
-- 在 Supabase SQL Editor 執行一次即可（已有 cpp- 前綴的列不受影響）

UPDATE problem_progress
SET problem_id = 'java-' || problem_id
WHERE problem_id ~ '^\d+-\d+$';
