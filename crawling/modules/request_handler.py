"""
API 요청 및 응답 모듈 (Request Handler)
기능 ID: F-REQ-001
"""

import requests
import time
from typing import Dict, Optional, Any
from config import TIMEOUT, MAX_RETRIES, REQUEST_DELAY
from utils.logger import logger


class RequestHandler:
    """HTTP 요청 처리 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        
    def make_request(
        self,
        url: str,
        params: Dict[str, Any],
        headers: Dict[str, str],
        cookies: Dict[str, str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Naver 부동산 API에 HTTP GET 요청 전송
        
        Args:
            url: 요청할 API 엔드포인트 URL
            params: 쿼리 파라미터
            headers: HTTP 요청 헤더
            cookies: HTTP 요청 쿠키
            
        Returns:
            API 응답 JSON 데이터 (성공 시) 또는 None (실패 시)
        """
        retry_count = 0
        
        while retry_count < MAX_RETRIES:
            try:
                logger.info(f"API 요청 시도 {retry_count + 1}/{MAX_RETRIES}: {url}")
                logger.debug(f"요청 파라미터: {params}")
                
                # HTTP GET 요청 전송
                response = self.session.get(
                    url=url,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=TIMEOUT
                )
                
                # HTTP 상태 코드 확인
                if response.status_code == 200:
                    try:
                        # JSON 응답 파싱
                        json_data = response.json()
                        logger.info(f"API 요청 성공: HTTP {response.status_code}")
                        return json_data
                        
                    except ValueError as e:
                        logger.error(f"JSON 파싱 오류: {str(e)}")
                        logger.debug(f"응답 내용: {response.text[:500]}")
                        return None
                        
                elif response.status_code == 429:
                    # Too Many Requests - 재시도 전 더 긴 지연
                    wait_time = REQUEST_DELAY * (retry_count + 1) * 2
                    logger.warning(f"요청 제한 발생 (HTTP 429). {wait_time}초 대기 후 재시도")
                    time.sleep(wait_time)
                    
                elif response.status_code in [401, 403]:
                    # 인증 오류 - 즉시 실패
                    logger.error(f"인증 오류: HTTP {response.status_code}")
                    logger.debug(f"응답 내용: {response.text[:500]}")
                    return None
                    
                else:
                    # 기타 HTTP 오류
                    logger.warning(f"HTTP 오류: {response.status_code}")
                    logger.debug(f"응답 내용: {response.text[:500]}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"요청 타임아웃 (시도 {retry_count + 1}/{MAX_RETRIES})")
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"연결 오류 (시도 {retry_count + 1}/{MAX_RETRIES})")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"요청 예외 발생: {str(e)}")
                
            except Exception as e:
                logger.error(f"예상치 못한 오류 발생: {str(e)}", exc_info=True)
                
            # 재시도 전 지연
            if retry_count < MAX_RETRIES - 1:
                wait_time = REQUEST_DELAY * (retry_count + 1)
                logger.info(f"{wait_time}초 대기 후 재시도")
                time.sleep(wait_time)
                
            retry_count += 1
        
        logger.error(f"최대 재시도 횟수 초과. 요청 실패: {url}")
        return None
    
    def validate_response(self, response_data: Dict[str, Any]) -> bool:
        """
        API 응답 데이터 유효성 검증
        
        Args:
            response_data: API 응답 JSON 데이터
            
        Returns:
            유효성 여부
        """
        if not isinstance(response_data, dict):
            logger.warning("응답 데이터가 딕셔너리 형태가 아닙니다")
            return False
            
        # 기본적인 응답 구조 검증
        if 'articleList' not in response_data:
            logger.warning("응답 데이터에 'articleList' 키가 없습니다")
            return False
            
        if not isinstance(response_data['articleList'], list):
            logger.warning("'articleList'가 리스트 형태가 아닙니다")
            return False
            
        logger.debug(f"응답 데이터 유효성 검증 통과. 매물 수: {len(response_data['articleList'])}")
        return True
    
    def close_session(self):
        """세션 종료"""
        if self.session:
            self.session.close()
            logger.info("HTTP 세션 종료") 