import random
import json

CAMPOS = 6
TAM_POB = 65
TAM_TRAINING = 52
TAM_TESTING = 13

vgood = []
good = []
acc = []
unacc = []

with open("new_cars.data") as file:
    idx = 0
    for line in file:
        list = line.rstrip().split(',')
        list.append(idx)
        if list[-2] == "vgood":
            vgood.append(list)
        if list[-2] == "good":
            good.append(list)
        if list[-2] == "acc":
            acc.append(list)
        if list[-2] == "unacc":
            unacc.append(list)
        idx += 1

# dividir el conjunto en training y testing:

# shuffle
random.shuffle(vgood)
random.shuffle(good)
random.shuffle(acc)
random.shuffle(unacc)

vgood_training = []
vgood_testing = []
good_training = []
good_testing = []
acc_training = []
acc_testing = []
unacc_training = []
unacc_testing = []

for i in range(0, TAM_TRAINING):
    vgood_training.append(vgood[i])
    good_training.append(good[i])
    acc_training.append(acc[i])
    unacc_training.append(unacc[i])

for i in range(TAM_TRAINING, TAM_POB):
    vgood_testing.append(vgood[i])
    good_testing.append(good[i])
    acc_training.append(acc[i])
    unacc_training.append(unacc[i])


# armar clasificador:

vgood_prob = [{} for i in range(0, CAMPOS)]
good_prob  = [{} for i in range(0, CAMPOS)]
acc_prob   = [{} for i in range(0, CAMPOS)]
unacc_prob = [{} for i in range(0, CAMPOS)]

vgood_prob = [
    {"vhigh": 1, "high": 1, "med": 1, "low": 1},
    {"vhigh": 1,"high": 1,"med": 1,"low": 1},
    {"2": 1,"3": 1,"4": 1,"5more": 1},
    {"2": 1,"4": 1,"more": 1},
    {"small": 1,"med": 1,"big": 1},
    {"low": 1,"med": 1,"high": 1}
]
good_prob   = [
    {"vhigh": 1, "high": 1, "med": 1, "low": 1},
    {"vhigh": 1,"high": 1,"med": 1,"low": 1},
    {"2": 1,"3": 1,"4": 1,"5more": 1},
    {"2": 1,"4": 1,"more": 1},
    {"small": 1,"med": 1,"big": 1},
    {"low": 1,"med": 1,"high": 1}
]
acc_prob    = [
    {"vhigh": 1, "high": 1, "med": 1, "low": 1},
    {"vhigh": 1,"high": 1,"med": 1,"low": 1},
    {"2": 1,"3": 1,"4": 1,"5more": 1},
    {"2": 1,"4": 1,"more": 1},
    {"small": 1,"med": 1,"big": 1},
    {"low": 1,"med": 1,"high": 1}
]
unacc_prob  = [
    {"vhigh": 1, "high": 1, "med": 1, "low": 1},
    {"vhigh": 1,"high": 1,"med": 1,"low": 1},
    {"2": 1,"3": 1,"4": 1,"5more": 1},
    {"2": 1,"4": 1,"more": 1},
    {"small": 1,"med": 1,"big": 1},
    {"low": 1,"med": 1,"high": 1}
]

for record in vgood_training:
    for i in range(0, CAMPOS):
        vgood_prob[i][record[i]] += 1

for record in good_training:
    for i in range(0, CAMPOS):
        good_prob[i][record[i]] += 1

for record in acc_training:
    for i in range(0, CAMPOS):
        acc_prob[i][record[i]] += 1

for record in unacc_training:
    for i in range(0, CAMPOS):
        unacc_prob[i][record[i]] += 1

# normalizar:

for i in range(0, CAMPOS):
    for key in vgood_prob[i]:
        vgood_prob[i][key] /= TAM_TRAINING + len(vgood_prob[i])
    for key in good_prob[i]:
        good_prob[i][key] /= TAM_TRAINING + len(vgood_prob[i])
    for key in acc_prob[i]:
        acc_prob[i][key] /= TAM_TRAINING + len(vgood_prob[i])
    for key in unacc_prob[i]:
        unacc_prob[i][key] /= TAM_TRAINING + len(vgood_prob[i])

# print(json.dumps(vgood_prob, indent=4))

# print(json.dumps(good_prob, indent=4))

# print(json.dumps(acc_prob, indent=4))

# print(json.dumps(unacc_prob, indent=4))

# clasificar y testear:

precision = 0

for record in vgood_testing:
    probs = [1,1,1,1]
    for i in range(0,CAMPOS):
        probs[0] *= vgood_prob[i][record[i]]
        probs[1] *= good_prob[i][record[i]]
        probs[2] *= acc_prob[i][record[i]]
        probs[3] *= unacc_prob[i][record[i]]

    if probs.index(max(probs)) == 0:
        precision += 1

for record in good_testing:
    probs = [1,1,1,1]
    for i in range(0,CAMPOS):
        probs[0] *= vgood_prob[i][record[i]]
        probs[1] *= good_prob[i][record[i]]
        probs[2] *= acc_prob[i][record[i]]
        probs[3] *= unacc_prob[i][record[i]]

    if probs.index(max(probs)) == 1:
        precision += 1

for record in good_testing:
    probs = [1,1,1,1]
    for i in range(0,CAMPOS):
        probs[0] *= vgood_prob[i][record[i]]
        probs[1] *= good_prob[i][record[i]]
        probs[2] *= acc_prob[i][record[i]]
        probs[3] *= unacc_prob[i][record[i]]

    if probs.index(max(probs)) == 2:
        precision += 1

for record in good_testing:
    probs = [1,1,1,1]
    for i in range(0,CAMPOS):
        probs[0] *= vgood_prob[i][record[i]]
        probs[1] *= good_prob[i][record[i]]
        probs[2] *= acc_prob[i][record[i]]
        probs[3] *= unacc_prob[i][record[i]]

    if probs.index(max(probs)) == 3:
        precision += 1

precision /= TAM_TESTING * 4

print("Precision: {0:.0%}".format(precision))
