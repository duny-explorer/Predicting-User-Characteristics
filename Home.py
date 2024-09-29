import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import folium
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
from PIL import Image

def main():

    st.sidebar.title("Навигация")


    pages = {
        "📊 EDA": eda_page,
        "🖼️ Аналитика по названиям видео": graphics_page,
        "📈 Метрики после обучения модели": metrics_page,
        "🗺️ Карты": maps_page,
        "👥 Поиск мульти-пользователей": multi_user_page
    }


    selection = st.sidebar.selectbox("Выберите страницу", list(pages.keys()))


    page = pages[selection]
    page()






def eda_page():
    
    st.title("EDA")
    st.write("На этой странице описаны найденные закономерности в данных")
    
    watchtime_age = pd.read_csv('csv_data/watchtime_age.csv')

    mean_age = pd.read_csv('csv_data/mean_age.csv')

    median_percent_df = pd.read_csv('csv_data/median_percent_watched_category.csv')

    time_of_day_counts = pd.read_csv('csv_data/ime_of_day_counts.csv')

    merged_df = pd.read_csv('csv_data/merged_df.csv')




    # Streamlit app to display DataFrames and WordCloud
    def display_data():
        age_class_counts = merged_df['age_class'].value_counts().reset_index()
        age_class_counts.columns = ['age_class', 'count']


        plt.figure(figsize=(10, 6))
        st.subheader('Количество по классам возраста')
        sns.barplot(x='age_class', y='count', data=age_class_counts, palette='pastel')
        plt.title("Количество пользователей по классам возраста")
        plt.xlabel("Класс возраста")
        plt.ylabel("Количество")
        
        st.pyplot(plt)


        sex_counts = merged_df['sex'].value_counts()

        # Create the pie chart
        plt.figure(figsize=(10, 6))
        st.subheader('Количество пользователей по полу')
        plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        plt.title("Распределение пользователей по полу")
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the plot in Streamlit
        st.pyplot(plt)

        # Additional information
        st.write('Количество target классов несбалансировано, будем использовать downsampling классов на train.')

        

        st.subheader('Среднее время просмотра в зависимости от возраста')
        plt.figure(figsize=(10, 6))
        sns.barplot(x='age', y='average_watchtime', data=watchtime_age, palette='pastel')
        plt.title("Среднее время просмотра в зависимости от возраста")
        plt.xlabel("Возраст")
        plt.ylabel("Среднее время просмотра")
        st.pyplot(plt)
        st.write('Cреднее время просмотра наименьшее у пользователей 11-15 лет, у пользователей возраст, которых превышает 15 лет среднее время просмотра видео на уровне 2000 секунд.')
      
        #кол-во использований ранее 



        # по классам 1-5 тип использования rutube

        # женщины тип использования rutube 

        
        # по классам 1-5 операционка 

        # мужчина операционка 
        




        plt.figure(figsize=(10, 6))
        st.subheader('Средний процент просмотренности видео в зависимости от категории')
        sns.barplot(x='category', y='median_percent_watched', data=median_percent_df, palette='pastel')

        plt.xticks(rotation=45, ha='right')

        plt.xlabel('Категория')
        plt.ylabel('Процент просмотренности видео в средне')
        plt.title('Средний процент просмотра видео в зависимости от категории')
        st.pyplot(plt)



        plt.figure(figsize=(10, 6))
        st.subheader('Количество видео в зависимости от времени суток')
        sns.barplot(x='time_of_day', y='count', data=time_of_day_counts, palette='pastel')
        plt.title("Количество видео в зависимости от времени суток")
        plt.title("Количество видео в зависимости от времени суток")
        plt.xlabel("Время суток")
        plt.ylabel("Количество видео")
        st.pyplot(plt)


        


        


    if __name__ == '__main__':
        display_data()















def metrics_page():
    st.title("Metrics")
    st.write("This page shows different metrics and key performance indicators.")


        











def graphics_page():
    st.title("Аналитика по названию видео")
    st.write("Visualize your data with different types of graphs and charts.")
    # Display Word Cloud
    st.subheader("Облако слов")
    image = Image.open('cloud_of_words.png')
    st.image(image, caption='Sample Image', use_column_width=True)













def maps_page():

    st.title("Карты")

# Read the CSVimport leafmap.foliumap as leafmap

    try:
        result_df = pd.read_csv('csv_data/category_result.csv', encoding='utf-8')
    except UnicodeDecodeError:
        st.error("Error loading the file. Try using a different encoding like 'latin1'.")
        result_df = pd.read_csv('csv_data/category_result.csv', encoding='latin1')


    # Replace the category names in the DataFrame with the English version
    category_mapping = {
        'Юмор': 'Humor',
        'Обучение': 'Education',
        'Интервью': 'Interview',
        'Развлечения': 'Entertainment',
        'Аниме': 'Anime',
        'Мультфильмы': 'Cartoons',
        'Видеоигры': 'Video Games',
        'Детям': 'For Kids',
        'Строительство и ремонт': 'Construction and Repair',
        'Наука': 'Science',
        'Музыка': 'Music'
    }
    result_df['category'] = result_df['category'].replace(category_mapping)

    # Color mapping for each category
    color_mapping = {
        'Humor': 'blue',
        'Education': 'green',
        'Interview': 'red',
        'Entertainment': 'purple',
        'Anime': 'orange',
        'Cartoons': 'pink',
        'Video Games': 'yellow',
        'For Kids': 'cyan',
        'Construction and Repair': 'brown',
        'Science': 'lightgreen',
        'Music': 'magenta'
    }



    # Filters at the bottom for Category and Region
    selected_category = st.selectbox("Выберите категорию", ['All'] + list(result_df['category'].unique()))
 

    # Filter the DataFrame based on the selected Category and Region
    filtered_df = result_df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # Set up the map
    st.subheader("Cамые просматриваемые категории видео в регионах")

    # Create a map centered on one of the coordinates (adjust as needed)
    if not filtered_df.empty:
        m = leafmap.Map(center=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom=4)
    else:
        m = leafmap.Map(center=[55.7558, 37.6176], zoom=4)  # Default center if no data

    # Add points from the filtered_df DataFrame to the map with different colors for each category
    filtered_df['color'] = filtered_df['category'].map(color_mapping)

    # Add the points from DataFrame with custom colors
    for _, row in filtered_df.iterrows():
        popup = f"{row['region']}<br>Category: {row['category']}<br>Videos: {row['max_count']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(color=row['color'])
        ).add_to(m)

    # Display the map in Streamlit
    m.to_streamlit(height=700)














def multi_user_page():
    st.title("Поиск мульти-пользователей")

    st.write("В процессе EDA мы обнаружили, что аккаунтами некоторых пользователей пользуются дети или другие люди. Будем называть таких пользователей мульти-пользователями. Для дальнейших рекомендаций хотелось бы уметь определять такие случаи.")
    
    st.subheader("Определение мульти-пользователя")
    image1 = Image.open('paxan.png')
    st.image(image1, caption='Просмотры взрослого пользователя', use_column_width=True)
    image2 = Image.open('roblox.png')
    st.image(image2, caption='Просмотры ребенка', use_column_width=True)

    st.write("Выше представлен пример использования аккаунта отцом и ребенком.")
    s
    

    


if __name__ == "__main__":
    main()