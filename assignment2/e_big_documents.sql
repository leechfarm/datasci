SELECT COUNT(*) FROM ( SELECT DOCID, SUM(COUNT) FROM FREQUENCY GROUP BY DOCID HAVING SUM(COUNT) > 300);
