import pandas as pd



abc = pd.DataFrame({'A': [11, 21, 31],
                   'B': [12, 22, 32],
                   'C': [13, 23, 33]})

print(abc)

abc = abc.rename(index={0:"ha",1:"ho",2:"hu"})

print(abc)