import pandas as pd


def clean_csv(file):
    df = pd.read_csv(file)
    df[['7']].sub(df[['8']])  # subtract ups from downs
    df = df.iloc[:, [1, 7]]  # get only comment and score columns
    df.rename(columns={'0': 'comment', '6': 'score'}, inplace=True)
    df = df.dropna(axis=0, how='any')  # delete any row with no data in either column
    df = df[~df.comment.str.contains('|'.join(['removed', 'deleted']))]  # delete rows with 'removed' or 'deleted' comments
    print(df)
    return df


clean_csv(file='news_news.csv')

