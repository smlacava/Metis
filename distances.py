from abc import ABC, abstractmethod
from scipy.spatial.distance import mahalanobis
import numpy as np

class distance(ABC):
  @abstractmethod
  def compute_distance(self, v1, v2):
    """
    The compute_distance method computes the distance between two arrays, with respect to the used distance type.

    :param v1: it is the first array or list of values
    :param v2: it is the second array or list of values

    :return: the distance value between the two arrays
    """
    pass


  def set_parameters(self, data):
    """
    The set_parameters method allows to set the inverse covariance matrix as object attribute (used for computing the
    Mahalanobis distance).

    :param data: it is the 2D (samples*values) input matrix
    """
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
    """
    The _inv_cov_managing methos is used to reiterate the inverse covariance matrix in case of singular input matrix,
    by adding a very small amount of randomness to the input matrix (FOR INTERNAL USE ONLY).

    :param data: it is the 2D (samples*values) input matrix
    """
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