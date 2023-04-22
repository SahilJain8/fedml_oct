
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from .forms import UploadImagesForm

def upload_images(request):
    if request.method == 'POST':
        form = UploadImagesForm(request.POST, request.FILES)
        if form.is_valid():
            # get the uploaded images for each class
            # assume we have 4 classes (class1, class2, class3, class4)
            # each class can have multiple images
            class_names = ['class1', 'class2', 'class3', 'class4']
            images_list = []
            for class_name in class_names:
                images = request.FILES.getlist(f'{class_name}_images')
                # resize all images to a fixed size of 128x128
                images_resized = [np.array(Image.open(img).resize((128, 128))) for img in images]
                images_list.append(images_resized)
            
            # combine all the images for each class into a single list
            # and convert them into numpy arrays
            X = np.concatenate([np.array(images_list[i]) for i in range(len(images_list))], axis=0)
            
            # create the labels for each class
            y = np.concatenate([np.full(len(images_list[i]), i) for i in range(len(images_list))], axis=0)
            
            # convert the labels into one-hot encoded format
            y = to_categorical(y, num_classes=4)
            
            # normalize the input images
            X = X.astype('float32') / 255.0
            
            # define the model architecture
            model = Sequential()
            model.add(Conv2D(32, (3, 3), activation='relu', input_shape=X[0].shape))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(4, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
         
            # train the model
            model.fit(X, y, epochs=10, batch_size=32, verbose=1)
            
            return HttpResponse('Model trained successfully!')
    else:
        form = UploadImagesForm()
    
    context = {'form': form}
    return render(request, 'upload.html', context)



