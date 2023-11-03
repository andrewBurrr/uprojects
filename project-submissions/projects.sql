BEGIN;

--
-- Create model Collaborator
--
CREATE TABLE "projects_collaborator" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "team_name" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Commit
--
CREATE TABLE "projects_commit" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "commit_id" varchar(60) NOT NULL
);

--
-- Create model Item
--
CREATE TABLE "projects_item" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Project
--
CREATE TABLE "projects_project" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "name" varchar(60) NOT NULL,
    "visibility" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Tag
--
CREATE TABLE "projects_tag" ("tag_name" varchar(60) NOT NULL PRIMARY KEY);

--
-- Create model CodeReview
--
CREATE TABLE "projects_codereview" (
    "item_ptr_id" bigint NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Issue
--
CREATE TABLE "projects_issue" (
    "item_ptr_id" bigint NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "issue_type" varchar(60) NOT NULL
);

--
-- Create model PullRequest
--
CREATE TABLE "projects_pullrequest" (
    "item_ptr_id" bigint NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "branch_name" varchar(60) NOT NULL
);

--
-- Create model Repository
--
CREATE TABLE "projects_repository" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "repo_name" varchar(60) NOT NULL,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Add field tags to project
--
CREATE TABLE "projects_project_tags" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "project_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" varchar(60) NOT NULL REFERENCES "projects_tag" ("tag_name") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model PartOf
--
CREATE TABLE "projects_partof" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Own
--
CREATE TABLE "projects_own" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Member
--
CREATE TABLE "projects_member" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "role" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Add field project_id to item
--
CREATE TABLE "new__projects_item" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO
    "new__projects_item" (
        "id",
        "item_id",
        "item_name",
        "status",
        "description",
        "is_approved",
        "due_date",
        "owner_id_id",
        "project_id_id"
    )
SELECT
    "id",
    "item_id",
    "item_name",
    "status",
    "description",
    "is_approved",
    "due_date",
    "owner_id_id",
    NULL
FROM
    "projects_item";

DROP TABLE "projects_item";

ALTER TABLE
    "new__projects_item" RENAME TO "projects_item";

CREATE INDEX "projects_collaborator_owner_id_id_b1d2900e" 
    ON "projects_collaborator" ("owner_id_id");

CREATE INDEX "projects_project_owner_id_id_0ceae041" 
    ON "projects_project" ("owner_id_id");

CREATE INDEX "projects_repository_project_id_id_def972fa" 
    ON "projects_repository" ("project_id_id");

CREATE UNIQUE INDEX "projects_project_tags_project_id_tag_id_5891719a_uniq" 
    ON "projects_project_tags" ("project_id", "tag_id");

CREATE INDEX "projects_project_tags_project_id_9bbfa17b" 
    ON "projects_project_tags" ("project_id");

CREATE INDEX "projects_project_tags_tag_id_c949773d" 
    ON "projects_project_tags" ("tag_id");

CREATE INDEX "projects_partof_owner_id_id_65bbe1e3" 
    ON "projects_partof" ("owner_id_id");

CREATE INDEX "projects_partof_project_id_id_5aea3206" 
    ON "projects_partof" ("project_id_id");

CREATE INDEX "projects_partof_team_name_id_9dfce6d8" 
    ON "projects_partof" ("team_name_id");

CREATE INDEX "projects_own_owner_id_id_251656c9" 
    ON "projects_own" ("owner_id_id");

CREATE INDEX "projects_own_project_id_id_889c56f9" 
    ON "projects_own" ("project_id_id");

CREATE INDEX "projects_member_owner_id_id_a39f68a0" 
    ON "projects_member" ("owner_id_id");

CREATE INDEX "projects_member_team_name_id_8f52c25d" 
    ON "projects_member" ("team_name_id");

CREATE INDEX "projects_member_user_id_id_59dad667" 
    ON "projects_member" ("user_id_id");

CREATE INDEX "projects_item_owner_id_id_ee2f9e13" 
    ON "projects_item" ("owner_id_id");

CREATE INDEX "projects_item_project_id_id_fb5c835a" 
    ON "projects_item" ("project_id_id");

--
-- Add field repo_name to item
--
CREATE TABLE "new__projects_item" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "repo_name_id" bigint NOT NULL REFERENCES "projects_repository" ("id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO
    "new__projects_item" (
        "id",
        "item_id",
        "item_name",
        "status",
        "description",
        "is_approved",
        "due_date",
        "owner_id_id",
        "project_id_id",
        "repo_name_id"
    )
SELECT
    "id",
    "item_id",
    "item_name",
    "status",
    "description",
    "is_approved",
    "due_date",
    "owner_id_id",
    "project_id_id",
    NULL
FROM
    "projects_item";

DROP TABLE "projects_item";

ALTER TABLE
    "new__projects_item" RENAME TO "projects_item";

CREATE INDEX "projects_item_owner_id_id_ee2f9e13" ON "projects_item" ("owner_id_id");

CREATE INDEX "projects_item_project_id_id_fb5c835a" ON "projects_item" ("project_id_id");

CREATE INDEX "projects_item_repo_name_id_55bcd92c" ON "projects_item" ("repo_name_id");

--
-- Add field team_name to item
--
ALTER TABLE
    "projects_item"
ADD
    COLUMN "team_name_id" bigint NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED;

--
-- Create model Follow
--
CREATE TABLE "projects_follow" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model CollaboratorPermission
--
CREATE TABLE "projects_collaboratorpermission" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "permission" varchar(1) NOT NULL,
    "collaborator_id_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Add field tags to collaborator
--
CREATE TABLE "projects_collaborator_tags" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "collaborator_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" varchar(60) NOT NULL REFERENCES "projects_tag" ("tag_name") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create constraint unique_project_repository_key_constraint on model repository
--
CREATE TABLE "new__projects_repository" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "repo_name" varchar(60) NOT NULL,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_repository_key_constraint" UNIQUE ("project_id_id", "repo_name")
);

INSERT INTO
    "new__projects_repository" ("id", "repo_name", "project_id_id")
SELECT
    "id",
    "repo_name",
    "project_id_id"
FROM
    "projects_repository";

DROP TABLE "projects_repository";

ALTER TABLE
    "new__projects_repository" RENAME TO "projects_repository";

CREATE INDEX "projects_item_team_name_id_9009666c" 
    ON "projects_item" ("team_name_id");

CREATE INDEX "projects_follow_project_id_id_419de939" 
    ON "projects_follow" ("project_id_id");

CREATE INDEX "projects_follow_user_id_id_51a01a0f" 
    ON "projects_follow" ("user_id_id");

CREATE INDEX "projects_collaboratorpermission_collaborator_id_id_2e4da7ca" 
    ON "projects_collaboratorpermission" ("collaborator_id_id");

CREATE UNIQUE INDEX "projects_collaborator_tags_collaborator_id_tag_id_f9ce0d0c_uniq" 
    ON "projects_collaborator_tags" ("collaborator_id", "tag_id");

CREATE INDEX "projects_collaborator_tags_collaborator_id_992afefd" 
    ON "projects_collaborator_tags" ("collaborator_id");

CREATE INDEX "projects_collaborator_tags_tag_id_8e9b5c79" 
    ON "projects_collaborator_tags" ("tag_id");

CREATE INDEX "projects_repository_project_id_id_def972fa" 
    ON "projects_repository" ("project_id_id");

--
-- Create constraint unique_project_owner_team_partof_constraint on model partof
--
CREATE TABLE "new__projects_partof" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_owner_team_partof_constraint" UNIQUE ("project_id_id", "owner_id_id", "team_name_id")
);

INSERT INTO
    "new__projects_partof" (
        "id",
        "owner_id_id",
        "project_id_id",
        "team_name_id"
    )
SELECT
    "id",
    "owner_id_id",
    "project_id_id",
    "team_name_id"
FROM
    "projects_partof";

DROP TABLE "projects_partof";

ALTER TABLE
    "new__projects_partof" RENAME TO "projects_partof";

CREATE INDEX "projects_partof_owner_id_id_65bbe1e3" 
    ON "projects_partof" ("owner_id_id");

CREATE INDEX "projects_partof_project_id_id_5aea3206" 
    ON "projects_partof" ("project_id_id");

CREATE INDEX "projects_partof_team_name_id_9dfce6d8" 
    ON "projects_partof" ("team_name_id");

--
-- Create constraint unique_owner_project_owns_constraint on model own
--
CREATE TABLE "new__projects_own" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_owner_project_owns_constraint" UNIQUE ("owner_id_id", "project_id_id")
);

INSERT INTO
    "new__projects_own" ("id", "owner_id_id", "project_id_id")
SELECT
    "id",
    "owner_id_id",
    "project_id_id"
FROM
    "projects_own";

DROP TABLE "projects_own";

ALTER TABLE
    "new__projects_own" RENAME TO "projects_own";

CREATE INDEX "projects_own_owner_id_id_251656c9" 
    ON "projects_own" ("owner_id_id");

CREATE INDEX "projects_own_project_id_id_889c56f9" 
    ON "projects_own" ("project_id_id");

--
-- Create constraint unique_user_owner_team_member_constraint on model member
--
CREATE TABLE "new__projects_member" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "role" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_user_owner_team_member_constraint" UNIQUE ("user_id_id", "owner_id_id", "team_name_id")
);

INSERT INTO
    "new__projects_member" (
        "id",
        "role",
        "owner_id_id",
        "team_name_id",
        "user_id_id"
    )
SELECT
    "id",
    "role",
    "owner_id_id",
    "team_name_id",
    "user_id_id"
FROM
    "projects_member";

DROP TABLE "projects_member";

ALTER TABLE
    "new__projects_member" RENAME TO "projects_member";

CREATE INDEX "projects_member_owner_id_id_a39f68a0" 
    ON "projects_member" ("owner_id_id");

CREATE INDEX "projects_member_team_name_id_8f52c25d" 
    ON "projects_member" ("team_name_id");

CREATE INDEX "projects_member_user_id_id_59dad667" 
    ON "projects_member" ("user_id_id");

--
-- Create constraint unique_project_repository_item_key_constraint on model item
--
CREATE TABLE "new__projects_item" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "repo_name_id" bigint NOT NULL REFERENCES "projects_repository" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" bigint NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_repository_item_key_constraint" UNIQUE ("project_id_id", "repo_name_id", "item_id")
);

INSERT INTO
    "new__projects_item" (
        "id",
        "item_id",
        "item_name",
        "status",
        "description",
        "is_approved",
        "due_date",
        "owner_id_id",
        "project_id_id",
        "repo_name_id",
        "team_name_id"
    )
SELECT
    "id",
    "item_id",
    "item_name",
    "status",
    "description",
    "is_approved",
    "due_date",
    "owner_id_id",
    "project_id_id",
    "repo_name_id",
    "team_name_id"
FROM
    "projects_item";

DROP TABLE "projects_item";

ALTER TABLE
    "new__projects_item" RENAME TO "projects_item";

CREATE INDEX "projects_item_owner_id_id_ee2f9e13" 
    ON "projects_item" ("owner_id_id");

CREATE INDEX "projects_item_project_id_id_fb5c835a" 
    ON "projects_item" ("project_id_id");

CREATE INDEX "projects_item_repo_name_id_55bcd92c" 
    ON "projects_item" ("repo_name_id");

CREATE INDEX "projects_item_team_name_id_9009666c" 
    ON "projects_item" ("team_name_id");

--
-- Create constraint unique_user_project_follow_constraint on model follow
--
CREATE TABLE "new__projects_follow" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_user_project_follow_constraint" UNIQUE ("user_id_id", "project_id_id")
);

INSERT INTO
    "new__projects_follow" ("id", "project_id_id", "user_id_id")
SELECT
    "id",
    "project_id_id",
    "user_id_id"
FROM
    "projects_follow";

DROP TABLE "projects_follow";

ALTER TABLE
    "new__projects_follow" RENAME TO "projects_follow";

CREATE INDEX "projects_follow_project_id_id_419de939" ON "projects_follow" ("project_id_id");

CREATE INDEX "projects_follow_user_id_id_51a01a0f" ON "projects_follow" ("user_id_id");

--
-- Create constraint unique_collaborator_permission_constraint on model collaboratorpermission
--
CREATE TABLE "new__projects_collaboratorpermission" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "permission" varchar(1) NOT NULL,
    "collaborator_id_id" bigint NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_collaborator_permission_constraint" UNIQUE ("collaborator_id_id", "permission")
);

INSERT INTO
    "new__projects_collaboratorpermission" ("id", "permission", "collaborator_id_id")
SELECT
    "id",
    "permission",
    "collaborator_id_id"
FROM
    "projects_collaboratorpermission";

DROP TABLE "projects_collaboratorpermission";

ALTER TABLE
    "new__projects_collaboratorpermission" RENAME TO "projects_collaboratorpermission";

CREATE INDEX "projects_collaboratorpermission_collaborator_id_id_2e4da7ca" 
    ON "projects_collaboratorpermission" ("collaborator_id_id");

--
-- Create constraint unique_owner_team_collaborator_constraint on model collaborator
--
CREATE TABLE "new__projects_collaborator" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "team_name" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_owner_team_collaborator_constraint" UNIQUE ("owner_id_id", "team_name")
);

INSERT INTO
    "new__projects_collaborator" ("id", "team_name", "owner_id_id")
SELECT
    "id",
    "team_name",
    "owner_id_id"
FROM
    "projects_collaborator";

DROP TABLE "projects_collaborator";

ALTER TABLE
    "new__projects_collaborator" RENAME TO "projects_collaborator";

CREATE INDEX "projects_collaborator_owner_id_id_b1d2900e" 
    ON "projects_collaborator" ("owner_id_id");

--
-- Add field commits to codereview
--
CREATE TABLE "projects_codereview_commits" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "codereview_id" bigint NOT NULL REFERENCES "projects_codereview" ("item_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "commit_id" bigint NOT NULL REFERENCES "projects_commit" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE UNIQUE INDEX "projects_codereview_commits_codereview_id_commit_id_e95922e7_uniq" 
    ON "projects_codereview_commits" ("codereview_id", "commit_id");

CREATE INDEX "projects_codereview_commits_codereview_id_373e0cda" 
    ON "projects_codereview_commits" ("codereview_id");

CREATE INDEX "projects_codereview_commits_commit_id_88c02a29" 
    ON "projects_codereview_commits" ("commit_id");

COMMIT;