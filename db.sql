CREATE DATABASE `neihanshequ` DEFAULT CHARSET utf8 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `material` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `rel_id` VARCHAR(64) NOT NULL COMMENT '视频或图片的ID',
    `content` VARCHAR(1024) NOT NULL COMMENT '视频或图片的文字描述',
    `category_id` INT(11) NOT NULL COMMENT '分类ID',
    `category_name` VARCHAR(128) NOT NULL COMMENT '分类名称',
    `url` VARCHAR(512) NOT NULL COMMENT '视频或图片的URL',
    `online_time` BIGINT(20) COMMENT '上线时间，可以做排序',
    `user_id` BIGINT(20) NOT NULL COMMENT '发布者ID',
    `user_name` VARCHAR(128) NOT NULL COMMENT '发布者名称',
    `user_avatar` VARCHAR(258) NOT NULL COMMENT '发布者头像',
    `play_count` INT(11) DEFAULT '0' COMMENT '视频播放次数',
    `bury_count` INT(11) DEFAULT '0' COMMENT '被踩次数',
    `repin_count` INT(11) DEFAULT '0' COMMENT '被顶次数',
    `share_count` INT(11) DEFAULT '0' COMMENT '分享次数',
    `has_comments` INT(11) DEFAULT '0' COMMENT '是否有置顶评论',
    `comments` TEXT COMMENT '置顶评论列表',
    PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
ALTER TABLE `material` ADD UNIQUE (`rel_id`);


CREATE TABLE IF NOT EXISTS `videos` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `group_id` BIGINT(20) NOT NULL COMMENT '视频分组ID',
    `item_id` BIGINT(20) NOT NULL COMMENT '该记录在第三方平台的ID',
    `video_id` VARCHAR(64) NOT NULL COMMENT '视频的ID',
    `content` VARCHAR(1024) NOT NULL COMMENT '视频的文字描述',
    `category_id` INT(11) NOT NULL COMMENT '分类ID',
    `category_name` VARCHAR(128) NOT NULL COMMENT '分类名称',
    `url` VARCHAR(512) NOT NULL COMMENT '视频或图片的URL',
    `online_time` BIGINT(20) COMMENT '上线时间，可以做排序',
    `user_id` BIGINT(20) NOT NULL COMMENT '发布者ID',
    `user_name` VARCHAR(128) NOT NULL COMMENT '发布者名称',
    `user_avatar` VARCHAR(258) NOT NULL COMMENT '发布者头像',
    `play_count` INT(11) DEFAULT '0' COMMENT '视频播放次数',
    `bury_count` INT(11) DEFAULT '0' COMMENT '被踩次数',
    `repin_count` INT(11) DEFAULT '0' COMMENT '被顶次数',
    `share_count` INT(11) DEFAULT '0' COMMENT '分享次数',
    `has_comments` INT(11) DEFAULT '0' COMMENT '是否有置顶评论',
    `comments` TEXT COMMENT '置顶评论列表',
    `top_comments` INT(11) DEFAULT '0' COMMENT '是否爬取了热门评论',
    PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
ALTER TABLE `videos` ADD UNIQUE (`video_id`);

CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT(20) NOT NULL COMMENT '发布者ID',
    `user_name` VARCHAR(128) NOT NULL COMMENT '发布者名称',
    `user_avatar` VARCHAR(258) NOT NULL COMMENT '发布者头像',
    `create_time` BIGINT(20) NOT NULL DEFAULT '0' COMMENT '发布时间',
    `content` VARCHAR(1024) NOT NULL COMMENT '内容',
    `digg_count` INT(11) NOT NULL DEFAULT '0' COMMENT '被顶次数',
    `comments_count` INT(11) NOT NULL DEFAULT '0' COMMENT '被评论次数',
    `group_id` BIGINT(20) NOT NULL COMMENT '视频分组ID',
    `item_id` BIGINT(20) NOT NULL COMMENT '该记录在第三方平台的ID',
    PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


