-- Create model CustomAccount
CREATE TABLE "customAccount" (
    "password" varchar(128) NOT NULL,
    "last_login" datetime NULL,
    "is_superuser" bool NOT NULL,
    "id" char(32) NOT NULL PRIMARY KEY,
    "profile_image" varchar(100) NOT NULL,
    "email" varchar(254) NOT NULL UNIQUE,
    "first_name" varchar(150) NOT NULL,
    "last_name" varchar(150) NOT NULL,
    "start_date" datetime NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL
);


CREATE TABLE "user_permissions" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "user_id" char(32) NOT NULL REFERENCES "customAccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- Create model Interest
CREATE TABLE "Interest" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "interest" varchar(60) NOT NULL UNIQUE);


-- Create model Owner
CREATE TABLE "owner" ("id" char(32) NOT NULL PRIMARY KEY);


-- Create model Tag
CREATE TABLE "Tag" (UTOINCR
    "id" char(32) NOT NULL PRIMARY KEY,
    "tag" varchar(60) NOT NULL UNIQUE,
    CONSTRAINT UC_Tag UNIQUE ("id","tag"),
    );


-- Create model CustomAdmin
CREATE TABLE "customadmin" (
    "user_id" char(32) NOT NULL PRIMARY KEY REFERENCES "customAccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "admin_type" varchar(60) NOT NULL,
);


-- Create model Organization
CREATE TABLE "Organization" (
    "org_id" char(32) NOT NULL PRIMARY KEY,
    "logo" varchar(100) NOT NULL,
    "name" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
);


CREATE TABLE "OrgTag" (
    "organization_id" char(32) NOT NULL REFERENCES "Organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "Tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT UC_OrgTag UNIQUE ("organization_id", "tag_id"),
);


-- Create model CustomUser
CREATE TABLE "customuser" (
    "user_id" char(32) NOT NULL PRIMARY KEY REFERENCES "customAccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED
    CONSTRAINT UC_customuser UNIQUE ("user_id", "owner_id")
);


CREATE TABLE "userInterests" (
    "user_id" char(32) NOT NULL REFERENCES "customuser" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "interest_id" char(32) NOT NULL REFERENCES "Interest" ("id") DEFERRABLE INITIALLY DEFERRED
    CONSTRAINT UC_userInterests UNIQUE ("user_id", "interest_id")
);

--
-- Create model CustomAdminPermission
--
CREATE TABLE "adminpermission" (
    "permission" varchar(1) NOT NULL,
    "admin_id" char(32) NOT NULL REFERENCES "customadmin" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT UC_Adminperms UNIQUE ("permission", "admin_id")
);

