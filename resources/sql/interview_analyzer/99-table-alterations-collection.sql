ALTER TABLE interviews
ALTER COLUMN transcript DROP DEFAULT;

ALTER TABLE users
ALTER COLUMN id SET DEFAULT uuid_generate_v4();

UPDATE interviews
SET data = jsonb_set(data, '{s3_path}', '"s3://ghosted-interviews-test/bb6f2012-15e8-49b1-88d0-afd350ec9870/test-interview.mp4"', true)
WHERE id = 'd313e351-4a1b-453a-8fb0-6de77ec7e549';
