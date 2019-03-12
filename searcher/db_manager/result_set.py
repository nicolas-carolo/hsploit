def queryset2list(queryset):
    list = []
    for instance in queryset:
        list.append(instance)
    return list


def print_instances(result_set):
    for instance in result_set:
        print(instance.description)


def void_result_set():
    list = []
    return list


def result_set_len(result_set):
    try:
        return len(result_set)
    except TypeError:
        return 0
