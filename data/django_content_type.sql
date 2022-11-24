/*
 Navicat Premium Data Transfer

 Source Server         : awm2023
 Source Server Type    : PostgreSQL
 Source Server Version : 130003
 Source Host           : localhost:25432
 Source Catalog        : gis
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 130003
 File Encoding         : 65001

 Date: 04/11/2022 13:50:13
*/


-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_content_type";
CREATE TABLE "public"."django_content_type" (
  "id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "app_label" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "model" varchar(100) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO "public"."django_content_type" VALUES (1, 'admin', 'logentry');
INSERT INTO "public"."django_content_type" VALUES (2, 'auth', 'permission');
INSERT INTO "public"."django_content_type" VALUES (3, 'auth', 'group');
INSERT INTO "public"."django_content_type" VALUES (4, 'auth', 'user');
INSERT INTO "public"."django_content_type" VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "public"."django_content_type" VALUES (6, 'sessions', 'session');
INSERT INTO "public"."django_content_type" VALUES (7, 'awm2023', 'worldborder');
INSERT INTO "public"."django_content_type" VALUES (8, 'awm2023', 'profile');

-- ----------------------------
-- Auto increment value for django_content_type
-- ----------------------------
SELECT setval('"public"."django_content_type_id_seq"', 8, true);

-- ----------------------------
-- Uniques structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_app_label_model_76bd3d3b_uniq" UNIQUE ("app_label", "model");

-- ----------------------------
-- Primary Key structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_pkey" PRIMARY KEY ("id");
