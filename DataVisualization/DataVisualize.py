import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
from DataVisualization.statisticaldata import NetflixDataAnalysis

class NetflixDataVisualization:
    def __init__(self, analysis):
        self.analysis = analysis
    def plot_movies_shows_by_year(self):
        movies_and_shows_by_year = self.analysis.df['release_year'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 6)) 
        plt.bar(movies_and_shows_by_year.index, movies_and_shows_by_year.values, color='skyblue')
        
        plt.title('Số lượng phim và chương trình theo năm phát hành', fontsize=14)
        plt.xlabel('Năm phát hành', fontsize=12)
        plt.ylabel('Số lượng', fontsize=12)
        plt.xticks(rotation=90, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.show()

    def plot_top_5_actors_by_genre(self):
        top_actors_by_genre = self.analysis.top_5_actors_by_genre()
        num_genres = min(len(top_actors_by_genre), 5)
        fig, axs = plt.subplots(1, num_genres, figsize=(12, 6), sharey=True) 
        fig.suptitle('Top 5 Diễn viên trong các Thể loại Phim phổ biến', fontsize=12, x=0.5)

        if num_genres == 1:
            axs = [axs]

        for i, (genre, actors) in enumerate(top_actors_by_genre.items()):
            if i >= num_genres:
                break
            actors.plot(kind='bar', ax=axs[i], color='darkorange')
            axs[i].set_title(genre, fontsize=10)
            axs[i].set_xlabel('Diễn viên', fontsize=8)
            axs[i].set_xticklabels(actors.index, rotation=90, fontsize=8)
            axs[i].tick_params(axis='x', labelsize=8)

        plt.tight_layout()
        plt.subplots_adjust(top=0.85, wspace=0.3)
        plt.show()

    def plot_movie_tv_show_distribution_by_country(self):
        all_countries = self.analysis.df['country'].dropna().str.split(', ').explode()
        country_counts = all_countries.value_counts().head(10)
        plt.figure(figsize=(10, 6))  
        country_counts.plot(kind='bar', color='lightcoral')
        plt.title('Top 10 Quốc Gia có nhiều Phim và Chương Trình TV trên Netflix', fontsize=12)
        plt.xlabel('Quốc Gia', fontsize=10)
        plt.ylabel('Số Lượng Phim và Chương Trình TV', fontsize=10)
        plt.xticks(rotation=90, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        plt.show()

    def plot_top_genres(self, top_n=5):
        genre_counts = self.analysis.df['genres'].value_counts().head(top_n)
        plt.figure(figsize=(10, 6)) 
        genre_counts.plot(kind='barh', color='cornflowerblue', edgecolor='black')
        plt.title(f'Top {top_n} Thể loại Phổ biến trên Netflix', fontsize=12)
        plt.xlabel('Số lượng', fontsize=10)
        plt.ylabel('Thể loại', fontsize=10)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def plot_movie_vs_tv_show_distribution(self):
        type_counts = self.analysis.df['type'].value_counts()
        explode = [0.1 if i == 0 else 0 for i in range(len(type_counts))]
        plt.figure(figsize=(10, 6))  
        plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', 
                colors=['lightcoral', 'skyblue'], explode=explode, 
                wedgeprops={'edgecolor': 'black'})
        plt.title('Tỷ lệ Phim và Chương trình TV trên Netflix', fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_exclusive_movies_by_year(self):
        exclusive_counts = self.analysis.exclusive_movies_count()
        plt.figure(figsize=(10, 6))  
        exclusive_counts.plot(kind='line', marker='o', color='green')
        plt.title('Số lượng Phim Độc Quyền phát hành bởi Netflix theo Năm', fontsize=12)
        plt.xlabel('Năm', fontsize=10)
        plt.ylabel('Số lượng Phim Độc Quyền', fontsize=10)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_added_year_trend(self):
        added_year_counts = self.analysis.df['date_added'].dt.year.value_counts().sort_index()
        plt.figure(figsize=(10, 6)) 
        plt.fill_between(
            added_year_counts.index, 
            added_year_counts.values, 
            color='mediumseagreen', 
            alpha=0.7
        )
        plt.plot(
            added_year_counts.index, 
            added_year_counts.values, 
            color='mediumseagreen', 
            linestyle='-', 
            linewidth=2
        )
        plt.title('Số lượng Phim và Chương trình TV được đưa vào nền tảng Netflix theo năm', fontsize=12)
        plt.xlabel('Năm', fontsize=10)
        plt.ylabel('Số lượng nội dung thêm vào', fontsize=10)
        plt.grid(True)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        plt.show()

    def plot_duration_distribution(self):
        filtered_minutes = self.analysis.df['minutes'].dropna()
        filtered_minutes = filtered_minutes[filtered_minutes > 0]

        plt.figure(figsize=(10, 6)) 

        sns.scatterplot(
            x=range(len(filtered_minutes)), 
            y=filtered_minutes, 
            hue=filtered_minutes, 
            palette='coolwarm', 
            size=filtered_minutes,
            sizes=(10, 200),  
            alpha=0.7
        )
        plt.title('Phân tán Thời lượng Phim và Chương trình TV trên Netflix', fontsize=12)
        plt.xlabel('Chỉ số thời lượng', fontsize=10)
        plt.ylabel('Thời lượng (phút)', fontsize=10)
        plt.legend(title='Thời lượng (phút)', loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()
   
    def plot_top_directors_by_rating(self):
        top_directors_by_rating = self.analysis.top_1_directors_by_rating()
        filtered_top_directors = {rating: directors.nlargest(1) for rating, directors in top_directors_by_rating.items()}

        ratings = list(filtered_top_directors.keys())
        directors = [directors.index[0] for directors in filtered_top_directors.values()]
        values = [directors.iloc[0] for directors in filtered_top_directors.values()]
        plt.figure(figsize=(10, 6))  
        plt.barh(ratings, values, color='teal', height=0.5)

        for i, (value, director) in enumerate(zip(values, directors)):
            plt.text(value + 0.1, i, director, va='center', fontsize=8)

        plt.title('Top 1 Đạo diễn theo tất cả loại đánh giá', fontsize=12)
        plt.xlabel('Số lượng phim', fontsize=10)
        plt.ylabel('Loại đánh giá', fontsize=10)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

def plot_correlation_matrix_matrix(matrix, title="Genre Correlation Matrix"):
    plt.figure(figsize=(10, 6))  
    plt.imshow(matrix.values, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label="Correlation")
    plt.title(title, fontsize=12)

    plt.xticks(ticks=np.arange(len(matrix.columns)), labels=matrix.columns, rotation=90, ha='right', fontsize=8)
    plt.yticks(ticks=np.arange(len(matrix.index)), labels=matrix.index, fontsize=8)

    for i in range(len(matrix.index)):
        for j in range(len(matrix.columns)):
            plt.text(j, i, f"{matrix.values[i, j]:.2f}", ha="center", va="center", color="black")

    plt.tight_layout()
    plt.show()
