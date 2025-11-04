create schema if not exists dims;
create schema if not exists raw;
create schema if not exists marts;

-- Dimensions
create table if not exists dims.dim_date (
  date_key integer primary key,
  date date not null,
  week integer,
  month integer,
  quarter integer,
  year integer
);

create table if not exists dims.dim_platform (
  platform_id serial primary key,
  name text unique not null
);

create table if not exists dims.dim_account (
  account_id text primary key,
  platform_id integer references dims.dim_platform(platform_id),
  handle text
);

-- Raw landing tables
create table if not exists raw.raw_x_posts (
  id text primary key,
  account_id text,
  posted_at timestamptz,
  text text,
  impressions bigint,
  likes bigint,
  comments bigint,
  shares bigint,
  clicks bigint
);

create table if not exists raw.raw_linkedin_posts (
  id text primary key,
  account_id text,
  posted_at timestamptz,
  text text,
  impressions bigint,
  likes bigint,
  comments bigint,
  shares bigint,
  clicks bigint
);

create table if not exists raw.raw_tiktok_videos (
  id text primary key,
  account_id text,
  posted_at timestamptz,
  caption text,
  views bigint,
  likes bigint,
  comments bigint,
  shares bigint
);

create table if not exists raw.raw_seo_keywords (
  keyword text,
  url text,
  date date,
  position numeric,
  traffic numeric,
  cost numeric,
  intent text,
  primary key (keyword, url, date)
);

create table if not exists raw.raw_backlinks (
  domain text,
  source_url text,
  target_url text,
  date date,
  status text,
  primary key (domain, source_url, target_url, date)
);

create table if not exists raw.raw_pr_mentions (
  id text primary key,
  source text,
  url text,
  published_at timestamptz,
  reach bigint,
  sentiment text
);

create table if not exists raw.raw_web_sessions (
  date date,
  sessions bigint,
  users bigint,
  bounce_rate numeric,
  conversions bigint,
  source text,
  medium text,
  campaign text,
  primary key (date, source, medium, campaign)
);