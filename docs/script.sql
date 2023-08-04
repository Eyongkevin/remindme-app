CREATE TABLE remindmeapp (
   id SERIAL PRIMARY KEY,
   label VARCHAR(100),
   alert_time TIME NOT NULL,
   days CHAR(3) ARRAY, 
   type JSONB, -- {'sound': true, 'popup': false}
   active BOOL,
   created_at TIMESTAMP DEFAULT now(),
   modified_at TIMESTAMP DEFAULT now()
);