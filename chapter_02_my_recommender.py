from math import sqrt 


class MyRecommender:


    def __init__(self, userData, metric='minkowski'):

        # Determines which metric of calculating distance to use
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        elif self.metric == 'minkowski':
            self.fn = self.minkowski
        elif self.metric == 'manhattan':
            self.fn = self.manhattan
        elif self.metric == 'cosine_similarity':
            self.fn = self.cosine_similarity

        self.data = {}
        if type(userData).__name__ == 'dict':
            self.data = userData
        

    # Give list of recommendations
    def recommend(self, username):
     
      users = self.data

      recommendations = []

      # grab username's ratings
      userRatings = users[username]

      # find nearest neighbor and grab all their ratings
      nearest = self.computeNearestNeighbor(username, users)[0][1]
      neighborRatings = users[nearest]

      # now find bands neighbor rated that user didn't and append to rec list
      for artist in neighborRatings:
        if not artist in userRatings:
          recommendations.append((artist, neighborRatings[artist]))
     
      # (author note: using the fn sorted for variety - sort is more efficient)
      # key is an anonymous (lambda) function whose name (artistTuple) 
      # represents each object in the collection being sorted
      return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)


    # Creates a sorted list of users based on their distance to username

    def computeNearestNeighbor(self, username, users):

      distances = []

      for user in users:
        if user != username:
          distance = self.fn(users[user], users[username], 2)
          distances.append((distance, user))
          
          # sort based on distance -- closest first
          distances.sort()
     
      return distances



    # Computes the Manhattan distance. Both rating1 and rating2 are dictionaries of the form
    # {'The Strokes': 3.0, 'Slightly Stoopid': 2.5 ...}

    def manhattan(self, rating1, rating2):

      distance = 0
     
      for key in rating1:
        if key in rating2:
          distance += abs(rating1[key] - rating2[key])
     
      return distance



    # Computes the Minkowski distance. Both rating1 and rating2 are dictionaries of the form
    # {'The Strokes': 3.0, 'Slightly Stoopid': 2.5 ...}
    # r = 1 is Manhattan distance; r = 2 is Euclidian distance; r = oo is Supremum distance

    def minkowski(self, rating1, rating2, r):

      distance = 0
     
      for key in rating1:
        if key in rating2:
          distance += pow(abs(rating1[key] - rating2[key]), r)
     
      return pow(distance, 1/r)



    def pearson(self, rating1, rating2):
      
      sum_xi_yi = 0
      sum_xi    = 0
      sum_yi    = 0
      sum_x_2   = 0
      sum_y_2   = 0
      n         = 0
      
      for key in rating1:
        if key in rating2:
          n         += 1
          sum_xi    += rating1[key]
          sum_yi    += rating2[key]
          sum_x_2   += (rating1[key] ** 2)
          sum_y_2   += (rating2[key] ** 2)
          sum_xi_yi += (rating1[key] * rating2[key])

      if n == 0:
        return 0
      else:
        covar     = sum_xi_yi - (sum_xi * sum_yi / n)
        std_dev_x = sqrt(sum_x_2 - ((sum_xi ** 2) / n))
        std_dev_y = sqrt(sum_y_2 - ((sum_yi ** 2) / n))
        return covar / (std_dev_x * std_dev_y)



    def cosine_similarity(self, rating1, rating2):
      
      dot_product = 0
      sum_x_2   = 0
      sum_y_2   = 0

      for key in rating1:
        sum_x_2   += (rating1[key] ** 2)
        if key in rating2:
          dot_product += (rating1[key] * rating2[key]) 

      for key in rating2:
        sum_y_2   += (rating2[key] ** 2)
     
      x_vector_length = sqrt(sum_x_2)
      y_vector_length = sqrt(sum_y_2)

      return dot_product / (x_vector_length * y_vector_length)




