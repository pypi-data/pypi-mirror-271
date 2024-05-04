from PyQt5 import QtWidgets
import numpy as np
from optimeed.core.tools import order_lists


class Widget_simplifyMetamodel(QtWidgets.QWidget):
    """This widget works using SALib and restrains the number of parameters used to perform the metamodel fit to the first N most influencials.
    Usage:
    - Instantiates the widget using the base sensitivty parameters
    - Set the slave sensitivity analysis using set_slave_SA
    - Update the slave with the selected limited number of parameters using update_SA
    """
    def __init__(self, master_sensitivityAnalysis, controled_metamodel):
        """Using a sensitivity analysis, reduce the number of parameters to fit in controled_metamodel

        :param master_sensitivityAnalysis:
        :param controled_metamodel:
        """
        super().__init__()
        self.master_SA = master_sensitivityAnalysis

        self.theMetamodel_PC = controled_metamodel
        self.nb_fit = 5

        # Input
        main_horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.label_dimensionality = QtWidgets.QLabel("Max number of parameters in SA: ")
        main_horizontal_layout.addWidget(self.label_dimensionality)

        self.textInput = QtWidgets.QSpinBox()
        self.textInput.setMinimum(1)
        self.textInput.setMaximum(100)
        self.textInput.setValue(1)
        self.textInput.textChanged.connect(self.set_nb_fit)

        main_horizontal_layout.addWidget(self.textInput)

        self.buttonValid = QtWidgets.QPushButton()
        self.buttonValid.clicked.connect(self.update_controled_metamodel)
        self.buttonValid.setText("OK")
        main_horizontal_layout.addWidget(self.buttonValid)

    def set_nb_fit(self):
        num_variables = int(self.textInput.text())
        self.nb_fit = min(num_variables, len(self.master_SA.get_SA_params().get_optivariables()))
        self.update_controled_metamodel()

    def set_controled_metamodel(self, theMetamodel_PC):
        self.theMetamodel_PC = theMetamodel_PC

    def set_master_SA(self, theSensitivityAnalysis):
        self.master_SA = theSensitivityAnalysis

    def update_controled_metamodel(self):
        SA_params = self.master_SA.get_SA_params()

        ST = self.master_SA.get_sobol_ST()
        _, ordered_ST = order_lists(ST, list(range(len(SA_params.get_optivariables()))))
        ordered_ST.reverse()
        columns_to_extract = ordered_ST[0:self.nb_fit]

        # Get paramvalues
        self.theMetamodel_PC.set_main_inputs_indices(columns_to_extract)
        self.theMetamodel_PC.refresh()

