from collections import defaultdict
import csv

assignments_filename = 'pldi21-pcassignments.csv'
bids_filename = 'pldi21-allprefs.csv'

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

def load_assignments(filename):
    res = defaultdict(list)
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


if __name__ == '__main__':
    reviewer_paper_expertise, mail_to_name, paper_to_title = load_bids(bids_filename)
    paper_to_revs = load_assignments(assignments_filename)

    print('Papers without experts:')
    for paper, revs in paper_to_revs.items():
        if all(paper in reviewer_paper_expertise[r] for r in revs):
            # All reviewers have bids for this paper
            experts = []
            for r in revs:
                expertise = reviewer_paper_expertise[r][paper]
                if expertise.lower() == 'x':
                    experts.append(r)
            experts_str = ",".join(experts) if len(experts) > 0 else 'NONE'
            if len(experts) == 0:
                print(f'Paper: {paper} (\"{paper_to_title[paper]}\"), experts: {experts_str}')
        else:
            continue

    print('Suspected papers without experts (because not all reviewers have bids):')
    for paper, revs in paper_to_revs.items():
        if not all(paper in reviewer_paper_expertise[r] for r in revs):
            # Not all reviewers have bids for this paper
            if any(reviewer_paper_expertise[r][paper].lower() == 'x' for r in revs):
                continue
            possible_experts = [r for r in revs if (r not in reviewer_paper_expertise)
                                or (paper not in reviewer_paper_expertise[r])
                                or (len(reviewer_paper_expertise[r][paper]) == 0)]
            not_experts = [r for r in revs if reviewer_paper_expertise[r][paper].lower() == 'x']

            print(f'Paper: {paper} (\"{paper_to_title[paper]}\") is OK only if one of the following is an expert: ')
            for r in possible_experts:
                print(f'\t{r} ({mail_to_name[r]})')
            print()
        else:
            continue
