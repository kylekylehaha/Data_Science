import numpy as np
import math as m
from numpy.random import default_rng

# you must use python 3.6, 3.7, 3.8, 3.9 for sourcedefender
import sourcedefender
from HomeworkFramework import Function



class RS_optimizer(Function): # need to inherit this class "Function"
    def __init__(self, target_func):
        super().__init__(target_func) # must have this init to work normally

        self.lower = self.f.lower(target_func)
        self.upper = self.f.upper(target_func)
        self.dim = self.f.dimension(target_func)
         
        self.target_func = target_func

        self.eval_times = 0
        self.optimal_value = float("inf")
        self.optimal_solution = np.empty(self.dim)
        
        # Set input
        rng = default_rng()
        self.mean = rng.standard_normal(self.dim)
        self.sigma = 0.25

        # Set parameter
        self.lamda = 4 + m.floor(3 * np.log(self.dim))
        self.mu = m.floor(self.lamda / 2)

        self.weights = np.array([np.log(self.lamda / 2 + 0.5) - np.log(i) for i in range(1, self.mu+1)])
        self.weights = np.array([w / np.sum(self.weights) for w in self.weights])

        self.mu_eff = 1 / np.sum(np.power(w, 2) for w in self.weights)

        self.c_c = (4 + self.mu_eff / self.dim) / (self.dim + 4 + 2 * self.mu_eff / self.dim)
        self.c_1 = 2 / (np.power(self.dim + 1.3, 2) + self.mu_eff)
        self.c_mu = min(1 - self.c_1, 2 * (self.mu_eff - 2 + 1 / self.mu_eff) / (np.power(self.dim + 2, 2) + self.mu_eff))
        self.c_sigma = (self.mu_eff + 2) / (self.dim + self.mu_eff + 5)
        self.d_sigma = 1 + 2 * max(0, np.power(((self.mu_eff - 1) / (self.dim + 1)), 0.5) - 1) + self.c_sigma

        #Initialization
        self.p_c = np.zeros(self.dim)
        self.p_sigma = np.zeros(self.dim)
        self.C = np.eye(self.dim)
        
        self.chi_n = np.sqrt(self.dim) * (1.0 - (1.0 / (4.0 * self.dim)) + 1.0 / (21.0 * (self.dim ** 2)))

    def get_optimal(self):
        return self.optimal_solution, self.optimal_value

    def run(self, FES):
        while self.eval_times < FES:
            # print('=====================FE=====================')
            # print(self.eval_times)
            
            self.C = (self.C + self.C.T) / 2
            eigen_values, eigen_vectors = np.linalg.eig(self.C)
            self.D = np.sqrt(np.where(eigen_values < 0, 1e-8, eigen_values))
            self.B = eigen_vectors
            self.C = np.dot(np.dot(self.B, np.diag(self.D ** 2)), self.B.T)
            
            z_params = np.zeros((self.lamda, self.dim))
            y_params = np.zeros((self.lamda, self.dim))
            x_params = np.zeros((self.lamda, self.dim))

            solution = np.zeros((self.lamda, self.dim))
            values = np.zeros(self.lamda)

            for i in range(self.lamda):
                z_params[i] = np.random.normal(0, 1, self.dim)
                y_params[i] = np.dot(np.dot(self.B, np.diag(self.D)), z_params[i])
                x_params[i] = self.mean + self.sigma * y_params[i]

                solution[i] = np.clip(x_params[i], self.lower, self.upper)
                value = self.f.evaluate(func_num, solution[i])

                self.eval_times += 1
                if value == "ReachFunctionLimit":
                    print("ReachFunctionLimit")
                    break
                
                values[i] = value
                if values[i] < self.optimal_value:
                    self.optimal_solution = solution[i]
                    self.optimal_value = values[i]

            if value == "ReachFunctionLimit":
                print("ReachFunctionLimit")
                break

            # Update mean
            idx = np.argsort(values)
            weighted_y_params = np.sum(self.weights[i] * y_params[idx[i]] for i in range(self.mu))
            self.mean += self.sigma * weighted_y_params

            # Update p_sigma
            self.p_sigma -= self.c_sigma * self.p_sigma
            
            weighted_C = self.B.dot(np.diag(1 / self.D)).dot(self.B.T).dot(weighted_y_params)
            np.add(self.p_sigma, np.sqrt(self.c_sigma * (2 - self.c_sigma) * self.mu_eff) * weighted_C, out=self.p_sigma, casting="unsafe")
            
            norm_p_sigma = np.linalg.norm(self.p_sigma)
            h_sigma_cond_left = norm_p_sigma / np.sqrt(1 - (1 - self.c_sigma) ** (2 * (self.eval_times + 1)))
            h_sigma_cond_right = (1.4 + 2 / (self.dim + 1)) * self.chi_n
            h_sigma = 1.0 if h_sigma_cond_left < h_sigma_cond_right else 0.0
    
            # Update p_c
            self.p_c -= self.c_c * self.p_c
            self.p_c += h_sigma * np.sqrt(self.c_c * (2 - self.c_c) * self.mu_eff) * weighted_y_params

            # Update C
            delta_h_sigma = (1 - h_sigma) * self.c_c * (2 - self.c_c)
            
            self.C *=  (1 - self.c_1 - self.c_mu + self.c_1 * delta_h_sigma)
            self.C += self.c_1 * (np.dot(self.p_c.reshape(self.dim, 1), self.p_c.reshape(1, self.dim))) 
            for i in range(self.mu):
                self.C += self.c_mu * self.weights[i] * np.dot(y_params[idx[i]].reshape(self.dim, 1), y_params[idx[i]].reshape(1, self.dim))
        
            # Update sigma
            with np.errstate(invalid='ignore'):
                self.sigma *= np.exp((self.c_sigma / self.d_sigma) * (norm_p_sigma / self.chi_n - 1))
                self.sigma = min(self.sigma, 1e32)     

            # print("optimal: {}\n".format(self.get_optimal()[1]))
            

if __name__ == '__main__':
    func_num = 1
    fes = 0
    #function1: 1000, function2: 1500, function3: 2000, function4: 2500
    while func_num < 5:
        if func_num == 1:
            fes = 1000
        elif func_num == 2:
            fes = 1500
        elif func_num == 3:
            fes = 2000 
        else:
            fes = 2500

        # you should implement your optimizer
        op = RS_optimizer(func_num)
        op.run(fes)
        
        best_input, best_value = op.get_optimal()
        print('Result')
        print(best_input, best_value)
        
        # change the name of this file to your student_ID and it will output properlly
        with open("{}_function{}.txt".format(__file__.split('_')[0], func_num), 'w+') as f:
            for i in range(op.dim):
                f.write("{}\n".format(best_input[i]))
            f.write("{}\n".format(best_value))
        func_num += 1 
