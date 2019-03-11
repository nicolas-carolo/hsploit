class ResultSet:
    list = []

    def __init__(self, queryset):
        l = list()
        for instance in queryset:
            l.append(instance)
        self.list = l


def new_result_set(queryset):
    return ResultSet(queryset)


def print_instances(result_set):
    for instance in result_set.list:
        print(instance.description)


def void_result_set():
    return ResultSet()


def exclude(result_set, description):
    print(result_set.list.__len__())
    for instance in result_set.list:
        if instance.description == description:
            result_set.list = result_set.list.remove(instance)
    return result_set

