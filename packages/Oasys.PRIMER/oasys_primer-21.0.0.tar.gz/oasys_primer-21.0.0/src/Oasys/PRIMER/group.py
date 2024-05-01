import Oasys.gRPC


# Metaclass for static properties and constants
class GroupType(type):
    _consts = {'ADD', 'REMOVE'}

    def __getattr__(cls, name):
        if name in GroupType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Group class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in GroupType._consts:
            raise AttributeError("Cannot set Group class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Group(Oasys.gRPC.OasysItem, metaclass=GroupType):
    _props = {'include', 'label', 'lock', 'title'}
    _rprops = {'exists', 'model', 'numtypes'}


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
        if name in Group._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Group._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Group instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Group._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Group._rprops:
            raise AttributeError("Cannot set read-only Group instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, label, title=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, label, title)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Group object

        Parameters
        ----------
        model : Model
            Model that Group will be created in
        label : integer
            Group number
        title : string
            Optional. Title for the group

        Returns
        -------
        dict
            Group object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the groups in the model

        Parameters
        ----------
        model : Model
            Model that all groups will be blanked in
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
        Blanks all of the flagged groups in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged groups will be blanked in
        flag : Flag
            Flag set on the groups that you want to blank
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
        Starts an interactive editing panel to create a group

        Parameters
        ----------
        model : Model
            Model that the group will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        dict
            Group object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first group in the model

        Parameters
        ----------
        model : Model
            Model to get first group in

        Returns
        -------
        Group
            Group object (or None if there are no groups in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free group label in the model.
        Also see Group.LastFreeLabel(),
        Group.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free group label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Group label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the groups in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all groups will be flagged in
        flag : Flag
            Flag to set on the groups

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of Group objects for all of the groups in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get groups from

        Returns
        -------
        list
            List of Group objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns a list of Group objects for all of the flagged groups in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get groups from
        flag : Flag
            Flag set on the groups that you want to retrieve

        Returns
        -------
        list
            List of Group objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the Group object for a group ID

        Parameters
        ----------
        model : Model
            Model to find the group in
        number : integer
            number of the group you want the Group object for

        Returns
        -------
        Group
            Group object (or None if group does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last group in the model

        Parameters
        ----------
        model : Model
            Model to get last group in

        Returns
        -------
        Group
            Group object (or None if there are no groups in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free group label in the model.
        Also see Group.FirstFreeLabel(),
        Group.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free group label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Group label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) group label in the model.
        Also see Group.FirstFreeLabel(),
        Group.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free group label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Group label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a group

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only groups from that model can be picked.
            If the argument is a Flag then only groups that
            are flagged with limit can be selected.
            If omitted, or None, any groups from any model can be selected.
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
            Group object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the groups in the model

        Parameters
        ----------
        model : Model
            Model that all groups will be renumbered in
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
        Renumbers all of the flagged groups in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged groups will be renumbered in
        flag : Flag
            Flag set on the groups that you want to renumber
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
        Allows the user to select groups using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting groups
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only groups from that model can be selected.
            If the argument is a Flag then only groups that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any groups can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of groups selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged groups in the model. The groups will be sketched until you either call
        Group.Unsketch(),
        Group.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged groups will be sketched in
        flag : Flag
            Flag set on the groups that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the groups are sketched.
            If omitted redraw is true. If you want to sketch flagged groups several times and only
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
        Returns the total number of groups in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing groups should be counted. If false or omitted
            referenced but undefined groups will also be included in the total

        Returns
        -------
        int
            number of groups
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the groups in the model

        Parameters
        ----------
        model : Model
            Model that all groups will be unblanked in
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
        Unblanks all of the flagged groups in the model

        Parameters
        ----------
        model : Model
            Model that the flagged groups will be unblanked in
        flag : Flag
            Flag set on the groups that you want to unblank
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
        Unsets a defined flag on all of the groups in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all groups will be unset in
        flag : Flag
            Flag to unset on the groups

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all groups

        Parameters
        ----------
        model : Model
            Model that all groups will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the groups are unsketched.
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
        Unsketches all flagged groups in the model

        Parameters
        ----------
        model : Model
            Model that all groups will be unsketched in
        flag : Flag
            Flag set on the groups that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the groups are unsketched.
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
        Associates a comment with a group

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the group is blanked or not

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
        Clears a flag on the group

        Parameters
        ----------
        flag : Flag
            Flag to clear on the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the group. The target include of the copied group can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Group
            Group object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a group

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the group

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

    def Flagged(self, flag):
        """
        Checks if the group is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the group

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a group

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetDataAll(self, type, index):
        """
        Returns 'all' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'all' row you want the data for. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalAll()

        Returns
        -------
        list
            A list containing data [Group.ADD or Group.REMOVE, BOX (if defined)]
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDataAll", type, index)

    def GetDataList(self, type, index):
        """
        Returns 'list' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'list' row you want the data for. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalList()

        Returns
        -------
        list
            A list containing data [Group.ADD or Group.REMOVE, ITEM1 (if defined), ITEM2 (if defined), ITEM3 (if defined), ITEM4 (if defined), ITEM5 (if defined), BOX (if defined)]
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDataList", type, index)

    def GetDataRange(self, type, index):
        """
        Returns 'range' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'range' row you want the data for. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalRange()

        Returns
        -------
        list
            A list containing data [Group.ADD or Group.REMOVE, START, END, BOX (if defined)]
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDataRange", type, index)

    def GetParameter(self, prop):
        """
        Checks if a Group property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Group.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            group property to get parameter for

        Returns
        -------
        dict
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetTotalAll(self, type):
        """
        Returns the total number of 'all' rows for a type in a group

        Parameters
        ----------
        type : string
            The type of the item

        Returns
        -------
        int
            The number of 'all' rows defined
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTotalAll", type)

    def GetTotalList(self, type):
        """
        Returns the total number of 'list' rows for a type in a group

        Parameters
        ----------
        type : string
            The type of the item

        Returns
        -------
        int
            The number of 'list' rows defined
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTotalList", type)

    def GetTotalRange(self, type):
        """
        Returns the total number of 'range' rows for a type in a group

        Parameters
        ----------
        type : string
            The type of the item

        Returns
        -------
        int
            The number of 'range' rows defined
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTotalRange", type)

    def GetTotals(self, type):
        """
        Returns the total number of 'all', 'list' and 'range' rows for a type in a group

        Parameters
        ----------
        type : string
            The type of the item

        Returns
        -------
        list
            List containing number of 'all', 'list' and 'range' rows defined or None if type not in group
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTotals", type)

    def GetType(self, row):
        """
        Returns the type for an entry in a group

        Parameters
        ----------
        row : integer
            The entry in the group types that you want the type for.
            Note that entries start at 0, not 1

        Returns
        -------
        str
            The type of the item (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetType", row)

    def Keyword(self):
        """
        Returns the keyword for this group.
        Note that a carriage return is not added.
        See also Group.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Group.
        Note that a carriage return is not added.
        See also Group.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next group in the model

        Returns
        -------
        Group
            Group object (or None if there are no more groups in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous group in the model

        Returns
        -------
        Group
            Group object (or None if there are no more groups in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveDataAll(self, type, index):
        """
        Removes 'all' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'all' row you want to Remove. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalAll()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveDataAll", type, index)

    def RemoveDataList(self, type, index):
        """
        Removes 'list' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'list' row you want to Remove. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalList()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveDataList", type, index)

    def RemoveDataRange(self, type, index):
        """
        Removes 'range' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'range' row you want to Remove. Note that indices start at 0, not 1.
            0 <= index < Group.GetTotalRange()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveDataRange", type, index)

    def SetDataAll(self, type, index, data):
        """
        Sets 'all' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'all' row you want the data for. Note that indices start at 0, not 1.
            0 <= index <= Group.GetTotalAll()
        data : List of data
            An list containing data [Group.ADD or
            Group.REMOVE, BOX (if defined)]

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetDataAll", type, index, data)

    def SetDataList(self, type, index, data):
        """
        Sets 'list' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'list' row you want the data for. Note that indices start at 0, not 1.
            0 <= index <= Group.GetTotalList()
        data : List of data
            An list containing data [Group.ADD or
            Group.REMOVE,
            ITEM1 (if defined), ITEM2 (if defined), ITEM3 (if defined), ITEM4 (if defined),
            ITEM5 (if defined), BOX (if defined)]

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetDataList", type, index, data)

    def SetDataRange(self, type, index, data):
        """
        Sets 'range' data for a given row number and type in the group

        Parameters
        ----------
        type : string
            The type of the item
        index : integer
            Index of 'all' row you want the data for. Note that indices start at 0, not 1.
            0 <= index <= Group.GetTotalRange()
        data : List of data
            An list containing data [Group.ADD or
            Group.REMOVE, START, END, BOX (if defined)]

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetDataRange", type, index, data)

    def SetFlag(self, flag):
        """
        Sets a flag on the group

        Parameters
        ----------
        flag : Flag
            Flag to set on the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the group. The group will be sketched until you either call
        Group.Unsketch(),
        Group.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the group is sketched.
            If omitted redraw is true. If you want to sketch several groups and only
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
        Unblanks the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the group

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the group is unsketched.
            If omitted redraw is true. If you want to unsketch several groups and only
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
            Group object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this group

        Returns
        -------
        dict
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

