import Oasys.gRPC


# Metaclass for static properties and constants
class NodalForceGroupType(type):

    def __getattr__(cls, name):

        raise AttributeError("NodalForceGroup class attribute '{}' does not exist".format(name))


class NodalForceGroup(Oasys.gRPC.OasysItem, metaclass=NodalForceGroupType):
    _props = {'cid', 'id', 'include', 'label', 'nsid'}
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
        if name in NodalForceGroup._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in NodalForceGroup._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("NodalForceGroup instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in NodalForceGroup._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in NodalForceGroup._rprops:
            raise AttributeError("Cannot set read-only NodalForceGroup instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nsid, cid=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nsid, cid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new NodalForceGroup object

        Parameters
        ----------
        model : Model
            Model that nodal force group will be created in
        nsid : integer
            Set Node Set ID
        cid : integer
            Optional. Coordinate System ID

        Returns
        -------
        dict
            NodalForceGroup object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that all nodal force groups will be blanked in
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
        Blanks all of the flagged nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged nodal force groups will be blanked in
        flag : Flag
            Flag set on the nodal force groups that you want to blank
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

    def First(model):
        """
        Returns the first nodal force group in the model

        Parameters
        ----------
        model : Model
            Model to get first nodal force group in

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object (or None if there are no nodal force groups in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the nodal force groups in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all nodal force groups will be flagged in
        flag : Flag
            Flag to set on the nodal force groups

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of NodalForceGroup objects for all of the nodal force groups in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get nodal force groups from

        Returns
        -------
        list
            List of NodalForceGroup objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns a list of NodalForceGroup objects for all of the flagged nodal force groups in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get nodal force groups from
        flag : Flag
            Flag set on the nodal force groups that you want to retrieve

        Returns
        -------
        list
            List of NodalForceGroup objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the NodalForceGroup object for a nodal force group ID

        Parameters
        ----------
        model : Model
            Model to find the nodal force group in
        number : integer
            number of the nodal force group you want the NodalForceGroup object for

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object (or None if nodal force group does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last nodal force group in the model

        Parameters
        ----------
        model : Model
            Model to get last nodal force group in

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object (or None if there are no nodal force groups in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a nodal force group

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only nodal force groups from that model can be picked.
            If the argument is a Flag then only nodal force groups that
            are flagged with limit can be selected.
            If omitted, or None, any nodal force groups from any model can be selected.
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
            NodalForceGroup object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select nodal force groups using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting nodal force groups
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only nodal force groups from that model can be selected.
            If the argument is a Flag then only nodal force groups that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any nodal force groups can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of nodal force groups selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged nodal force groups in the model. The nodal force groups will be sketched until you either call
        NodalForceGroup.Unsketch(),
        NodalForceGroup.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged nodal force groups will be sketched in
        flag : Flag
            Flag set on the nodal force groups that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the nodal force groups are sketched.
            If omitted redraw is true. If you want to sketch flagged nodal force groups several times and only
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
        Returns the total number of nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing nodal force groups should be counted. If false or omitted
            referenced but undefined nodal force groups will also be included in the total

        Returns
        -------
        int
            number of nodal force groups
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that all nodal force groups will be unblanked in
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
        Unblanks all of the flagged nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that the flagged nodal force groups will be unblanked in
        flag : Flag
            Flag set on the nodal force groups that you want to unblank
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
        Unsets a defined flag on all of the nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all nodal force groups will be unset in
        flag : Flag
            Flag to unset on the nodal force groups

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all nodal force groups

        Parameters
        ----------
        model : Model
            Model that all nodal force groups will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the nodal force groups are unsketched.
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
        Unsketches all flagged nodal force groups in the model

        Parameters
        ----------
        model : Model
            Model that all nodal force groups will be unsketched in
        flag : Flag
            Flag set on the nodal force groups that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the nodal force groups are unsketched.
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
        Associates a comment with a nodal force group

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the nodal force group is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the nodal force group

        Parameters
        ----------
        flag : Flag
            Flag to clear on the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the nodal force group. The target include of the copied nodal force group can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a nodal force group

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the nodal force group is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the nodal force group

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a nodal force group

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a NodalForceGroup property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the NodalForceGroup.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            nodal force group property to get parameter for

        Returns
        -------
        dict
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this nodal force group.
        Note that a carriage return is not added.
        See also NodalForceGroup.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the nodal force group.
        Note that a carriage return is not added.
        See also NodalForceGroup.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next nodal force group in the model

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object (or None if there are no more nodal force groups in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous nodal force group in the model

        Returns
        -------
        NodalForceGroup
            NodalForceGroup object (or None if there are no more nodal force groups in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the nodal force group

        Parameters
        ----------
        flag : Flag
            Flag to set on the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the nodal force group. The nodal force group will be sketched until you either call
        NodalForceGroup.Unsketch(),
        NodalForceGroup.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the nodal force group is sketched.
            If omitted redraw is true. If you want to sketch several nodal force groups and only
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
        Unblanks the nodal force group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the nodal force group

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the nodal force group is unsketched.
            If omitted redraw is true. If you want to unsketch several nodal force groups and only
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
            NodalForceGroup object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this nodal force group

        Returns
        -------
        dict
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

