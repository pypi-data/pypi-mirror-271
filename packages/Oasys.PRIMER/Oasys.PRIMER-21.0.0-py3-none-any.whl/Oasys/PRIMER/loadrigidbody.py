import Oasys.gRPC


# Metaclass for static properties and constants
class LoadRigidBodyType(type):

    def __getattr__(cls, name):

        raise AttributeError("LoadRigidBody class attribute '{}' does not exist".format(name))


class LoadRigidBody(Oasys.gRPC.OasysItem, metaclass=LoadRigidBodyType):
    _props = {'cid', 'dof', 'include', 'lcid', 'm1', 'm2', 'm3', 'pid', 'sf'}
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
        if name in LoadRigidBody._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in LoadRigidBody._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("LoadRigidBody instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in LoadRigidBody._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in LoadRigidBody._rprops:
            raise AttributeError("Cannot set read-only LoadRigidBody instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, pid, dof, lcid, sf=Oasys.gRPC.defaultArg, cid=Oasys.gRPC.defaultArg, m1=Oasys.gRPC.defaultArg, m2=Oasys.gRPC.defaultArg, m3=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, pid, dof, lcid, sf, cid, m1, m2, m3)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new LoadRigidBody object

        Parameters
        ----------
        model : Model
            Model that load rigidbody will be created in
        pid : integer
            Part ID
        dof : integer
            Applicable degrees-of-freedom
        lcid : integer
            Curve ID
        sf : float
            Optional. Curve scale factor
        cid : integer
            Optional. Coordinate system ID
        m1 : integer
            Optional. Node 1 ID
        m2 : integer
            Optional. Node 2 ID
        m3 : integer
            Optional. Node 3 ID

        Returns
        -------
        dict
            LoadRigidBody object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that all load rigidbodys will be blanked in
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
        Blanks all of the flagged load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged load rigidbodys will be blanked in
        flag : Flag
            Flag set on the load rigidbodys that you want to blank
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
        Returns the first load rigidbody in the model

        Parameters
        ----------
        model : Model
            Model to get first load rigidbody in

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object (or None if there are no load rigidbodys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the load rigidbodys in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all load rigidbodys will be flagged in
        flag : Flag
            Flag to set on the load rigidbodys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of LoadRigidBody objects for all of the load rigidbodys in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get load rigidbodys from

        Returns
        -------
        list
            List of LoadRigidBody objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns a list of LoadRigidBody objects for all of the flagged load rigidbodys in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get load rigidbodys from
        flag : Flag
            Flag set on the load rigidbodys that you want to retrieve

        Returns
        -------
        list
            List of LoadRigidBody objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the LoadRigidBody object for a load rigidbody ID

        Parameters
        ----------
        model : Model
            Model to find the load rigidbody in
        number : integer
            number of the load rigidbody you want the LoadRigidBody object for

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object (or None if load rigidbody does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last load rigidbody in the model

        Parameters
        ----------
        model : Model
            Model to get last load rigidbody in

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object (or None if there are no load rigidbodys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a load rigidbody

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only load rigidbodys from that model can be picked.
            If the argument is a Flag then only load rigidbodys that
            are flagged with limit can be selected.
            If omitted, or None, any load rigidbodys from any model can be selected.
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
            LoadRigidBody object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select load rigidbodys using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting load rigidbodys
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only load rigidbodys from that model can be selected.
            If the argument is a Flag then only load rigidbodys that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any load rigidbodys can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of load rigidbodys selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged load rigidbodys in the model. The load rigidbodys will be sketched until you either call
        LoadRigidBody.Unsketch(),
        LoadRigidBody.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged load rigidbodys will be sketched in
        flag : Flag
            Flag set on the load rigidbodys that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the load rigidbodys are sketched.
            If omitted redraw is true. If you want to sketch flagged load rigidbodys several times and only
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
        Returns the total number of load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing load rigidbodys should be counted. If false or omitted
            referenced but undefined load rigidbodys will also be included in the total

        Returns
        -------
        int
            number of load rigidbodys
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that all load rigidbodys will be unblanked in
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
        Unblanks all of the flagged load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that the flagged load rigidbodys will be unblanked in
        flag : Flag
            Flag set on the load rigidbodys that you want to unblank
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
        Unsets a defined flag on all of the load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all load rigidbodys will be unset in
        flag : Flag
            Flag to unset on the load rigidbodys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all load rigidbodys

        Parameters
        ----------
        model : Model
            Model that all load rigidbodys will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the load rigidbodys are unsketched.
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
        Unsketches all flagged load rigidbodys in the model

        Parameters
        ----------
        model : Model
            Model that all load rigidbodys will be unsketched in
        flag : Flag
            Flag set on the load rigidbodys that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the load rigidbodys are unsketched.
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
        Associates a comment with a load rigidbody

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the load rigidbody is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the load rigidbody

        Parameters
        ----------
        flag : Flag
            Flag to clear on the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the load rigidbody. The target include of the copied load rigidbody can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a load rigidbody

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the load rigidbody is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the load rigidbody

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a load rigidbody

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a LoadRigidBody property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the LoadRigidBody.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            load rigidbody property to get parameter for

        Returns
        -------
        dict
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this load rigidbody (\*LOAD_RIGIDBODY).
        Note that a carriage return is not added.
        See also LoadRigidBody.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the load rigidbody.
        Note that a carriage return is not added.
        See also LoadRigidBody.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next load rigidbody in the model

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object (or None if there are no more load rigidbodys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous load rigidbody in the model

        Returns
        -------
        LoadRigidBody
            LoadRigidBody object (or None if there are no more load rigidbodys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the load rigidbody

        Parameters
        ----------
        flag : Flag
            Flag to set on the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the load rigidbody. The load rigidbody will be sketched until you either call
        LoadRigidBody.Unsketch(),
        LoadRigidBody.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the load rigidbody is sketched.
            If omitted redraw is true. If you want to sketch several load rigidbodys and only
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
        Unblanks the load rigidbody

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the load rigidbody

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the load rigidbody is unsketched.
            If omitted redraw is true. If you want to unsketch several load rigidbodys and only
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
            LoadRigidBody object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this load rigidbody

        Returns
        -------
        dict
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

