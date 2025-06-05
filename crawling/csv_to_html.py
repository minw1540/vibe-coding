#!/usr/bin/env python3
"""
CSV 파일을 보기 좋은 HTML 테이블로 변환하는 스크립트
"""

import pandas as pd
import os
from datetime import datetime
import sys

def create_html_table(csv_file_path: str, output_file: str = None) -> str:
    """
    CSV 파일을 HTML 테이블로 변환
    
    Args:
        csv_file_path: CSV 파일 경로
        output_file: 출력할 HTML 파일명 (None이면 자동 생성)
    
    Returns:
        생성된 HTML 파일 경로
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {csv_file_path}")
    
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)
    
    # 출력 파일명 결정
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        output_file = f"{base_name}.html"
    
    # HTML 템플릿
    html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>네이버 부동산 크롤링 결과 - {title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .stats {{
            background: #f8f9fa;
            padding: 20px;
            display: flex;
            justify-content: space-around;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .stat-item {{
            flex: 1;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-label {{
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .table-container {{
            padding: 20px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0;
            font-size: 0.9rem;
        }}
        
        th {{
            background: linear-gradient(45deg, #34495e, #2c3e50);
            color: white;
            padding: 15px 8px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        td {{
            padding: 12px 8px;
            border-bottom: 1px solid #e9ecef;
            vertical-align: top;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e3f2fd;
            transform: scale(1.002);
            transition: all 0.2s ease;
        }}
        
        .price {{
            font-weight: bold;
            color: #e74c3c;
        }}
        
        .area {{
            color: #27ae60;
            font-size: 0.85rem;
        }}
        
        .type {{
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8rem;
            display: inline-block;
        }}
        
        .floor {{
            background: #9b59b6;
            color: white;
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 0.8rem;
        }}
        
        .description {{
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .realtor {{
            color: #8e44ad;
            font-weight: 500;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .stats {{
                flex-direction: column;
                gap: 15px;
            }}
            
            table {{
                font-size: 0.8rem;
            }}
            
            th, td {{
                padding: 8px 4px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 네이버 부동산 크롤링 결과</h1>
            <div class="subtitle">백현마을2단지 (Complex No. 27643) - {date}</div>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <span class="stat-number">{total_count}</span>
                <div class="stat-label">총 매물 수</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{apt_count}</span>
                <div class="stat-label">아파트</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{sale_count}</span>
                <div class="stat-label">매매</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{avg_price}</span>
                <div class="stat-label">평균 가격</div>
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
        
        <div class="footer">
            Generated on {generation_time} | 네이버 부동산 크롤링 시스템 v1.0
        </div>
    </div>
</body>
</html>
"""
    
    # 데이터 통계 계산
    total_count = len(df)
    apt_count = len(df[df['realEstateTypeName'] == '아파트']) if 'realEstateTypeName' in df.columns else 0
    sale_count = len(df[df['tradeTypeName'] == '매매']) if 'tradeTypeName' in df.columns else 0
    
    # 평균 가격 계산 (숫자만 추출)
    avg_price = "정보없음"
    if 'dealOrWarrantPrc' in df.columns:
        prices = []
        for price in df['dealOrWarrantPrc'].dropna():
            if isinstance(price, str):
                # 숫자만 추출 (억, 천만 등 단위 제거)
                import re
                numbers = re.findall(r'[\d,]+', str(price))
                if numbers:
                    try:
                        # 억 단위로 변환
                        price_str = numbers[0].replace(',', '')
                        if '억' in str(price):
                            prices.append(float(price_str))
                    except:
                        continue
        
        if prices:
            avg = sum(prices) / len(prices)
            avg_price = f"{avg:.1f}억"
    
    # HTML 테이블 생성 (pandas to_html 사용하되 스타일링 적용)
    table_html = df.to_html(
        table_id="data-table",
        classes="table",
        escape=False,
        index=False,
        na_rep="N/A"
    )
    
    # 특정 컬럼에 CSS 클래스 적용
    table_html = table_html.replace('class="table"', 'class="data-table"')
    
    # 컬럼별 스타일링 적용
    if 'formatted_price' in df.columns:
        for price in df['formatted_price'].dropna():
            if '억' in str(price):
                table_html = table_html.replace(
                    f'<td>{price}</td>', 
                    f'<td class="price">{price}</td>'
                )
    
    if 'area_detail' in df.columns:
        for area in df['area_detail'].dropna():
            if 'm²' in str(area):
                table_html = table_html.replace(
                    f'<td>{area}</td>', 
                    f'<td class="area">{area}</td>'
                )
    
    if 'realEstateTypeName' in df.columns:
        for estate_type in df['realEstateTypeName'].dropna():
            table_html = table_html.replace(
                f'<td>{estate_type}</td>', 
                f'<td><span class="type">{estate_type}</span></td>'
            )
    
    if 'floor_detail' in df.columns:
        for floor in df['floor_detail'].dropna():
            if '층' in str(floor):
                table_html = table_html.replace(
                    f'<td>{floor}</td>', 
                    f'<td><span class="floor">{floor}</span></td>'
                )
    
    if 'realtorName' in df.columns:
        for realtor in df['realtorName'].dropna():
            table_html = table_html.replace(
                f'<td>{realtor}</td>', 
                f'<td class="realtor">{realtor}</td>'
            )
    
    # HTML 완성
    html_content = html_template.format(
        title=os.path.basename(csv_file_path),
        date=datetime.now().strftime("%Y년 %m월 %d일"),
        total_count=total_count,
        apt_count=apt_count,
        sale_count=sale_count,
        avg_price=avg_price,
        table_html=table_html,
        generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # HTML 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML 파일이 생성되었습니다: {output_file}")
    print(f"📊 총 {total_count}개의 매물 데이터를 변환했습니다.")
    
    return output_file

def main():
    # 가장 최신 CSV 파일 찾기
    data_dir = "./data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ data 폴더에 CSV 파일이 없습니다.")
        return
    
    # 파일명에서 타임스탬프 기준으로 정렬
    csv_files.sort(reverse=True)
    latest_csv = os.path.join(data_dir, csv_files[0])
    
    print(f"🔄 변환할 파일: {latest_csv}")
    
    try:
        html_file = create_html_table(latest_csv)
        print(f"🌐 브라우저에서 확인하세요: file://{os.path.abspath(html_file)}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 