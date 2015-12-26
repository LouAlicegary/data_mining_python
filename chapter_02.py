from chapter_02_my_recommender import MyRecommender
from chapter_02_recommender import Recommender
from chapter_02_data_loader import DataLoader



users = {
    "Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
    "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
    "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
    "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
    "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
    "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
    "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
}



"""
Given product id number return product name 
"""
def convertProductID2name(bookData, id):
    if id in bookData['productid2name']:
        return bookData['productid2name'][id]
    else:
        return id





""" ========================== ACTUALLY RUNNING CODE HERE =============================== """





print "\n\n"


my_rec = MyRecommender(users)

# %.3f formats the float to 3 decimal places
print "The manhattan distance between Hailey and Veronica should be 2.0 => %.3f" % my_rec.manhattan(users['Hailey'], users['Veronica'])
print "The manhattan distance between Hailey and Jordyn should be 7.5 => %.3f" % my_rec.manhattan(users['Hailey'], users['Jordyn']) 

print "The computed Manhattan distances for Hailey are: %s" % my_rec.computeNearestNeighbor("Hailey", users)


print "\n\n"


print "Recommended artists for Hailey are: %s" % my_rec.recommend('Hailey', users) 
print "Recommended artists for Chan are: %s" % my_rec.recommend('Chan', users)
print "Recommended artists for Sam are: %s" % my_rec.recommend('Sam', users)
print "Recommended artists for Angelica are: %s" % my_rec.recommend('Angelica', users)


print "\n\n"


print "Pearson coefficient between Angelica and Bill is %.3f" % my_rec.pearson(users['Angelica'], users['Bill']) 
print "Pearson coefficient between Angelica and Hailey is %.3f" % my_rec.pearson(users['Angelica'], users['Hailey']) 
print "Pearson coefficient between Angelica and Jordyn is %.3f" % my_rec.pearson(users['Angelica'], users['Jordyn']) 


print "\n\n"


print "Cosine similarity between Angelica and Veronica is %.3f" % my_rec.cosine_similarity(users['Angelica'], users['Veronica'])


print "\n\n"


r = Recommender(users)

print "Jordyn's recommendations: %s" % r.recommend('Jordyn')
print "Hailey's recommendations: %s" % r.recommend('Hailey')


print "\n\n"


print "Loading CSV book data."

dl = DataLoader();
bookData = dl.loadBookDB();


print "\n\n"


print "Book Recommendations:"

book_rec = Recommender(bookData['data'])

recommendations = book_rec.recommend('171118')
recommendations = [(convertProductID2name(bookData, k), v) for (k, v) in recommendations]

for recommendation in recommendations:
  print("%s\t%.1f" % (recommendation[0], recommendation[1]))


print "\n\n"


print "Ratings for " + bookData['userid2name']['171118']

ratings = book_rec.userRatings('171118', 5)
ratings = [(convertProductID2name(bookData, k), v) for (k, v) in ratings]

for rating in ratings:
    print("%s\t%.1f" % (rating[0], rating[1]))


print "\n\n"


