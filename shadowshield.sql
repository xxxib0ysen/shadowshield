/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80033 (8.0.33)
 Source Host           : localhost:3306
 Source Schema         : shadowshield

 Target Server Type    : MySQL
 Target Server Version : 80033 (8.0.33)
 File Encoding         : 65001

 Date: 10/03/2025 23:35:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for content_filter
-- ----------------------------
DROP TABLE IF EXISTS `content_filter`;
CREATE TABLE `content_filter`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `keyword` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '关键词',
  `scope` int NOT NULL COMMENT '适用范围',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '过滤关键词的原因',
  `status` int NOT NULL DEFAULT 1 COMMENT '状态',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '内容过滤规则表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of content_filter
-- ----------------------------

-- ----------------------------
-- Table structure for cpu_memory_monitor
-- ----------------------------
DROP TABLE IF EXISTS `cpu_memory_monitor`;
CREATE TABLE `cpu_memory_monitor`  (
  `monitor_id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `cpu_usage` decimal(5, 2) NOT NULL COMMENT 'CPU使用率',
  `memory_usage` decimal(5, 2) NOT NULL COMMENT '内存使用率',
  `disk_usage` decimal(5, 2) NOT NULL COMMENT '磁盘使用率',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`monitor_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'CPU & 内存监控表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cpu_memory_monitor
-- ----------------------------

-- ----------------------------
-- Table structure for custom_rule
-- ----------------------------
DROP TABLE IF EXISTS `custom_rule`;
CREATE TABLE `custom_rule`  (
  `custom_rule_id` int NOT NULL AUTO_INCREMENT COMMENT '自定义规则ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '自定义规则名称',
  `type` int NOT NULL COMMENT '规则类型',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '规则详情',
  `status` int NOT NULL DEFAULT 1 COMMENT '状态',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`custom_rule_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户自定义规则表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of custom_rule
-- ----------------------------

-- ----------------------------
-- Table structure for log
-- ----------------------------
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` int NULL DEFAULT NULL COMMENT '用户ID',
  `action_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '操作类型',
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '详细信息',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '通用日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of log
-- ----------------------------

-- ----------------------------
-- Table structure for privacy_log
-- ----------------------------
DROP TABLE IF EXISTS `privacy_log`;
CREATE TABLE `privacy_log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '记录隐私相关操作',
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '操作内容',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '隐私日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of privacy_log
-- ----------------------------

-- ----------------------------
-- Table structure for rule
-- ----------------------------
DROP TABLE IF EXISTS `rule`;
CREATE TABLE `rule`  (
  `rule_id` int NOT NULL AUTO_INCREMENT COMMENT '规则ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '规则名称',
  `type` int NOT NULL COMMENT '规则类型',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '规则内容',
  `status` int NOT NULL DEFAULT 1 COMMENT '状态',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`rule_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '规则表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rule
-- ----------------------------

-- ----------------------------
-- Table structure for rule_engine_update
-- ----------------------------
DROP TABLE IF EXISTS `rule_engine_update`;
CREATE TABLE `rule_engine_update`  (
  `update_id` int NOT NULL AUTO_INCREMENT COMMENT '更新ID',
  `rule_type` int NOT NULL COMMENT '规则类型',
  `version` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '规则库版本号',
  `updatedon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`update_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '规则引擎更新记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rule_engine_update
-- ----------------------------

-- ----------------------------
-- Table structure for rule_execution_log
-- ----------------------------
DROP TABLE IF EXISTS `rule_execution_log`;
CREATE TABLE `rule_execution_log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `rule_id` int NOT NULL COMMENT '规则ID',
  `user_id` int NULL DEFAULT NULL COMMENT '触发规则的用户',
  `triggered_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '被拦截的内容',
  `triggered_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_rule_id`(`rule_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '规则执行日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rule_execution_log
-- ----------------------------

-- ----------------------------
-- Table structure for rule_log
-- ----------------------------
DROP TABLE IF EXISTS `rule_log`;
CREATE TABLE `rule_log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `rule_id` int NOT NULL COMMENT '规则ID',
  `user_id` int NULL DEFAULT NULL COMMENT '触发规则的用户',
  `type` int NOT NULL COMMENT '规则类型',
  `triggered_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '触发内容',
  `triggered_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '触发时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_rule_id`(`rule_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '规则日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rule_log
-- ----------------------------

-- ----------------------------
-- Table structure for system_monitor_log
-- ----------------------------
DROP TABLE IF EXISTS `system_monitor_log`;
CREATE TABLE `system_monitor_log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `event_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '事件类型',
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '详细记录异常内容',
  `severity` int NOT NULL COMMENT '严重性',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`log_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统监控日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_monitor_log
-- ----------------------------

-- ----------------------------
-- Table structure for ums_menu
-- ----------------------------
DROP TABLE IF EXISTS `ums_menu`;
CREATE TABLE `ums_menu`  (
  `menu_id` int NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `menu_pid` int NULL DEFAULT NULL COMMENT '父级菜单 ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单名称',
  `level` int NULL DEFAULT NULL COMMENT '菜单层级',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '前端路由命名',
  `icon` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `hidden` int NOT NULL DEFAULT 0 COMMENT '是否隐藏菜单（0=显示，1=隐藏）',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `window_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '窗口标识',
  PRIMARY KEY (`menu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_menu
-- ----------------------------
INSERT INTO `ums_menu` VALUES (4, 0, '后台管理', 1, 'ums', 'Management', 0, '2025-03-09 23:15:49', 'B');
INSERT INTO `ums_menu` VALUES (5, 4, '用户列表', 2, 'user', 'UserFilled', 0, '2025-03-09 23:19:07', 'B');
INSERT INTO `ums_menu` VALUES (6, 4, '角色列表', 2, 'role', 'Avatar', 0, '2025-03-09 23:22:35', 'B');
INSERT INTO `ums_menu` VALUES (7, 4, '菜单列表', 2, 'menu', 'Menu', 0, '2025-03-09 23:23:38', 'B');
INSERT INTO `ums_menu` VALUES (8, 4, '资源列表', 2, 'resource', 'Grid', 0, '2025-03-10 00:14:28', 'B');
INSERT INTO `ums_menu` VALUES (9, 4, '权限列表', 2, 'permission', 'Opportunity', 0, '2025-03-10 00:15:11', 'B');
INSERT INTO `ums_menu` VALUES (10, 0, '首页', 1, 'home', 'HomeFilled', 0, '2025-03-10 00:19:19', 'A');
INSERT INTO `ums_menu` VALUES (11, 0, '浏览保护', 1, 'BrowsingProtection', 'HelpFilled', 0, '2025-03-10 00:22:00', 'A');
INSERT INTO `ums_menu` VALUES (12, 0, '广告拦截', 1, 'AdBlock', 'RemoveFilled', 0, '2025-03-10 00:24:21', 'A');
INSERT INTO `ums_menu` VALUES (13, 0, '监控防护', 1, 'monitor', 'InfoFilled', 0, '2025-03-10 00:25:30', 'A');
INSERT INTO `ums_menu` VALUES (14, 0, '日志分析', 1, 'log', 'List', 0, '2025-03-10 00:26:09', 'A');
INSERT INTO `ums_menu` VALUES (15, 0, '上网管理', 1, 'network', 'Platform', 0, '2025-03-10 00:28:49', 'A');
INSERT INTO `ums_menu` VALUES (16, 0, '系统设置', 1, 'setting', 'Tools', 0, '2025-03-10 00:30:58', 'A');

-- ----------------------------
-- Table structure for ums_permission
-- ----------------------------
DROP TABLE IF EXISTS `ums_permission`;
CREATE TABLE `ums_permission`  (
  `permission_id` int NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `permission_pid` bigint NULL DEFAULT NULL COMMENT '父级权限 ID',
  `permission_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限名称',
  `permission_value` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限值',
  `permission_icon` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限图标',
  `permission_type` int NULL DEFAULT NULL COMMENT '权限类型：1=页面权限, 2=操作权限, 3=数据权限',
  `permission_uri` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '前端资源路径',
  `permission_status` int NULL DEFAULT NULL COMMENT '启用状态：0->禁用；1->启用',
  `permission_createdon` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '权限创建时间',
  PRIMARY KEY (`permission_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '权限表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_permission
-- ----------------------------

-- ----------------------------
-- Table structure for ums_resource
-- ----------------------------
DROP TABLE IF EXISTS `ums_resource`;
CREATE TABLE `ums_resource`  (
  `resource_id` int NOT NULL AUTO_INCREMENT COMMENT '资源ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '资源名称',
  `category_id` int NOT NULL COMMENT '资源分类',
  `uri` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源访问路径',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源详细描述',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`resource_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '资源表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_resource
-- ----------------------------

-- ----------------------------
-- Table structure for ums_resource_category
-- ----------------------------
DROP TABLE IF EXISTS `ums_resource_category`;
CREATE TABLE `ums_resource_category`  (
  `category_id` int NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `category_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分类名称，如“系统管理”',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '分类描述',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '资源分类表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_resource_category
-- ----------------------------

-- ----------------------------
-- Table structure for ums_role
-- ----------------------------
DROP TABLE IF EXISTS `ums_role`;
CREATE TABLE `ums_role`  (
  `role_id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色描述',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '角色创建时间',
  `status` int NOT NULL DEFAULT 1 COMMENT '账号启用状态：0->禁用；1->启用',
  `count` int NULL DEFAULT 0 COMMENT '该角色下的用户数量',
  PRIMARY KEY (`role_id`) USING BTREE,
  UNIQUE INDEX `role_name`(`role_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_role
-- ----------------------------
INSERT INTO `ums_role` VALUES (1, '超级管理员', '系统最高权限', '2025-02-28 15:37:14', 1, 0);
INSERT INTO `ums_role` VALUES (2, '测试角色', '测试测试测试111111237657547436646665343456634666356354', '2025-03-09 15:51:41', 1, 0);

-- ----------------------------
-- Table structure for ums_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `ums_role_menu`;
CREATE TABLE `ums_role_menu`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_role_id`(`role_id` ASC) USING BTREE,
  INDEX `idx_menu_id`(`menu_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色-菜单关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_role_menu
-- ----------------------------

-- ----------------------------
-- Table structure for ums_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `ums_role_permission`;
CREATE TABLE `ums_role_permission`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `permission_id` int NOT NULL COMMENT '权限ID',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_role_id`(`role_id` ASC) USING BTREE,
  INDEX `idx_permission_id`(`permission_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色-权限关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_role_permission
-- ----------------------------

-- ----------------------------
-- Table structure for ums_role_resource
-- ----------------------------
DROP TABLE IF EXISTS `ums_role_resource`;
CREATE TABLE `ums_role_resource`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `resource_id` int NOT NULL COMMENT '资源ID',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_role_id`(`role_id` ASC) USING BTREE,
  INDEX `idx_resource_id`(`resource_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色-资源关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_role_resource
-- ----------------------------

-- ----------------------------
-- Table structure for ums_user
-- ----------------------------
DROP TABLE IF EXISTS `ums_user`;
CREATE TABLE `ums_user`  (
  `user_id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账号',
  `fullname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户真实姓名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '加密后的用户密码',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '用户创建时间',
  `lastlogin` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `status` int NOT NULL DEFAULT 1 COMMENT '账号启用状态：0->禁用；1->启用',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_user
-- ----------------------------
INSERT INTO `ums_user` VALUES (1, 'root', '超级管理员', '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', '2025-02-28 15:37:14', '2025-03-10 23:32:46', 1);
INSERT INTO `ums_user` VALUES (2, 'hr1', '测试', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2025-03-08 21:16:39', NULL, 0);

-- ----------------------------
-- Table structure for ums_user_role
-- ----------------------------
DROP TABLE IF EXISTS `ums_user_role`;
CREATE TABLE `ums_user_role`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_role_id`(`role_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户-角色关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ums_user_role
-- ----------------------------
INSERT INTO `ums_user_role` VALUES (1, 1, 1, '2025-02-28 15:37:14');

-- ----------------------------
-- Table structure for website_blacklist
-- ----------------------------
DROP TABLE IF EXISTS `website_blacklist`;
CREATE TABLE `website_blacklist`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `domain` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '被拦截的网站',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '拦截原因',
  `status` int NOT NULL DEFAULT 1 COMMENT '状态',
  `createdon` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网站黑名单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of website_blacklist
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
