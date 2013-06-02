import driver

"""
This file contains the code that runs the main experiment.
"""
def main():
    distribution = [
        (0.9, NormalDistribution(1, 0.5)),
        (0.1, UniformDistribution(9, 10))
    ]

    # Initialize a basic learner
    learner = BasicLearner(len(distribution))

    driver = driver.Driver(distribution, driver.STEPS, 10000)

    # Obtain the prediction population
    (prediction, payout, individuals) = driver.run()

    # Output information about the test
    print("population:\n" + str(driver.population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(payout))

if __name__ == "__main__":
    main()
