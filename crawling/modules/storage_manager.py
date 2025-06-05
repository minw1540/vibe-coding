"""
데이터 저장 모듈 (Storage Manager)
기능 ID: F-SAVE-001
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Any
from config import OUTPUT_DIR, COMPLEX_NO
from utils.logger import logger


class StorageManager:
    """데이터 저장 관리 클래스"""
    
    def __init__(self):
        # 출력 디렉토리 생성
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def save_to_csv(
        self,
        articles_data: List[Dict[str, Any]],
        complex_no: int = COMPLEX_NO,
        custom_filename: str = None
    ) -> bool:
        """
        수집된 매물 정보를 CSV 파일로 저장
        
        Args:
            articles_data: 저장할 매물 정보 딕셔너리 리스트
            complex_no: 아파트 단지 번호
            custom_filename: 사용자 정의 파일명 (선택사항)
            
        Returns:
            저장 성공 여부
        """
        try:
            if not articles_data:
                logger.warning("저장할 매물 데이터가 없습니다")
                return False
            
            logger.info(f"CSV 파일 저장 시작. 매물 수: {len(articles_data)}")
            
            # DataFrame 생성
            df = pd.DataFrame(articles_data)
            
            # 파일명 생성
            if custom_filename:
                filename = custom_filename
                if not filename.endswith('.csv'):
                    filename += '.csv'
            else:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_complex_{complex_no}_articles.csv"
            
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # CSV 파일로 저장
            df.to_csv(
                filepath,
                index=False,
                encoding='utf-8-sig',  # 한글 깨짐 방지
                na_rep='N/A'  # NaN 값을 'N/A'로 표시
            )
            
            # 파일 정보 로깅
            file_size = os.path.getsize(filepath)
            logger.info(f"CSV 파일 저장 완료: {filepath}")
            logger.info(f"파일 크기: {file_size:,} bytes, 레코드 수: {len(df)}")
            
            # 데이터 요약 정보 로깅
            self._log_data_summary(df)
            
            return True
            
        except Exception as e:
            logger.error(f"CSV 파일 저장 중 오류 발생: {str(e)}", exc_info=True)
            return False
    
    def _log_data_summary(self, df: pd.DataFrame):
        """
        데이터 요약 정보 로깅
        
        Args:
            df: 저장된 DataFrame
        """
        try:
            logger.info("=== 저장된 데이터 요약 ===")
            logger.info(f"총 매물 수: {len(df)}")
            
            # 부동산 유형별 통계
            if 'realEstateType' in df.columns:
                estate_type_counts = df['realEstateType'].value_counts()
                logger.info("부동산 유형별 매물 수:")
                for estate_type, count in estate_type_counts.items():
                    logger.info(f"  - {estate_type}: {count}개")
            
            # 거래 유형별 통계
            if 'tradeType' in df.columns:
                trade_type_counts = df['tradeType'].value_counts()
                logger.info("거래 유형별 매물 수:")
                for trade_type, count in trade_type_counts.items():
                    trade_type_name = self._get_trade_type_name(trade_type)
                    logger.info(f"  - {trade_type_name}: {count}개")
            
            # 가격대별 분포 (가격 정보가 있는 경우)
            if 'price' in df.columns:
                price_stats = df['price'].describe()
                logger.info("가격 통계:")
                logger.info(f"  - 평균: {price_stats.get('mean', 'N/A')}")
                logger.info(f"  - 최소: {price_stats.get('min', 'N/A')}")
                logger.info(f"  - 최대: {price_stats.get('max', 'N/A')}")
            
            logger.info("========================")
            
        except Exception as e:
            logger.warning(f"데이터 요약 정보 생성 중 오류: {str(e)}")
    
    def _get_trade_type_name(self, trade_type: str) -> str:
        """
        거래 유형 코드를 한글명으로 변환
        
        Args:
            trade_type: 거래 유형 코드
            
        Returns:
            한글 거래 유형명
        """
        trade_type_map = {
            'A1': '매매',
            'B1': '전세',
            'B2': '월세'
        }
        return trade_type_map.get(trade_type, trade_type)
    
    def save_metadata(
        self,
        metadata: Dict[str, Any],
        complex_no: int = COMPLEX_NO
    ) -> bool:
        """
        크롤링 메타데이터 저장
        
        Args:
            metadata: 저장할 메타데이터
            complex_no: 아파트 단지 번호
            
        Returns:
            저장 성공 여부
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_complex_{complex_no}_metadata.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"메타데이터 저장 완료: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"메타데이터 저장 중 오류 발생: {str(e)}", exc_info=True)
            return False
    
    def get_output_files(self) -> List[str]:
        """
        출력 디렉토리의 파일 목록 반환
        
        Returns:
            파일 경로 리스트
        """
        try:
            if not os.path.exists(OUTPUT_DIR):
                return []
            
            files = []
            for filename in os.listdir(OUTPUT_DIR):
                filepath = os.path.join(OUTPUT_DIR, filename)
                if os.path.isfile(filepath):
                    files.append(filepath)
            
            return sorted(files, key=os.path.getmtime, reverse=True)  # 최신 파일 순
            
        except Exception as e:
            logger.error(f"파일 목록 조회 중 오류 발생: {str(e)}")
            return []
    
    def cleanup_old_files(self, keep_count: int = 10):
        """
        오래된 파일 정리 (최신 N개 파일만 유지)
        
        Args:
            keep_count: 유지할 파일 개수
        """
        try:
            files = self.get_output_files()
            
            if len(files) <= keep_count:
                logger.info(f"파일 개수({len(files)})가 유지 개수({keep_count}) 이하입니다")
                return
            
            # 오래된 파일 삭제
            files_to_delete = files[keep_count:]
            deleted_count = 0
            
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.debug(f"파일 삭제: {os.path.basename(filepath)}")
                except Exception as e:
                    logger.warning(f"파일 삭제 실패 {filepath}: {str(e)}")
            
            logger.info(f"오래된 파일 {deleted_count}개 정리 완료")
            
        except Exception as e:
            logger.error(f"파일 정리 중 오류 발생: {str(e)}")
    
    def validate_data_before_save(self, articles_data: List[Dict[str, Any]]) -> bool:
        """
        저장 전 데이터 유효성 검증
        
        Args:
            articles_data: 검증할 매물 데이터
            
        Returns:
            유효성 여부
        """
        if not isinstance(articles_data, list):
            logger.error("매물 데이터가 리스트 형태가 아닙니다")
            return False
        
        if len(articles_data) == 0:
            logger.warning("저장할 매물 데이터가 없습니다")
            return False
        
        # 필수 필드 검증
        required_fields = ['articleNo', 'realEstateType']
        sample_article = articles_data[0]
        
        for field in required_fields:
            if field not in sample_article:
                logger.error(f"필수 필드 '{field}'가 누락되었습니다")
                return False
        
        logger.info("저장 전 데이터 유효성 검증 통과")
        return True 