import torch
import numpy as np
from kmeans_pytorch import kmeans
import pickle

# data
num_clusters = 25


with open('./data/ptb/ptb300fasttext.pkl', 'rb') as f:
  data = pickle.load(f)

vals = np.array(list(data.values()), dtype=float)
# print(vals.shape)
vals = torch.from_numpy(vals)
# kmeans
cluster_ids_x, cluster_centers = kmeans(
    X=vals, num_clusters=num_clusters, distance='cosine', device=torch.device('cuda:0')
)
np.savetxt('fasttext-ptb-kmeans-25-centroids-300.txt', cluster_centers.numpy())
#torch.save(cluster_centers.data, 'glovevico-kmeans-20-centroids.txt')
