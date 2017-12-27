#!/usr/bin/env python
# encoding: utf-8
# 共用表定义
import time
from random import randint
from sqlalchemy import *
from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, Numeric, DateTime, Boolean, and_, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TINYINT, DATETIME, TEXT, CHAR
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from time import time
import logging
import json
import traceback

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }


class Video(BaseModel):
    __tablename__ = "videos"
    id = Column("id", Integer, primary_key=True)

    group_id = Column(VARCHAR(64), nullable=False)
    item_id = Column(VARCHAR(64), nullable=False)
    video_id = Column(VARCHAR(64), nullable=False)
    content = Column(VARCHAR(1024), nullable=True)
    category_id = Column(Integer, nullable=False)
    category_name = Column(VARCHAR(128), nullable=False)
    sub_category_name = Column(VARCHAR(128), nullable=False)
    url = Column(VARCHAR(512), nullable=False)
    vurl = Column(VARCHAR(256))
    cover_image = Column(VARCHAR(512), nullable=False)
    online_time = Column(Integer)

    user_id = Column(VARCHAR(64), nullable=False)
    user_name = Column(VARCHAR(128), nullable=False)
    user_avatar = Column(VARCHAR(256), nullable=False)

    play_count = Column(Integer, default=0)
    bury_count = Column(Integer, default=0)
    repin_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    digg_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    has_comments = Column(Integer, default=0)
    comments = Column(TEXT, nullable=True)
    top_comments = Column(Integer)
    is_expired = Column(Integer)
    check_expire_time = Column(BIGINT)
    source = Column(VARCHAR(16))
    comment_crawled = Column(Integer)

    def conv_result(self):
        ret = {}
        ret["id"] = self.id
        ret["group_id"] = self.group_id
        ret["item_id"] = self.item_id
        ret["video_id"] = self.video_id
        ret["content"] = self.content
        ret["category_id"] = self.category_id
        ret["category_name"] = self.category_name
        ret["sub_category_name"] = self.sub_category_name
        ret["url"] = self.url
        ret["vurl"] = self.vurl
        ret["cover_image"] = self.cover_image
        ret["user_id"] = self.user_id
        ret["user_name"] = self.user_name
        ret["user_avatar"] = self.user_avatar
        ret["play_count"] = int(self.play_count)
        ret["bury_count"] = int(self.bury_count)
        ret["repin_count"] = int(self.repin_count)
        ret["share_count"] = int(self.share_count)
        ret["digg_count"] = int(self.digg_count)
        ret["comment_count"] = int(self.comment_count)
        ret["has_comments"] = int(self.has_comments)
        ret["comments"] = json.loads(self.comments)
        ret["top_comments"] = int(self.top_comments)
        # ret["is_expired"] = int(self.is_expired)
        # ret["check_expire_time"] = int(self.check_expire_time)
        ret['online_time'] = int(self.online_time)
        ret['source'] = self.source
        ret['comment_crawled'] = self.comment_crawled
        return ret


class VideoWeb(BaseModel):
    __tablename__ = "videos_web"
    id = Column("id", Integer, primary_key=True)

    group_id = Column(Integer)
    item_id = Column(Integer)
    video_id = Column(VARCHAR(64), nullable=False)
    content = Column(VARCHAR(1024), nullable=True)
    category_id = Column(Integer, nullable=False)
    category_name = Column(VARCHAR(128), nullable=False)
    url = Column(VARCHAR(512), nullable=False)
    vurl = Column(VARCHAR(256))
    cover_image = Column(VARCHAR(512), nullable=False)
    online_time = Column(Integer)

    user_id = Column(VARCHAR(64), nullable=False)
    user_name = Column(VARCHAR(128), nullable=False)
    user_avatar = Column(VARCHAR(256), nullable=False)

    play_count = Column(Integer, default=0)
    bury_count = Column(Integer, default=0)
    repin_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    digg_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    has_comments = Column(Integer, default=0)
    comments = Column(TEXT, nullable=True)
    top_comments = Column(Integer)
    is_expired = Column(Integer)
    check_expire_time = Column(BIGINT)

    def conv_result(self):
        ret = {}
        ret["id"] = self.id
        ret["group_id"] = self.group_id
        ret["item_id"] = self.item_id
        ret["video_id"] = self.video_id
        ret["content"] = self.content
        ret["category_id"] = self.category_id
        ret["category_name"] = self.category_name
        ret["url"] = self.url
        ret["vurl"] = self.vurl
        ret["cover_image"] = self.cover_image
        ret["user_id"] = self.user_id
        ret["user_name"] = self.user_name
        ret["user_avatar"] = self.user_avatar
        ret["play_count"] = int(self.play_count)
        ret["bury_count"] = int(self.bury_count)
        ret["repin_count"] = int(self.repin_count)
        ret["share_count"] = int(self.share_count)
        ret["digg_count"] = int(self.digg_count)
        ret["comment_count"] = int(self.comment_count)
        ret["has_comments"] = int(self.has_comments)
        ret["comments"] = json.loads(self.comments)
        ret["top_comments"] = int(self.top_comments)
        # ret["is_expired"] = int(self.is_expired)
        # ret["check_expire_time"] = int(self.check_expire_time)
        ret['online_time'] = int(self.online_time)
        return ret


class Comment(BaseModel):
    __tablename__ = "comments_v3"
    id = Column("id", Integer, primary_key=True)
    group_id = Column(VARCHAR(64), nullable=False)
    item_id = Column(VARCHAR(64), nullable=False)
    user_id = Column(VARCHAR(64), nullable=False)
    user_name = Column(VARCHAR(128), nullable=False)
    user_avatar = Column(VARCHAR(256), nullable=False)
    create_time = Column(Integer)
    digg_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    content = Column(VARCHAR(1024), nullable=False)

    def conv_result(self):
        ret = {}
        ret["id"] = self.id
        ret["group_id"] = self.group_id
        ret["item_id"] = self.item_id

        ret["user_id"] = self.user_id
        ret["user_name"] = self.user_name
        ret["user_avatar"] = self.user_avatar
        ret["create_time"] = int(self.create_time)
        ret["digg_count"] = int(self.digg_count)
        ret["comment_count"] = int(self.comment_count)
        ret["content"] = content
        return ret


class Mgr(object):
    def __init__(self, engine):
        BaseModel.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()
        self.engine = engine

    def add_video(self, data):
        try:
            if not data:
                return None
            if 'source' not in data:
                data['source'] = 'neihan'
            if not self.video_exists(data['video_id']):
                self.session.add(Video(**data))
            else:
                self.session.query(Video) \
                    .filter(Video.video_id == data['video_id']) \
                    .update({
                        'url': data['url'],
                        'play_count': data['play_count'],
                        'bury_count': data['bury_count'],
                        'repin_count': data['repin_count'],
                        'share_count': data['share_count'],
                        'digg_count': data['digg_count'],
                        'comment_count': data['comment_count']
                    }, synchronize_session='fetch')
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.warning("add video error : %s" % e, exc_info=True)
        finally:
            self.session.close()

    def video_exists(self, video_id):
        try:
            exists = self.session.query(Video) \
                .filter(Video.video_id == video_id) \
                .count()
            if exists:
                return True
        except Exception as e:
            logging.warning("check video exists error : %s" % e, exc_info=True)
        finally:
            self.session.close()
        return False

    def add_video_web(self, data):
        try:
            if not data:
                return None
            if not self.video_web_exists(data['video_id']):
                self.session.add(VideoWeb(**data))
            else:
                self.session.query(VideoWeb) \
                    .filter(VideoWeb.video_id == data['video_id']) \
                    .update({
                        'url': data['url'],
                        'play_count': data['play_count'],
                        'bury_count': data['bury_count'],
                        'repin_count': data['repin_count'],
                        'share_count': data['share_count'],
                        'digg_count': data['digg_count'],
                        'comment_count': data['comment_count']
                    }, synchronize_session='fetch')
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.warning("add video web error : %s" % e, exc_info=True)
        finally:
            self.session.close()

    def video_web_exists(self, video_id):
        return False
        try:
            exists = self.session.query(VideoWeb) \
                .filter(VideoWeb.video_id == video_id) \
                .count()
            if exists:
                return True
        except Exception as e:
            logging.warning("check video exists error : %s" % e, exc_info=True)
        finally:
            self.session.close()
        return False

    def video_top_comments_updated(self, gids):
        try:
            if not gids:
                return None
            self.session.query(Video) \
                .filter(Video.group_id.in_(gids)) \
                .update(
                    {'top_comments': 1, 'comment_crawled': 1},
                    synchronize_session='fetch'
                )
            self.session.commit()
        except Exception, e:
            traceback.print_exc()
            self.session.rollback()
            logging.warning('video top_comments updated error: %s' % e, exc_info=True)
        finally:
            self.session.close()

    def video_expire_updated(self, gids):
        try:
            if not gids:
                return None
            self.session.query(Video) \
                .filter(Video.group_id.in_(gids)) \
                .update({'is_expired': 1, 'check_expire_time': time()}, synchronize_session='fetch')
            self.session.commit()
        except Exception, e:
            traceback.print_exc()
            self.session.rollback()
            logging.warning('video expire update error: %s' % e, exc_info=True)
        finally:
            self.session.close()

    def get_videos(self, params):
        try:
            ret = []
            q = self.session.query(Video)
            if params.get('top_comments', '') != '':
                q = q.filter(Video.top_comments == int(params['top_comments']))
            if params.get('comment_crawled', '') != '':
                q = q.filter(Video.comment_crawled == int(params['comment_crawled']))
            if params.get('category_id', '') != '':
                q = q.filter(Video.category_id == int(params['category_id']))
            if params.get('category_ids', ''):
                q = q.filter(Video.category_id.in_(params['category_ids']))
            if params.get('category_name', '') != '':
                q = q.filter(Video.category_name.contains(category_name))
            if params.get('is_expired', '') != '':
                q = q.filter(Video.is_expired == int(params['is_expired']))
            if params.get('online_time', '') != '':
                q = q.filter(Video.online_time >= int(params['online_time']))
            if params.get('source', '') != '':
                q = q.filter(Video.source == params['source'])
            if params.get('order', '') == 'asc':
                q = q.order_by(Video.comment_count.asc())
            else:
                q = q.order_by(Video.comment_count.desc())
            if params.get('limit', '') == '':
                limit = 100
            else:
                limit = int(params.get('limit'))
            if int(params.get('page', 0)) == 0:
                offset = 0
            else:
                offset = (int(params.get('page'))-1)*limit
            rows = q.limit(limit).offset(offset)

            for row in rows:
                ret.append(row.conv_result())
        except Exception as e:
            logging.warning("check video exists error : %s" % e, exc_info=True)
        finally:
            self.session.close()
        return ret

    def add_comment(self, data):
        try:
            self.session.add(Comment(**data))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.warning("add comment error : %s" % e, exc_info=True)
        finally:
            self.session.close()
