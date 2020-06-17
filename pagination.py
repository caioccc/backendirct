from math import ceil, floor


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.currentPage = page
        self.pageSize = per_page
        self.totalCount = total_count

    def pages(self):
        return int(ceil(self.totalCount / float(self.pageSize)))

    def has_prev(self):
        return self.currentPage > 1

    def has_next(self):
        return self.currentPage < self.pages()

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages() + 1):
            if num <= left_edge or (num > self.currentPage - left_current - 1 and num < self.currentPage + right_current) or num > self.pages() - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
