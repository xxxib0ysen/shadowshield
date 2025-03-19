from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

from app.services.rule.SourceService import SourceService

#  自动同步广告规则源
def update_adblock_sources_task():
    with current_app.app_context():
        print("正在自动同步广告规则源......")
        SourceService.update_sources()

    # 启动定时任务
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_adblock_sources_task, 'interval', hours=12)
    scheduler.start()

    with current_app.app_context():
        update_adblock_sources_task()
