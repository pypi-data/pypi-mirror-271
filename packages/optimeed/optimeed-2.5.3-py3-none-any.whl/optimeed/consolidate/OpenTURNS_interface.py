from .sensitivity_analysis import SensitivityAnalysis_LibInterface
import openturns as ot
from typing import List
import numpy as np
import math


class Collection_Metamodels:
    def __init__(self, collection_to_fit, inputs, inputs_as_optivariables, name_collection="Chaos Expansion Fit"):
        """Class for that mimicks the behaviour of a collection so that it can be used with LinkDataGraph.

        :param collection_to_fit: collection whose attributes are to be fitted with PCE
        :param inputs: inputs variables to perform the fit (usually from a sensitivity analysis)
        :param inputs_as_optivariables: list of optivariables type of objects (usually from a sensitivity analysis)
        """
        self.fitted_metamodels = dict()  # Will contain mimic of attributes

        self.inputs = inputs
        self.inputs_as_optivariables = inputs_as_optivariables
        self.collection_to_fit = collection_to_fit  # Original collection to which data are fitted
        #
        # if inputs is None:
        #     inputs = [theCollection.get_list_attributes("device.{}".format(optivariable.get_attribute_name()))
        #               for optivariable in theSensitivityParameters.get_optivariables()]
        # self.inputs = list(zip(*inputs))
        self.callbacks = set()
        self.name_collection = name_collection

    def _do_callbacks(self):
        for callback in self.callbacks:
            callback()

    def add_callback(self, theCallback):
        """ Method to call when this item has changed"""
        self.callbacks.add(theCallback)

    def get_list_attributes(self, attributeName):
        if not attributeName:
            return []

        theMetamodel_PC = self.get_metamodel(attributeName)
        return theMetamodel_PC.evaluate_metamodel(self.inputs)

    def refresh_attribute(self, attributeName):
        if attributeName not in self.get_fitted_attributes():
            self.fitted_metamodels[attributeName] = Metamodel_PC_Openturns(self.inputs, self.collection_to_fit.get_list_attributes(attributeName),
                                                                           1, self.inputs_as_optivariables)
            self.fitted_metamodels[attributeName].add_callback(self._do_callbacks)

    def get_metamodel(self, attributeName):
        self.refresh_attribute(attributeName)
        return self.fitted_metamodels[attributeName]

    def get_fitted_attributes(self):
        return list(self.fitted_metamodels.keys())

    def __str__(self):
        return self.name_collection


class Metamodel_PC_Openturns:
    def __init__(self, inputs, outputs, degree_fitted, inputs_as_optivariables=None):
        """Class that performs a fit using polynomial chaos expansion"""
        self.inputs = inputs
        self.inputs_as_optivariables = inputs_as_optivariables
        self.outputs = outputs
        self.degree_fitted = degree_fitted
        self.fit_performed = False
        self.chaosresult = None  # Type FunctionalChaosResult
        self.callbacks = set()
        self.main_inputs_indices = list()  # Relax the fit by telling which columns to consider

    def add_callback(self, theCallback):
        """Add a callback method, to call everytime the metamodel is changed"""
        self.callbacks.add(theCallback)

    def refresh(self):
        self.get_metamodel()

    def _do_callbacks(self):
        for callback in self.callbacks:
            callback()

    @staticmethod
    def _end_training_index(outputs):
        return int(0.7*len(outputs))

    def _get_main_inputs_and_outputs(self):
        """Manage the case of reduce fit"""
        init_inputs = np.array(self.inputs)
        init_outputs = self.outputs

        if not len(self.main_inputs_indices):
            return init_inputs, init_outputs

        extracted_inputs = init_inputs[:, self.main_inputs_indices]
        _, row_lists = np.unique(extracted_inputs, return_index=True, axis=0)
        row_lists = np.sort(row_lists)

        new_inputs = extracted_inputs[row_lists]
        new_objectives = np.array(init_outputs)[row_lists]

        return new_inputs, new_objectives

    def get_reduced_optivariables(self):
        init_variables = self.inputs_as_optivariables
        new_variables = init_variables
        if len(self.main_inputs_indices) and init_variables is not None:
            new_variables = [init_variables[i] for i in self.main_inputs_indices]
        return new_variables

    def get_FunctionalChaosResult(self):
        """Perform the fit (if not performed before).

        :return: FunctionalChaosResult, from openturns. Check https://openturns.github.io/openturns/latest/user_manual/response_surface/_generated/openturns.FunctionalChaosResult.html
        """
        if not self.fit_performed:  # Perform the fit
            inputs, outputs = self._get_main_inputs_and_outputs()
            variables = self.get_reduced_optivariables()
            end_training = self._end_training_index(outputs)
            subset_objectives = outputs[0:end_training]
            subset_inputs = inputs[0:end_training]

            if self.inputs_as_optivariables is None:
                print("by hand")
                chaosalgo = ot.FunctionalChaosAlgorithm(subset_inputs, [[obji] for obji in subset_objectives])  # Distribution has not been provided -> slow !
                # Todo: test it
            else:
                # Give the distribution
                dim = len(variables)
                marginals = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in variables]
                d = ot.ComposedDistribution(marginals)

                # Give the PCE
                polynomials = [ot.StandardDistributionPolynomialFactory(m) for m in marginals]
                # enumeratefunction = ot.HyperbolicAnisotropicEnumerateFunction(dim, 0.5)  # Truncation strategy
                enumeratefunction = ot.LinearEnumerateFunction(dim)  # Truncation strategy
                basis = ot.OrthogonalProductPolynomialFactory(polynomials, enumeratefunction)

                index_max = basis.getEnumerateFunction().getStrataCumulatedCardinal(self.degree_fitted)  # We select all polynomials of degrees <= degree_fitted
                adaptive = ot.FixedStrategy(basis, index_max)  # Method to fit. Fixed = we keep all terms. Total_size = number of elements

                projectionStrategy = ot.LeastSquaresStrategy()  # To compute the coefficients

                chaosalgo = ot.FunctionalChaosAlgorithm(subset_inputs, [[obji] for obji in subset_objectives], d, adaptive, projectionStrategy)
            chaosalgo.run()
            self.chaosresult = chaosalgo.getResult()
            self.fit_performed = True
            self._do_callbacks()
        return self.chaosresult

    def get_metamodel(self):
        return self.get_FunctionalChaosResult().getMetaModel()

    def get_metamodel_as_python_method(self):
        arg_name = "theDevice"
        theStr = "def mymetamodel({}):\n".format(arg_name)

        if self.inputs_as_optivariables is None:
            raise NotImplementedError("Not yet implemented :(")  # TODO: implement in case of no optivariables (unknown distribution)

        for k, optiVariable in enumerate(self.get_reduced_optivariables()): #self.get_SA_params().get_optivariables()):
            a, b, n = optiVariable.get_min_value(), optiVariable.get_max_value(), optiVariable.get_attribute_name()
            T1 = 2/(b-a)
            T2 = -(a+b)/(b-a)
            if T2 < 0:
                theStr += "    x{} = {}*{}.{} - {}\n".format(k, T1, arg_name, n, -T2)
            else:
                theStr += "    x{} = {}*{}.{} + {}\n".format(k, T1, arg_name, n, T2)
        theComposedMetamodel = str(self.get_FunctionalChaosResult().getComposedMetaModel())
        theStr += "    return {}\n".format(theComposedMetamodel.replace("^", "**"))
        return theStr

    def evaluate_metamodel(self, inputs, already_reduced=False):
        """Evaluate the metamodel at inputs. X (as array [[x1i, ... xni], ..., [x1j, ... xnj]])

        :param inputs: list of variables combinations [x1i, ... xni], ..., [x1j, ... xnj]
        :return: list of corresponding evaluations [output_1, ... output_j]
        """
        new_inputs = np.array(inputs)
        if len(self.main_inputs_indices) and not already_reduced:
            new_inputs = new_inputs[:, self.main_inputs_indices]

        return np.array(self.get_metamodel()(new_inputs)).flatten()

    def set_fit_degree(self, degree):
        if self.degree_fitted != degree:
            self.degree_fitted = degree
            self.fit_performed = False

    def set_inputs(self, inputs, inputs_as_optivariables=None):
        self.inputs = inputs
        self.inputs_as_optivariables = inputs_as_optivariables
        self.fit_performed = False

    def set_main_inputs_indices(self, list_main_indices):
        self.main_inputs_indices = list_main_indices
        self.fit_performed = False

    def set_outputs(self, outputs):
        self.outputs = outputs
        self.fit_performed = False

    def check_goodness_of_fit(self):
        inputs, outputs = self._get_main_inputs_and_outputs()
        end_training = self._end_training_index(outputs)

        inputs_valid = inputs[end_training:]
        outputs_valid = outputs[end_training:]
        _outputs_valid_formatted = [[obji] for obji in outputs_valid]
        theMetaModel = self.get_metamodel()
        val = ot.MetaModelValidation(inputs_valid, _outputs_valid_formatted, theMetaModel)
        Q2 = val.computePredictivityFactor()[0]

        outputs_model = self.evaluate_metamodel(inputs_valid, already_reduced=True)  # Main inputs only
        return Q2, outputs_valid, outputs_model


class SensitivityAnalysis_OpenTURNS_Chaos(SensitivityAnalysis_LibInterface):
    """Polynomial chaos expansions based.
    Sobol indices are computed from metamodel."""

    def __init__(self, theSensitivityParameters, theObjectives, theMetamodel: Metamodel_PC_Openturns):
        super().__init__(theSensitivityParameters, theObjectives)
        self.theMetamodel = theMetamodel

    @staticmethod
    def sample_sobol(theOptimizationVariables, N):
        distributionList = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in theOptimizationVariables]
        distribution = ot.ComposedDistribution(distributionList)
        inputDesign = ot.SobolIndicesExperiment(distribution, N, True)
        return inputDesign.generate()

    def get_sobol_S1(self):
        length = len(self.get_SA_params().get_optivariables())
        theMetamodel = self.theMetamodel
        chaosSI = ot.FunctionalChaosSobolIndices(theMetamodel.get_FunctionalChaosResult())
        if not len(theMetamodel.main_inputs_indices):
            return [chaosSI.getSobolIndex(i) for i in range(length)]
        S1 = [0.0] * len(self.get_SA_params().get_optivariables())
        for index_metamodel, index_true in enumerate(theMetamodel.main_inputs_indices):
            S1[index_true] = chaosSI.getSobolIndex(index_metamodel)
        return S1


    def get_sobol_S1conf(self):
        """Not available using Chaos Expansion"""
        return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_ST(self):
        length = len(self.get_SA_params().get_optivariables())
        theMetamodel = self.theMetamodel
        chaosSI = ot.FunctionalChaosSobolIndices(theMetamodel.get_FunctionalChaosResult())
        if not len(theMetamodel.main_inputs_indices):
            return [chaosSI.getSobolTotalIndex(i) for i in range(length)]
        S1 = [0.0] * len(self.get_SA_params().get_optivariables())
        for index_metamodel, index_true in enumerate(theMetamodel.main_inputs_indices):
            S1[index_true] = chaosSI.getSobolTotalIndex(index_metamodel)
        return S1

    def get_sobol_STconf(self):
        """Not available using Chaos Expansion"""
        return [0.0] * len(self.get_SA_params().get_optivariables())

    def get_sobol_S2(self):
        theMetamodel = self.theMetamodel
        chaosSI = ot.FunctionalChaosSobolIndices(theMetamodel.get_FunctionalChaosResult())

        N = len(self.get_SA_params().get_optivariables())
        a = np.empty((N, N,))
        a[:] = np.nan
        if not len(theMetamodel.main_inputs_indices):  # No mapping
            for i in range(N):
                for j in range(N):
                    if i != j:
                        a[i, j] = chaosSI.getSobolIndex([i, j])
            return a

        for index_metamodel_i, index_true_i in enumerate(theMetamodel.main_inputs_indices):
            for index_metamodel_j, index_true_j in enumerate(theMetamodel.main_inputs_indices):
                if index_metamodel_i != index_metamodel_j:
                    a[index_true_i, index_true_j] = chaosSI.getSobolIndex([index_metamodel_i, index_metamodel_j])
        return a


class SensitivityAnalysis_OpenTURNS(SensitivityAnalysis_LibInterface):
    coefficients: List[List[float]]

    def __init__(self, theSensitivityParameters, theObjectives):
        super().__init__(theSensitivityParameters, theObjectives)
        self.SA = None

    @staticmethod
    def sample_sobol(theOptimizationVariables, N):
        distributionList = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in theOptimizationVariables]
        distribution = ot.ComposedDistribution(distributionList)
        raw_sample = ot.SobolIndicesExperiment(distribution, N, True).generate()
        return np.array(raw_sample)

    def get_sobol_S1(self):
        return self._get_SA().getFirstOrderIndices()

    def get_sobol_S1conf(self):
        try:
            intervals = self._get_SA().getFirstOrderIndicesInterval()
            lower_bounds = intervals.getLowerBound()
            upper_bounds = intervals.getUpperBound()
            return [up - (low+up)/2 for low, up in zip(lower_bounds, upper_bounds)]
        except TypeError:
            return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_ST(self):
        return self._get_SA().getTotalOrderIndices()

    def get_sobol_STconf(self):
        try:
            intervals = self._get_SA().getTotalOrderIndicesInterval()
            lower_bounds = intervals.getLowerBound()
            upper_bounds = intervals.getUpperBound()
            return [up - (low+up)/2 for low, up in zip(lower_bounds, upper_bounds)]
        except TypeError:
            return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_S2(self):
        return np.matrix(self._get_SA().getSecondOrderIndices())

    def _get_SA(self):
        if not self.performed:
            nb_params = len(self.get_SA_params().get_optivariables())

            # Size of sample
            if nb_params == 2:
                eval_per_sample = (2 + nb_params)
            else:
                eval_per_sample = (2 + 2 * nb_params)
            max_N = int(math.floor(len(self.theObjectives) / eval_per_sample))
            objectives = np.array(self.theObjectives[0:max_N * eval_per_sample])
            params = np.array(self.get_SA_params().get_paramvalues()[0:max_N * eval_per_sample])
            self.SA = ot.SaltelliSensitivityAlgorithm(params, [[obji] for obji in objectives], max_N)
            self.performed = True
        return self.SA

