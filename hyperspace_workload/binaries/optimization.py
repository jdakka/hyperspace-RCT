# script to run optimizations 

class hyperspaces(self, hyperspace_index): 
    ## needs 

    # data 
    # regressor function from scikit learn
    # 
    def get_spaces(self):

        # load hyperparameter list

        with open('home/dakka/spaces.txt', 'rb') as fp:
            spaces = pickle.load(fp)
        return spaces[hyperspace_index]


    def loading(self):

        boston = load_boston()
        X, y = boston.data, boston.target
        n_features = X.shape[1]

        reg = GradientBoostingRegressor(n_estimators=50, random_state=0)
        return reg 



    def new_function(self, objective, hyperparameters, results_path, model, ):
        ## make these attributes to the class 
        objective=objective,
               hyperparameters=hparams,
               results_path=args.results_dir,
               model="GP",
               n_iterations=100,
               verbose=True,
               random_state=0,
               checkpoints=True,
               restart=checkpoint)


class new_class(self):

     def __init__(self):

        self.objective = None
        self.model = None
        self.n_iterations = None
        self.verbose = True
        self.random_state = 0 

    def objective(params):
    """
    Objective function to be minimized.
    Parameters
    ----------
    * params [list, len(params)=n_hyperparameters]
        Settings of each hyperparameter for a given optimization iteration.
        - Controlled by hyperspaces's hyperdrive function.
        - Order preserved from list passed to hyperdrive's hyperparameters argument.
    """
        max_depth, learning_rate = params

        reg.set_params(max_depth=max_depth,
                       learning_rate=learning_rate)

        return -np.mean(cross_val_score(reg, X, y, cv=5, n_jobs=-1,
                    scoring="neg_mean_absolute_error"))



    if self.model == "GP":

        if verbose:
            result = gp_minimize(objective, space, n_calls=n_iterations, verbose=verbose,
                                 callback=callbacks, x0=init_points, y0=init_response,
                                 n_random_starts=n_rand, random_state=random_state)
        else:
            result = gp_minimize(objective, space, n_calls=n_iterations,
                                 callback=callbacks, x0=init_points, y0=init_response,
                                 n_random_starts=n_rand, random_state=random_state)

    # Case 1
    elif self.model == "RF":
        if verbose:
            result = forest_minimize(objective, space, n_calls=n_iterations, verbose=verbose,
                                     callback=callbacks, x0=init_points, y0=init_response,
                                     n_random_starts=n_rand, random_state=random_state)
        else:
            result = forest_minimize(objective, space, n_calls=n_iterations,
                                     callback=callbacks, x0=init_points, y0=init_response, 
                                     n_random_starts=n_rand, random_state=random_state)
    # Case 2
    elif self.model == "GBRT":
        if verbose:
            result = gbrt_minimize(objective, space, n_calls=self.n_iterations, verbose=verbose,
                                   callback=callbacks, x0=init_points, y0=init_response, 
                                   n_random_starts=n_rand, random_state=random_state)
        else:
            result = gbrt_minimize(objective, space, n_calls=n_iterations,
                                   callback=callbacks, x0=init_points, y0=init_response, 
                                   n_random_starts=n_rand, random_state=random_state)
    # Case 3
    elif self.model == "RAND":
        if verbose:
            result = dummy_minimize(objective, space, n_calls=n_iterations, verbose=verbose,
                                    callback=callbacks, x0=init_points, y0=init_response, 
                                    random_state=random_state)
        else:
            result = dummy_minimize(objective, space, n_calls=n_iterations,
                                    callback=callbacks, x0=init_points, y0=init_response,
                                    random_state=random_state)
    else:
        raise ValueError("Invalid model {}. Read the documentation for "
                         "supported models.".format(model))


if __name__ == '__main__':


    
    hyperspaces.get_spaces(hyperspace_index = int(sys.argv[1]))
