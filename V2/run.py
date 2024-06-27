from transform import Transform, GroupBy, Temp
from pipeline import Pipeline
from transform_impl import Cube, Double, Filter, WriteToFile, CreateGroups


t = Temp()
c = Cube()
g = GroupBy()
# c >> Double() >> Filter() >> WriteToFile()

c >> CreateGroups() >> GroupBy()
pipe = Pipeline(c)

pipe.run([1,2])
"""
expected
double1_1718138638.txt
output4_1718138638.txt
Processing element: 4
output1_1718138638.txt
Processing element: 1
double8_1718138638.txt
output32_1718138638.txt
Processing element: 32
output8_1718138638.txt
Processing element: 8
"""

"""
actual
double1_1718138930.txt
output4_1718138930.txt
Processing element: 4
output1_1718138930.txt
Processing element: 1
double8_1718138930.txt
output32_1718138930.txt
Processing element: 32
output8_1718138930.txt
Processing element: 8
"""
