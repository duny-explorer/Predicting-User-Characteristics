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
    
    watchtime_age = pd.read_csv('csv_data\watchtime_age.csv')

    mean_age = pd.read_csv('csv_data\mean_age.csv')

    median_percent_df = pd.read_csv('csv_data\median_percent_watched_category.csv')

    time_of_day_counts = pd.read_csv('csv_data\ime_of_day_counts.csv')

    merged_df = pd.read_csv('csv_data\merged_df.csv')



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
        plt.axis('equal')  


        st.pyplot(plt)


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

        st.write('В среднем пользователи просмаривают 8 процентов от длительности видео, дольше всего смотрят категории Спорт и Юмор')

        plt.figure(figsize=(10, 6))
        st.subheader('Количество видео в зависимости от времени суток')
        sns.barplot(x='time_of_day', y='count', data=time_of_day_counts, palette='pastel')
        plt.title("Количество видео в зависимости от времени суток")
        plt.title("Количество видео в зависимости от времени суток")
        plt.xlabel("Время суток")
        plt.ylabel("Количество видео")
        st.pyplot(plt)

        st.write('Большинство видео пользователи просмотрели вечером днем и утром, наименьший класс это ночь.')


        


        


    if __name__ == '__main__':
        display_data()









#Cамая важная фича оказалась из эмбеддинга 



def metrics_page():
    st.title("Метрики")
    st.write("На этой странице представлены посчитанные метрики после обучения модели")
    
    st.subheader("Пайплайн модели")
    image1 = Image.open('pipeline.png')
    st.image(image1, caption='Пайплайн модели', use_column_width=True)

    data_metrics = {
    'model': ['baseline', 'CoLES', 'aggregate', 'CoLES + aggregate'],
    'score_weighted': [0.4463, 0.5143, 0.5352, 0.5389],
    }


    st.subheader("Подсчет метрик")
    metrics = pd.DataFrame(data_metrics)
    st.dataframe(metrics)

    st.write("Формула расчета score_weighted в зависимости от n - количества просмотренных видео пользователем:")
    st.latex(r'''Score = F_{\text{weighted}}/n''')
        

    x_values = [1, 2, 5, 10, 15]
    y_values = [0.4463, 0.2268, 0.09452, 0.04817, 0.03344]

    
    st.subheader("График")
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
 


    plt.title("Score модели в зависимости от того, начиная с какого количества видео мы рассматриваем пользователя")
    plt.xlabel("Количество просмотренных видео")
    plt.ylabel("Score")
    st.pyplot(plt)


    st.write('По графику, используя правило локтя, определим, что наиболее оптимальное количество видео, просмотренных пользователем  — 5')


    st.subheader("Время работы модели")

    st.write('Модель для определения пола и модель для определения возраста на инференесе в сумме работают 25 минут')

    
def graphics_page():
    df_keywords = pd.read_csv('csv_data\keywords.csv')
    df_keywords_2 = df_keywords.head(20)
    st.title("Аналитика по названию видео")

    st.subheader("Облако слов для названий видео")
    image = Image.open('cloud_of_words.png')
    st.image(image, caption='Облако слов', use_column_width=True)
    st.write('На графике представлено облако слов названий видео. Самые часто встречающиеся слова это СЕРИЯ, ВЫПУСК, МУЖСКОЕ, ЖЕНСКОЕ, СЕЗОН ')


    plt.figure(figsize=(10, 6))
    st.subheader('Возраст пользователей в зависимости от ключевого слова в названии')
    sns.barplot(x='id', y='age', data=df_keywords_2, palette='pastel')
    
    plt.xticks(rotation=45, ha='right')

    plt.xlabel('Ключевое слово')
    plt.ylabel('Возраст')
    plt.title('Возраст пользователей в зависимости от ключевого слова в названии')

    st.write('В среднем самые распространенными ключевыми словами являются названия сериалов, в средний возраст пользователя варьируется от 26 до 35 ')
        
    st.pyplot(plt)
    











def maps_page():

    st.title("Карты")



    try:
        result_df = pd.read_csv('csv_data\category_result.csv', encoding='utf-8')
    except UnicodeDecodeError:
        st.error("Error loading the file. Try using a different encoding like 'latin1'.")
        result_df = pd.read_csv('csv_data\category_result.csv', encoding='latin1')


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




    selected_category = st.selectbox("Выберите категорию", ['All'] + list(result_df['category'].unique()))
 

    filtered_df = result_df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]


    st.subheader("Cамые просматриваемые категории видео в регионах")

    if not filtered_df.empty:
        m = leafmap.Map(center=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom=4)
    else:
        m = leafmap.Map(center=[55.7558, 37.6176], zoom=4)  

    
    filtered_df['color'] = filtered_df['category'].map(color_mapping)


    for _, row in filtered_df.iterrows():
        popup = f"{row['region']}<br>Category: {row['category']}<br>Videos: {row['max_count']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(color=row['color'])
        ).add_to(m)


    m.to_streamlit(height=700)














def multi_user_page():
    st.title("Поиск мульти-пользователей")

    st.write("В процессе EDA мы обнаружили, что многие пользователи реальный возраст не соответствует контенту, которого они просматривают. Но, проанализировав данные, мы определили, что есть пользователи которые не солгали о своем возрасте при регистрации, также существуют так называемые 'мультипользователи' - это аккаунт которым пользуется два или более человек")

    st.write("Мы придумали алгоритм для выискивания подобных аккаунтов. Суть алгоритма в определении с помощью квантилей роликов на на которых есть потенциально молодой зритель, и находим тех пользователей, у которых разница между 10-ым квантилем и 90-ым квантилем наибольшая. Далее разбиваем просмотренные видео на кластеры." )
    
    st.write("На примере ниже можно увидеть, что ребенок смотрел видео по выходным, а отец по рабочим дням. Можно сделать вывод, что при дальнейших рекомендациях для многопользовательских аккаунтов нужно учитывать время просмотра и является ли день рабочим или выходным" )

    st.subheader("Определение мульти-пользователя")
    image1 = Image.open('paxan.png')
    st.image(image1, caption='Просмотры взрослого пользователя', use_column_width=True)
    image2 = Image.open('roblox.png')
    st.image(image2, caption='Просмотры ребенка', use_column_width=True)

    st.write("Выше представлен пример использования аккаунта отцом и ребенком.")

   
    

    


if __name__ == "__main__":
    main()