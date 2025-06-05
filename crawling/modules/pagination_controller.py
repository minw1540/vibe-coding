"""
페이지네이션 제어 모듈 (Pagination Controller)
기능 ID: F-PAG-001
"""

import time
from typing import Dict, List, Any
from config import (
    NAVER_REAL_ESTATE_API_URL, 
    DEFAULT_PARAMS, 
    REQUEST_DELAY, 
    COMPLEX_NO
)
from modules.request_handler import RequestHandler
from modules.data_extractor import DataExtractor
from utils.logger import logger


class PaginationController:
    """페이지네이션 제어 클래스"""
    
    def __init__(self):
        self.request_handler = RequestHandler()
        self.data_extractor = DataExtractor()
    
    def collect_all_pages(
        self,
        complex_no: int = COMPLEX_NO,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        max_pages: int = 100  # 안전장치
    ) -> List[Dict[str, Any]]:
        """
        모든 페이지의 매물 데이터 순차적 수집
        
        Args:
            complex_no: 크롤링할 아파트 단지 번호
            headers: HTTP 헤더
            cookies: HTTP 쿠키
            max_pages: 최대 페이지 수 (무한 루프 방지)
            
        Returns:
            모든 페이지에서 수집된 매물 정보의 통합 리스트
        """
        try:
            logger.info(f"페이지네이션 크롤링 시작 - Complex No: {complex_no}")
            
            all_articles_data = []
            current_page = 1
            empty_page_count = 0  # 연속된 빈 페이지 카운트
            max_empty_pages = 3   # 최대 허용 연속 빈 페이지 수
            
            while current_page <= max_pages:
                logger.info(f"페이지 {current_page} 크롤링 시작")
                
                # 페이지별 매물 데이터 수집
                page_articles = self._collect_single_page(
                    complex_no, current_page, headers, cookies
                )
                
                # 빈 페이지 처리
                if not page_articles:
                    empty_page_count += 1
                    logger.warning(f"페이지 {current_page}: 매물 데이터 없음 (연속 빈 페이지: {empty_page_count})")
                    
                    if empty_page_count >= max_empty_pages:
                        logger.info(f"연속 {max_empty_pages}개 빈 페이지 발견. 크롤링 종료")
                        break
                else:
                    # 성공적으로 데이터를 가져온 경우
                    empty_page_count = 0  # 빈 페이지 카운트 리셋
                    all_articles_data.extend(page_articles)
                    logger.info(f"페이지 {current_page}: {len(page_articles)}개 매물 수집 완료")
                
                # 다음 페이지로 이동
                current_page += 1
                
                # 요청 간 지연
                if current_page <= max_pages:
                    logger.debug(f"{REQUEST_DELAY}초 대기 중...")
                    time.sleep(REQUEST_DELAY)
            
            logger.info(f"페이지네이션 크롤링 완료. 총 {len(all_articles_data)}개 매물 수집")
            logger.info(f"처리된 페이지 수: {current_page - 1}")
            
            return all_articles_data
            
        except Exception as e:
            logger.error(f"페이지네이션 크롤링 중 오류 발생: {str(e)}", exc_info=True)
            return []
        
        finally:
            # 리소스 정리
            self.request_handler.close_session()
    
    def _collect_single_page(
        self,
        complex_no: int,
        page: int,
        headers: Dict[str, str],
        cookies: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        단일 페이지 매물 데이터 수집
        
        Args:
            complex_no: 아파트 단지 번호
            page: 페이지 번호
            headers: HTTP 헤더
            cookies: HTTP 쿠키
            
        Returns:
            해당 페이지의 매물 정보 리스트
        """
        try:
            # 페이지별 파라미터 설정
            params = DEFAULT_PARAMS.copy()
            params['page'] = page
            params['complexNo'] = complex_no
            
            # API 요청
            response_data = self.request_handler.make_request(
                url=NAVER_REAL_ESTATE_API_URL,
                params=params,
                headers=headers,
                cookies=cookies
            )
            
            if not response_data:
                logger.warning(f"페이지 {page}: API 응답 없음")
                return []
            
            # 응답 데이터 유효성 검증
            if not self.request_handler.validate_response(response_data):
                logger.warning(f"페이지 {page}: 응답 데이터 유효성 검증 실패")
                return []
            
            # 매물 데이터 추출
            articles_data = self.data_extractor.extract_articles_data(response_data)
            
            if articles_data:
                logger.debug(f"페이지 {page}: {len(articles_data)}개 매물 추출 완료")
            else:
                logger.debug(f"페이지 {page}: 추출된 매물 없음")
            
            return articles_data
            
        except Exception as e:
            logger.error(f"페이지 {page} 수집 중 오류 발생: {str(e)}")
            return []
    
    def collect_pages_range(
        self,
        start_page: int,
        end_page: int,
        complex_no: int = COMPLEX_NO,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None
    ) -> List[Dict[str, Any]]:
        """
        지정된 범위의 페이지 매물 데이터 수집
        
        Args:
            start_page: 시작 페이지
            end_page: 종료 페이지
            complex_no: 아파트 단지 번호
            headers: HTTP 헤더
            cookies: HTTP 쿠키
            
        Returns:
            지정 범위 페이지의 매물 정보 리스트
        """
        try:
            logger.info(f"범위 페이지 크롤링 시작 - 페이지 {start_page}~{end_page}")
            
            all_articles_data = []
            
            for page in range(start_page, end_page + 1):
                logger.info(f"페이지 {page} 크롤링")
                
                page_articles = self._collect_single_page(
                    complex_no, page, headers, cookies
                )
                
                if page_articles:
                    all_articles_data.extend(page_articles)
                    logger.info(f"페이지 {page}: {len(page_articles)}개 매물 수집")
                else:
                    logger.warning(f"페이지 {page}: 매물 데이터 없음")
                
                # 마지막 페이지가 아닌 경우 지연
                if page < end_page:
                    time.sleep(REQUEST_DELAY)
            
            logger.info(f"범위 페이지 크롤링 완료. 총 {len(all_articles_data)}개 매물 수집")
            return all_articles_data
            
        except Exception as e:
            logger.error(f"범위 페이지 크롤링 중 오류 발생: {str(e)}", exc_info=True)
            return []
    
    def get_total_pages_estimate(
        self,
        complex_no: int = COMPLEX_NO,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None
    ) -> int:
        """
        전체 페이지 수 추정 (첫 번째 페이지 응답 기반)
        
        Args:
            complex_no: 아파트 단지 번호
            headers: HTTP 헤더
            cookies: HTTP 쿠키
            
        Returns:
            추정 전체 페이지 수
        """
        try:
            params = DEFAULT_PARAMS.copy()
            params['page'] = 1
            params['complexNo'] = complex_no
            
            response_data = self.request_handler.make_request(
                url=NAVER_REAL_ESTATE_API_URL,
                params=params,
                headers=headers,
                cookies=cookies
            )
            
            if response_data and 'totalCount' in response_data:
                total_count = response_data['totalCount']
                page_size = len(response_data.get('articleList', []))
                
                if page_size > 0:
                    estimated_pages = (total_count + page_size - 1) // page_size
                    logger.info(f"전체 매물 수: {total_count}, 예상 페이지 수: {estimated_pages}")
                    return estimated_pages
            
            logger.warning("전체 페이지 수 추정 실패")
            return 0
            
        except Exception as e:
            logger.error(f"전체 페이지 수 추정 중 오류 발생: {str(e)}")
            return 0
    
    def validate_pagination_params(self, complex_no: int) -> bool:
        """
        페이지네이션 파라미터 유효성 검증
        
        Args:
            complex_no: 아파트 단지 번호
            
        Returns:
            유효성 여부
        """
        if not isinstance(complex_no, int) or complex_no <= 0:
            logger.error(f"유효하지 않은 단지 번호: {complex_no}")
            return False
        
        logger.info("페이지네이션 파라미터 유효성 검증 통과")
        return True 