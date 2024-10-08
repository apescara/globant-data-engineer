WITH
  -- Norm and select fields
  base_data AS (
  SELECT
    department,
    h.id AS id
  FROM
    `globant-apescara.data.hired_employees` AS h
  LEFT JOIN
    `globant-apescara.data.departments` AS d
  ON
    h.department_id = d.id
  WHERE
    EXTRACT(YEAR
    FROM
      CAST(`datetime` AS timestamp)) = 2021),
  -- group and get hired
  hired_by_dep AS (
  SELECT
    department,
    COUNT(DISTINCT id) AS hired
  FROM
    base_data
  GROUP BY
    ALL)
-- select above mean and display
SELECT
  *
FROM
  hired_by_dep
WHERE
  hired > (
  SELECT
    AVG(hired)
  FROM
    hired_by_dep )
ORDER BY
  hired DESC