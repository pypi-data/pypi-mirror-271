import numpy as np
from optimeed.core import printIfShown, SHOW_INFO


class Combinator:
    def __init__(self, S2, ST, names):
        self.dependent_lists = dict()  # Updated stored lists
        self.S2 = S2  # Updated matrix
        self.ST = ST  # Updated list
        self.names = names[:]  # Updated list
        self.find_parent_names = dict()
        for name in self.names:
            self.find_parent_names[name] = name  # 1:1 correspondence

    def set_elem_dependent_list(self, name_list, name_elem, value):
        """Set element of a dependent list to a value, accounting for the combinations (will set to the parent if element is a child)"""
        name_parent = self.find_parent_names[name_elem]  # Find parent
        index = self.names.index(name_parent)  # Find index of the parent in list
        self.get_dependent_list(name_list)[index] = value  # Assign good value in list

    def get_dependent_list(self, name_list):
        return self.dependent_lists[name_list]

    def add_dependent_list(self, name_list, thelist):
        self.dependent_lists[name_list] = thelist

    def combine_indices(self, indices, new_name):
        S2, ST, names = self.S2, self.ST, self.names

        for index in indices:
            self.find_parent_names[names[index]] = new_name  # They have been combined

        S2, ST, names = combine_sobol_parameters(S2, ST, indices, names=names, new_name=new_name)

        self.S2, self.ST, self.names = S2, ST, names
        for key in self.dependent_lists:
            init_list = self.dependent_lists[key]
            self.dependent_lists[key] = [elem for index, elem in enumerate(init_list) if index not in indices[1:]]

    def reorder_indices(self, new_order):
        S2 = self.S2
        ST = self.ST
        names = self.names

        new_names = [names[permut_i] for permut_i in new_order]
        new_ST = np.array([ST[permut_i] for permut_i in new_order])
        new_S2 = np.copy(S2)
        N = len(new_ST)

        for i in range(N):
            new_S2[:, i] = new_S2[new_order, i]
        for i in range(N):
            new_S2[i, :] = new_S2[i, new_order]

        # assign
        for key in self.dependent_lists:
            init_list = self.dependent_lists[key]
            self.dependent_lists[key] = [init_list[permut_i] for permut_i in new_order]

        self.S2, self.ST, self.names = new_S2, new_ST, new_names

    def get_names(self):
        return self.names


def combine_sobol_parameters(mat, ST, indices_selected, names=None, new_name=''):
    """Combine some entries of the sensitivity analysis

    :param mat: initial matrix of the second order interactions
    :param ST: sobol total index
    :param indices_selected: desired list of the indices to merge
    :param names: if not None, the names of the parameters of the SA
    :param new_name: when using the argument names, this is the new name to give to the combined indices
    :return: new_mat, new_ST, new_names: the new mat, ST, names
    """
    new_mat = np.copy(mat)
    new_ST = np.copy(ST)
    index_first = indices_selected[0]

    # S1_cumul = mat[index_first, index_first]
    for index_selected in indices_selected[1:]:
        # i, j = index_first, index_selected
        #
        # S1_cumul += mat[j, j] + mat[i, j] + mat[j,i]
        # bring the column of second into the first, then fills it with zeros
        new_mat[:, index_first] += new_mat[:, index_selected]
        new_mat[:, index_selected] = 0.0
        #
        # # bring the row of the second into the first, then fills it with zeros
        new_mat[index_first, :] += new_mat[index_selected, :]
        new_mat[index_selected, :] = 0.0

        # fix ST
        new_ST[index_first] += new_ST[index_selected]
        new_ST[index_selected] = 0

    # new_mat[index_first, index_first] = S1_cumul
    new_mat = np.delete(new_mat, indices_selected[1:], axis=1)  # Delete the columns
    new_mat = np.delete(new_mat, indices_selected[1:], axis=0)  # Delete the rows
    new_ST = np.delete(new_ST, indices_selected[1:])

    if names is not None:
        new_names = names[:]
        new_names[index_first] = "{}".format(new_name)
        new_names = [new_names[i] for i in range(len(names)) if i not in indices_selected[1:]]

        theStr = 'After merging:'
        for i, name in enumerate(new_names):
            theStr += "\n{} {}".format(i, name)
        # printIfShown(theStr, SHOW_INFO)
    else:
        new_names = None

    return new_mat, new_ST, new_names

def get_SA_names(SA_params):
    """Convenience method to retrieve a list of attribute names from a sensitivity analysis."""
    return [variable.get_attribute_name() for variable in SA_params.get_optivariables()]

def permutations_from_SAnames(init_names, list_desiredorder_fromnames):
    """From the parameters of a sensitivity analysis,
    find the permutations to apply to the sobol indices to follow the specified order"""
    result_order = list()
    for desired_name in list_desiredorder_fromnames:
        result_order.append(init_names.index(desired_name))
    return result_order


def reorder_parameters(S1, S2, ST, permutations):
    """Given the permutations, give new matrices S1, S2, ST. Does not change the original matrices

    :param S1: First order sobol indices
    :param S2: Second order sobol matrix
    :param ST: total order sobol indices
    :param permutations: list of the desired indices order
    :return: new matrices S1, S2, ST.
    """
    new_S1 = np.array([S1[permut_i] for permut_i in permutations])
    new_ST = np.array([ST[permut_i] for permut_i in permutations])
    new_S2 = np.copy(S2)
    N = len(new_S1)

    for i in range(N):
        new_S2[:, i] = new_S2[permutations, i]
    for i in range(N):
        new_S2[i, :] = new_S2[i, permutations]

    # # Resymmetricalise
    # for i in range(N):
    #     for j in range(i, N):
    #         print(new_S2[j, i], new_S2[i, j])
    #         new_S2[j, i] = new_S2[i, j]

    return new_S1, new_S2, new_ST

