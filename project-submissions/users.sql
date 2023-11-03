BEGIN;

--
-- Create model CustomAccount
--
CREATE TABLE "users_customaccount" (
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

CREATE TABLE "users_customaccount_groups" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "customaccount_id" char(32) NOT NULL REFERENCES "users_customaccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE "users_customaccount_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "customaccount_id" char(32) NOT NULL REFERENCES "users_customaccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Interest
--
CREATE TABLE "users_interest" ("interest" varchar(60) NOT NULL PRIMARY KEY);

--
-- Create model Owner
--
CREATE TABLE "users_owner" ("id" char(32) NOT NULL PRIMARY KEY);

--
-- Create model Tag
--
CREATE TABLE "users_tag" ("tag" varchar(60) NOT NULL PRIMARY KEY);

--
-- Create model CustomAdmin
--
CREATE TABLE "users_customadmin" (
    "customaccount_ptr_id" char(32) NOT NULL PRIMARY KEY REFERENCES "users_customaccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "admin_type" varchar(60) NOT NULL
);

--
-- Create model Organization
--
CREATE TABLE "users_organization" (
    "org_id" char(32) NOT NULL PRIMARY KEY,
    "logo" varchar(100) NOT NULL,
    "name" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE "users_organization_tag" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "organization_id" char(32) NOT NULL REFERENCES "users_organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" varchar(60) NOT NULL REFERENCES "users_tag" ("tag") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model CustomUser
--
CREATE TABLE "users_customuser" (
    "customaccount_ptr_id" char(32) NOT NULL PRIMARY KEY REFERENCES "users_customaccount" ("id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE "users_customuser_interest" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "customuser_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "interest_id" varchar(60) NOT NULL REFERENCES "users_interest" ("interest") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model CustomAdminPermission
--
CREATE TABLE "users_customadminpermission" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "permission" varchar(1) NOT NULL,
    "admin_id_id" char(32) NOT NULL REFERENCES "users_customadmin" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create constraint unique_admin_permission_constraint on model customadminpermission
--
CREATE TABLE "new__users_customadminpermission" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "permission" varchar(1) NOT NULL,
    "admin_id_id" char(32) NOT NULL REFERENCES "users_customadmin" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_admin_permission_constraint" UNIQUE ("admin_id_id", "permission")
);

INSERT INTO
    "new__users_customadminpermission" ("id", "permission", "admin_id_id")
SELECT
    "id",
    "permission",
    "admin_id_id"
FROM
    "users_customadminpermission";

DROP TABLE "users_customadminpermission";

ALTER TABLE
    "new__users_customadminpermission" RENAME TO "users_customadminpermission";

CREATE UNIQUE INDEX "users_customaccount_groups_customaccount_id_group_id_52bfee2f_uniq" 
    ON "users_customaccount_groups" ("customaccount_id", "group_id");

CREATE INDEX "users_customaccount_groups_customaccount_id_7ac7df7c" 
    ON "users_customaccount_groups" ("customaccount_id");

CREATE INDEX "users_customaccount_groups_group_id_7a4184a7" 
    ON "users_customaccount_groups" ("group_id");

CREATE UNIQUE INDEX "users_customaccount_user_permissions_customaccount_id_permission_id_1c72516c_uniq" 
    ON "users_customaccount_user_permissions" ("customaccount_id", "permission_id");

CREATE INDEX "users_customaccount_user_permissions_customaccount_id_b60963ad" 
    ON "users_customaccount_user_permissions" ("customaccount_id");

CREATE INDEX "users_customaccount_user_permissions_permission_id_93437528" 
    ON "users_customaccount_user_permissions" ("permission_id");

CREATE INDEX "users_organization_owner_id_id_bad05eb0" 
    ON "users_organization" ("owner_id_id");

CREATE UNIQUE INDEX "users_organization_tag_organization_id_tag_id_50216fb4_uniq" 
    ON "users_organization_tag" ("organization_id", "tag_id");

CREATE INDEX "users_organization_tag_organization_id_cb055b82" 
    ON "users_organization_tag" ("organization_id");

CREATE INDEX "users_organization_tag_tag_id_9f989c99" 
    ON "users_organization_tag" ("tag_id");

CREATE INDEX "users_customuser_owner_id_id_b1ece482" 
    ON "users_customuser" ("owner_id_id");

CREATE UNIQUE INDEX "users_customuser_interest_customuser_id_interest_id_edd05eb6_uniq" 
    ON "users_customuser_interest" ("customuser_id", "interest_id");

CREATE INDEX "users_customuser_interest_customuser_id_8b841d9a" 
    ON "users_customuser_interest" ("customuser_id");

CREATE INDEX "users_customuser_interest_interest_id_903e8336" 
    ON "users_customuser_interest" ("interest_id");

CREATE INDEX "users_customadminpermission_admin_id_id_5e0ff70f" 
    ON "users_customadminpermission" ("admin_id_id");

COMMIT;