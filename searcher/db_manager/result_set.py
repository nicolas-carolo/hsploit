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


def exclude(result_set, description):
    try:
        for instance in result_set:
            if instance.description == description:
                to_remove = instance
        result_set.remove(to_remove)
    except UnboundLocalError:
        pass
    return result_set
