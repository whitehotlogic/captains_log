import django.core.paginator


class Paginator(django.core.paginator.Paginator):
    def _check_object_list_is_ordered(self):
        pass


django.core.paginator.Paginator = Paginator
