from .onclickInterface import OnclickInterface
from PyQt5.QtWidgets import QApplication
from optimeed.core import obj_to_json, printIfShown, SHOW_INFO


class Onclick_tojson(OnclickInterface):
    def __init__(self, theDataLink):
        self.theLinkDataGraph = theDataLink

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        for index_point in indices_points:
            theDevice = self.theLinkDataGraph.get_clicked_item(index_graph, index_trace, index_point)
            theStr = str(obj_to_json(theDevice))
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(theStr, mode=cb.Clipboard)
            printIfShown("{}\nCopied to clipboard!".format(theStr), SHOW_INFO)

    def get_name(self):
        return "Extract json"
