import sys
import numpy as np


def read_observation(filepath):
    """reads the observation file and returns
       observation as element of list
    """
    with open(filepath, 'r') as f:
        observation = f.read()
        observation = observation.split()
        return observation


def get_x_vec(observations):
    """takes observations and returns
       a x vector that contains 0 or 1
       0 if 'T' and 1 if 'H'
    """
    x_vec = np.empty([len(observations), 1], dtype=int)
    i = 0
    for obs in observations:
        if obs == 'H':
            x_vec[i] = 1
        else:
            x_vec[i] = 0
        i += 1
    return x_vec


def get_expection_z(x_vec, p, p1, p2):
    """ returns expectation vector
    """
    # A = p1^x_i; B = (1-p)^(1-x_i)
    A = np.power(p1, x_vec)
    B = np.power((1-p1), (1-x_vec))
    C = np.power(p2, x_vec)
    D = np.power((1-p2), (1-x_vec))

    num = p*(np.multiply(A, B))
    denom = p*(np.multiply(A, B)) + (1-p)*(np.multiply(C, D))

    exp_z = np.divide(num, denom)

    return exp_z


def get_updated_p(exp_z, obs_size):
    """ calculates and returns updated
        p value
    """
    p = np.sum(exp_z)/float(obs_size)
    return p


def get_updated_p1(exp_z, x_vec):
    """ calculates and returns updated
        p1 value
    """
    num = np.dot(exp_z.T, x_vec)[0][0]
    denom = np.sum(exp_z)
    p1 = num/float(denom)
    return p1


def get_updated_p2(exp_z, x_vec, obs_size):
    """ calculates and returns updataed
        p2 value
    """
    num = np.sum(x_vec) - np.dot(exp_z.T, x_vec)
    denom = obs_size - np.sum(exp_z)
    p2 = num/float(denom)
    return p2


def initialize_parameters(state='uniform'):
    """ If state is uniform then uniform initialization
        of parameters. If state is random then random
        initialization of parameters. omega is parameter
        vector. omega = [p, p1, p2]. returns omega
    """
    omega = np.empty([3, 1])
    if state == 'uniform':
        omega[0], omega[1], omega[2] = [0.5]*3
    elif state == 'random':
        omega = np.random.rand(3, 1)
    return omega


def update_omega(old_omega, observations, obs_size):
    p, p1, p2 = old_omega
    x_vec = get_x_vec(observations)
    exp_z = get_expection_z(x_vec, p, p1, p2)
    u_p = get_updated_p(exp_z, obs_size)
    u_p1 = get_updated_p1(exp_z, x_vec)
    u_p2 = get_updated_p2(exp_z, x_vec, obs_size)
    new_omega = np.empty([3, 1])
    new_omega[0], new_omega[1], new_omega[2] = u_p, u_p1, u_p2
    return new_omega


def run(iteration):
    for i in xrange(iteration):
        new_omega = update_omega(curr_omega, obs, obs_size)

    p, p1, p2 = new_omega[0][0], new_omega[1][0], new_omega[2][0]
    return p, p1, p2


if __name__ == '__main__':
    filepath = sys.argv[1]
    state = sys.argv[2]

    if state != "uniform" and state != "random":
        print "usage: python [module] [observation file] [state] [iteration]\n\
               state can be either uniform or random"
        sys.exit(1)

    obs = read_observation(filepath)
    obs_size = len(obs)

    curr_omega = initialize_parameters(state)
    print "Initial parameters"
    print "p: %s, p1: %s, p2: %s" % (curr_omega[0][0], curr_omega[1][0],
                                     curr_omega[2][0])
    new_omega = None

    print "Estimated parameters"
    p, p1, p2 = run(10)
    print "Iteration: %s p: %s, p1: %s, p2:%s" % (10, p, p1, p2)
    p, p1, p2 = run(25)
    print "Iteration: %s p: %s, p1:%s, p2:%s" % (25, p, p1, p2)
    p, p1, p2 = run(50)
    print "Iteration: %s p: %s, p1:%s, p2:%s" % (50, p, p1, p2)
