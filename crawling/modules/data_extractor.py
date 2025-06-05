"""
데이터 추출/파싱 모듈 (Data Extractor)
기능 ID: F-EXT-001
"""

from typing import Dict, List, Any, Optional
from utils.logger import logger


class DataExtractor:
    """매물 데이터 추출 및 파싱 클래스"""
    
    # 추출할 핵심 데이터 필드 정의 (실제 API 응답 필드명 기준)
    CORE_FIELDS = [
        'articleNo',              # 매물 고유 ID
        'realEstateTypeCode',     # 부동산 유형 코드
        'realEstateTypeName',     # 부동산 유형명
        'tradeTypeCode',          # 거래 유형 코드  
        'tradeTypeName',          # 거래 유형명
        'dealOrWarrantPrc',       # 가격 정보
        'areaName',               # 면적 정보
        'area1',                  # 면적1
        'area2',                  # 면적2
        'floorInfo',              # 층 정보
        'buildingName',           # 동 정보
        'articleConfirmYmd',      # 확인일
        'direction',              # 방향
        'articleFeatureDesc',     # 매물 특징 설명
        'realtorName',            # 공인중개사명
        'cpName'                  # 중개업체명
    ]
    
    def extract_articles_data(self, api_response_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        JSON 응답에서 매물 정보 추출 및 정제
        
        Args:
            api_response_json: Naver 부동산 API의 원본 JSON 응답
            
        Returns:
            각 딕셔너리가 하나의 매물 정보를 담고 있는 리스트
        """
        try:
            logger.info("매물 데이터 추출 시작")
            
            # API 응답 구조 디버깅
            logger.info(f"API 응답 키들: {list(api_response_json.keys())}")
            
            # articleList 키 확인
            if 'articleList' not in api_response_json:
                logger.warning("응답에서 'articleList' 키를 찾을 수 없습니다")
                # 첫 번째 매물이 있으면 구조 확인
                if api_response_json and len(list(api_response_json.keys())) > 0:
                    first_key = list(api_response_json.keys())[0]
                    logger.info(f"첫 번째 키 '{first_key}'의 샘플 데이터: {api_response_json[first_key][:1] if isinstance(api_response_json[first_key], list) else api_response_json[first_key]}")
                return []
            
            article_list = api_response_json['articleList']
            
            if not isinstance(article_list, list):
                logger.warning("'articleList'가 리스트 형태가 아닙니다")
                return []
            
            extracted_articles = []
            
            # 각 매물 정보 처리
            for idx, article in enumerate(article_list):
                try:
                    # 첫 번째 매물의 구조 확인
                    if idx == 0:
                        logger.info(f"첫 번째 매물 키들: {list(article.keys()) if isinstance(article, dict) else 'Not a dict'}")
                        if isinstance(article, dict):
                            sample_fields = {k: v for k, v in list(article.items())[:5]}
                            logger.info(f"첫 번째 매물 샘플 데이터: {sample_fields}")
                    
                    extracted_article = self._extract_single_article(article, idx)
                    if extracted_article:
                        extracted_articles.append(extracted_article)
                        
                except Exception as e:
                    logger.warning(f"매물 {idx} 처리 중 오류 발생: {str(e)}")
                    continue
            
            logger.info(f"매물 데이터 추출 완료. 총 {len(extracted_articles)}개 매물 처리")
            return extracted_articles
            
        except Exception as e:
            logger.error(f"매물 데이터 추출 중 오류 발생: {str(e)}", exc_info=True)
            return []
    
    def _extract_single_article(self, article: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """
        단일 매물 정보 추출
        
        Args:
            article: 단일 매물 데이터
            index: 매물 인덱스 (로깅용)
            
        Returns:
            추출된 매물 정보 딕셔너리 또는 None
        """
        if not isinstance(article, dict):
            logger.warning(f"매물 {index}: 딕셔너리 형태가 아닙니다")
            return None
        
        extracted_data = {}
        
        # 핵심 필드 추출
        for field in self.CORE_FIELDS:
            extracted_data[field] = self._safe_extract_field(article, field)
        
        # 가격 정보 특별 처리
        extracted_data['formatted_price'] = self._format_price(
            article.get('dealOrWarrantPrc', ''),
            article.get('tradeTypeCode', '')
        )
        
        # 면적 정보 특별 처리
        extracted_data['area_detail'] = self._format_area(
            article.get('areaName', ''),
            article.get('area1', ''),
            article.get('area2', '')
        )
        
        # 층 정보 특별 처리
        extracted_data['floor_detail'] = self._format_floor(article.get('floorInfo', ''))
        
        # 확인일 포맷팅
        extracted_data['formatted_confirm_date'] = self._format_date(article.get('articleConfirmYmd', ''))
        
        logger.debug(f"매물 {index} 추출 완료: articleNo={extracted_data.get('articleNo', 'N/A')}")
        return extracted_data
    
    def _safe_extract_field(self, article: Dict[str, Any], field: str) -> Any:
        """
        안전한 필드 추출 (기본값 처리)
        
        Args:
            article: 매물 데이터
            field: 추출할 필드명
            
        Returns:
            필드 값 또는 기본값
        """
        value = article.get(field)
        
        # None 또는 빈 문자열인 경우 기본값 처리
        if value is None or value == '':
            return None
        
        # 문자열인 경우 앞뒤 공백 제거
        if isinstance(value, str):
            return value.strip()
        
        return value
    
    def _format_price(self, price: str, trade_type: str) -> str:
        """
        가격 정보 포맷팅
        
        Args:
            price: 원본 가격 정보
            trade_type: 거래 유형
            
        Returns:
            포맷팅된 가격 정보
        """
        if not price:
            return '가격 미정'
        
        try:
            # 거래 유형별 가격 표시 방식 구분
            if trade_type == 'A1':  # 매매
                return f"{price} (매매)"
            elif trade_type == 'B1':  # 전세
                return f"{price} (전세)"
            elif trade_type == 'B2':  # 월세
                return f"{price} (월세)"
            else:
                return str(price)
                
        except Exception:
            return str(price) if price else '가격 미정'
    
    def _format_area(self, area_name: str, area1: str, area2: str) -> str:
        """
        면적 정보 포맷팅
        
        Args:
            area_name: 면적명 (예: 84A)
            area1: 면적1 (공급면적)
            area2: 면적2 (전용면적)
            
        Returns:
            포맷팅된 면적 정보
        """
        areas = []
        
        if area_name:
            areas.append(f"타입: {area_name}")
        if area1:
            areas.append(f"공급: {area1}m²")
        if area2:
            areas.append(f"전용: {area2}m²")
        
        if areas:
            return " / ".join(areas)
        
        return '면적 정보 없음'
    
    def _format_floor(self, floor_info: str) -> str:
        """
        층 정보 포맷팅
        
        Args:
            floor_info: 원본 층 정보
            
        Returns:
            포맷팅된 층 정보
        """
        if not floor_info:
            return '층 정보 없음'
        
        try:
            # 층 정보 정리
            if '층' not in str(floor_info):
                return f"{floor_info}층"
            return str(floor_info)
        except Exception:
            return str(floor_info) if floor_info else '층 정보 없음'
    
    def _format_date(self, date_string: str) -> str:
        """
        날짜 정보 포맷팅
        
        Args:
            date_string: 원본 날짜 정보
            
        Returns:
            포맷팅된 날짜 정보
        """
        if not date_string:
            return '날짜 정보 없음'
        
        try:
            # 날짜 형식 정리 (YYYY.MM.DD 또는 YYYY-MM-DD 형태로 통일)
            date_str = str(date_string).replace('-', '.').replace('/', '.')
            return date_str
        except Exception:
            return str(date_string) if date_string else '날짜 정보 없음'
    
    def validate_extracted_data(self, articles_data: List[Dict[str, Any]]) -> bool:
        """
        추출된 데이터 유효성 검증
        
        Args:
            articles_data: 추출된 매물 데이터 리스트
            
        Returns:
            유효성 여부
        """
        if not isinstance(articles_data, list):
            logger.warning("추출된 데이터가 리스트 형태가 아닙니다")
            return False
        
        if len(articles_data) == 0:
            logger.warning("추출된 매물 데이터가 없습니다")
            return False
        
        # 샘플 데이터 검증
        sample_article = articles_data[0]
        required_fields = ['articleNo', 'realEstateType', 'tradeType']
        
        for field in required_fields:
            if field not in sample_article:
                logger.warning(f"필수 필드 '{field}'가 누락되었습니다")
                return False
        
        logger.info(f"추출된 데이터 유효성 검증 통과. 매물 수: {len(articles_data)}")
        return True 