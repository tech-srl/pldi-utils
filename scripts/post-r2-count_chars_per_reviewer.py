from collections import defaultdict
import numpy as np
import csv

reviews_filename = 'pldi21-reviews.csv'
topk = 1000

def load_reviews(filename):
    res = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            # paper_id = int(row[0])
            reviewer_name = row[3]
            summary = row[7]
            review = row[8]
            res[reviewer_name].append(summary + review)
    return res


if __name__ == '__main__':
    reviews_per_rev = load_reviews(reviews_filename)

    total_chars_per_rev = [(rev, sum(len(r) for r in reviews)) for rev, reviews in reviews_per_rev.items()]
    avg_chars_per_rev = [(rev, np.mean([len(r) for r in reviews])) for rev, reviews in reviews_per_rev.items()]

    sorted_total_chars_per_rev = sorted(total_chars_per_rev, key=lambda x: x[1], reverse=True)
    sorted_avg_chars_per_rev = sorted(avg_chars_per_rev, key=lambda x: x[1], reverse=True)

    print('Total characters: ')
    for rev, score in sorted_total_chars_per_rev[:topk]:
        print(f'{rev}: {score}')

    print()

    print('Average characters per review: ')
    for rev, score in sorted_avg_chars_per_rev[:topk]:
        print(f'{rev}: {score}')
