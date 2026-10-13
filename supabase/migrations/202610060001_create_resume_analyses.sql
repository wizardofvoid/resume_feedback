create table public.resume_analyses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  resume_name text not null,
  contact_email text,
  contact_phone text,
  ats_score double precision not null check (ats_score between 0 and 100),
  skill_match_score double precision not null check (skill_match_score between 0 and 100),
  format_score double precision not null check (format_score between 0 and 100),
  found_skills jsonb not null default '[]'::jsonb
    check (jsonb_typeof(found_skills) = 'array'),
  missing_skills jsonb not null default '[]'::jsonb
    check (jsonb_typeof(missing_skills) = 'array'),
  job_skill_weights jsonb not null default '{}'::jsonb
    check (jsonb_typeof(job_skill_weights) = 'object'),
  ai_feedback text not null default '',
  quality_analysis jsonb not null default '{}'::jsonb
    check (jsonb_typeof(quality_analysis) = 'object'),
  created_at timestamptz not null default now()
);

create index resume_analyses_user_created_at_idx
  on public.resume_analyses (user_id, created_at desc);

alter table public.resume_analyses enable row level security;

revoke all on table public.resume_analyses from anon, authenticated;
grant select, insert, delete on table public.resume_analyses to authenticated;

create policy "Users can read their own analyses"
  on public.resume_analyses
  for select
  to authenticated
  using ((select auth.uid()) = user_id);

create policy "Users can create their own analyses"
  on public.resume_analyses
  for insert
  to authenticated
  with check ((select auth.uid()) = user_id);

create policy "Users can delete their own analyses"
  on public.resume_analyses
  for delete
  to authenticated
  using ((select auth.uid()) = user_id);
