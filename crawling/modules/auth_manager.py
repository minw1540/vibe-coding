"""
인증/헤더 관리 모듈 (Auth/Header Manager)
기능 ID: F-AUTH-001
"""

from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from config import DEFAULT_HEADERS
from utils.logger import logger


class AuthManager:
    """인증 토큰 및 쿠키 관리 클래스"""
    
    def __init__(self):
        self.headers = DEFAULT_HEADERS.copy()
        self.cookies = {}
        self.driver = None
    
    def get_auth_info(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        최신 인증 토큰 및 쿠키 확보
        
        Returns:
            tuple: (headers, cookies)
        """
        logger.info("인증 정보 확보 시작")
        
        # 초기 구현 시: 하드코딩된 헤더 사용
        # 향후 확장 시: Selenium을 통한 동적 획득
        try:
            # 기본 헤더 반환 (이미 Authorization 포함됨)
            auth_token = self.headers.get('Authorization', 'None')
            logger.info(f"사용할 인증 토큰: {auth_token[:50]}...")
            return self.headers, self.cookies
        except Exception as e:
            logger.error(f"인증 정보 확보 중 오류 발생: {str(e)}", exc_info=True)
            return self.headers, self.cookies
    
    def setup_selenium_driver(self) -> Optional[webdriver.Chrome]:
        """
        Selenium WebDriver 설정 (향후 확장용)
        
        Returns:
            webdriver.Chrome: Chrome WebDriver 인스턴스
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            # 헤드리스 모드 설정 (선택사항)
            # chrome_options.add_argument('--headless')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            logger.info("Selenium WebDriver 설정 완료")
            return driver
            
        except Exception as e:
            logger.error(f"WebDriver 설정 중 오류 발생: {str(e)}", exc_info=True)
            return None
    
    def get_dynamic_auth_info(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        Selenium을 통한 동적 인증 정보 획득 (향후 확장용)
        
        Returns:
            tuple: (headers, cookies)
        """
        try:
            self.driver = self.setup_selenium_driver()
            if not self.driver:
                return self.headers, self.cookies
            
            # 네이버 부동산 페이지 접속
            self.driver.get("https://new.land.naver.com/complexes/27643")
            time.sleep(3)
            
            # 페이지 로딩 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 쿠키 및 로컬 스토리지에서 인증 정보 추출
            cookies = self.driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            # Authorization 토큰 추출 (로컬 스토리지 또는 쿠키에서)
            try:
                auth_token = self.driver.execute_script(
                    "return localStorage.getItem('authorization') || "
                    "sessionStorage.getItem('authorization')"
                )
                if auth_token:
                    self.headers['Authorization'] = f'Bearer {auth_token}'
            except Exception as e:
                logger.warning(f"Authorization 토큰 추출 실패: {str(e)}")
            
            self.cookies = cookie_dict
            logger.info("동적 인증 정보 획득 완료")
            
            return self.headers, self.cookies
            
        except Exception as e:
            logger.error(f"동적 인증 정보 획득 중 오류 발생: {str(e)}", exc_info=True)
            return self.headers, self.cookies
        
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def validate_auth_info(self, headers: Dict[str, str], cookies: Dict[str, str]) -> bool:
        """
        인증 정보 유효성 검증
        
        Args:
            headers: HTTP 헤더
            cookies: HTTP 쿠키
            
        Returns:
            bool: 유효성 여부
        """
        # 기본적인 헤더 유효성 검증
        required_headers = ['User-Agent', 'Accept', 'Referer']
        for header in required_headers:
            if header not in headers:
                logger.warning(f"필수 헤더 누락: {header}")
                return False
        
        logger.info("인증 정보 유효성 검증 통과")
        return True
    
    def update_headers(self, new_headers: Dict[str, str]):
        """헤더 업데이트"""
        self.headers.update(new_headers)
        logger.info("헤더 정보 업데이트 완료")
    
    def update_cookies(self, new_cookies: Dict[str, str]):
        """쿠키 업데이트"""
        self.cookies.update(new_cookies)
        logger.info("쿠키 정보 업데이트 완료") 