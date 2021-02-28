import itertools
from collections import defaultdict
import csv
import numpy as np
from prettytable import PrettyTable

scores_file = 'accepted-scores.csv'
all_topics_file = 'pldi21-topics.csv'

def load_paper_to_title(filename):
    paper_to_title = defaultdict(str)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            title = row[1]
            if paper_id not in paper_to_title:
                paper_to_title[paper_id] = title
    return paper_to_title

def load_paper_to_topics(filename):
    topic_to_papers = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            topic = row[2]
            topic_to_papers[topic].append(paper_id)
    return topic_to_papers

if __name__ == '__main__':
    accepted_paper_to_title = load_paper_to_title(scores_file)
    topic_to_papers = load_paper_to_topics(all_topics_file)

    for topic, all_papers_in_topic in topic_to_papers.items():
        accepted_papers = [p for p in all_papers_in_topic if p in accepted_paper_to_title]
        topic_accept_rate = len(accepted_papers) / len(all_papers_in_topic)*100 if len(all_papers_in_topic) > 0 else None
        print(f'Topic: {topic}, accepted papers: {len(accepted_papers)}, out of {len(all_papers_in_topic)} ({topic_accept_rate:.0f}%)')
        for pid in accepted_papers:
            print(f'\t{pid}: {accepted_paper_to_title[pid]}')




