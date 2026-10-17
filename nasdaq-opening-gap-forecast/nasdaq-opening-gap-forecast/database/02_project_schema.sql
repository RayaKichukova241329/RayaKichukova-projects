-- Schema used by the models: project_schema.daily_index_stats.
-- Loads the NASDAQ-100 and the seven international indices into one table
-- keyed by (date_value, stock_index), with CHECK constraints and indexes.

-- Creating a schema
create schema if not exists project_schema;

-- 2. Create NASDAQ modeling table 
drop table if exists project_schema.nasdaq_table;

create table project_schema.nasdaq_table (
    date_value date not null,
    stock_index varchar(20) not null,
    open_value numeric(12,4) not null check (open_value >= 0),
    close_value numeric(12,4) not null check (close_value >= 0),
    primary key (date_value, stock_index)
);

-- Insert NASDAQ index data
insert into project_schema.nasdaq_table
select
    date_value,
    'NASDAQ' as stock_index,
    open_value,
    close_value
from public.nasdaq_100_index;

-- 3. Create other indices table
drop table if exists project_schema.indices_table;

create table project_schema.indices_table (
    date_value date not null,
    stock_index varchar(25) not null,
    open_value numeric(12,4) not null check (open_value >= 0),
    close_value numeric(12,4) not null check (close_value >= 0),
    primary key (date_value, stock_index)
);

-- Insert other stock index data
insert into project_schema.indices_table
select
    date_value,
    stock_index,
    open_value,
    close_value
from public.stock_indices;

-- 4. Create final combined table
drop table if exists project_schema.daily_index_stats;

create table project_schema.daily_index_stats (
    date_value date not null,
    stock_index varchar(25) not null,
    open_value numeric(12,4) not null check (open_value >= 0),
    close_value numeric(12,4) not null check (close_value >= 0),
    primary key (date_value, stock_index)
);

-- Insert merged data
insert into project_schema.daily_index_stats
select * from project_schema.indices_table
union all
select * from project_schema.nasdaq_table;

-- 5. Create indexes (renamed with "1")
create index if not exists idx_final_date1 on project_schema.daily_index_stats(date_value);
create index if not exists idx_final_index_name1 on project_schema.daily_index_stats(stock_index);
