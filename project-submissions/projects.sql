--
-- Create model BugReport
--
CREATE TABLE "projects_bugreport" {
    "bug_id" char(32) NOT NULL PRIMARY KEY,
    "time_stamp" datetime NOT NULL,
    "description" text NOT NULL,
    "user_id" char(32) NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Tag
--
CREATE TABLE "tag" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "tag" varchar(60) NOT NULL UNIQUE,
    CONSTRAINT "UC_Tag" UNIQUE ("id","tag")
);

--
-- Create model Respond
--
CREATE TABLE "projects_respond" {
    "id" char(32) NOT NULL PRIMARY KEY,
    "admin_id" char(32) NULL REFERENCES "users_customadmin" ("id") DEFERRABLE INITIALLY DEFERRED,
    "bug_id" char(32) NULL REFERENCES "projects_bugreport" ("bug_id") DEFERRABLE INITIALLY DEFERRED,
    "comment" text NOT NULL,
    CONSTRAINT "unique_admin_bug_respond_constraint" UNIQUE ("admin_id", "bug_id")
);

--
-- Create model Collaborator
--
CREATE TABLE "projects_collaborator" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "team_name" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Commit
--
CREATE TABLE "projects_commit" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "commit_id" varchar(60) NOT NULL
);

--
-- Create model Item
--
CREATE TABLE "projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
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
-- Create model CodeReview
--
CREATE TABLE "projects_codereview" (
    "item_ptr_id" char(32) NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Issue
--
CREATE TABLE "projects_issue" (
    "item_ptr_id" char(32) NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "issue_type" varchar(60) NOT NULL
);

--
-- Create model PullRequest
--
CREATE TABLE "projects_pullrequest" (
    "item_ptr_id" char(32) NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "branch_name" varchar(60) NOT NULL
);

--
-- Create model Repository
--
CREATE TABLE "projects_repository" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "repo_name" varchar(60) NOT NULL,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Add field tags to project
--
CREATE TABLE "projects_project_tags" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "project_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" varchar(60) NOT NULL REFERENCES "projects_tag" ("tag_name") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model PartOf
--
CREATE TABLE "projects_partof" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Own
--
CREATE TABLE "projects_own" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Member
--
CREATE TABLE "projects_member" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "role" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model Event
--
CREATE TABLE "projects_event" (
    "event_id" char(32) NOT NULL PRIMARY KEY,
    "event_type" varchar(60) NOT NULL,
    "owner_id" char(32) NULL REFERENCES "projects_organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    "start_date" datetime NOT NULL,
    "end_date" datetime NOT NULL,
    "name" varcahr(60) NOT NULL
);

--
-- Create model Hosts
--
CREATE TABLE "projects_hosts" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "projects_event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "org_id" char(32) NOT NULL REFERENCES "projects_organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_event_org_host_constraint" UNIQUE ("event_id", "org_id")
);

--
-- Create model ProjectSubmission
--
CREATE TABLE "projects_projectsubmission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "projects_event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id" char(32) NOT NULL REFERENCES "projects_organization" ("owner_id_id") DEFERRABLE INITIALLY DEFERRED,
    "team_name" varchar(60) NOT NULL REFERENCES "projects_organization" ("name") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_event_owner_project_submission_constraint" UNIQUE ("event_id", "owner_id")
);

--
-- Create model FileSubmission
--
CREATE TABLE "projects_filesubmission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "projects_event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id" char(32) NOT NULL REFERENCES "projects_organization" ("owner_id_id") DEFERRABLE INITIALLY DEFERRED,
    "team_name" varchar(60) NOT NULL REFERENCES "projects_organization" ("name") DEFERRABLE INITIALLY DEFERRED,
    "file" varchar(100) NOT NULL,
    "file_type"  varchar(20) NOT NULL,
    CONSTRAINT "unique_event_owner_name_file_submission_constraint" UNIQUE ("event_id", "owner_id", "team_name")
);

--
-- Add field project_id to item
--
CREATE TABLE "new__projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
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

--
-- Add field repo_name to item
--
CREATE TABLE "new__projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "repo_name_id" char(32) NOT NULL REFERENCES "projects_repository" ("id") DEFERRABLE INITIALLY DEFERRED
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

--
-- Add field team_name to item
--
ALTER TABLE
    "projects_item"
ADD
    COLUMN "team_name_id" char(32) NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED;

--
-- Create model Follow
--
CREATE TABLE "projects_follow" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model CollaboratorPermission
--
CREATE TABLE "projects_collaboratorpermission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "permission" varchar(1) NOT NULL,
    "collaborator_id_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Add field tags to collaborator
--
CREATE TABLE "projects_collaboratortags" (
    "collaborator_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_collaborator" UNIQUE ("project_id", "tag_id")
);

--
-- Create constraint unique_project_repository_key_constraint on model repository
--
CREATE TABLE "new__projects_repository" (
    "id" char(32) NOT NULL PRIMARY KEY,
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
--
-- Create constraint unique_project_owner_team_partof_constraint on model partof
--
CREATE TABLE "new__projects_partof" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id_id" char(32) NOT NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
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

--
-- Create constraint unique_owner_project_owns_constraint on model own
--
CREATE TABLE "new__projects_own" (
    "id" char(32) NOT NULL PRIMARY KEY,
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

--
-- Create constraint unique_user_owner_team_member_constraint on model member
--
CREATE TABLE "new__projects_member" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "role" varchar(60) NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
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

--
-- Create constraint unique_project_repository_item_key_constraint on model item
--
CREATE TABLE "new__projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id_id" char(32) NULL REFERENCES "users_owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "repo_name_id" char(32) NOT NULL REFERENCES "projects_repository" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
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

--
-- Create constraint unique_user_project_follow_constraint on model follow
--
CREATE TABLE "new__projects_follow" (
    "id" char(32) NOT NULL PRIMARY KEY,
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

--
-- Create constraint unique_collaborator_permission_constraint on model collaboratorpermission
--
CREATE TABLE "new__projects_collaboratorpermission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "permission" varchar(1) NOT NULL,
    "collaborator_id_id" char(32) NOT NULL REFERENCES "projects_collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
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

--
-- Create constraint unique_owner_team_collaborator_constraint on model collaborator
--
CREATE TABLE "new__projects_collaborator" (
    "id" char(32) NOT NULL PRIMARY KEY,
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

--
-- Add field commits to codereview
--
CREATE TABLE "projects_codereview_commits" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "codereview_id" char(32) NOT NULL REFERENCES "projects_codereview" ("item_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "commit_id" char(32) NOT NULL REFERENCES "projects_commit" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model EventTags
--
CREATE TABLE "projects_eventtags" (
    "event_id" char(32) NOT NULL REFERENCES "projects_event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_event" UNIQUE ("event_id", "tag_id")
);

--
-- Create model ProjectTags
--
CREATE TABLE "projects_projecttags" (
    "project_id" char(32) NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_project" UNIQUE ("project_id", "tag_id")
);
