import twint
from os.path import join
from tqdm.auto import tqdm
from .coalitions import coalitions

def generate_csv_with_tweets_posted_by_a_user(user_name, since, save_dir=""):
    c = twint.Config()
    c.Username = user_name
    c.Since = since
    c.Store_csv = True
    c.Output = f"{join(save_dir, user_name)}.csv"

    c.Retweet = True
    twint.run.Profile(c)


def generate_csv_with_tweets_mentioning_user(user_name, since, save_dir=""):
    c = twint.Config()
    c.Since = since
    c.Search = f"@{user_name}"
    c.Store_csv = True
    c.Output = f"{join(save_dir, user_name)}.csv"
    twint.run.Search(c)


if __name__ == '__main__':
    since = "2020-10-01"
    for coalition in tqdm(coalitions.values()):
        for party_name in coalition:
            generate_csv_with_tweets_posted_by_a_user(party_name, since, save_dir=f"data")

