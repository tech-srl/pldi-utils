from collections import defaultdict
from sklearn.cluster import KMeans, Birch
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.preprocessing import MultiLabelBinarizer
import csv
import numpy as np

# This file is obtained from HotCRP by filtering the "Accepted" papers:
# https://pldi21.hotcrp.com/search?q=&t=acc
# and then pressing "Download" -> "Topics"
accepted_topics_file = '/Users/urialon/Documents/PLDI21/accepted/pldi21-topics.csv'
preference_file = '/Users/urialon/Documents/PLDI21/accepted/prefs.csv'

def load_paper_to_topics(filename):
    paper_to_topics = defaultdict(list)
    all_topics = set()
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            title = row[1]
            topic = row[2]
            paper_to_topics[(paper_id, title)].append(topic)
            all_topics.add(topic)
    return paper_to_topics, list(all_topics)

def load_preferred_session_to_papers(filename):
    early_session = []
    late_session = []
    no_pref = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            if len(row[3]) == 0 or row[0] == 'Total':
                continue
            paper_id = int(row[3])
            if row[6] == 'Y':
                early_session.append(paper_id)
            elif row[7] == 'Y':
                late_session.append(paper_id)
            elif row[8] == 'Y':
                no_pref.append(paper_id)
            else:
                print(f'Problem reading session preferrence for paper {paper_id}')
    return early_session, late_session, no_pref


if __name__ == '__main__':
    paper_to_topics, all_topics = load_paper_to_topics(accepted_topics_file)
    paper_to_topics_list = list(paper_to_topics.items())
    early_session, late_session, no_pref = load_preferred_session_to_papers(preference_file)

    mlb = MultiLabelBinarizer()
    features = mlb.fit_transform([topics for _, topics in paper_to_topics_list])


    early_features = [f for f, ((pid, title), _) in zip(features, paper_to_topics_list) if pid in early_session]
    late_features = [f for f, ((pid, title), _) in zip(features, paper_to_topics_list) if pid in late_session + no_pref]

    kmeans_early = KMeans(n_clusters=6, init='k-means++').fit(early_features)
    kmeans_late = KMeans(n_clusters=6, init='k-means++').fit(late_features)

    assignment_early = sorted(
        [(label, pid, title, feat) for (pid, title, feat), label in
                        zip([(pid, title, feat) for ((pid, title), _), feat in zip(paper_to_topics_list, features)
                            if pid in early_session], kmeans_early.labels_)], key=lambda x: x[0])
    assignment_late = sorted(
        [(label, pid, title, feat) for (pid, title, feat), label in
                        zip([(pid, title, feat) for ((pid, title), _), feat in zip(paper_to_topics_list, features)
                            if pid in (late_session + no_pref)], kmeans_late.labels_)], key=lambda x: x[0])

    print('Sessions at 13:00:')
    for label, pid, title, f in assignment_early:
        print(f'[{label}] {pid} "{title}" ({",".join(paper_to_topics[(pid,title)])})')

    print()
    print('Sessions at 13:00:')
    for label, pid, title, f in assignment_late:
        print(f'[{label}] {pid} "{title}" ({",".join(paper_to_topics[(pid,title)])})')
    print()
    print(f'early: {len(assignment_early)}, late: {len(assignment_late)}')
    print(f'Total: {len(assignment_late) + len(assignment_early)}')

