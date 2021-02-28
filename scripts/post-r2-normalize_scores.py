import itertools
from collections import defaultdict
import csv
import numpy as np
from prettytable import PrettyTable

scores_file = 'scores/pldi21-scores.csv'

score_char_to_number = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
min_reviews = 3

def load_scores(filename):
    res = defaultdict(list)
    paper_to_title = defaultdict(str)
    paper_to_decision = defaultdict(str)
    email_to_name = defaultdict(str)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            title = row[1]
            decision = row[2]
            name = row[4]
            email = row[5]
            score = score_char_to_number[row[6]]
            res[paper_id].append((email, score))

            if paper_id not in paper_to_title:
                paper_to_title[paper_id] = title
            if email not in email_to_name:
                email_to_name[email] = name
            if paper_id not in paper_to_decision:
                paper_to_decision[paper_id] = decision
    return res, paper_to_title, email_to_name, paper_to_decision

def get_average_score(papers_to_raw_scores):
    all_scores = list(itertools.chain.from_iterable([[s[1] for s in scores_per_rev] for scores_per_rev in papers_to_raw_scores.values()]))
    avg = np.mean(all_scores)
    return avg

def get_per_user_avg(papers_to_raw_scores):
    rev_to_scores = defaultdict(list)
    for email, score in itertools.chain.from_iterable(papers_to_raw_scores.values()):
        rev_to_scores[email].append(score)
    result = {e: np.mean(scores) for e, scores in rev_to_scores.items() if len(scores) >= min_reviews}
    return result


def normalize_paper_scores(avg_score, papers_to_raw_scores, per_user_avg):
    per_user_avg = defaultdict(lambda: avg_score, per_user_avg)
    result = {}
    for paper_id, emails_and_scores in papers_to_raw_scores.items():
        scores = [(s - per_user_avg[e] + avg_score) for e, s in emails_and_scores]
        result[paper_id] = np.mean(scores)
    return result

if __name__ == '__main__':
    papers_to_raw_scores, paper_to_title, email_to_name, paper_to_decision = load_scores(scores_file)
    avg_score = get_average_score(papers_to_raw_scores)
    print(f'Average score: {avg_score:.3f}')
    print('(A=1, D=4, so lower is better)')
    per_user_avg = get_per_user_avg(papers_to_raw_scores)

    print()
    print('Reviewers ranked by their average score: ')
    pt = PrettyTable()
    pt.field_names = ['Email', 'Name', 'Avg. Score']
    pt.align = 'l'
    for e, user_avg_score in sorted(per_user_avg.items(), key=lambda item: item[1]):
        # print(f'{email_to_name[e]}:\t\t {user_avg_score:.3f}')
        pt.add_row([e, email_to_name[e], f'{user_avg_score:.3f}'])
    # print(pt)

    print()
    paper_to_normalized_score = normalize_paper_scores(avg_score, papers_to_raw_scores, per_user_avg)
    print('Ranked normalized papers:')
    pt = PrettyTable()
    pt.field_names = ['ID', 'Title', 'Normalized Score', 'Original Score', 'Decision']
    pt.align = 'l'
    for paper_id, normalized_score in sorted(paper_to_normalized_score.items(), key=lambda item: item[1]):
        pt.add_row([paper_id, paper_to_title[paper_id], f'{normalized_score:.3f}',
                    f'{np.mean([p[1] for p in papers_to_raw_scores[paper_id]]):.3f}',
                    paper_to_decision[paper_id]])
    print(pt)


