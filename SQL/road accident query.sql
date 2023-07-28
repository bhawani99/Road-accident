SELECT * FROM road_accident

SELECT SUM(number_of_casualties) AS CY_casualties_snow
From road_accident 
Where YEAR(accident_date) = '2022' and road_surface_conditions like '%snow%'

SELECT SUM(number_of_casualties) AS CY_casualties_snow
FROM road_accident 
WHERE YEAR(accident_date) = '2022' AND 
      road_surface_conditions LIKE '%Snow%' OR road_surface_conditions LIKE '%Frost%'

SELECT SUM(number_of_casualties) AS CY_casualties_snow
FROM road_accident 
WHERE YEAR(accident_date) = '2022' AND 
      UPPER(road_surface_conditions) LIKE 'SNOW' OR UPPER(road_surface_conditions) LIKE 'FROST'



SELECT COUNT(distinct accident_index) AS Total_Accident
From road_accident 
Where YEAR(accident_date) = '2021'


SELECT SUM(number_of_casualties) AS Fatal_Casualties
From road_accident 
Where accident_severity = 'Fatal'

SELECT SUM(number_of_casualties) AS PY_Fatal_Casualties
From road_accident 
Where YEAR(accident_date) = '2021' and accident_severity = 'Fatal'


SELECT SUM(number_of_casualties) AS Serious_Casualties
From road_accident 
Where accident_severity = 'Serious'

SELECT SUM(number_of_casualties) AS PY_Serious_Casualties
From road_accident 
Where YEAR(accident_date) = '2021' and accident_severity = 'Serious'

SELECT SUM(number_of_casualties) AS Slight_Casualties
From road_accident 
Where accident_severity = 'Slight'

SELECT SUM(number_of_casualties) AS PY_Slight_Casualties
From road_accident 
Where YEAR(accident_date) = '2021' and accident_severity = 'Slight'

SELECT CAST(SUM(number_of_casualties) AS decimal (10,2))*100/
(SELECT CAST(SUM(number_of_casualties) AS decimal(10,2)) From road_accident)
From road_accident 
Where accident_severity = 'Slight' 

SELECT CAST(SUM(number_of_casualties) AS decimal (10,2))*100/
(SELECT CAST(SUM(number_of_casualties) AS decimal(10,2)) From road_accident)
From road_accident 
Where accident_severity = 'Serious' 

SELECT CAST(SUM(number_of_casualties) AS decimal (10,2))*100/
(SELECT CAST(SUM(number_of_casualties) AS decimal(10,2)) From road_accident)
From road_accident 
Where accident_severity = 'Fatal' 

SELECT DATENAME(MONTH, accident_date) AS Month_Name,Sum(number_of_casualties) as CY_Casualties
FROM road_accident
WHERE YEAR(accident_date) = '2022'
GROUP BY DATENAME(MONTH, accident_date)

SELECT road_type, Sum(number_of_casualties) AS PY_Casua1ties 
FROM road_accident
WHERE YEAR(accident_date) =' 2021'
GROUP BY road_type


SELECT urban_or_rural_area,CAST(Sum(number_of_casualties) AS decimal (10,2)) *100 /
(SELECT CAST(Sum(number_of_casualties) AS decimal (10,2)) FROM road_accident WHERE YEAR(accident_date) = '2022' ) AS "% Total"
FROM road_accident
WHERE YEAR(accident_date) = '2021' 
GROUP BY urban_or_rural_area   

SELECT TOP 10 local_authority, Sum(number_of_casualties) AS Total_Casua1ties
FROM road_accident
GROUP BY local_authority
ORDER BY Total_Casua1ties DESC

SELECT 
	CASE 
		WHEN vehicle_type IN ('Agricultural vehicle') THEN 'Agriculture' 
		WHEN vehicle_type IN ('Car', 'Taxi/Private hire car') THEN 'Cars'
		WHEN vehicle_type IN ('Motorcycle 125cc and under','Motorcycle 50cc and under','Motorcycle over 125cc and up to 500cc',
							'Motorcycle over 500cc', 'Pedal cycle') THEN 'Bike'
		WHEN vehicle_type IN ('Bus or coach (17 or more pass seats)', 'Minibus (8 - 16 passenger seats)') THEN 'Bus'
		WHEN vehicle_type IN ('Goods 7.5 tonnes mgw and over', 'Goods over 3.5t. and under 7.5t','Van / Goods 3.5 tonnes mgw or under') THEN 'Goods'
    ELSE 'others'
 END AS vehicle_group,
 Sum(number_of_casualties) AS CY_Casua1ties 
FROM road_accident
 --WHERE YEAR(accident_date) =' 2022'
  GROUP BY
	CASE
		WHEN vehicle_type IN ('Agricultural vehicle') THEN 'Agriculture' 
		WHEN vehicle_type IN ('Car', 'Taxi/Private hire car') THEN 'Cars'
		WHEN vehicle_type IN ('Motorcycle 125cc and under','Motorcycle 50cc and under','Motorcycle over 125cc and up to 500cc',
							'Motorcycle over 500cc', 'Pedal cycle') THEN 'Bike'
		WHEN vehicle_type IN ('Bus or coach (17 or more pass seats)', 'Minibus (8 - 16 passenger seats)') THEN 'Bus'
		WHEN vehicle_type IN ('Goods 7.5 tonnes mgw and over', 'Goods over 3.5t. and under 7.5t','Van / Goods 3.5 tonnes mgw or under') THEN 'Goods'
    ELSE 'others'
END

SELECT 
	CASE 
		WHEN light_conditions IN ('Daylight') THEN 'Day'
		WHEN light_conditions IN ('Darkness - lighting unknown', 'Darkness - lights lit',
		'Darkness - lights unlit','Darkness - no lighting') THEN 'Night'
	END AS Light_Conditions,
	CAST(CAST(Sum(number_of_casualties) AS decimal (10,2)) *100 /
(SELECT CAST(Sum(number_of_casualties) AS decimal (10,2)) FROM road_accident WHERE YEAR(accident_date) = '2022' )AS decimal (10,2)) AS "Total % Casualties"
FROM road_accident
WHERE YEAR(accident_date) = '2022' 
GROUP BY 
	CASE
		WHEN light_conditions IN ('Daylight') THEN 'Day'
		WHEN light_conditions IN ('Darkness - lighting unknown', 'Darkness - lights lit',
		'Darkness - lights unlit','Darkness - no lighting') THEN 'Night'
	END


