"""
로깅 모듈 (Logging Module)
기능 ID: F-LOG-001
"""

import logging
import os
from datetime import datetime
from config import LOG_DIR


class CrawlerLogger:
    """크롤링 시스템 로거 클래스"""
    
    def __init__(self, name: str = 'naver_real_estate_crawler'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 중복 핸들러 방지
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self):
        """로거 설정"""
        # 로그 디렉토리 생성
        os.makedirs(LOG_DIR, exist_ok=True)
        
        # 파일 핸들러 설정
        log_filename = f"crawler_log_{datetime.now().strftime('%Y%m%d')}.log"
        log_filepath = os.path.join(LOG_DIR, log_filename)
        
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 콘솔 핸들러 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 포매터 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """정보 레벨 로그 기록"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """경고 레벨 로그 기록"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """오류 레벨 로그 기록"""
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        """디버그 레벨 로그 기록"""
        self.logger.debug(message)


# 전역 로거 인스턴스
logger = CrawlerLogger() 