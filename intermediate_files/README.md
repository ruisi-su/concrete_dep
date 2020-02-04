# Contains files to compute noun probability according to role labels and dependency labels

Currently the combined_prob.json is *NOT CORRECT*. However, this file should contain each noun in terms of dependency labels (i.e., 'nsubj', 'dobj', 'pobj', etc.). This number is computed from the proabilities of each word given the P(n=noun|role=r)P(role=r|dep=d).

*dep_data.json* and *role_data.json* contain counts from the train.json dataset
