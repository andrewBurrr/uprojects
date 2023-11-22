--
-- Create model BugReport
CREATE TABLE "bugreport" (
    "bug_id" char(32) NOT NULL PRIMARY KEY,
    "time_stamp" datetime NOT NULL,
    "description" text NOT NULL,
    "user_id" char(32) NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED
);


--
-- Create model Tag
CREATE TABLE "tag" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "tag" varchar(60) NOT NULL UNIQUE,
    CONSTRAINT "UC_Tag" UNIQUE ("id","tag")
);


--
-- Create model Respond
CREATE TABLE "respond" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "admin_id" char(32) NULL REFERENCES "users_customadmin" ("id") DEFERRABLE INITIALLY DEFERRED,
    "bug_id" char(32) NULL REFERENCES "bugreport" ("bug_id") DEFERRABLE INITIALLY DEFERRED,
    "time_stamp" datetime NOT NULL,
    "comment" text NOT NULL,
    CONSTRAINT "unique_admin_bug_respond_constraint" UNIQUE ("admin_id", "bug_id","time_stamp")
);


--
-- Create model Collaborator
CREATE TABLE "collaborator" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "team_name" varchar(60) NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_owner_team_collaborator_constraint" UNIQUE ("owner_id", "team_name")
);


--
-- Create model Commit
CREATE TABLE "commit" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "commit_id" varchar(60) NOT NULL
);


--
-- Create model Item
CREATE TABLE "projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED
);


--
-- Create model Project
CREATE TABLE "project" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "name" varchar(60) NOT NULL,
    "visibility" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED
);


--
-- Create model CodeReview
CREATE TABLE "codereview" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "codereview_id" char(32) NOT NULL REFERENCES "codereview" ("item_id") DEFERRABLE INITIALLY DEFERRED,
    "commit_id" char(32) NOT NULL REFERENCES "commit" ("id") DEFERRABLE INITIALLY DEFERRED
);


--
-- Create model Issue
CREATE TABLE "projects_issue" (
    "item_id" char(32) NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "issue_type" varchar(60) NOT NULL
);


--
-- Create model PullRequest
CREATE TABLE "pullrequest" (
    "item_id" char(32) NOT NULL PRIMARY KEY REFERENCES "projects_item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "branch_name" varchar(60) NOT NULL
);

--
-- Create model Repository
CREATE TABLE "repository" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "repo_name" varchar(60) NOT NULL,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_repository_key_constraint" UNIQUE ("project_id", "repo_name")
);


--
-- Create model PartOf
CREATE TABLE "partof" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id" char(32) NOT NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_owner_team_partof_constraint" UNIQUE ("project_id", "owner_id", "team_name_id")
);


--
-- Create model Own
CREATE TABLE "projects_own" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id" char(32) NOT NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED
);


--
-- Create model Member
CREATE TABLE "member" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "role" varchar(60) NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NOT NULL REFERENCES "collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_user_owner_team_member_constraint" UNIQUE ("user_id", "owner_id", "team_name_id")
);


--
-- Create model Event
CREATE TABLE "event" (
    "event_id" char(32) NOT NULL PRIMARY KEY,
    "event_type" varchar(60) NOT NULL,
    "owner_id" char(32) NULL REFERENCES "projects_organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    "start_date" datetime NOT NULL,
    "end_date" datetime NOT NULL,
    "name" varcahr(60) NOT NULL
);


--
-- Create model Hosts
CREATE TABLE "projects_hosts" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "org_id" char(32) NOT NULL REFERENCES "projects_organization" ("org_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_event_org_host_constraint" UNIQUE ("event_id", "org_id")
);


--
-- Create model ProjectSubmission
CREATE TABLE "projectsubmission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id" char(32) NOT NULL REFERENCES "projects_organization" ("owner_id") DEFERRABLE INITIALLY DEFERRED,
    "team_name" varchar(60) NOT NULL REFERENCES "projects_organization" ("name") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_event_owner_project_submission_constraint" UNIQUE ("event_id", "owner_id")
);


--
-- Create model FileSubmission
CREATE TABLE "filesubmission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "event_id" char(32) NOT NULL REFERENCES "event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "owner_id" char(32) NOT NULL REFERENCES "projects_organization" ("owner_id") DEFERRABLE INITIALLY DEFERRED,
    "team_name" varchar(60) NOT NULL REFERENCES "projects_organization" ("name") DEFERRABLE INITIALLY DEFERRED,
    "file" varchar(100) NOT NULL,
    "file_type"  varchar(20) NOT NULL,
    CONSTRAINT "unique_event_owner_name_file_submission_constraint" UNIQUE ("event_id", "owner_id", "team_name")
);


--
-- Add field project_id to item
CREATE TABLE "projects_item" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "item_id" integer NOT NULL,
    "item_name" varchar(60) NOT NULL,
    "status" varchar(60) NOT NULL,
    "description" text NOT NULL,
    "is_approved" bool NOT NULL,
    "due_date" date NOT NULL,
    "owner_id" char(32) NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "repo_name_id" char(32) NOT NULL REFERENCES "repository" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_name_id" char(32) NULL REFERENCES "collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_project_repository_item_key_constraint" UNIQUE ("project_id", "repo_name_id", "item_id")
);


--
-- Create model Follow
--
CREATE TABLE "follow" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" char(32) NOT NULL REFERENCES "users_customuser" ("customaccount_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_user_project_follow_constraint" UNIQUE ("user_id", "project_id")
);


--
-- Create model CollaboratorPermission
CREATE TABLE "collaboratorpermission" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "permission" varchar(1) NOT NULL,
    "collaborator_id" char(32) NOT NULL REFERENCES "collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_collaborator_permission_constraint" UNIQUE ("collaborator_id", "permission")
);


--
-- Add field tags to collaborator
--
CREATE TABLE "collabTags" (
    "collaborator_id" char(32) NOT NULL REFERENCES "collaborator" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_collaborator" UNIQUE ("project_id", "tag_id")
);


--
-- Create constraint unique_owner_project_owns_constraint on model own
CREATE TABLE "new__projects_own" (
    "id" char(32) NOT NULL PRIMARY KEY,
    "owner_id" char(32) NOT NULL REFERENCES "owner" ("id") DEFERRABLE INITIALLY DEFERRED,
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_owner_project_owns_constraint" UNIQUE ("owner_id", "project_id")
);


--
-- Create model EventTags
CREATE TABLE "eventTags" (
    "event_id" char(32) NOT NULL REFERENCES "event" ("event_id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_event" UNIQUE ("event_id", "tag_id")
);


--
-- Create model ProjectTags
CREATE TABLE "projecttags" (
    "project_id" char(32) NOT NULL REFERENCES "project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" char(32) NOT NULL REFERENCES "tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "UC_Tag_project" UNIQUE ("project_id", "tag_id")
);
