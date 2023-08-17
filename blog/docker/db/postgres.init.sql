/* put database initialization script here */

-- for example
CREATE ROLE blogadmin WITH ENCRYPTED PASSWORD 'password' LOGIN;
COMMENT ON ROLE blogadmin IS 'docker user for tests';

CREATE DATABASE blogdb OWNER blogadmin;
COMMENT ON DATABASE blogdb IS 'docker db for tests owned by docker user';
