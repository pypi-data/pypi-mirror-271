import Oasys.gRPC


# Metaclass for static properties and constants
class AirbagType(type):
    _consts = {'ADIABATIC_GAS_MODEL', 'ADVANCED_ALE', 'ALE', 'HYBRID', 'HYBRID_CHEMKIN', 'HYBRID_JETTING', 'LINEAR_FLUID', 'LOAD_CURVE', 'PARTICLE', 'SIMPLE_AIRBAG_MODEL', 'SIMPLE_PRESSURE_VOLUME', 'WANG_NEFSKE', 'WANG_NEFSKE_JETTING', 'WANG_NEFSKE_MULTIPLE_JETTING'}

    def __getattr__(cls, name):
        if name in AirbagType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Airbag class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in AirbagType._consts:
            raise AttributeError("Cannot set Airbag class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Airbag(Oasys.gRPC.OasysItem, metaclass=AirbagType):
    _props = {'abid', 'colour', 'id', 'include', 'label', 'properties', 'title', 'type'}
    _rprops = {'cols', 'exists', 'model', 'rows'}


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
        if name in Airbag._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Airbag._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Airbag instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Airbag._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Airbag._rprops:
            raise AttributeError("Cannot set read-only Airbag instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, sid, sidtyp=Oasys.gRPC.defaultArg, abid=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, sid, sidtyp, abid, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Airbag object

        Parameters
        ----------
        model : Model
            Model that airbag will be created in
        type : string
            Airbag type. Can be Airbag.SIMPLE_PRESSURE_VOLUME,
            Airbag.SIMPLE_AIRBAG_MODEL,
            Airbag.ADIABATIC_GAS_MODEL,
            Airbag.WANG_NEFSKE,
            Airbag.WANG_NEFSKE_JETTING,
            Airbag.WANG_NEFSKE_MULTIPLE_JETTING,
            Airbag.LOAD_CURVE,
            Airbag.LINEAR_FLUID,
            Airbag.HYBRID,
            Airbag.HYBRID_JETTING,
            Airbag.HYBRID_CHEMKIN,
            Airbag.ALE,
            Airbag.ADVANCED_ALE or
            Airbag.PARTICLE
        sid : integer
            Set ID
        sidtyp : integer
            Optional. Set type: segment/part set ID
        abid : integer
            Optional. Airbag number
        heading : string
            Optional. Airbag title

        Returns
        -------
        dict
            Airbag object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create an airbag

        Parameters
        ----------
        model : Model
            Model that the airbag will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        dict
            Airbag object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first airbag in the model

        Parameters
        ----------
        model : Model
            Model to get first airbag in

        Returns
        -------
        Airbag
            Airbag object (or None if there are no airbags in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free airbag label in the model.
        Also see Airbag.LastFreeLabel(),
        Airbag.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free airbag label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Airbag label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the airbags in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all airbags will be flagged in
        flag : Flag
            Flag to set on the airbags

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of Airbag objects for all of the airbags in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get airbags from

        Returns
        -------
        list
            List of Airbag objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns a list of Airbag objects for all of the flagged airbags in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get airbags from
        flag : Flag
            Flag set on the airbags that you want to retrieve

        Returns
        -------
        list
            List of Airbag objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the Airbag object for a airbag ID

        Parameters
        ----------
        model : Model
            Model to find the airbag in
        number : integer
            number of the airbag you want the Airbag object for

        Returns
        -------
        Airbag
            Airbag object (or None if airbag does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last airbag in the model

        Parameters
        ----------
        model : Model
            Model to get last airbag in

        Returns
        -------
        Airbag
            Airbag object (or None if there are no airbags in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free airbag label in the model.
        Also see Airbag.FirstFreeLabel(),
        Airbag.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free airbag label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Airbag label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) airbag label in the model.
        Also see Airbag.FirstFreeLabel(),
        Airbag.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free airbag label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Airbag label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the airbags in the model

        Parameters
        ----------
        model : Model
            Model that all airbags will be renumbered in
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
        Renumbers all of the flagged airbags in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged airbags will be renumbered in
        flag : Flag
            Flag set on the airbags that you want to renumber
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
        Allows the user to select airbags using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting airbags
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only airbags from that model can be selected.
            If the argument is a Flag then only airbags that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any airbags can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of airbags selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged airbags in the model. The airbags will be sketched until you either call
        Airbag.Unsketch(),
        Airbag.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged airbags will be sketched in
        flag : Flag
            Flag set on the airbags that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the airbags are sketched.
            If omitted redraw is true. If you want to sketch flagged airbags several times and only
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
        Returns the total number of airbags in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing airbags should be counted. If false or omitted
            referenced but undefined airbags will also be included in the total

        Returns
        -------
        int
            number of airbags
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the airbags in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all airbags will be unset in
        flag : Flag
            Flag to unset on the airbags

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all airbags

        Parameters
        ----------
        model : Model
            Model that all airbags will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the airbags are unsketched.
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
        Unsketches all flagged airbags in the model

        Parameters
        ----------
        model : Model
            Model that all airbags will be unsketched in
        flag : Flag
            Flag set on the airbags that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the airbags are unsketched.
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
        Associates a comment with a airbag

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the airbag

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

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
        Clears a flag on the airbag

        Parameters
        ----------
        flag : Flag
            Flag to clear on the airbag

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the airbag. The target include of the copied airbag can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Airbag
            Airbag object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a airbag

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the airbag

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
        Extracts the actual colour used for airbag.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the airbag colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the airbag

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the airbag is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the airbag

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a airbag

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Airbag property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Airbag.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            airbag property to get parameter for

        Returns
        -------
        dict
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPropertyByIndex(self, index):
        """
        Returns the value of property at index index for this
        Airbag object or None if no property exists

        Parameters
        ----------
        index : integer
            The index of the property value to retrieve.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for an airbag may not have adjacent indices

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByIndex", index)

    def GetPropertyByName(self, acronym):
        """
        Returns the value of property string acronym for this
        Airbag object or None if no property exists

        Parameters
        ----------
        acronym : string
            The acronym of the property value to retrieve

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByName", acronym)

    def GetPropertyByRowCol(self, row, col):
        """
        Returns the value of the property for row and col for this
        Airbag object or None if no property exists.
        Note that columns start at 0. Rows start at 1 if the _ID option is set,
        at 0 otherwise

        Parameters
        ----------
        row : integer
            The row of the property value to retrieve
        col : integer
            The column of the property value to retrieve

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByRowCol", row, col)

    def GetPropertyNameForIndex(self, index):
        """
        Returns the name of the property at index index for this
        Airbag object or None if there is no property

        Parameters
        ----------
        index : integer
            The index of the property name to retrieve.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for an airbag may not have adjacent indices

        Returns
        -------
        str
            Property name (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyNameForIndex", index)

    def GetPropertyNameForRowCol(self, row, col):
        """
        Returns the name of the property at row and col for this
        Airbag object or None if there is no property.
        Note that columns start at 0. Rows start at 1 if the _ID option is set,
        at 0 otherwise

        Parameters
        ----------
        row : integer
            The row of the property name to retrieve
        col : integer
            The column of the property name to retrieve

        Returns
        -------
        str
            Property name (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyNameForRowCol", row, col)

    def Keyword(self):
        """
        Returns the keyword for this airbag (e.g. \*AIRBAG_SIMPLE_PRESSURE_VOLUME,
        \*AIRBAG_SIMPLE_AIRBAG_MODEL etc).
        Note that a carriage return is not added.
        See also Airbag.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the airbag.
        Note that a carriage return is not added.
        See also Airbag.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next airbag in the model

        Returns
        -------
        Airbag
            Airbag object (or None if there are no more airbags in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous airbag in the model

        Returns
        -------
        Airbag
            Airbag object (or None if there are no more airbags in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the airbag

        Parameters
        ----------
        flag : Flag
            Flag to set on the airbag

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPropertyByIndex(self, index, value):
        """
        Sets the value of property at index index for this Airbag object

        Parameters
        ----------
        index : integer
            The index of the property value to set.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for an airbag may not have adjacent indices
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByIndex", index, value)

    def SetPropertyByName(self, acronym, value):
        """
        Sets the value of property string acronym for this Airbag object

        Parameters
        ----------
        acronym : string
            The acronym of the property value to set
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByName", acronym, value)

    def SetPropertyByRowCol(self, row, col, value):
        """
        Sets the value of the property for row and col for this
        Airbag object. Note that columns start at 0.
        Rows start at 1 if the _ID option is set, at 0 otherwise

        Parameters
        ----------
        row : integer
            The row of the property value to set
        col : integer
            The column of the property value to set
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByRowCol", row, col, value)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the airbag. The airbag will be sketched until you either call
        Airbag.Unsketch(),
        Airbag.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag is sketched.
            If omitted redraw is true. If you want to sketch several airbags and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the airbag

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag is unsketched.
            If omitted redraw is true. If you want to unsketch several airbags and only
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
            Airbag object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this airbag

        Returns
        -------
        dict
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

