from os.path import join, realpath, dirname, exists, basename
from os import makedirs
import pandas as pd
from pandas import CategoricalDtype
from tqdm.auto import tqdm
from .coalitions import coalitions


def generate_number_of_tweets_per_day(df, output_dir):
    # exclude retweets
    df = df[df.user_rt.isnull()]

    value_counts = df['date'].value_counts()

    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['date', 'number_of_tweets']
    df_value_counts = df_value_counts.sort_values(by=['date'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "number_of_tweets_per_day.csv")
    df_value_counts.to_csv(path, index=False)


def generate_number_of_retweets_per_day(df, output_dir):
    df = df.dropna(subset=['user_rt'])
    value_counts = df['date'].value_counts()

    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['date', 'number_of_retweets']
    df_value_counts = df_value_counts.sort_values(by=['date'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "number_of_retweets_per_day.csv")
    df_value_counts.to_csv(path, index=False)


def generate_number_of_retweets_for_users_tweets_per_day(df, output_dir):
    df_retweets_counts = df.groupby("date")['retweets_count'].sum().reset_index()
    df_retweets_counts = df_retweets_counts.sort_values(by=['date'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "number_of_retweets_for_users_tweets_per_day.csv")
    df_retweets_counts.to_csv(path, index=False)


def generate_number_of_likes_for_users_tweets_per_day(df, output_dir):
    df_likes_counts = df.groupby("date")['likes_count'].sum().reset_index()
    df_likes_counts = df_likes_counts.sort_values(by=['date'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "number_of_likes_for_users_tweets_per_day.csv")
    df_likes_counts.to_csv(path, index=False)


def generate_tweeting_activity_distribution_in_a_day(df, output_dir):
    # exclude retweets
    df = df[df.user_rt.isnull()]

    value_counts = pd.to_datetime(df['time']).dt.hour.value_counts(dropna=True)
    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['hour', 'number_of_tweets']
    df_value_counts = df_value_counts.sort_values(by=['hour'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "tweeting_activity_distribution_in_a_day.csv")
    df_value_counts.to_csv(path, index=False)


def generate_tweeting_activity_distribution_in_a_week(df, output_dir):
    # exclude retweets
    df = df[df.user_rt.isnull()]

    value_counts = pd.to_datetime(df['date']).dt.day_name().value_counts(dropna=True)
    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['week_day', 'number_of_tweets']

    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    df_value_counts['week_day'] = df_value_counts['week_day'].astype(cat_type)
    df_value_counts = df_value_counts.sort_values(by=['week_day'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "tweeting_activity_distribution_in_a_week.csv")
    df_value_counts.to_csv(path, index=False)


def generate_retweeting_activity_distribution_in_a_day(df, output_dir):
    df = df.dropna(subset=['user_rt'])
    value_counts = pd.to_datetime(df['time']).dt.hour.value_counts(dropna=True)
    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['hour', 'number_of_retweets']
    df_value_counts = df_value_counts.sort_values(by=['hour'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "retweeting_activity_distribution_in_a_day.csv")
    df_value_counts.to_csv(path, index=False)


def generate_retweeting_activity_distribution_in_a_week(df, output_dir):
    df = df.dropna(subset=['user_rt'])
    value_counts = pd.to_datetime(df['date']).dt.day_name().value_counts(dropna=True)
    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['week_day', 'number_of_retweets']

    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    df_value_counts['week_day'] = df_value_counts['week_day'].astype(cat_type)
    df_value_counts = df_value_counts.sort_values(by=['week_day'])

    if not exists(output_dir):
        makedirs(output_dir)

    path = join(output_dir, "retweeting_activity_distribution_in_a_week.csv")
    df_value_counts.to_csv(path, index=False)


if __name__ == '__main__':
    data_dir_path = "data"



    for coalition_name in tqdm(coalitions.keys()):
        for party_name in coalitions[coalition_name]:

            save_dir = join("processed_data", coalition_name, party_name)
            df = pd.read_csv(join(data_dir_path, f"{party_name}.csv"))

            generate_number_of_tweets_per_day(df, join(save_dir))
            generate_number_of_retweets_per_day(df, join(save_dir))

            generate_number_of_retweets_for_users_tweets_per_day(df, join(save_dir))
            generate_number_of_likes_for_users_tweets_per_day(df, join(save_dir))

            generate_tweeting_activity_distribution_in_a_day(df, join(save_dir))
            generate_tweeting_activity_distribution_in_a_week(df, join(save_dir))

            generate_retweeting_activity_distribution_in_a_day(df, join(save_dir))
            generate_retweeting_activity_distribution_in_a_week(df, join(save_dir))