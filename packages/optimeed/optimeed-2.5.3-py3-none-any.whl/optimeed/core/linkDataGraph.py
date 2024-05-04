from optimeed.core import Graphs, Data, ListDataStruct_Interface
import numpy as np
from optimeed.core import SHOW_INFO, printIfShown, SHOW_ERROR


class HowToPlotGraph:
    def __init__(self, attribute_x, attribute_y, kwargs_graph=None, check_if_plot_elem=None, meta=None):
        """
        Tells to LinkDataGraph how to plot it

        :param attribute_x: attribute (as string) to plot in X axis
        :param attribute_y: attribute (as string) to plot in Y axis
        :param kwargs_graph: kwargs (as dictionary) of plot options
        :param check_if_plot_elem: function taking an item of the collection as input and outputting True if item has to be displayed.
        :param meta:
        """
        self.attribute_x = attribute_x
        self.attribute_y = attribute_y
        self.meta = meta

        if kwargs_graph is None:
            self.kwargs_graph = dict()
        else:
            self.kwargs_graph = kwargs_graph

        self.check_if_plot_elem = check_if_plot_elem

    def __str__(self):
        theStr = ''
        theStr += "x: {} \t y: {}".format(self.attribute_x, self.attribute_y)
        return theStr


class LinkDataGraph:
    def __init__(self):
        self.theGraphs = Graphs()
        self.collections = dict()  # keys are unique ids of collection
        self.shadow_collections = dict()  # Keys are unique ids of collection
        self.kwargs_collections = dict()  # keys are unique ids of collection
        self.howToPlotGraphs = dict()  # keys are ids of graph
        self.ids_graphs_to_col = dict()  # Dict of dicts. First keys are ids of graphs, second keys are ids of traces.
        self.curr_id = 0
        self.meta_from_shadow = False

    # Main user function to use the class
    def add_collection(self, theCollection, kwargs=None):
        """ Add a collection (that will be a future trace)

        :param theCollection:
        :param kwargs: kwargs associated with the collection (e.g., color, symbol style, etc.)
        :return: unique id associated with the collection
        """
        theId = self.curr_id
        if kwargs is None:
            kwargs = dict()
        self.kwargs_collections[theId] = kwargs
        self.collections[theId] = theCollection
        self.curr_id += 1
        self.update_graphs()
        return theId

    def remove_collection(self, collectionId):
        """
        Remove collection from the graphs

        :param collectionId: ID of the collection
        :return:
        """
        # Remove from trace
        res, _ = self.get_graph_and_trace_from_idCollection(collectionId)
        for idGraph, idTrace in res:
            self.theGraphs.get_graph(idGraph).remove_trace(idTrace)
            self.ids_graphs_to_col[idGraph].pop(idTrace, None)
        # Remove collection
        self.collections.pop(collectionId, None)
        self.kwargs_collections.pop(collectionId, None)
        self.shadow_collections.pop(collectionId, None)
        self.update_graphs()

    def set_shadow_collection(self, master_collectionId, shadow_collection):
        """
        Link a collection to an other

        :param master_collectionId: ID of the collection that is displayed in the graph
        :param shadow_collection: collection to link to the master.
        :return:
        """
        self.shadow_collections[master_collectionId] = shadow_collection

    def get_graphs(self):
        return self.theGraphs

    def get_howToPlotGraph(self, idGraph):
        return self.howToPlotGraphs[idGraph]

    def add_graph(self, howToPlotGraph):
        """Add new graph to be plotted.

        :param howToPlotGraph: :class:`HowToPlotGraph`
        :return:
        """
        idGraph = self.theGraphs.add_graph()
        self.howToPlotGraphs[idGraph] = howToPlotGraph
        self.ids_graphs_to_col[idGraph] = dict()
        self.update_graphs()
        return idGraph

    def get_idCollections(self):
        """Get all ids of the plotted collections"""
        return list(self.collections.keys())

    def get_idGraphs(self):
        """Get all ids of the graphs"""
        return list(self.ids_graphs_to_col.keys())

    def get_idTraces(self, idGraph):
        """Get all ids of the traces of graph $idGraph"""
        return list(self.ids_graphs_to_col[idGraph].keys())

    def get_idCollection_from_graph(self, idGraph, idTrace):
        """Get id of collection plotted in graph $idGraph and trace $idTrace"""
        return self.ids_graphs_to_col[idGraph][idTrace]

    def get_collection(self, idCollection, getShadow=True):
        if getShadow:
            try:
                return self.shadow_collections[idCollection]
            except KeyError:
                pass
        return self.collections[idCollection]

    def get_kwargs_collection(self, idCollection):
        return self.kwargs_collections[idCollection]

    @staticmethod
    def get_x_y_to_plot(theCollection, howToPlotGraph):
        """Extract X-Y infos from collection and howtoplotGraph"""
        y_data = theCollection.get_list_attributes(howToPlotGraph.attribute_y)
        if howToPlotGraph.attribute_x is None:
            x_data = list(range(len(y_data)))
        else:
            x_data = theCollection.get_list_attributes(howToPlotGraph.attribute_x)
        min_length = min(len(x_data), len(y_data))
        return x_data[:min_length], y_data[:min_length]  # Truncate if lengths are not the same

    @staticmethod
    def get_meta_to_plot(theCollection, howToPlotGraph):
        """Get Z info from collection and HowToPlotGraph"""
        if howToPlotGraph.meta is None:
            return None
        else:
            return theCollection.get_list_attributes(howToPlotGraph.meta)

    def update_graphs(self):
        """Update the graphs: update graphs, traces, and X-Y data"""
        for idGraph in self.get_idGraphs():
            howToPlotGraph = self.howToPlotGraphs[idGraph]

            for idCollection in self.collections:
                # Check if collection belongs in traces, if not create it
                if idCollection not in self.ids_graphs_to_col[idGraph].values():
                    theData = Data([], [])
                    idTrace = self.theGraphs.add_trace(idGraph, theData, updateChildren=False)
                    self.ids_graphs_to_col[idGraph][idTrace] = idCollection

            for idTrace in self.get_idTraces(idGraph):
                idCollection = self.get_idCollection_from_graph(idGraph, idTrace)
                theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
                theCollection = self.get_collection(idCollection, getShadow=False)
                try:
                    x, y = self.get_x_y_to_plot(theCollection, howToPlotGraph)
                except AttributeError as e:
                    x, y = [], []
                    printIfShown("{}".format(e), SHOW_ERROR)

                # Replace infinite and nan numbers by 0
                vec = [x, y]
                for i in range(2):
                    # Replace "inf" by "nan
                    vec[i] = np.array(vec[i], dtype=float)
                    vec[i][np.isinf(vec[i])] = float('nan')
                    pos_infinite = np.argwhere(np.logical_not(np.isfinite(vec[i])))
                    vec[i][pos_infinite] = 0
                    if all(np.isnan(vec[i])):
                        vec[i] = []
                    else:
                        vec[i] = vec[i].tolist()
                x, y = vec[0], vec[1]

                kwargs = dict()
                kwargs.update(howToPlotGraph.kwargs_graph)
                kwargs.update(self.get_kwargs_collection(idCollection))

                theData.set_data(x, y)
                theData.set_meta(self.get_meta_to_plot(self.get_collection(idCollection, getShadow=self.meta_from_shadow), howToPlotGraph))
                theData.set_kwargs(kwargs)

                indices_to_plot = list()
                if howToPlotGraph.check_if_plot_elem is not None:
                    for k, data in enumerate(theCollection.get_data_generator()):
                        if howToPlotGraph.check_if_plot_elem(data) and k < len(x):
                            indices_to_plot.append(k)
                    theData.set_indices_points_to_plot(indices_to_plot)
        self.theGraphs.updateChildren()

    # Direct search functions: from graphs -> to collection

    def get_collection_from_graph(self, idGraph, idTrace, getShadow=True) -> ListDataStruct_Interface:
        """From indices in the graph, get corresponding collection"""
        return self.get_collection(self.get_idCollection_from_graph(idGraph, idTrace), getShadow=getShadow)

    def get_clicked_item(self, idGraph, idTrace, idPoint, getShadow=True):
        """
        Get the data hidden behind the clicked point

        :param idGraph: ID of the graph
        :param idTrace: ID of the trace
        :param idPoint: ID of the point
        :param getShadow: If true, will return the data from the collection linked to the collection that is plotted
        :return: Object in collection
        """
        theCol = self.get_collection_from_graph(idGraph, idTrace, getShadow)
        theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
        index_in_data = theData.get_dataIndex_from_graphIndex(idPoint)
        return theCol.get_data_at_index(index_in_data)

    def get_clicked_items(self, idGraph, idTrace, idPoint_list, getShadow=True):
        """Same as get_clicked_item, but using a list of points"""
        theCol = self.get_collection_from_graph(idGraph, idTrace, getShadow)
        theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
        indices_in_data = theData.get_dataIndices_from_graphIndices(idPoint_list)
        return [theCol.get_data_at_index(index_in_data) for index_in_data in indices_in_data]

    def delete_clicked_item(self, idGraph, idTrace, idPoint):
        """Remove item from the collection"""
        theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
        index_in_data = theData.get_dataIndex_from_graphIndex(idPoint)
        getShadows = [True, False] if self.get_idCollection_from_graph(idGraph, idTrace) in self.shadow_collections else [False]
        for getShadow in getShadows:
            self.get_collection_from_graph(idGraph, idTrace, getShadow).delete_points_at_indices([index_in_data])
        self.update_graphs()

    def delete_clicked_items(self, idGraph, idTrace, idPoints):
        """Same, but for a list of points"""
        theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
        indices_in_data = theData.get_dataIndices_from_graphIndices(idPoints)
        getShadows = [True, False] if self.get_idCollection_from_graph(idGraph, idTrace) in self.shadow_collections else [False]
        for getShadow in getShadows:
            self.get_collection_from_graph(idGraph, idTrace, getShadow).delete_points_at_indices(indices_in_data)
        self.update_graphs()

    # Functions here are reverse search: from collection -> find graphs
    def get_graph_and_trace_from_idCollection(self, idCollection):
        """Reverse search: from a collection, get all associated graphs"""
        res = list()
        for idGraph in self.get_idGraphs():
            for idTrace in self.get_idTraces(idGraph):
                if self.get_idCollection_from_graph(idGraph, idTrace) == idCollection:
                    res.append((idGraph, idTrace))
        return res, self.collections[idCollection]

    def get_idcollection_from_collection(self, theCollection):
        """Reverse search: from a collection, find its id"""
        for idCollection in self.collections:
            if self.collections[idCollection] == theCollection:
                return idCollection

    def get_idPoints_from_indices_in_collection(self, idGraph, idTrace, indices_in_collection):
        """From indices in a collection, find the associated idPoints of the graph"""
        theData = self.theGraphs.get_graph(idGraph).get_trace(idTrace)
        return theData.get_graphIndices_from_dataIndices(indices_in_collection)

    def get_collections(self):
        return list(self.collections.values())

    def set_meta_from_shadow(self):
        """Use this method if 'howToPlot' must use shadow collection"""
        self.meta_from_shadow = True
