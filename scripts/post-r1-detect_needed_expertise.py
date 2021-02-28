from collections import defaultdict
import csv

scores_file = 'scores/pldi21-scores.csv'
assignments_filename = 'pldi21-pcassignments.csv'
bids_filename = 'pldi21-allprefs.csv'

def load_expertise(filename):
    res = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            email = row[5]
            expertise = row[7]
            res[paper_id].append((email, expertise))
    return res

def load_assignments(filename):
    res = defaultdict(list)
    email_to_name = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            if row[1].lower() != 'primary':
                continue
            paper_id = int(row[0])
            reviewer_mail = row[2]
            res[paper_id].append(reviewer_mail)
    return res


def load_bids(filename):
    res = defaultdict(lambda: defaultdict(str))
    mail_to_name = {}
    paper_to_title = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            reviewer_mail = row[4]
            expertise = row[6]
            if len(expertise) > 0:
                res[reviewer_mail][paper_id] = expertise

            reviewer_name = f'{row[2]} {row[3]}'
            if reviewer_mail not in mail_to_name:
                mail_to_name[reviewer_mail] = reviewer_name

            title = row[1]
            if paper_id not in paper_to_title:
                paper_to_title[paper_id] = title

    return res, mail_to_name, paper_to_title

if __name__ == '__main__':
    papers_to_expertise = load_expertise(scores_file)
    paper_to_revs = load_assignments(assignments_filename)
    _, mail_to_name, _ = load_bids(bids_filename)

    print('Papers without experts, and all assigned PC already reviewed:')
    for paper, revs in paper_to_revs.items():
        reviewers_expertise = papers_to_expertise[paper]
        actual_reviewers = [r[0] for r in reviewers_expertise]
        actual_expertise = [r[1] for r in reviewers_expertise]
        if 'X' in actual_expertise:
            continue
        if all((r in actual_reviewers) for r in revs):
            print(f'Paper: {paper}')


    print('Papers without experts, but not all PC members reviewed yet:')
    for paper, revs in paper_to_revs.items():
        reviewers_expertise = papers_to_expertise[paper]
        actual_reviewers = [r[0] for r in reviewers_expertise]
        actual_expertise = [r[1] for r in reviewers_expertise]
        if 'X' in actual_expertise:
            continue
        if not all((r in actual_reviewers) for r in revs):
            left_revs = [mail_to_name[r] for r in revs if r not in actual_reviewers]
            print(f'Paper: {paper} (did not review yet: {left_revs})')
