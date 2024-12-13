import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class NetflixDataAnalysis:

    def __init__(self, df):
        self.df = df

#gọi một số biến cần thiết
    def preprocess_data(self):
        self.movies_and_shows = self.df[(self.df['type'] == 'Movie') | (self.df['type'] == 'TV Show')]
        self.df["date_added"] = pd.to_datetime(self.df["date_added"], dayfirst=True, errors='coerce')
        self.tv_shows = self.df[self.df['type'] == 'TV Show']
        self.movies = self.df[self.df['type'] == 'Movie']
        self.added_year = self.df['date_added'].dt.year 
        self.df = self.df.explode('genres')

#đếm loại movies
    def count_movies(self):
        temporary = self.movies['country'].str.split(', ')
        all_movies = temporary.explode()
        return all_movies.value_counts().sort_index()
    
    #đếm loại tv_show
    def count_tv_shows(self):
        temporary = self.tv_shows['country'].str.split(', ')
        all_tv_shows = temporary.explode()
        return all_tv_shows.value_counts().sort_index()
    
    #đếm số lượng sản phẩm theo quốc gia
    def count_movies_and_shows_by_country(self):
        temporary = self.movies_and_shows['country'].str.split(', ')
        all_movies_and_shows = temporary.explode() 
        return all_movies_and_shows.value_counts().sort_index() 

#trung bình thời lượng phim
    def average_duration_by_year(self):
        return self.movies_and_shows.groupby('release_year')['minutes'].mean()

#lượng phim do netflix phân phối
    def exclusive_movies_count(self):
        exclusive_movies = self.df[(self.df['type'] == 'Movie') & (self.df['release_year'] == self.df['date_added'].dt.year)]
        return exclusive_movies['release_year'].value_counts().sort_index()

#số lượng phim netflix thêm vào
    def count_by_year_added(self):
        return self.added_year.value_counts().sort_index()

#top 5 diễn viên theo thể loại
    def top_5_actors_by_genre(self):
        genre_counts = self.df['genres'].value_counts()
        top_genres = genre_counts.head(5).index
        top_actors = {}

        for genre in top_genres:
            actors_count = self.df[self.df['genres'] == genre]['cast'].str.split(', ').explode().value_counts().head(5)
            top_actors[genre] = actors_count
    
        return top_actors

#top 1 diễn viên theo ratings
    def top_1_directors_by_rating(self):
        top_directors = {}
        for rating, group in self.df.groupby('rating'):
            directors_count = group['director'].str.split(', ').explode().value_counts().head(1)
            top_directors[rating] = directors_count
        return top_directors
    
# ma trận tương quan của 10 thể loại nổi bật
    def genre_correlation(self, top_n=10):
        tv_shows = self.tv_shows['genres'].str.split(', ')
        movies = self.movies['genres'].str.split(', ')

        top_genres_tv_shows = tv_shows.explode().value_counts().head(top_n).index

        top_genres_movies = movies.explode().value_counts().head(top_n).index

        one_hot_tv_shows = pd.DataFrame(0, index=self.tv_shows.index, columns=top_genres_tv_shows)
        for i, genres in tv_shows.items():
            for genre in genres:
                if genre in top_genres_tv_shows:
                    one_hot_tv_shows.loc[i, genre] = 1

        one_hot_movies = pd.DataFrame(0, index=self.movies.index, columns=top_genres_movies)
        for i, genres in movies.items():
            for genre in genres:
                if genre in top_genres_movies:
                    one_hot_movies.loc[i, genre] = 1

        correlation_matrix_tv_shows = cosine_similarity(one_hot_tv_shows.T)
        correlation_matrix_movies = cosine_similarity(one_hot_movies.T)

        genre_correlation_tv_shows = pd.DataFrame(
            correlation_matrix_tv_shows,
            index=top_genres_tv_shows,
            columns=top_genres_tv_shows
        )
        genre_correlation_movies = pd.DataFrame(
            correlation_matrix_movies,
            index=top_genres_movies,
            columns=top_genres_movies
        )
        
        return genre_correlation_tv_shows, genre_correlation_movies
    #một số thống kê về thời lượng
    def calculate_duration_statistics(self):
        duration_data = self.movies_and_shows['minutes'].to_numpy()
        stats = {
            'Thời gian trung bình': np.mean(duration_data),
            'Tổng thời gian': np.sum(duration_data),
            'Thời gian ngắn nhất': np.min(duration_data),
            'Thời gian dài nhất': np.max(duration_data),
            'Phương sai thời gian': np.var(duration_data),
            'Độ lệch chuẩn thời gian': np.std(duration_data)
        }
        return stats


    def print_summary(self):
        print("Các quốc gia có cột 'type' là 'TV show':")
        print(self.count_tv_shows())

        print("Các quốc gia có cột 'type' là 'Movie':")
        print(self.count_movies())

        print("Số lượng phim và show TV theo quốc gia:")
        print(self.count_movies_and_shows_by_country())

        print("Thời gian trung bình phim và show TV theo năm phát hành:")
        print(self.average_duration_by_year())

        print("Thống kê số lượng phim độc quyền bởi Netflix:")
        print(self.exclusive_movies_count())

        print("Thống kê số lượng phim và show TV theo năm được thêm vào Netflix:")
        print(self.count_by_year_added())

        print("Ma trận tương quan của các thể loại nổi bật của TV Show, Movie:")
        print(self.genre_correlation())
        
        print("Top 5 diễn viên đóng nhiều phim nhất theo thể loại:")
        for genre, actors in self.top_5_actors_by_genre().items():
            print(f"Thể loại {genre}:")
            print(actors)
            print()

        print("Top 5 đạo diễn có nhiều phim nhất theo loại đánh giá:")
        for rating, directors in self.top_1_directors_by_rating().items():
            print(f"Rating {rating}:")
            print(directors)
            print()

        stats = self.calculate_duration_statistics()
        print("Thống kê thời gian:")
        for key, value in stats.items():
            print(f"{key}: {value}")
