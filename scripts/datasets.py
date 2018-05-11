import pandas as pd
import praw
import numpy as np
#import matplotlib
import seaborn as sns
import os


def clean_csv(file, print_sub_id = False, output_file = False):
    df = pd.read_csv(file)
    df[['7']].sub(df[['8']])  # subtract ups from downs

    df = df.iloc[1:4, [1, 2, 7]] if print_sub_id else df.iloc[:, [1, 7]] # get only comment and score columns unless specified to get id
    df.rename(columns={'0': 'comment', '1': 'id', '6': 'score'}, inplace=True)
   
    df = df.dropna(axis=0, how='any')  # delete any row with no data in either column
    df = df[~df.comment.str.contains('|'.join(['removed', 'deleted']))]  # delete rows with 'removed' or 'deleted' comments

    if print_sub_id: # if executed, convert the comment ids to submission ids
        password = input("enter password for username karmalutionalNetwork: ")
        reddit = login(password)
        df[['id']] = df.id.apply(lambda id: convert_comment_id_to_submission_id(id, reddit))

    return df


# def get_max_comment_length(df):
#     count = df['comment'].str.split().str.len().max()
#     print(count)
#     count.index = count.index.astype(str) + ' words:'
#     return count


def get_input_df_with_labels(df, file, output_file=True):
    # the df above was already parsed with clean_csv...
    # with the format ,comment,id,score.
    # the output return of this function is a DataFrame which represents the
    # same csv as the input, but with additional column at the end representing
    # the classified representation of the score using function get_single_classifier_for_score
    df = df.loc[:, ['comment', 'score']] # order by comment,score
    #df['rank'] = df.score.apply(lambda score: get_single_classifier_for_score(score, df.score))
    df['rank'] = df.score.apply(lambda score: get_percentile_for_score(score, df.score))
    df = df.loc[:, ['comment', 'rank']]
    df.set_index('comment', inplace=True)
    if output_file: # if executed, write DataFrame to new csv file
        filename = str(file.replace(".csv", ".out"))
        f = open(filename, 'w')
        f.write(df.to_csv())
        with open(filename, 'r') as istr:
             with open(filename + "final", 'w') as ostr:
               for line in istr:
                 line = line.rstrip('\n') + ','
                 print(line, file=ostr)
        f.close()
   
    return df


def get_percentile_for_score(score, all_scores):
    i = 90
    while i != -10:
        if score > np.percentile(all_scores, i):
            return str(float(i / 100))[2:]
            # return float(i / 100) -> previous version
        i -= 10


def get_single_classifier_for_score(score, all_scores, TOP = 90, GOOD = 75, NEUTRAL = 50, BAD = 35, TERRIBLE = 20):
    # scores is one score, all_scores is a series of all_scores
    # this function will return either 'top','good','neutral','bad', or 'terrible'
    # representation as a one-hot vector with a 1 in the place of the appropriate
    # classification from top...terrible,
    # dependent on whether or not the score is above the percentile threshold
    # specified by the input parameters TOP, GOOD, NEUTRAL, BAD, AND TERRIBLE.
    # there are placeholder values provided, however these parameters should be changed
    # to lower arbitrariness of the chosen values.
    # global iteration
    # iteration += 1
    if score > np.percentile(all_scores, TOP):
        print('top') # + str(iteration))
        return [1,0,0,0,0]
    elif score > np.percentile(all_scores, GOOD):
        print('good')# + str(iteration))
        return [0,1,0,0,0]
    elif score > np.percentile(all_scores, NEUTRAL):
        print('neutral')# + str(iteration))
        return [0,0,1,0,0]
    elif score > np.percentile(all_scores, BAD):
        print('bad')# + str(iteration))
        return [0,0,0,1,0]
    else:
        print('terrible')# + str(iteration))
        return [0,0,0,0,1]

#iteration = 1


def train_test_sets(df, pct): # pct is cutoff point for train | test
    train_index = round(df.shape[0] * pct)

    train = df[:train_index]
    test = df[train_index:]

    X_train = train[['comment']]
    X_test = test[['comment']]

    Y_train = train[['rank']]
    Y_test = test[['rank']]

    x_y_train_test = {'X_train': X_train, 'X_test': X_test, 'Y_train': Y_train, 'Y_test': Y_test}

    return x_y_train_test


def plot_pints(df):
    matplotlib.plot(df.iloc[1])


def get_sets(file):
    print("get sets")
    if file.split('.')[1] == "out":
        df = pd.read_csv(file)
    else:
        df = clean_csv(file)
        df = get_input_df_with_labels(df, file)
    return train_test_sets(df, 0.9)  #90 percent train


def convert_comment_id_to_submission_id(comment_id, reddit): # attempt to get thread id
    try:
        submission_id = reddit.comment(id=comment_id).submission
        return submission_id
    except Exception as e:
        return "fail"

def main():
    df = clean_csv(os.getcwd() + '/data/news_news_small_test.csv')
    df = get_input_df_with_labels(df, os.getcwd() + '/data/news_news_small_test.out', output_file = True)
    print(df)

main()


# def plot_data(file):
#     df = clean_csv(file)
#     sns.set_style("whitegrid")
#     ax = plt.subplot(111)
#     ax = sns.violinplot(x=df["score"])
#     ax.set_xlim([0, 1200])
#     plt.show()

    #km = KMeans()
    #km.fit(df["score"].reshape(-1,1))

    #print(df)
'''
    df = clean_csv(file)
    df = df.loc[:, ['score']]
    sns.set_style("whitegrid")
    sns.violinplot(data=df)
    ax1 = plt.subplot()
    #total = [data[x] for x in data]
    #ylim_max = np.percentile(total, 97.5)
    #ax1.set_ylim([0, ylim_max])
    plt.show()
    print(df)
    '''

#plot_data('./news_news.csv')

# def login(password): # login as username karmalutionalNetwork
#     return praw.Reddit(client_id='wBnuJlXAeHDnKQ',
#                        client_secret='BE_SL0MrlgAtKktUGGFYI_RXtjc', password=password,
#                        user_agent='karmalutionalNetwork', username='karmalutionalNetwork')
