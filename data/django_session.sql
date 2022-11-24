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

 Date: 04/11/2022 13:50:22
*/


-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_session";
CREATE TABLE "public"."django_session" (
  "session_key" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "session_data" text COLLATE "pg_catalog"."default" NOT NULL,
  "expire_date" timestamptz(6) NOT NULL
)
;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO "public"."django_session" VALUES ('nz0km8q7bu2ws4rereqwn118b0vzs027', '.eJxVjDEOwyAQBP9CHSEfZ4OdMr3fgA4OgpMIJGNXUf4eLLlImi1mZ_ctLO1bsnsNq11YXAWIyy9z5J8hHwU_KN-L9CVv6-LkocizrXIuHF630_07SFRTWxNo8Dz1YJgYzUhBtUQ1GsJJa4wBAjgcVOc1NQqdVoixH4CdMRHE5wvIAjba:1omHtw:FYNPmYbQXSbLSXolDTyCFoglYrei8vhMh4NCFA2dE0M', '2022-11-05 17:03:12.643919+00');

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "django_session_expire_date_a5c62663" ON "public"."django_session" USING btree (
  "expire_date" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);
CREATE INDEX "django_session_session_key_c0390e0f_like" ON "public"."django_session" USING btree (
  "session_key" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table django_session
-- ----------------------------
ALTER TABLE "public"."django_session" ADD CONSTRAINT "django_session_pkey" PRIMARY KEY ("session_key");
