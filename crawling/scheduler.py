"""
스케줄링 모듈 (Scheduler)
APScheduler를 사용한 정기적 크롤링 스케줄링
"""

import sys
import os
import signal
from datetime import datetime, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from main_crawler import MainCrawler
from config import COMPLEX_NO
from utils.logger import logger


class CrawlingScheduler:
    """크롤링 스케줄러 클래스"""
    
    def __init__(self):
        # 스케줄러 설정
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=1)  # 동시 실행 방지
        }
        job_defaults = {
            'coalesce': True,          # 중복 실행 방지
            'max_instances': 1,        # 최대 인스턴스 수
            'misfire_grace_time': 300  # 5분 지연 허용
        }
        
        self.scheduler = BlockingScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults
        )
        
        self.crawler = MainCrawler()
        self.is_running = False
        
        # 종료 시그널 핸들러 등록
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """종료 시그널 핸들러"""
        logger.info(f"종료 시그널 수신: {signum}")
        self.stop_scheduler()
    
    def add_daily_job(
        self,
        hour: int = 9,
        minute: int = 0,
        complex_no: int = COMPLEX_NO,
        job_id: str = None
    ):
        """
        일일 크롤링 작업 추가
        
        Args:
            hour: 실행 시간 (24시간 형식)
            minute: 실행 분
            complex_no: 아파트 단지 번호
            job_id: 작업 ID
        """
        try:
            if job_id is None:
                job_id = f"daily_crawling_{complex_no}"
            
            self.scheduler.add_job(
                func=self._run_scheduled_crawling,
                trigger=CronTrigger(hour=hour, minute=minute),
                args=[complex_no],
                id=job_id,
                name=f"일일 크롤링 - Complex {complex_no}",
                replace_existing=True
            )
            
            logger.info(f"일일 크롤링 작업 추가: 매일 {hour:02d}:{minute:02d}")
            
        except Exception as e:
            logger.error(f"일일 작업 추가 중 오류: {str(e)}")
    
    def add_weekly_job(
        self,
        day_of_week: int = 0,  # 0=월요일, 6=일요일
        hour: int = 9,
        minute: int = 0,
        complex_no: int = COMPLEX_NO,
        job_id: str = None
    ):
        """
        주간 크롤링 작업 추가
        
        Args:
            day_of_week: 요일 (0=월요일, 6=일요일)
            hour: 실행 시간
            minute: 실행 분
            complex_no: 아파트 단지 번호
            job_id: 작업 ID
        """
        try:
            if job_id is None:
                job_id = f"weekly_crawling_{complex_no}"
            
            weekdays = ['월', '화', '수', '목', '금', '토', '일']
            
            self.scheduler.add_job(
                func=self._run_scheduled_crawling,
                trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
                args=[complex_no],
                id=job_id,
                name=f"주간 크롤링 - Complex {complex_no}",
                replace_existing=True
            )
            
            logger.info(f"주간 크롤링 작업 추가: 매주 {weekdays[day_of_week]}요일 {hour:02d}:{minute:02d}")
            
        except Exception as e:
            logger.error(f"주간 작업 추가 중 오류: {str(e)}")
    
    def add_interval_job(
        self,
        hours: int = 0,
        minutes: int = 30,
        complex_no: int = COMPLEX_NO,
        job_id: str = None
    ):
        """
        주기적 크롤링 작업 추가
        
        Args:
            hours: 시간 간격
            minutes: 분 간격
            complex_no: 아파트 단지 번호
            job_id: 작업 ID
        """
        try:
            if job_id is None:
                job_id = f"interval_crawling_{complex_no}"
            
            self.scheduler.add_job(
                func=self._run_scheduled_crawling,
                trigger=IntervalTrigger(hours=hours, minutes=minutes),
                args=[complex_no],
                id=job_id,
                name=f"주기적 크롤링 - Complex {complex_no}",
                replace_existing=True
            )
            
            logger.info(f"주기적 크롤링 작업 추가: {hours}시간 {minutes}분 간격")
            
        except Exception as e:
            logger.error(f"주기적 작업 추가 중 오류: {str(e)}")
    
    def _run_scheduled_crawling(self, complex_no: int):
        """
        스케줄된 크롤링 실행
        
        Args:
            complex_no: 아파트 단지 번호
        """
        try:
            start_time = datetime.now()
            logger.info("=" * 50)
            logger.info("스케줄된 크롤링 작업 시작")
            logger.info(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"대상 단지: {complex_no}")
            logger.info("=" * 50)
            
            # 크롤링 실행
            success = self.crawler.run_crawling(
                complex_no=complex_no,
                max_pages=100,
                use_dynamic_auth=False
            )
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            if success:
                logger.info(f"스케줄된 크롤링 성공 완료 (소요시간: {duration})")
            else:
                logger.error(f"스케줄된 크롤링 실패 (소요시간: {duration})")
            
        except Exception as e:
            logger.error(f"스케줄된 크롤링 실행 중 오류: {str(e)}", exc_info=True)
    
    def start_scheduler(self):
        """스케줄러 시작"""
        try:
            if self.scheduler.running:
                logger.warning("스케줄러가 이미 실행 중입니다")
                return
            
            logger.info("크롤링 스케줄러 시작")
            self._print_scheduled_jobs()
            
            self.is_running = True
            self.scheduler.start()
            
        except Exception as e:
            logger.error(f"스케줄러 시작 중 오류: {str(e)}", exc_info=True)
            self.is_running = False
    
    def stop_scheduler(self):
        """스케줄러 종료"""
        try:
            if not self.scheduler.running:
                logger.info("스케줄러가 실행 중이 아닙니다")
                return
            
            logger.info("크롤링 스케줄러 종료 중...")
            self.scheduler.shutdown(wait=True)
            self.is_running = False
            logger.info("크롤링 스케줄러 종료 완료")
            
        except Exception as e:
            logger.error(f"스케줄러 종료 중 오류: {str(e)}")
    
    def _print_scheduled_jobs(self):
        """등록된 작업 목록 출력"""
        try:
            jobs = self.scheduler.get_jobs()
            if jobs:
                logger.info("등록된 스케줄 작업:")
                for job in jobs:
                    logger.info(f"  - {job.name} (ID: {job.id})")
                    logger.info(f"    다음 실행: {job.next_run_time}")
            else:
                logger.warning("등록된 스케줄 작업이 없습니다")
                
        except Exception as e:
            logger.error(f"작업 목록 출력 중 오류: {str(e)}")
    
    def remove_job(self, job_id: str):
        """작업 제거"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"작업 제거 완료: {job_id}")
        except Exception as e:
            logger.error(f"작업 제거 중 오류: {str(e)}")
    
    def list_jobs(self):
        """현재 등록된 작업 목록 반환"""
        return self.scheduler.get_jobs()


def main():
    """메인 실행 함수"""
    try:
        import argparse
        
        parser = argparse.ArgumentParser(description='네이버 부동산 크롤링 스케줄러')
        parser.add_argument('--mode', choices=['daily', 'weekly', 'interval', 'test'], 
                          default='daily', help='스케줄링 모드')
        parser.add_argument('--complex', type=int, default=COMPLEX_NO, 
                          help=f'아파트 단지 번호 (기본값: {COMPLEX_NO})')
        parser.add_argument('--hour', type=int, default=9, 
                          help='실행 시간 (0-23, 기본값: 9)')
        parser.add_argument('--minute', type=int, default=0, 
                          help='실행 분 (0-59, 기본값: 0)')
        parser.add_argument('--day-of-week', type=int, default=0, 
                          help='요일 (0=월요일, 6=일요일, 기본값: 0)')
        parser.add_argument('--interval-hours', type=int, default=0, 
                          help='주기 실행 시간 간격 (기본값: 0)')
        parser.add_argument('--interval-minutes', type=int, default=30, 
                          help='주기 실행 분 간격 (기본값: 30)')
        
        args = parser.parse_args()
        
        # 스케줄러 생성 및 설정
        scheduler = CrawlingScheduler()
        
        if args.mode == 'daily':
            scheduler.add_daily_job(
                hour=args.hour,
                minute=args.minute,
                complex_no=args.complex
            )
        elif args.mode == 'weekly':
            scheduler.add_weekly_job(
                day_of_week=args.day_of_week,
                hour=args.hour,
                minute=args.minute,
                complex_no=args.complex
            )
        elif args.mode == 'interval':
            scheduler.add_interval_job(
                hours=args.interval_hours,
                minutes=args.interval_minutes,
                complex_no=args.complex
            )
        elif args.mode == 'test':
            # 테스트 모드: 1분 후 실행
            from datetime import datetime, timedelta
            test_time = datetime.now() + timedelta(minutes=1)
            
            scheduler.scheduler.add_job(
                func=scheduler._run_scheduled_crawling,
                trigger='date',
                run_date=test_time,
                args=[args.complex],
                id='test_crawling',
                name='테스트 크롤링'
            )
            logger.info(f"테스트 크롤링 작업 등록: {test_time.strftime('%Y-%m-%d %H:%M:%S')} 실행 예정")
        
        # 스케줄러 시작
        scheduler.start_scheduler()
        
    except KeyboardInterrupt:
        logger.info("사용자에 의해 스케줄러가 중단되었습니다")
    except Exception as e:
        logger.error(f"스케줄러 실행 중 오류 발생: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main() 