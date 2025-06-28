import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Настройки страницы
st.set_page_config(page_title="🛒 Мой ИИ Байтера", layout="wide")
st.title("📊 Ваш персональный помощник для закупок")

# Генератор данных о товарах
def generate_product_data():
    brands = ['Nike', 'Adidas', 'Apple', 'Samsung', 'Zara', 'Levi\'s', 'Sony', 'Dyson']
    categories = ['Одежда', 'Обувь', 'Электроника', 'Аксессуары']
    countries = ['Китай', 'США', 'Германия', 'Италия']
    
    np.random.seed(42)
    data = []
    
    for i in range(1, 51):
        brand = np.random.choice(brands)
        category = np.random.choice(categories)
        country = np.random.choice(countries)
        
        # Определение цен
        if category == 'Электроника':
            base_price = np.random.randint(300, 2000)
        elif category == 'Обувь':
            base_price = np.random.randint(60, 300)
        else:
            base_price = np.random.randint(30, 150)
        
        # Премиум бренды
        if brand in ['Apple', 'Dyson']:
            base_price *= 1.5
        
        # Параметры страны
        logistics = np.random.uniform(3, 15)
        delivery_time = np.random.randint(10, 40)
        
        # Дополнительные параметры
        min_order = np.random.choice([10, 25, 50, 100])
        rating = round(np.random.uniform(3.0, 5.0), 1)
        
        data.append({
            'ID': i,
            'Бренд': brand,
            'Категория': category,
            'Страна': country,
            'Товар': f"{brand} {category[:3]}-{i}",
            'Цена ($)': round(base_price, 2),
            'Мин. заказ (шт)': min_order,
            'Логистика ($/шт)': round(logistics, 2),
            'Срок доставки (дн)': delivery_time,
            'Таможня (%)': np.random.choice([5, 7, 10]),
            'Рейтинг поставщика': rating,
            'Ссылка': f"https://example.com/{brand.lower()}/{i}"
        })
    
    return pd.DataFrame(data)

# Расчет итоговой стоимости
def calculate_total(row):
    base_price = row['Цена ($)']
    logistics = row['Логистика ($/шт)']
    customs = base_price * (row['Таможня (%)'] / 100)
    return round(base_price + logistics + customs, 2)

# Основное приложение
def main():
    st.sidebar.header("🔍 Фильтры")
    df = generate_product_data()
    df['Итоговая цена ($/шт)'] = df.apply(calculate_total, axis=1)
    
    selected_brands = st.sidebar.multiselect(
        "Бренды:", 
        options=df['Бренд'].unique(),
        default=['Nike', 'Adidas']
    )
    
    # Фильтрация
    filtered_df = df[df['Бренд'].isin(selected_brands)]
    
    # Показать товары
    st.header("📋 Список товаров")
    for _, row in filtered_df.iterrows():
        st.subheader(f"{row['Товар']} ({row['Бренд']})")
        st.write(f"**Страна:** {row['Страна']}")
        st.write(f"**Итоговая цена:** ${row['Итоговая цена ($/шт)']} "
                 f"(Товар: ${row['Цена ($)']} + "
                 f"Логистика: ${row['Логистика ($/шт)']} + "
                 f"Пошлина: {row['Таможня (%)']}%)")
        st.write(f"**Мин. заказ:** {row['Мин. заказ (шт)']} шт | "
                 f"**Доставка:** {row['Срок доставки (дн)']} дней | "
                 f"**Рейтинг:** {row['Рейтинг поставщика']}/5.0")
        st.markdown(f"[Перейти к товару]({row['Ссылка']})")
        st.divider()
    
    # График цен
    st.header("📊 Сравнение цен")
    fig = px.bar(
        filtered_df,
        x='Товар',
        y='Итоговая цена ($/шт)',
        color='Бренд',
        title='Цены товаров'
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
