
-- name: fetch-all
-- Get all the remindme in the database
SELECT 
   id,
   label,
   alert_time,
   days,
   type,
   active,
   created_at,
   modified_at
FROM remindmeapp
ORDER BY alert_time;