import itertools
from collections import defaultdict
import csv
import numpy as np
from prettytable import PrettyTable

accepted_scores_file = 'accepted-scores.csv'
all_scores_file = 'pldi21-scores.csv'

def load_reviewer_to_papers(filename):
    reviewer_to_papers = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            reviewer = row[4]
            reviewer_to_papers[reviewer].append(paper_id)
    return reviewer_to_papers


if __name__ == '__main__':
    reviewer_to_papers = load_reviewer_to_papers(all_scores_file)
    reviewer_to_accepted_papers = load_reviewer_to_papers(accepted_scores_file)

    rev_to_acceptance_rate = {}

    for reviewer, all_reviewed_papers in reviewer_to_papers.items():
        num_reviewed_papers = len(all_reviewed_papers)
        num_accepted_papers = len(reviewer_to_accepted_papers[reviewer])
        rev_to_acceptance_rate[reviewer] = num_accepted_papers / num_reviewed_papers

    pt = PrettyTable()
    pt.field_names = ['Reviewer', 'Acceptance Rate', 'Number of papers reviewed']
    pt.align = 'l'
    for rev in sorted(rev_to_acceptance_rate.keys(), key=lambda x: rev_to_acceptance_rate[x], reverse=True):
        pt.add_row([rev, rev_to_acceptance_rate[rev], len(reviewer_to_papers[rev])])
    print(pt)




