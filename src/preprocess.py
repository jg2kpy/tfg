import os
import pandas as pd
import logger
from collections import Counter

from classes.Movies_info import Movies_info, Movie_info
from classes.Users import Users

count = 0

def main(dataset_path = '../datasets/ml-100k/ratings.csv', output_path = './data', top_usuarios = 10000, new_comer_filter = 5, dataset_100k_item_info_path = '../datasets/ml-100k/u.item.csv'):
    global count
    log = logger.logger_class('PREPROCESS')
    print("\nLeyendo el dataset desde:", dataset_path)
    df_og = pd.read_csv(dataset_path)

    print("\nTamaño del dataframe original:", len(df_og))

    df_item_info = pd.read_csv(dataset_100k_item_info_path)

    print("Eliminando la columna 'timestamp'")
    df_og = df_og.drop(columns='timestamp')

    print("Ordenando el dataset por la primera columna...")
    df_og = df_og.sort_values(by=df_og.columns[0])

    print(f"Seleccionando los {top_usuarios} usuarios películas más comunes...")
    user_ids_count = Counter(df_og.userId)
    user_ids = [u for u, c in user_ids_count.most_common(top_usuarios)]

    print("Filtrando el dataframe para que solo contenga los usuarios seleccionados...")
    df_small = df_og[df_og.userId.isin(user_ids)].copy()

    movie_ids_count = Counter(df_small.movieId)
    movies_no_newcomers = [movieId for movieId, count in movie_ids_count.items() if count > new_comer_filter]
    new_comers = [movieId for movieId, count in movie_ids_count.items() if count <= new_comer_filter]
    movie_ids = movies_no_newcomers + new_comers

    print(f"Películas que aparecen más de {new_comer_filter} veces: {len(movies_no_newcomers)}")
    print(f"Películas que aparecen menos o igual a {new_comer_filter} veces (Newcomers): {len(new_comers)}")

    print("\nCantidad total de usuarios:", len(user_ids))
    print("Cantidad total de peliculas:", len(movie_ids))
    print("Tamaño del dataframe actual:", len(df_small))

    print("\nGenerando users2movie_ratings...")
    users2movie_ratings = Users()
    df_small_len = len(df_small)
    ratings_by_movie = {}
    log_users2movie = logger.logger_class('update_users2movie_ratings')
    movies_counter = {}
    count = 0

    def update_users2movie_ratings(row):
        global count
        if count % 10000:
            log_users2movie.percentage(count, df_small_len)
        count+=1

        user_id = int(row.userId)
        movie_id = int(row.movieId)
        rating = float(row.rating)

        user = users2movie_ratings.get_or_create_user_by_id(user_id)

        user.add_movie_rating(movie_id, rating)
        if movie_id not in ratings_by_movie:
            ratings_by_movie[movie_id] = []
        ratings_by_movie[movie_id].append(rating)

    df_small.apply(update_users2movie_ratings, axis=1)

    def calcular_profit(ratings):
        if not ratings:
            return 0
        positive_ratings = sum(1 for rating in ratings if rating >= 3)
        return 1 + (9 * (positive_ratings / len(ratings)))

    print("\nGenerando movies_info...")
    movies_info = Movies_info()
    log_movies_info = logger.logger_class('Movies_info')
    count = 0

    for movie_id in movie_ids:
        if count % 1000:
            log_movies_info.percentage(count, len(movie_ids))
        count+=1

        ratings = ratings_by_movie[movie_id]
        popularity = len(ratings)
        profit = calcular_profit(ratings)
        is_newcomer = True if movie_id in new_comers else False

        movie_info = Movie_info(movie_id, profit, is_newcomer, popularity)
        movies_info.add_movie(movie_info)

    print("\nEliminando usuarios que solo tienen películas newcomers...")

    def has_non_newcomer_movies(user):
        return any(not movies_info.get_movie_by_id(movie_id).is_newcomer for movie_id in user.get_movie_ids())

    cant_usuarios = users2movie_ratings.get_len_users()
    valid_users = [user for user in users2movie_ratings.get_all_users() if has_non_newcomer_movies(user)]
    users2movie_ratings.set_users(valid_users)

    print(f"Cantidad de usuarios eliminados por solo tener newcomers: {cant_usuarios - len(valid_users)}")

    for movie in movies_info.get_all_movies():
        movie_id = movie.get_id()
        movie_details = df_item_info[df_item_info.iloc[:, 0] == movie_id].iloc[:, 2:].astype(bool).any(axis=0)
        binary_array = movie_details.astype(int).tolist()
        movie.set_content(binary_array)

    for user in users2movie_ratings.get_all_users():
        top_movies = sorted(user.get_movies_and_ratings(), key=lambda x: x[1], reverse=True)[:10]
        movie_details = []
        for movie_id, _ in top_movies:
            movie_details.append(movies_info.get_movie_by_id(movie_id).get_content())
        if movie_details:
            binary_sum_result = [sum(bits) for bits in zip(*movie_details)]
        else:
            binary_sum_result = []
        user.set_profile(binary_sum_result)

    print("\nGuardando los datos procesados en formato JSON...")

    if not os.path.exists(output_path):
        print(f"El directorio {output_path} no existe. Creándolo...")
        try:
            os.makedirs(output_path)
        except Exception as e:
            print(f"Error al crear el directorio {output_path}: {e}")
            output_path = './data'
            if not os.path.exists(output_path):
                print(f"Creando el directorio {output_path} en el directorio actual...")
                os.makedirs(output_path)

    users_output_file = f"{output_path}/users2movie_ratings.json"
    movies_output_file = f"{output_path}/movies_info.json"

    with open(users_output_file, 'w') as f:
        f.write(users2movie_ratings.to_json())
    log.success(f"Datos de usuarios guardados en: {users_output_file}")

    with open(movies_output_file, 'w') as f:
        f.write(movies_info.to_json())
    log.success(f"Datos de películas guardados en: {movies_output_file}")

if __name__ == "__main__":
    main()
