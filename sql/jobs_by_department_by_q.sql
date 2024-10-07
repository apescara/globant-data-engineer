WITH
  -- Norm data and select columns
  base_data AS (
  SELECT
    department,
    job,
    CAST(`datetime` AS timestamp) AS `datetime`,
    h.id AS id
  FROM
    `globant-apescara.data.hired_employees` AS h
  LEFT JOIN
    `globant-apescara.data.departments` AS d
  ON
    h.department_id = d.id
  LEFT JOIN
    `globant-apescara.data.jobs` AS j
  ON
    h.job_id = j.id
  WHERE
    EXTRACT(YEAR
    FROM
      CAST(`datetime` AS timestamp)) = 2021 --only hires in 2021
  ),
  -- group by quarter
  quarter_data AS (
  SELECT
    department,
    job,
    CONCAT("Q",EXTRACT(QUARTER
      FROM
        `datetime`)) AS quarter,
    COUNT(DISTINCT id) AS hired
  FROM
    base_data
  GROUP BY
    ALL)
-- pivot and display
SELECT
  *
FROM
  quarter_data
PIVOT
  (SUM(hired) FOR quarter IN ("Q1",
      "Q2",
      "Q3",
      "Q4"))
ORDER BY
  department ASC,
  job ASC