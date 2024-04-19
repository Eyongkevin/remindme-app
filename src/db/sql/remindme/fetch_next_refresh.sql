
-- name: fetch-next-refresh
-- Get upcoming reminder to refresh
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
WHERE alert_time > CURRENT_TIME + '00:01:00'::TIME AND active IS true
ORDER BY alert_time -- DESC
LIMIT 2;