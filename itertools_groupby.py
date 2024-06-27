from itertools import groupby

# things = [("animal", "bear"), ("animal", "duck"), ("plant", "cactus"), ("vehicle", "speed boat"), ("vehicle", "school bus")]
#
# for key, group in groupby(things, lambda x: x[0]):
#     for thing in group:
#         print("A %s is a %s." % (thing[1], key))
#     print("")

things = [("animal", 2), ("animal", 1), ("plant", 1), ("vehicle", 1),
          ("vehicle", 1)]



from functools import reduce

def group_by(things):
    def extract_values(things):
        for key, group in groupby(things, get_key()):
            # print(key, group)
            # print(f'Group: {key} - {sum(group)}')
            for g in group:
                yield g[1]
            # for thing in group:
            #     print("A %s is a %s." % (thing[1], key))
            # print("")

    yield sum(extract_values(things))

# for x in group_by(things):
#     print(x)


yokes = ['strawberry', 'raspberry', 'blueberry', 'blackberry', 'banana']


def groupvals(inputs):
    def get_key(i):
        return lambda x: x[0]

    groups = {}
    for key, group in groupby(inputs, get_key(1)):
        if key not in groups.keys():
            groups[key] = []
        # print(f'Group: {key} - {sum(group)}')
        for g in group:
            groups[key].append(g)
        #     yield g[1]x
    return groups


print(groupvals(yokes))


"""
>>> d = { 'a': 1, 'b': 2, 'c': 3 }
>>> list(d.items())
[('a', 1), ('c', 3), ('b', 2)]

----------------------------------------------------
https://beam.apache.org/documentation/transforms/python/aggregation/groupby/
def groupby_expr(test=None):
  with beam.Pipeline() as p:
    # [START groupby_expr]
    grouped = (
        p
        | beam.Create(
            ['strawberry', 'raspberry', 'blueberry', 'blackberry', 'banana'])
        | beam.GroupBy(lambda s: s[0])
        | beam.Map(print))
    
"""