"""
메인 크롤러 제어 모듈 (Main Crawler Orchestrator)
기능 ID: F-MAIN-001

네이버 부동산 매물 정보 크롤링 시스템
"""

import sys
import os
from datetime import datetime
from typing import Optional

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from config import COMPLEX_NO
from modules.auth_manager import AuthManager
from modules.pagination_controller import PaginationController
from modules.storage_manager import StorageManager
from utils.logger import logger


class MainCrawler:
    """메인 크롤러 제어 클래스"""
    
    def __init__(self):
        self.auth_manager = AuthManager()
        self.pagination_controller = PaginationController()
        self.storage_manager = StorageManager()
        self.start_time = None
        self.end_time = None
    
    def run_crawling(
        self,
        complex_no: int = COMPLEX_NO,
        max_pages: int = 100,
        use_dynamic_auth: bool = False
    ) -> bool:
        """
        크롤링 프로세스 실행
        
        Args:
            complex_no: 아파트 단지 번호
            max_pages: 최대 페이지 수
            use_dynamic_auth: 동적 인증 사용 여부
            
        Returns:
            크롤링 성공 여부
        """
        try:
            self.start_time = datetime.now()
            logger.info("=" * 60)
            logger.info("네이버 부동산 매물 정보 크롤링 시작")
            logger.info(f"시작 시간: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"대상 단지: Complex No. {complex_no}")
            logger.info("=" * 60)
            
            # 1. 인증 정보 확보
            logger.info("1단계: 인증 정보 확보")
            headers, cookies = self._get_authentication_info(use_dynamic_auth)
            
            if not self.auth_manager.validate_auth_info(headers, cookies):
                logger.error("인증 정보 유효성 검증 실패")
                return False
            
            # 2. 페이지네이션을 통한 데이터 수집
            logger.info("2단계: 매물 데이터 수집")
            all_articles_data = self.pagination_controller.collect_all_pages(
                complex_no=complex_no,
                headers=headers,
                cookies=cookies,
                max_pages=max_pages
            )
            
            if not all_articles_data:
                logger.warning("수집된 매물 데이터가 없습니다")
                return False
            
            # 3. 데이터 저장
            logger.info("3단계: 데이터 저장")
            if not self.storage_manager.validate_data_before_save(all_articles_data):
                logger.error("저장 전 데이터 유효성 검증 실패")
                return False
            
            save_success = self.storage_manager.save_to_csv(
                articles_data=all_articles_data,
                complex_no=complex_no
            )
            
            if not save_success:
                logger.error("데이터 저장 실패")
                return False
            
            # 4. 메타데이터 저장
            logger.info("4단계: 메타데이터 저장")
            self._save_crawling_metadata(complex_no, len(all_articles_data))
            
            # 5. 크롤링 완료
            self.end_time = datetime.now()
            duration = self.end_time - self.start_time
            
            logger.info("=" * 60)
            logger.info("크롤링 프로세스 완료")
            logger.info(f"종료 시간: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"소요 시간: {duration}")
            logger.info(f"수집된 매물 수: {len(all_articles_data):,}개")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"크롤링 프로세스 중 오류 발생: {str(e)}", exc_info=True)
            return False
        
        finally:
            # 리소스 정리
            self._cleanup_resources()
    
    def _get_authentication_info(self, use_dynamic_auth: bool = False) -> tuple:
        """
        인증 정보 획득
        
        Args:
            use_dynamic_auth: 동적 인증 사용 여부
            
        Returns:
            (headers, cookies) 튜플
        """
        try:
            if use_dynamic_auth:
                logger.info("동적 인증 정보 획득 시도")
                return self.auth_manager.get_dynamic_auth_info()
            else:
                logger.info("기본 인증 정보 사용")
                return self.auth_manager.get_auth_info()
                
        except Exception as e:
            logger.error(f"인증 정보 획득 중 오류: {str(e)}")
            # 기본 인증 정보 반환
            return self.auth_manager.get_auth_info()
    
    def _save_crawling_metadata(self, complex_no: int, total_articles: int):
        """
        크롤링 메타데이터 저장
        
        Args:
            complex_no: 아파트 단지 번호
            total_articles: 총 수집된 매물 수
        """
        try:
            metadata = {
                'crawling_info': {
                    'complex_no': complex_no,
                    'start_time': self.start_time.isoformat() if self.start_time else None,
                    'end_time': self.end_time.isoformat() if self.end_time else None,
                    'duration_seconds': (
                        (self.end_time - self.start_time).total_seconds() 
                        if self.start_time and self.end_time else None
                    ),
                    'total_articles_collected': total_articles,
                    'crawler_version': '1.0.0',
                    'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                },
                'system_info': {
                    'platform': sys.platform,
                    'cwd': os.getcwd()
                }
            }
            
            self.storage_manager.save_metadata(metadata, complex_no)
            
        except Exception as e:
            logger.warning(f"메타데이터 저장 중 오류: {str(e)}")
    
    def _cleanup_resources(self):
        """리소스 정리"""
        try:
            logger.info("리소스 정리 중...")
            
            # HTTP 세션 정리
            if hasattr(self.pagination_controller, 'request_handler'):
                self.pagination_controller.request_handler.close_session()
            
            # 오래된 파일 정리 (최신 10개 파일만 유지)
            self.storage_manager.cleanup_old_files(keep_count=10)
            
            logger.info("리소스 정리 완료")
            
        except Exception as e:
            logger.warning(f"리소스 정리 중 오류: {str(e)}")
    
    def run_test_crawling(self, complex_no: int = COMPLEX_NO, pages: int = 2, use_dynamic_auth: bool = False) -> bool:
        """
        테스트용 제한적 크롤링 실행
        
        Args:
            complex_no: 아파트 단지 번호
            pages: 크롤링할 페이지 수
            use_dynamic_auth: 동적 인증 사용 여부
            
        Returns:
            테스트 크롤링 성공 여부
        """
        try:
            logger.info(f"테스트 크롤링 시작 - {pages}페이지 제한")
            
            # 인증 정보 확보
            headers, cookies = self._get_authentication_info(use_dynamic_auth)
            
            # 제한된 페이지 크롤링
            test_articles = self.pagination_controller.collect_pages_range(
                start_page=1,
                end_page=pages,
                complex_no=complex_no,
                headers=headers,
                cookies=cookies
            )
            
            if test_articles:
                logger.info(f"테스트 크롤링 성공 - {len(test_articles)}개 매물 수집")
                
                # 테스트 데이터 저장
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                test_filename = f"test_{timestamp}_complex_{complex_no}_articles.csv"
                
                return self.storage_manager.save_to_csv(
                    articles_data=test_articles,
                    complex_no=complex_no,
                    custom_filename=test_filename
                )
            else:
                logger.warning("테스트 크롤링에서 데이터를 수집하지 못했습니다")
                return False
                
        except Exception as e:
            logger.error(f"테스트 크롤링 중 오류 발생: {str(e)}", exc_info=True)
            return False


def main():
    """메인 실행 함수"""
    try:
        # 명령행 인수 처리
        import argparse
        
        parser = argparse.ArgumentParser(description='네이버 부동산 매물 정보 크롤러')
        parser.add_argument('--complex', type=int, default=COMPLEX_NO, 
                          help=f'아파트 단지 번호 (기본값: {COMPLEX_NO})')
        parser.add_argument('--max-pages', type=int, default=100, 
                          help='최대 크롤링 페이지 수 (기본값: 100)')
        parser.add_argument('--test', action='store_true', 
                          help='테스트 모드 (2페이지만 크롤링)')
        parser.add_argument('--dynamic-auth', action='store_true', 
                          help='동적 인증 사용 (Selenium)')
        
        args = parser.parse_args()
        
        # 크롤러 실행
        crawler = MainCrawler()
        
        if args.test:
            success = crawler.run_test_crawling(complex_no=args.complex, pages=2, use_dynamic_auth=args.dynamic_auth)
        else:
            success = crawler.run_crawling(
                complex_no=args.complex,
                max_pages=args.max_pages,
                use_dynamic_auth=args.dynamic_auth
            )
        
        if success:
            logger.info("크롤링이 성공적으로 완료되었습니다")
            sys.exit(0)
        else:
            logger.error("크롤링이 실패했습니다")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("사용자에 의해 크롤링이 중단되었습니다")
        sys.exit(0)
    except Exception as e:
        logger.error(f"메인 실행 중 오류 발생: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 