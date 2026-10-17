-- Dimensional design draft for the NASDAQ opening gap project.
-- Date, company and index dimensions, a fact table with composite primary key, foreign keys,
-- non-negative CHECK constraints and indexes, a range-partitioned parent table, and a
-- model-ready join of company prices with the international indices.
-- Source tables referenced below were loaded from the raw price exports (see data/README.md).

-- Date Dimension
CREATE TABLE date_dim (
    date_id DATE PRIMARY KEY
);

-- Company Dimension
CREATE TABLE company (
    company_id SERIAL PRIMARY KEY,
    company_prefix VARCHAR(10) UNIQUE NOT NULL
);

-- Index Dimension
CREATE TABLE stock_index (
    index_id SERIAL PRIMARY KEY,
    index_name VARCHAR(25) UNIQUE NOT NULL
);

-- Core Fact Table for Daily Company and Index Data
CREATE TABLE daily_company_index_data (
    date_id DATE NOT NULL,
    company_id INTEGER NOT NULL,
    index_id INTEGER NOT NULL,
    open_value NUMERIC(12,4) NOT NULL CHECK (open_value >= 0),
    close_value NUMERIC(12,4) NOT NULL CHECK (close_value >= 0),
    adj_close_index NUMERIC(12,4) NOT NULL CHECK (adj_close_index >= 0),

    -- Constraints
    PRIMARY KEY (date_id, company_id, index_id),
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (index_id) REFERENCES stock_index(index_id)
);

-- Indexes for Query Optimization
CREATE INDEX idx_fact_date ON daily_company_index_data (date_id);
CREATE INDEX idx_fact_company ON daily_company_index_data (company_id);
CREATE INDEX idx_fact_index ON daily_company_index_data (index_id);

-- Parent Table with Partitioning
CREATE TABLE daily_company_index_data_partitioned (
    date_id DATE NOT NULL,
    company_id INTEGER NOT NULL,
    index_id INTEGER NOT NULL,
    open_value NUMERIC(12,4) NOT NULL CHECK (open_value >= 0),
    close_value NUMERIC(12,4) NOT NULL CHECK (close_value >= 0),
    adj_close_index NUMERIC(12,4) NOT NULL CHECK (adj_close_index >= 0),

    PRIMARY KEY (date_id, company_id, index_id),
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (index_id) REFERENCES stock_index(index_id)
) PARTITION BY RANGE (date_id);



DROP TABLE IF EXISTS model_ready_data;

CREATE TABLE model_ready_data AS
SELECT 
    nd.date_value AS date,
    nd.company_prefix AS company,
    nd.open_value AS company_open,
    nd.close_value AS company_close,
    ni.adj_close AS index_adj_close,
    ni.stock_index AS index_name
FROM nasdaq_100_daily nd
JOIN nasdaq.index ni 
    ON nd.date_value = ni.date_value
WHERE ni.stock_index IN ('CAC', 'DAX', 'FTSE', 'HANG_Seng', 'NIFTY', 'Shanghai_Composite')
ORDER BY nd.date_value;

-- Step 2: Clean Up (Optional but Recommended)
-- Set column types and add constraints for better reliability

ALTER TABLE model_ready_data
    ALTER COLUMN date TYPE DATE,
    ALTER COLUMN company TYPE VARCHAR(10),
    ALTER COLUMN company_open TYPE NUMERIC(12,4),
    ALTER COLUMN company_close TYPE NUMERIC(12,4),
    ALTER COLUMN index_adj_close TYPE NUMERIC(12,4),
    ALTER COLUMN index_name TYPE VARCHAR(25);

-- Step 3: Add Constraints
ALTER TABLE model_ready_data
    ADD CONSTRAINT chk_open CHECK (company_open >= 0),
    ADD CONSTRAINT chk_close CHECK (company_close >= 0),
    ADD CONSTRAINT chk_index CHECK (index_adj_close >= 0);

-- Step 4: Add Indexes
CREATE INDEX idx_model_date ON model_ready_data (date);
CREATE INDEX idx_model_company ON model_ready_data (company);
CREATE INDEX idx_model_index_name ON model_ready_data (index_name);