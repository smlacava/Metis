from abc import ABC, abstractmethod
from scipy.spatial.distance import mahalanobis
import numpy as np

class distance(ABC):
  @abstractmethod
  def compute_distance(self, v1, v2):
    pass

  def set_parameters(self, data):
    pass


class manhattan_distance(distance):
  def compute_distance(self, v1, v2):
    return sum(abs(v1-v2))


class euclidean_distance(distance):
  def compute_distance(self, v1, v2):
    return np.linalg.norm(v1-v2)


class minkowski_distance(distance):
  def compute_distance(self, v1, v2):
    p = len(v1)
    return sum((v1-v2)**p)**(1/p)


class mahalanobis_distance(distance):
  def compute_distance(self, v1, v2):
    return mahalanobis(v1, v2, self.inv_cov)

  def _inv_cov_managing(self, data):
    try:
      self.inv_cov = np.linalg.inv(np.cov(data+np.absolute(data).min()*0.00001*np.random.rand(np.shape(data)[0], np.shape(data)[1])))
    except:
      self._inv_cov_managing(data)


  def set_parameters(self, data):
    aux_data = np.transpose(data)
    try:
      self.inv_cov = np.linalg.inv(np.cov(aux_data))
    except:
      self._inv_cov_managing(aux_data)