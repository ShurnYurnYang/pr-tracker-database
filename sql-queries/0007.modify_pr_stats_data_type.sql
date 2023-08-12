ALTER TABLE historical DROP COLUMN pr;
DROP TYPE pr_stats;

CREATE TYPE pr_stats AS (
    name VARCHAR(100),
    bench DECIMAL(5,1),
    squat DECIMAL(5,1),
    deadlift DECIMAL(10,1)
);

ALTER TABLE historical ADD COLUMN pr pr_stats;