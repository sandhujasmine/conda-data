# conda-data

Anaconda server data client

```py

import conda_data

conda_data.authenticate('username', 'password')

data = conda_data.pull('sean/test_data')

print(data)

```