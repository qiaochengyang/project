import pickle
from multiprocessing import Queue
serverSendQueue=Queue()
serverSendQueue.put(1)
serverSendQueue.put(2)
serverSendQueue.put(3)
print (serverSendQueue)
with open('data_object.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(serverSendQueue, f)
    f.close()
with open('data_object.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    serverSendQueue = pickle.load(f)
print (serverSendQueue)