import Oasys.gRPC


# Metaclass for static properties and constants
class NodeSetType(type):

    def __getattr__(cls, name):

        raise AttributeError("NodeSet class attribute '{}' does not exist".format(name))


class NodeSet(Oasys.gRPC.OasysItem, metaclass=NodeSetType):
    _props = {'cnsid', 'colour', 'dof', 'id', 'include', 'label', 'nsid', 'tf'}
    _rprops = {'exists', 'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        if self._handle is None:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

# If one of the properties we define then get it
        if name in NodeSet._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in NodeSet._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("NodeSet instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in NodeSet._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in NodeSet._rprops:
            raise AttributeError("Cannot set read-only NodeSet instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nsid, dof, tf, label=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nsid, dof, tf, label)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new NodeSet object

        Parameters
        ----------
        model : Model
            Model that constrained node set will be created in
        nsid : integer
            Set Node ID
        dof : integer
            Degree of freedom
        tf : float
            Failure time
        label : integer
            Optional. Constrained node set number

        Returns
        -------
        dict
            NodeSet object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the node sets in the model

        Parameters
        ----------
        model : Model
            Model that all node sets will be blanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, redraw)

    def BlankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged node sets in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged node sets will be blanked in
        flag : Flag
            Flag set on the node sets that you want to blank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, redraw)

    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a node_set

        Parameters
        ----------
        model : Model
            Model that the node_set will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        dict
            NodeSet object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first node set in the model

        Parameters
        ----------
        model : Model
            Model to get first node set in

        Returns
        -------
        NodeSet
            NodeSet object (or None if there are no node sets in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free node set label in the model.
        Also see NodeSet.LastFreeLabel(),
        NodeSet.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free node set label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            NodeSet label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the node sets in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all node sets will be flagged in
        flag : Flag
            Flag to set on the node sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of NodeSet objects for all of the node sets in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get node sets from

        Returns
        -------
        list
            List of NodeSet objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns a list of NodeSet objects for all of the flagged node sets in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get node sets from
        flag : Flag
            Flag set on the node sets that you want to retrieve

        Returns
        -------
        list
            List of NodeSet objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the NodeSet object for a node set ID

        Parameters
        ----------
        model : Model
            Model to find the node set in
        number : integer
            number of the node set you want the NodeSet object for

        Returns
        -------
        NodeSet
            NodeSet object (or None if node set does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last node set in the model

        Parameters
        ----------
        model : Model
            Model to get last node set in

        Returns
        -------
        NodeSet
            NodeSet object (or None if there are no node sets in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free node set label in the model.
        Also see NodeSet.FirstFreeLabel(),
        NodeSet.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free node set label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            NodeSet label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) node set label in the model.
        Also see NodeSet.FirstFreeLabel(),
        NodeSet.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free node set label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            NodeSet label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a node set

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only node sets from that model can be picked.
            If the argument is a Flag then only node sets that
            are flagged with limit can be selected.
            If omitted, or None, any node sets from any model can be selected.
            from any model
        modal : boolean
            Optional. If picking is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the pick will be modal
        button_text : string
            Optional. By default the window with the prompt will have a button labelled 'Cancel'
            which if pressed will cancel the pick and return None. If you want to change the
            text on the button use this argument. If omitted 'Cancel' will be used

        Returns
        -------
        dict
            NodeSet object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the node sets in the model

        Parameters
        ----------
        model : Model
            Model that all node sets will be renumbered in
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberAll", model, start)

    def RenumberFlagged(model, flag, start):
        """
        Renumbers all of the flagged node sets in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged node sets will be renumbered in
        flag : Flag
            Flag set on the node sets that you want to renumber
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select node sets using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting node sets
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only node sets from that model can be selected.
            If the argument is a Flag then only node sets that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any node sets can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of node sets selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged node sets in the model. The node sets will be sketched until you either call
        NodeSet.Unsketch(),
        NodeSet.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged node sets will be sketched in
        flag : Flag
            Flag set on the node sets that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the node sets are sketched.
            If omitted redraw is true. If you want to sketch flagged node sets several times and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", model, flag, redraw)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of node sets in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing node sets should be counted. If false or omitted
            referenced but undefined node sets will also be included in the total

        Returns
        -------
        int
            number of node sets
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the node sets in the model

        Parameters
        ----------
        model : Model
            Model that all node sets will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, redraw)

    def UnblankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged node sets in the model

        Parameters
        ----------
        model : Model
            Model that the flagged node sets will be unblanked in
        flag : Flag
            Flag set on the node sets that you want to unblank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, redraw)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the node sets in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all node sets will be unset in
        flag : Flag
            Flag to unset on the node sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all node sets

        Parameters
        ----------
        model : Model
            Model that all node sets will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the node sets are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model, redraw)

    def UnsketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flagged node sets in the model

        Parameters
        ----------
        model : Model
            Model that all node sets will be unsketched in
        flag : Flag
            Flag set on the node sets that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the node sets are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, redraw)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a node set

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the node set is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def Browse(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an edit panel in Browse mode

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Browse", modal)

    def ClearFlag(self, flag):
        """
        Clears a flag on the node set

        Parameters
        ----------
        flag : Flag
            Flag to clear on the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the node set. The target include of the copied node set can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        NodeSet
            NodeSet object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a node set

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Edit(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Edit", modal)

    def ExtractColour(self):
        """
        Extracts the actual colour used for node set.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the node set colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the node set

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the node set is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the node set

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a node set

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a NodeSet property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the NodeSet.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            node set property to get parameter for

        Returns
        -------
        dict
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this node_set (\*CONSTRAINED_NODE_SET).
        Note that a carriage return is not added.
        See also NodeSet.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the node_set.
        Note that a carriage return is not added.
        See also NodeSet.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next node set in the model

        Returns
        -------
        NodeSet
            NodeSet object (or None if there are no more node sets in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous node set in the model

        Returns
        -------
        NodeSet
            NodeSet object (or None if there are no more node sets in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the node set

        Parameters
        ----------
        flag : Flag
            Flag to set on the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the node set. The node set will be sketched until you either call
        NodeSet.Unsketch(),
        NodeSet.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the node set is sketched.
            If omitted redraw is true. If you want to sketch several node sets and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unblank(self):
        """
        Unblanks the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the node set

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the node set is unsketched.
            If omitted redraw is true. If you want to unsketch several node sets and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        dict
            NodeSet object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this node set

        Returns
        -------
        dict
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

