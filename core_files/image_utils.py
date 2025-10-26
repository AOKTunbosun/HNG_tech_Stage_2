from PIL import Image, ImageDraw, ImageFont
from sqlmodel import Session, select, func
from datetime import datetime
import io
import os
from .models import Country


def generate_simple_countries_image(db: Session):
    total_countries = db.exec(select(func.count(Country.id))).one()

    top_countries_statement = (select(Country.name, Country.estimated_gdp).order_by(Country.estimated_gdp.desc()).limit(5))

    top_countries = db.exec(top_countries_statement).all()

    country = db.exec(select(Country)).first()
    last_refresh = country.last_refreshed_at
    current_time = datetime.now()

    lines = [
        'COUNTRIES STATISTICS',
        '=' * 35, 
        f'Total Countries: {total_countries}',
        ""
        f'Last Refreshed: {last_refresh.strftime("%Y-%m-%d %H:%M:%S") if last_refresh else "Never"}',
        f'Generated: {current_time.strftime("%Y-%m-%d %H:%M:%S")}'
        "",
        "TOP 5 COUNTRIES BY GDP:"
    ]

    for i, (name, gdp) in enumerate(top_countries, 1):
        gdp_trillions = gdp / 1e12
        lines.append(f'{i}. {name}: ${gdp_trillions:.2f}T')

    if not top_countries:
        lines.append('No country data available')

    line_height = 30
    padding = 40
    width = 700
    height = padding * 2 + len(lines) * line_height

    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype('arial.ttf', 20)
    except:
        font = ImageFont.load_default()
    
    for i, line in enumerate(lines):
        y = padding + i * line_height
        if "=" in line:
            draw.text((width//2, y), line, fill='black', font=font, anchor='mm')
        elif line.upper() == line and not line.isdigit():
            draw.text((width//2, y), line, fill='darkblue', font=font, anchor='mm')
        else:
            draw.text((padding, y), line, fill='black', font=font)
        
    draw.rectangle([5, 5, width-5, height-5], outline='black', width=2)

    return image


def save_image_to_file(image: Image.Image, filepath: str = 'cache/summary.png'):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        image.save(filepath, format('PNG'))
        print(f'Image successfully saved to: {filepath}')
        return True
    
    except Exception as e:
        print(f'Error saving image to {filepath}: {e}')
        return False

def generate_countries_image(db: Session):
    image = generate_simple_countries_image(db)

    save_image_to_file(image, 'cache/summary.png')

    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)

    return buf.getvalue()