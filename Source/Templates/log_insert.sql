INSERT INTO log (timestamp, tweet_id, tweet, CPU, RAM, dynu) 
VALUES (STR_TO_DATE("{{timestamp}}", '%d-%m-%Y %H:%i:%s'), {{tweet_id}}, {{tweet}}, "{{cpu_load}}", "{{ram_load}}", "{{dynu}}");