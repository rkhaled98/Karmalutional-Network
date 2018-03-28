import pandas as pd
import praw


def clean_csv(file, print_sub_id = False, output_file = False):
    df = pd.read_csv(file)
    df[['7']].sub(df[['8']])  # subtract ups from downs
    df = df.iloc[:, [1,2,7]] if print_sub_id else df.iloc[:, [1,7]] # get only comment and score columns unless specified to get id
    df.rename(columns={'0': 'comment', '1': 'id', '6': 'score'}, inplace=True)

    df = df.dropna(axis=0, how='any')  # delete any row with no data in either column
    df = df[~df.comment.str.contains('|'.join(['removed', 'deleted']))]  # delete rows with 'removed' or 'deleted' comments

    if print_sub_id: # if executed, convert the comment ids to submission ids
        password = input("enter password for username karmalutionalNetwork: ")
        reddit = login(password)
        df[['id']] = df.id.apply(lambda id: convert_comment_id_to_submission_id(id, reddit))

    if output_file: # if executed, write DataFrame to new csv file
        f = open(str(file.replace(".csv", ".out")), 'w')
        f.write(df.to_csv())

    print(df)
    return df

def login(password): # login as username karmalutionalNetwork
    return praw.Reddit(client_id='wBnuJlXAeHDnKQ',
                         client_secret='BE_SL0MrlgAtKktUGGFYI_RXtjc', password=password,
                         user_agent='karmalutionalNetwork', username='karmalutionalNetwork')

def convert_comment_id_to_submission_id(comment_id, reddit): # attempt to get thread id
    try{
        submission_id = reddit.comment(id=comment_id).submission
        return submission_id
    }
    catch(err){
        return "fail"
    }


clean_csv(file='news_news.csv', print_sub_id = True, output_file = True)
