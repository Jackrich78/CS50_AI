# An Image recognition test using TensorFlow and OpenCV
- An exercise from the CS50 intro to AI with Python course. Document contains tterations on exercise 5 - Traffic - to learn TensorFlow capabilities. 
- Uses the gtsrb dataset as image input

# Observations
- Dropout layer greatly reduces accuracy. It also varies depending on where it sits in the network. Before the hidden dense layer seems to have better results than after.
- Increasing filters and kernel size greatly increases accuracy up to a point but tapers off at tested settings. Time increases at the same rate as # filters.
- Increasing hidden nodes increases accuracy.
- Different optimizers product different results, possible Adamax performs best out of those tested.
- A second convolutional layer with different # of filters and kernel size increases accuracy and reduces loss without too much additional time.

### future
- Other categorical functions AdaGrad
- change learning rate

---
# V4.2 change model type to Adamax
- change neurons to 128
- change optimiser to Adamax
- best performing so far with almost 99% accuracy and 5.6% loss
### Results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 23s 43ms/step - accuracy: 0.3354 - loss: 6.8460 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.8513 - loss: 0.5778
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.9230 - loss: 0.2917
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.9551 - loss: 0.1780
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.9680 - loss: 0.1211
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.9761 - loss: 0.0939
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 23s 46ms/step - accuracy: 0.9789 - loss: 0.0812
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 30s 61ms/step - accuracy: 0.9823 - loss: 0.0688
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 33s 66ms/step - accuracy: 0.9869 - loss: 0.0509  
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 30s 60ms/step - accuracy: 0.9894 - loss: 0.0437
333/333 - 3s - 9ms/step - accuracy: 0.9886 - loss: 0.0563

# V4.1 reduce dropout to 0.3
- with previous settings model actually performed slightly worse
### Results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 26s 48ms/step - accuracy: 0.0963 - loss: 5.2039 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 30s 60ms/step - accuracy: 0.5338 - loss: 1.5653
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 26s 51ms/step - accuracy: 0.7785 - loss: 0.7408 
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 24s 49ms/step - accuracy: 0.8876 - loss: 0.3948
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 24s 48ms/step - accuracy: 0.9205 - loss: 0.3067
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.9352 - loss: 0.2379 
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 19s 38ms/step - accuracy: 0.9373 - loss: 0.2128
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 19s 38ms/step - accuracy: 0.9447 - loss: 0.2175
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 20s 40ms/step - accuracy: 0.9442 - loss: 0.2200
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 20s 38ms/step - accuracy: 0.9468 - loss: 0.2080  
333/333 - 2s - 7ms/step - accuracy: 0.9782 - loss: 0.1259

# V4.0 2 convolutional layers, adjust neruones, filters, kernels
- 1st convolutional:
- filters = 64
- kernel = 5x5
- 2nd convolutional:
- filters = 128
- kernel = 3x3
- neurons = 64
### Results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 24s 44ms/step - accuracy: 0.0580 - loss: 5.4653 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 45ms/step - accuracy: 0.4173 - loss: 2.1446
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 45ms/step - accuracy: 0.7870 - loss: 0.6977
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.8899 - loss: 0.3745
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.9165 - loss: 0.2926
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.9331 - loss: 0.2624
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.9379 - loss: 0.2366
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 44ms/step - accuracy: 0.9468 - loss: 0.1961  
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 23s 46ms/step - accuracy: 0.9506 - loss: 0.2023
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 24s 48ms/step - accuracy: 0.9470 - loss: 0.2022
333/333 - 3s - 8ms/step - accuracy: 0.9793 - loss: 0.0988

---
# V3.2 increaase filters and reduce kernel back to 3,3
- filters=128,
- kernel_size=(3,3),
- Higher accuracy but bigger losses too, also took twice as long.
### Result
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 38s 74ms/step - accuracy: 0.4126 - loss: 14.1079 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 40s 80ms/step - accuracy: 0.7907 - loss: 0.7916  
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 39s 78ms/step - accuracy: 0.8295 - loss: 0.6385  
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 39s 78ms/step - accuracy: 0.8696 - loss: 0.4947
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 41s 82ms/step - accuracy: 0.8825 - loss: 0.4615 
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 42s 84ms/step - accuracy: 0.8918 - loss: 0.4436  
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 42s 84ms/step - accuracy: 0.8948 - loss: 0.4286  
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 40s 79ms/step - accuracy: 0.9117 - loss: 0.3496  
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 40s 81ms/step - accuracy: 0.9114 - loss: 0.3870 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 40s 79ms/step - accuracy: 0.9234 - loss: 0.3203 
333/333 - 3s - 10ms/step - accuracy: 0.9413 - loss: 0.3599

# V3.1 change padding
- paddin='same'
- very similar overall but may increase accuracy and reduce losses
### Results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 19s 35ms/step - accuracy: 0.3102 - loss: 7.7333     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 18s 36ms/step - accuracy: 0.6732 - loss: 1.2079
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 35ms/step - accuracy: 0.7582 - loss: 0.9037
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.7835 - loss: 0.8019
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 35ms/step - accuracy: 0.7947 - loss: 0.7865
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 16s 32ms/step - accuracy: 0.8266 - loss: 0.6454
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.8105 - loss: 0.7141
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.8290 - loss: 0.6620
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.8438 - loss: 0.5700
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 18s 36ms/step - accuracy: 0.8483 - loss: 0.5775
333/333 - 1s - 4ms/step - accuracy: 0.9192 - loss: 0.3299

# V3.0 Double Neruons in hidden layer
- neurons = 128
- adam
- doesn't look to be much better. Maybe 128 is overkill?
### Results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 22s 41ms/step - accuracy: 0.2897 - loss: 8.0038 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 43ms/step - accuracy: 0.6710 - loss: 1.2136
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 41ms/step - accuracy: 0.7467 - loss: 0.9760
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 41ms/step - accuracy: 0.7795 - loss: 0.8303
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 20s 41ms/step - accuracy: 0.7987 - loss: 0.7304
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 41ms/step - accuracy: 0.8073 - loss: 0.6925
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 20s 40ms/step - accuracy: 0.8132 - loss: 0.6991
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.8322 - loss: 0.6323
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 20s 40ms/step - accuracy: 0.8289 - loss: 0.6614
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 21s 42ms/step - accuracy: 0.8409 - loss: 0.6376
333/333 - 2s - 6ms/step - accuracy: 0.9154 - loss: 0.3296

---
# V2.2 iteration
- add a dropout layer
- back to adam for optimizer

### results Adam
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 26ms/step - accuracy: 0.0491 - loss: 7.1568     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.0550 - loss: 3.6092    
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.0533 - loss: 3.5541
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 27ms/step - accuracy: 0.0563 - loss: 3.5267
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.0565 - loss: 3.5092    
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.0553 - loss: 3.5068
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.1867 - loss: 3.1074
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.3642 - loss: 2.1754
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 15s 30ms/step - accuracy: 0.4101 - loss: 1.9384
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 28ms/step - accuracy: 0.5238 - loss: 1.5403
333/333 - 2s - 6ms/step - accuracy: 0.6209 - loss: 1.1883

# V2.1 Experiment with different optimisers
### Adamax
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 25ms/step - accuracy: 0.1907 - loss: 10.1733  
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 25ms/step - accuracy: 0.7938 - loss: 0.8252
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 25ms/step - accuracy: 0.9241 - loss: 0.3283
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9563 - loss: 0.1841
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 23ms/step - accuracy: 0.9746 - loss: 0.1087
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9841 - loss: 0.0757
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9864 - loss: 0.0661
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 24ms/step - accuracy: 0.9919 - loss: 0.0398
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9909 - loss: 0.0438
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9923 - loss: 0.0366
333/333 - 1s - 4ms/step - accuracy: 0.9660 - loss: 0.1895

### RMSprop
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 24ms/step - accuracy: 0.4357 - loss: 14.4112 
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 24ms/step - accuracy: 0.8502 - loss: 0.7412
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 27ms/step - accuracy: 0.9099 - loss: 0.4960
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 25ms/step - accuracy: 0.9356 - loss: 0.4728
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9453 - loss: 0.3414
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 28ms/step - accuracy: 0.9509 - loss: 0.3862
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9631 - loss: 0.3164
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9688 - loss: 0.2958
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 27ms/step - accuracy: 0.9661 - loss: 0.3696
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 27ms/step - accuracy: 0.9760 - loss: 0.2469
333/333 - 2s - 5ms/step - accuracy: 0.9379 - loss: 0.9480

# V2.0 Iteration
- filters increased to 64
- kernel size increased to 5x5

### results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 23ms/step - accuracy: 0.3910 - loss: 7.5652    
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 11s 22ms/step - accuracy: 0.8472 - loss: 0.5823
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 11s 22ms/step - accuracy: 0.9039 - loss: 0.3594
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9202 - loss: 0.3008
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 24ms/step - accuracy: 0.9374 - loss: 0.2333
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 15s 30ms/step - accuracy: 0.9277 - loss: 0.2641
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 25ms/step - accuracy: 0.9487 - loss: 0.2089
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9508 - loss: 0.1943
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9641 - loss: 0.1392
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 12s 24ms/step - accuracy: 0.9296 - loss: 0.3216
333/333 - 2s - 5ms/step - accuracy: 0.9115 - loss: 0.5774
---

# V1.0 model iteration
- Accepts an input using defined IMG_WIDTH, IMG_HEIGHT, 3
- Uses convolutional layers to extract features
- filters = 32
- Reduces complexity using a 2x2 max pooling layer
- Flattens the output to feed to dense layers
- Has 64 hidden neurons
- Classifies the input into a num_category
- Compile with Adam to try iterative weights
- no dropout layer 

### results
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 11ms/step - accuracy: 0.0510 - loss: 11.2970     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.0608 - loss: 3.6090 
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.0566 - loss: 3.5546 
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.0574 - loss: 3.5290 
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.0556 - loss: 3.5022 
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.0550 - loss: 3.5031     
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.0590 - loss: 3.4972 
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.0564 - loss: 3.5003     
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.0576 - loss: 3.5061  
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.0582 - loss: 3.4993     
333/333 - 1s - 4ms/step - accuracy: 0.0541 - loss: 3.5010

