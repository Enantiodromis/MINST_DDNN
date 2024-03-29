from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten, Dropout, Activation, BatchNormalization, AveragePooling2D
from keras.models import Model
import numpy as np
from tensorflow.keras.callbacks import ReduceLROnPlateau
from keras.models import load_model
from keras.utils import plot_model
import matplotlib.pyplot as plt

# Loading the MNIST datasets
(x_train, labels_train), (x_test, labels_test) = mnist.load_data()

# Converting to floating point
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = x_train/255.0
x_test = x_test/255.0

# A one hot encoding
y_train = to_categorical(labels_train, 10) 
y_test = to_categorical(labels_test, 10)

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1) 
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

# Initialiasing the the network
LeNet5_var = Sequential()
# C1 & C2
LeNet5_var.add(Conv2D(filters= 32,kernel_size = (5,5),strides=(1,1), padding='same',activation='relu',input_shape=(28,28,1)))
LeNet5_var.add(Conv2D(32,(5,5),strides=(1,1), use_bias=False))
# B1
LeNet5_var.add(BatchNormalization())
LeNet5_var.add(Activation('relu'))
# MXPL1
LeNet5_var.add(MaxPooling2D(pool_size=(2,2),strides=(2,2), padding='same'))
LeNet5_var.add(Dropout(0.25))
# C3 & C4
LeNet5_var.add(Conv2D(filters=64,kernel_size = (5,5),strides=(1,1), padding='same',activation='relu'))
LeNet5_var.add(Conv2D(64,(3,3),strides=(1,1), use_bias=False))
# B2
LeNet5_var.add(BatchNormalization())
LeNet5_var.add(Activation('relu'))
# MXPL2
LeNet5_var.add(MaxPooling2D(pool_size=(2,2),strides=(2,2), padding='same'))
LeNet5_var.add(Dropout(0.25))
LeNet5_var.add(Flatten())
# FC1
LeNet5_var.add(Dense(units=256,activation='relu'))
# B3
LeNet5_var.add(BatchNormalization())
LeNet5_var.add(Activation('relu'))
# FC2
LeNet5_var.add(Dense(units=120,activation='relu'))
# B4
LeNet5_var.add(BatchNormalization())
LeNet5_var.add(Activation('relu'))
# FC3
LeNet5_var.add(Dense(units=84,activation='relu'))
# B5
LeNet5_var.add(BatchNormalization())
LeNet5_var.add(Activation('relu'))
LeNet5_var.add(Dropout(0.25))
# FC4
LeNet5_var.add(Dense(units=10,activation='softmax'))

LeNet5_var.summary()
plot_model(LeNet5_var, to_file='network_structure.png', show_shapes=True)

# NETWORK TRAINING
variable_learning_rate = ReduceLROnPlateau(monitor='loss', factor = 0.2, patience = 2)
LeNet5_var.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
history = LeNet5_var.fit(x_train,y_train, validation_data=(x_test,y_test), epochs=30, batch_size=64, callbacks = [variable_learning_rate])
# SAVING THE MODEL
LeNet5_var.save("LeNet_30_64_V2.h5")

plt.figure()
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

# LOADING MODEL
LeNet5_var = load_model("LeNet_30_64_V2.h5")

# TESTING
outputs=LeNet5_var.predict(x_test)
labels_predicted=np.argmax(outputs, axis=1) 
misclassified=sum(labels_predicted!=labels_test) 
print('Percentage misclassified = ',100*misclassified/labels_test.size)

score = LeNet5_var.evaluate(x_test, y_test) 

plt.figure(figsize=(8, 2))

for i in range(0,8):    
    ax=plt.subplot(2,8,i+1)    
    plt.imshow(x_test[i,:].reshape(28,28), cmap=plt.get_cmap('gray_r'))    
    plt.title(labels_test[i])    
    ax.get_xaxis().set_visible(False)    
    ax.get_yaxis().set_visible(False)
plt.show()

for i in range(0,8):      
    output = LeNet5_var.predict(x_test[i,:].reshape(1, 28,28,1)) #if CNN    
    output=output[0,0:]    
    plt.subplot(2,8,8+i+1)    
    plt.bar(np.arange(10.),output)    
    plt.title(np.argmax(output))
plt.show()