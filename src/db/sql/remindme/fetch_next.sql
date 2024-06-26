
-- name: fetch-next
-- Get upcoming reminder
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
WHERE alert_time > CURRENT_TIME AND active IS true
ORDER BY alert_time -- DESC
LIMIT 1;