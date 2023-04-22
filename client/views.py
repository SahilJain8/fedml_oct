
from PIL import Image
import numpy as np
from django.shortcuts import render
from .forms import UploadImagesForm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.utils import to_categorical

def upload_images(request):
    if request.method == 'POST':
        form = UploadImagesForm(request.POST, request.FILES)
        if form.is_valid():
            # get the uploaded images for each class
            # assume we have 4 classes (class1, class2, class3, class4)
            # each class can have multiple images
            class1_images = request.FILES.getlist('class1_images')
            class2_images = request.FILES.getlist('class2_images')
            class3_images = request.FILES.getlist('class3_images')
            class4_images = request.FILES.getlist('class4_images')
            
            # combine all the images for each class into a single list
            # and convert them into numpy arrays
            class1_images_np = np.array([np.array(Image.open(img)) for img in class1_images])
            class2_images_np = np.array([np.array(Image.open(img)) for img in class2_images])
            class3_images_np = np.array([np.array(Image.open(img)) for img in class3_images])
            class4_images_np = np.array([np.array(Image.open(img)) for img in class4_images])
            
            # concatenate all the images into a single numpy array
            X = np.concatenate([class1_images_np, class2_images_np, class3_images_np, class4_images_np], axis=0)
            
            # create the labels for each class
            y_class1 = np.zeros(len(class1_images_np))
            y_class2 = np.ones(len(class2_images_np))
            y_class3 = np.full(len(class3_images_np), 2)
            y_class4 = np.full(len(class4_images_np), 3)
            
            # concatenate all the labels into a single numpy array
            y = np.concatenate([y_class1, y_class2, y_class3, y_class4], axis=0)
            
            # convert the labels into one-hot encoded format
            y = to_categorical(y, num_classes=4)
            
            # normalize the input images
            X = X.astype('float32') / 255.0
            
          
            model = Sequential()
            model.add(Conv2D(32, (3, 3), activation='relu', input_shape=X[0].shape))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(4, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
         
            model.fit(X, y, epochs=10, batch_size=32, verbose=1)
            
  
            return render(request, 'success.html')
    else:
        form = UploadImagesForm()
    return render(request, 'upload.html', {'form': form})



