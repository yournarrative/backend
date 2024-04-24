CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION update_updated_on_column()
    RETURNS TRIGGER AS $update_updated_on_column$ BEGIN NEW.updated_on = (now() at time zone 'utc'); RETURN NEW; END; $update_updated_on_column$ language 'plpgsql';

CREATE TABLE users (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    auth_user_id            text            NOT NULL UNIQUE,
    data                    jsonb           NOT NULL DEFAULT '{}'::jsonb,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE user_events (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES users(id),
    event_type              text            NOT NULL,
    event_data              jsonb,
    event_timestamp         timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE check_ins (
    id                      uuid            NOT NULL DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES users(id),
    start_date              timestamptz(3)  NOT NULL,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE activity_status_options (
    id                      smallserial     NOT NULL,
    status                  varchar(20)     NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE activity_category_options (
    id                      smallserial     NOT NULL,
    category                varchar(20)     NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE activities (
    id                      uuid            NOT NULL DEFAULT uuid_generate_v4(),
    title                   text            NOT NULL DEFAULT '',
    description             text            NOT NULL DEFAULT '',
    category                varchar(20)     NOT NULL DEFAULT REFERENCES activity_category_options(category),
    status                  varchar(20)     NOT NULL DEFAULT REFERENCES activity_status_options(status),
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE brag_docs (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES users(id),
    version_number          integer         NOT NULL,
    data                    jsonb           NOT NULL DEFAULT '{}'::jsonb,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);


INSERT INTO activity_status_options (status) VALUES ('Not Started'), ('In Progress'), ('Completed'), ('Archived'));
INSERT INTO activity_category_options (category) VALUES ('Skill'), ('Endorsement'), ('Achievement'), ('Miscellaneous'));


CREATE TRIGGER trig_users_updated_on BEFORE INSERT OR UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_check_ins_updated_on BEFORE INSERT OR UPDATE ON check_ins FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_activities_updated_on BEFORE INSERT OR UPDATE ON activities FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_brag_docs_updated_on BEFORE INSERT OR UPDATE ON brag_docs FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
