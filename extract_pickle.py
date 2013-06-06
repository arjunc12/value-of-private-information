import pickle

time = "2013-06-05-17-38-05"
offer_type = "max"
f = open("data/run_" + time + "_" + offer_type, "r")
(prediction, payout, individuals, divergences, costs) = pickle.load(f)
print prediction
print payout
print individuals
print divergences
print costs

f = open("data/" + offer_type + "_divergences", "w")
for i in divergences:
    f.write(str(i) + "\n")

f = open("data/" + offer_type + "_costs", "w")
for i in costs:
    f.write(str(i) + "\n")

start = -10
end = 20
inc = 0.001
f1 = open("data/" + offer_type + "_pdf1", "w")
f2 = open("data/" + offer_type + "_pdf2", "w")
x = start
while x <= end:
    f1.write(str(prediction.distribution[0].pdf(x)) + "\n")
    f2.write(str(prediction.distribution[1].pdf(x)) + "\n")
    x += inc
