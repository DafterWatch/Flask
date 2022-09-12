from operator import mod
import pickle
import sklearn
import numpy

# if __name__ == "__main__":
#     with open("model.pkl", "rb") as f:
#         model = pickle.load(f)
#         res = numpy.array([[6,180,77,8,1,0,0,0]])
#         print(res)
#         print(model.predict(res))

def predecir(array):
    print(array)
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
        res = numpy.array([array])
        res = model.predict(res)
    return res