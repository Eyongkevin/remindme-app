-- name: fetch-by-active
-- Get all the remindme in the database where condition matches
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
WHERE active=:active;