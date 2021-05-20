from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _


class SafePaginator(Paginator):

    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                return self.num_pages
        return number

    def get_page(self, number):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            number = self.validate_number(number)
            if number > self.num_pages:
                number = self.num_pages
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return self.page(number)
