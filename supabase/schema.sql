-- Snakify Practice Platform（snakify_practice_platform）
-- 在 Supabase SQL Editor 執行此檔案
-- https://supabase.com → 你的專案 → SQL → New query

create table if not exists public.problem_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  problem_id text not null,
  solved boolean not null default false,
  code text,
  updated_at timestamptz not null default now(),
  primary key (user_id, problem_id)
);

create index if not exists problem_progress_user_id_idx
  on public.problem_progress (user_id);

alter table public.problem_progress enable row level security;

drop policy if exists "Users read own progress" on public.problem_progress;
create policy "Users read own progress"
  on public.problem_progress for select
  using (auth.uid() = user_id);

drop policy if exists "Users insert own progress" on public.problem_progress;
create policy "Users insert own progress"
  on public.problem_progress for insert
  with check (auth.uid() = user_id);

drop policy if exists "Users update own progress" on public.problem_progress;
create policy "Users update own progress"
  on public.problem_progress for update
  using (auth.uid() = user_id);

drop policy if exists "Users delete own progress" on public.problem_progress;
create policy "Users delete own progress"
  on public.problem_progress for delete
  using (auth.uid() = user_id);
