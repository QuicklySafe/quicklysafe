import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime

# Настройки страницы
st.set_page_config(page_title="🛒 Аналитик товаров", layout="wide")
st.title("🧠 ИИ Аналитик товаров без API")

# Генератор "умных" данных
def generate_smart_data():
    brands = ['Nike', 'Adidas', 'Apple', 'Samsung', 'Zara', 'Levi\'s', 'Sony', 'Dyson']
    categories = ['Одежда', 'Обувь', 'Электроника', 'Аксессуары']
    
    np.random.seed(42)
    data = []
    
    for i in range(1, 101):
        brand = np.random.choice(brands)
        category = np.random.choice(categories)
        
        # Базовые параметры
        base_price = np.random.randint(30, 500)
        min_order = np.random.choice([5, 10, 20, 50])
        delivery_time = np.random.randint(10, 40)
        quality_score = np.random.uniform(3.0, 5.0)
        popularity = np.random.randint(1, 100)
        
        # ИИ-анализ характеристик
        features = {
            'Материал': np.random.choice(['Хлопок', 'Полиэстер', 'Кожа', 'Резина', 'Металл', 'Стекло']),
            'Цвет': np.random.choice(['Черный', 'Белый', 'Синий', 'Красный', 'Зеленый']),
            'Размер': np.random.choice(['S', 'M', 'L', 'XL', 'Универсальный']),
            'Вес (г)': np.random.randint(50, 2000),
            'Гарантия': np.random.choice([0, 6, 12, 24]),
            'Энергоэффективность': np.random.choice(['A++', 'A+', 'A', 'B', 'C'])
        }
        
        # ИИ-оценка товара
        value_score = min_order * (quality_score / base_price) * 100
        
        data.append({
            'ID': i,
            'Бренд': brand,
            'Категория': category,
            'Название товара': f"{brand} {category}-{i}",
            'Описание': f"{features['Цвет']} {features['Материал']} {category.lower()} от {brand}",
            'Цена ($/шт)': base_price,
            'Мин. заказ (шт)': min_order,
            'Срок доставки (дн)': delivery_time,
            'Качество (1-5)': round(quality_score, 1),
            'Популярность (1-100)': popularity,
            'Оценка ценности': round(value_score, 1),
            **features
        })
    
    return pd.DataFrame(data)

# Основное приложение
def main():
    st.sidebar.header("⚙️ Параметры анализа")
    
    # Загрузка данных
    df = generate_smart_data()
    
    # Фильтры
    col1, col2 = st.sidebar.columns(2)
    with col1:
        selected_brands = st.multiselect(
            "Бренды:", 
            options=df['Бренд'].unique(),
            default=['Nike', 'Adidas']
        )
    with col2:
        selected_categories = st.multiselect(
            "Категории:", 
            options=df['Категория'].unique(),
            default=['Одежда', 'Обувь']
        )
    
    min_quality = st.sidebar.slider("Мин. качество", 3.0, 5.0, 4.0)
    max_delivery = st.sidebar.slider("Макс. срок доставки", 10, 40, 30)
    
    # Применение фильтров
    filtered_df = df[
        (df['Бренд'].isin(selected_brands)) &
        (df['Категория'].isin(selected_categories)) &
        (df['Качество (1-5)'] >= min_quality) &
        (df['Срок доставки (дн)'] <= max_delivery)
    ]
    
    # Аналитическая панель
    st.header("📊 Результаты анализа")
    
    if filtered_df.empty:
        st.warning("Товары не найдены. Измените фильтры.")
        return
    
    # Ключевые метрики
    st.subheader("Ключевые показатели")
    col1, col2, col3 = st.columns(3)
    avg_price = filtered_df['Цена ($/шт)'].mean()
    best_value = filtered_df['Оценка ценности'].max()
    popular_brand = filtered_df.groupby('Бренд')['Популярность (1-100)'].mean().idxmax()
    
    col1.metric("Средняя цена", f"${avg_price:.2f}")
    col2.metric("Лучшая ценность", f"{best_value:.1f} баллов")
    col3.metric("Самый популярный бренд", popular_brand)
    
    # Топ-5 товаров по ценности
    st.subheader("🚀 Топ-5 самых выгодных товаров")
    top_products = filtered_df.sort_values('Оценка ценности', ascending=False).head(5)
    st.dataframe(top_products[['Название товара', 'Бренд', 'Цена ($/шт)', 'Оценка ценности', 'Качество (1-5)']])
    
    # Визуализация
    st.subheader("📈 Визуальный анализ")
    
    tab1, tab2 = st.tabs(["Распределение цен", "Зависимость качества и цены"])
    
    with tab1:
        fig = px.histogram(filtered_df, x='Цена ($/шт)', nbins=20, 
                          title='Распределение цен по отобранным товарам')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.scatter(filtered_df, x='Цена ($/шт)', y='Качество (1-5)', 
                        color='Бренд', size='Популярность (1-100)',
                        hover_data=['Название товара'],
                        title='Соотношение цена/качество')
        st.plotly_chart(fig, use_container_width=True)
    
    # ИИ-рекомендации
    st.subheader("🧠 Рекомендации ИИ")
    
    # Анализ по категориям
    st.write("### Оптимальный выбор по категориям:")
    for category in selected_categories:
        cat_df = filtered_df[filtered_df['Категория'] == category]
        if not cat_df.empty:
            best_product = cat_df.loc[cat_df['Оценка ценности'].idxmax()]
            st.write(f"- **{category}**: {best_product['Название товара']} "
                     f"(Цена: ${best_product['Цена ($/шт)']}, "
                     f"Оценка: {best_product['Оценка ценности']:.1f})")
    
    # Общие рекомендации
    st.write("### Стратегические рекомендации:")
    st.write("1. **Фокус на бренде**: " + popular_brand + " имеет наибольшую популярность")
    
    price_quality_ratio = filtered_df['Качество (1-5)'] / filtered_df['Цена ($/шт)']
    best_ratio_brand = filtered_df.iloc[price_quality_ratio.idxmax()]['Бренд']
    st.write(f"2. **Лучшее соотношение цена/качество**: {best_ratio_brand}")
    
    # Предупреждения
    expensive_low_quality = filtered_df[
        (filtered_df['Цена ($/шт)'] > avg_price) & 
        (filtered_df['Качество (1-5)'] < 4.0)
    ]
    if not expensive_low_quality.empty:
        st.warning("3. **Внимание!** Обнаружены товары с высокой ценой и низким качеством:")
        st.dataframe(expensive_low_quality[['Название товара', 'Бренд', 'Цена ($/шт)', 'Качество (1-5)']])
    
    # Кнопка для экспорта
    st.download_button(
        label="📥 Экспорт результатов",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='товары_анализ.csv',
        mime='text/csv'
    )

if __name__ == "__main__":
    main()
