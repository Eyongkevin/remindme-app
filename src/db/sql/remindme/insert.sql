-- name: insert
-- Insert into the remindmeapp database
INSERT INTO remindmeapp(
   label,
   alert_time,
   days,
   type,
   active
) VALUES (%s,%s,%s,%s,%s) RETURNING *;