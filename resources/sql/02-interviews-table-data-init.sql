INSERT INTO interviews (
    user_id,
    data
)
VALUES
((SELECT id FROM users WHERE email = 'tryghosted@gmail.com'), '{"s3_path": "s3://ghosted-interviews-test/f2debf4c-511e-4ac1-879e-6581c0bfeed6/test-interview.mp4"}');