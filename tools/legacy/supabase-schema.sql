-- Rumo à Posse: tabela de progresso, um registro por usuário.
-- Cole no Supabase em SQL Editor > New query e clique em Run.
create table if not exists public.progresso (
  user_id uuid primary key references auth.users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);
alter table public.progresso enable row level security;
drop policy if exists "ler o proprio progresso" on public.progresso;
drop policy if exists "criar o proprio progresso" on public.progresso;
drop policy if exists "alterar o proprio progresso" on public.progresso;
create policy "ler o proprio progresso" on public.progresso
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "criar o proprio progresso" on public.progresso
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "alterar o proprio progresso" on public.progresso
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
