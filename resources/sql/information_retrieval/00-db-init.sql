CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION update_updated_on_column()
    RETURNS TRIGGER AS $update_updated_on_column$ BEGIN NEW.updated_on = (now() at time zone 'utc'); RETURN NEW; END; $update_updated_on_column$ language 'plpgsql';

CREATE TABLE users (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    email                   text            NOT NULL UNIQUE,
    data                    jsonb           NOT NULL DEFAULT '{}'::jsonb,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE documents (
    id                      uuid            NOT NULL DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES users(id),
    content                 text            NOT NULL DEFAULT '',
    question                string          NULL,
    document_type           text            NULL,
    data                    jsonb           NOT NULL DEFAULT '{}'::jsonb,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TRIGGER trig_users_updated_on BEFORE INSERT OR UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_interviews_updated_on BEFORE INSERT OR UPDATE ON documents FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
