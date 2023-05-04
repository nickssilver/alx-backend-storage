-- Write a SQL script that lists all bands with Glam rock
SELECT DISTINCT band_name,
    IFNULL(split, YEAR(CURDATE())) - formed as lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style)
ORDER BY lifespan DESC;
