ALTER TABLE historical DROP COLUMN graphs;
DROP TYPE pr_graphs;

CREATE TYPE pr_bench_graphs AS (
    plot_bench_all_time TEXT,
    plot_bench_one_year TEXT,
    plot_bench_six_month TEXT,
    plot_bench_one_month TEXT,
    plot_bench_one_week TEXT
);

CREATE TYPE pr_squat_graphs AS (
    plot_squat_all_time TEXT,
    plot_squat_one_year TEXT,
    plot_squat_six_month TEXT,
    plot_squat_one_month TEXT,
    plot_squat_one_week TEXT
);

CREATE TYPE pr_deadlift_graphs AS (
    plot_deadlift_all_time TEXT,
    plot_deadlift_one_year TEXT,
    plot_deadlift_six_month TEXT,
    plot_deadlift_one_month TEXT,
    plot_deadlift_one_week TEXT
);

CREATE TYPE pr_all_graphs AS (
    plot_all_time TEXT,
    plot_one_year TEXT,
    plot_six_month TEXT,
    plot_one_month TEXT,
    plot_one_week TEXT
);

ALTER TABLE historical ADD COLUMN bench_graphs pr_bench_graphs;
ALTER TABLE historical ADD COLUMN squat_graphs pr_squat_graphs;
ALTER TABLE historical ADD COLUMN deadlift_graphs pr_deadlift_graphs;
ALTER TABLE historical ADD COLUMN all_graphs pr_all_graphs;