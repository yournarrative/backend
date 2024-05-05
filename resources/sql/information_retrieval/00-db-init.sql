CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION update_updated_on_column()
    RETURNS TRIGGER AS $update_updated_on_column$ BEGIN NEW.updated_on = (now() at time zone 'utc'); RETURN NEW; END; $update_updated_on_column$ language 'plpgsql';

-- Create a table for public profiles
create table profiles (
  id uuid references auth.users on delete cascade not null primary key,
  updated_at timestamp with time zone,
  email text
);
-- Set up Row Level Security (RLS)
-- See https://supabase.com/docs/guides/auth/row-level-security for more details.
alter table profiles
  enable row level security;

create policy "Public profiles are viewable by everyone." on profiles
  for select using (true);

create policy "Users can insert their own profile." on profiles
  for insert with check ((select auth.uid()) = id);

create policy "Users can update own profile." on profiles
  for update using ((select auth.uid()) = id);

-- This trigger automatically creates a profile entry when a new user signs up via Supabase Auth.
-- See https://supabase.com/docs/guides/auth/managing-user-data#using-triggers for more details.
create function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email);
  return new;
end;
$$ language plpgsql security definer;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

CREATE TABLE user_events (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES profiles(id),
    event_type              text            NOT NULL,
    event_data              jsonb,
    event_timestamp         timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES profiles(id)
);

CREATE TABLE check_ins (
    id                      uuid            NOT NULL DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES profiles(id),
    start_date              timestamptz(3)  NOT NULL,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE activity_status_options (
    id                      smallserial     NOT NULL,
    status                  varchar(20)     NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE activity_category_options (
    id                      smallserial     NOT NULL,
    category                varchar(20)     NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE activities (
    id                      uuid            NOT NULL DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES profiles(id),
    title                   text            NOT NULL DEFAULT '',
    description             text            NOT NULL DEFAULT '',
    category                varchar(20)     NOT NULL REFERENCES activity_category_options(category),
    status                  varchar(20)     NOT NULL REFERENCES activity_status_options(status),
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);

CREATE TABLE brag_docs (
    id                      uuid            NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    user_id                 uuid            NOT NULL REFERENCES profiles(id),
    version_number          integer         NOT NULL,
    data                    jsonb           NOT NULL DEFAULT '{}'::jsonb,
    created_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_on              timestamptz(3)  NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(id)
);


INSERT INTO activity_status_options (status) VALUES ('Not Started'), ('In Progress'), ('Completed'), ('Archived');
INSERT INTO activity_category_options (category) VALUES ('Skill'), ('Endorsement'), ('Achievement'), ('Miscellaneous');

CREATE TRIGGER trig_check_ins_updated_on BEFORE INSERT OR UPDATE ON check_ins FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_activities_updated_on BEFORE INSERT OR UPDATE ON activities FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
CREATE TRIGGER trig_brag_docs_updated_on BEFORE INSERT OR UPDATE ON brag_docs FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();