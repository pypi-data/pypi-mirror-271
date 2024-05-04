from wasp import *
from io import StringIO

class DeserializedResult:
    '''Stores both input node (providence), action results (user data), and value default
    '''
    def __init__(self, node:WaspNode, interpreter:Interpreter, action=None):
        self.action = action
        self.node = node
        self.interpreter = interpreter
        self.userData:'dict{str:list(DeserializedResult)}' = {}

    def isTerminal(self):
        '''Determine if this deserialized result is terminal. I.e., it has no children data'''
        return len(self.node) == 0

    @staticmethod
    def fromDefault(node:WaspNode, interpreter:Interpreter, default, key="value"):
        '''
            Create a result from a default. This creates the equivalent
            {"value":{":=":default}}
            Later accessible as [key].value()
        '''
        # TODO - add support for list data as defaults
        # I.e., loop over each item in default creating a DR as done for scalar
        assert type(default) is not list
        dr = DeserializedResult(node, interpreter)
        cdr = DeserializedResult(node, interpreter)
        dr.userData[key] = cdr
        cdr.store(default)
        return dr

    def addResult(self, result:'DeserializedResult', inputObject):
        '''Append the deserialize result to existing userData dictionary
           mapping node name to user data

           If the result is expected to have a MaxOccurs of more than 1
           a list is created, if needed, and the result appended
           '''
        name = result.node.name()
        maxOccurs = inputObject.maxOccurs(name)
        # MaxOccurs of None is NoLimit
        aScalar = maxOccurs is not None and maxOccurs == 1
        if name not in self.userData and not aScalar:
            self.userData[name] = []

        if aScalar:
            self.userData[name] = result
        else:
            self.userData[name].append(result)
        return result

    def select(self, context:str):
        '''Obtain the deserialized result associated with the given context lookup
           context:str - the path to a child context. E.g., 'x/y/z' where z must be a terminal result
           return:list|None - the list of deserialized selection
        '''
        lineage = context.split("/")
        current = [self]
        next = []

        for name in lineage:
            while len(current) > 0:
                # wild card ignores
                if name == "*":
                    # Append all
                    for result in current[-1].userData.values():
                        if type(result) is list: next.extend(reversed(result))
                        else: next.append(result)
                elif name in current[-1].userData:
                    # Append only those that name match (non-null result)
                    result = current[-1].userData[name]
                    if result and type(result) is list:
                        next.extend(reversed(result))
                    elif result: next.append(result)
                current.pop()
            # Reverse order to preserve user-input order
            next.reverse()
            # Update current result being searched to be those identified
            current = next
            next = []

        return current if len(current) > 0 else None

    def store(self, value, key=None):
        if key is None: # default to ':=' scalar store
            key = ":="
        if key in self.userData and type(self.userData) is not list:
            self.userData[key] = [self.userData[key], value]
        else:
            self.userData[key] = value
        return value

    def storedResult(self, key=None):
        if key is None: key = ":="
        return self.userData[key] if key in self.userData else None

    def todict(self):
        '''Produce a dictionary representation of this deserialized result
           Stored results will have a key of ':='
        '''
        d = {}
        for key, value in self.userData.items():
            if type(value) is list:
                d[key] = []
                for v in value:
                    d[key].append(v.todict())
            elif type(value) is DeserializedResult:
                d[key] = value.todict()
            else:
                d[key] = value
        return d

    def value(self, vkey="value"):
        '''Obtain the associated 'value' nodes stored result '''
        dr = self.userData[vkey]
        assert dr is not None and type(dr) is DeserializedResult and ":=" in dr.userData, "value request requirements not met!"
        return dr.storedResult()

    def valuelist(self, vkey="value"):
        '''Convert the value of this DeserializedResult to a list.
        I.e., each deserialized stored result is converted to a list
        This is called for array user data. Because each 'value' is
        an input node with provedence, the ability to obtain a convenient
        list of the data is preferred.
        '''
        l = []
        assert vkey in self.userData, "valuelist request requirements not met!"
        for dr in self.userData[vkey]:
            l.append(dr.storedResult())
        return l


    def __bool__(self):
        '''Is this result valid based on if it has a node and an interpreter'''
        return self.node is not None and self.interpreter is not None

    def __len__(self):
        '''Obtain the length of this deserialized result.
        This will be the length of the stored result
        or if not a stored result (i.e., deserialized parent node) the number of
        child nodes '''
        if sr := self.storedResult():
            if type(sr) is list:
                return len(sr)
            else:
                return 1
        return len(self.userData)

    def __getitem__(self, key):
        '''Obtain the named deserialized result or if
        this is only a stored result, the result'''
        if key in self.userData:
            d = self.userData[key]
            # check if this items is only a storedResult (":=") and return it
            if type(d) is DeserializedResult and d.storedResult() is not None:
                return d.storedResult()
            return d
        # return null/invalid result
        # allows arbitrarily nested requests
        # without failing
        return DeserializedResult(None, None)


class InputObject:
    '''Generic Input object type used to track object requirements'''

    def __init__(self, **kwargs):
        '''
            Action - function pointer to be executed
            Desc: str - the description of this input object
            Enums:list(str) - enumerated values allowed
            MaxValExc:float - the maximum exclusive value for this input object
            MaxValInc:float - the maximum inclusive value for this input object
            MinValExc:float - the minimum exclusive value for this input object
            MinValInc:float - the minimum inclusive value for this input object
        '''

        self._action = kwargs.pop("Action", None)
        self._children = None  # dict(childKey:childObject)
        self._defaults = None  # dict(childKey, default)
        self._description  = kwargs.pop("Desc", None)
        self._enums = kwargs.pop("Enums", None)
        self._maxOccurs = None # dict(childKey:maxOccurs)
        self._maxValExc = kwargs.pop("MaxValExc", None)
        self._maxValInc = kwargs.pop("MaxValInc", None)
        self._minOccurs = None # dict(childKey:minOccurs)
        self._minValExc = kwargs.pop("MinValExc", None)
        self._minValInc = kwargs.pop("MinValInc", None)
        self._unique    = None # list(list(str)): list of path context to data which must be unique
        self._exists    = None

        assert len(kwargs) == 0, "Unexpected additional parameters to InputObject: " + str(kwargs)

    def isTerminal(self):
        '''Determine if this InputObject does not have children
           Return true, iff there are no children data
        '''
        # This is terminal if children is None
        return self._children is None

    def action(self):
        '''Obtain the action associated with the given child input key'''
        return self._action

    def _pre_add(self, inputKey, **kwargs):
        if self._children is None:
            self._children = {}
            self._defaults = {}
            self._maxOccurs = {}
            self._minOccurs = {}

        assert inputKey not in self._children

    def add(self, inputKey, inputObject, **kwargs):
        '''Add an exissting object as a child

        '''
        self._pre_add(inputKey, **kwargs)
        if "MaxOccurs" in kwargs: self._maxOccurs[inputKey] = kwargs.pop("MaxOccurs")
        if "MinOccurs" in kwargs: self._minOccurs[inputKey] = kwargs.pop("MinOccurs")
        if "Default" in kwargs: self._defaults[inputKey] = kwargs.pop("Default")
        self._children[inputKey] = inputObject
        return self._children[inputKey]

    def addSingle(self, inputKey, inputObject, **kwargs):
        kwargs["MaxOccurs"] = 1
        return self.add(inputKey, inputObject, **kwargs)

    def addRequired(self, inputKey, inputObject, **kwargs):
        kwargs["MinOccurs"] = 1
        return self.add(inputKey, inputObject, **kwargs)

    def addRequiredSingle(self, inputKey, inputObject, **kwargs):
        kwargs["MaxOccurs"] = 1
        kwargs["MinOccurs"] = 1
        return self.add(inputKey, inputObject, **kwargs)

    def select(self, context:str):
        '''Obtain the input objects associated with the given context lookup
           context:str - the path to a child context. E.g., 'x/y/z' where z must be a terminal object
           return:list|None - the list of input object selection
        '''
        lineage = context.split("/")
        current = [self]
        next = []

        for name in lineage:
            while len(current) > 0:
                # wild card ignores
                if current[-1]._children is not None:
                    if name == "*":
                        # Append all
                        for inputobject in current[-1]._children.values():
                            next.append(inputobject)
                    else:
                        # Append only those that name match
                        child = current[-1][name]
                        if child:
                            next.append(child)
                current.pop()
            # Reverse order to preserve user-input order
            next.reverse()
            # Update current objects being searched to be those identified
            current = next
            next = []

        return current if len(current) > 0 else None

    def addExistsConstraint(self, ec:'ExistsConstraint'):
        '''Add an ExistsConstraint to this object

            Raises: exception if referenced source or target do not exist or are not terminal
        '''
        # Check that source and target exist and are terminal
        for s in ec._source:
            selected = self.select(s)
            assert selected is not None, "Unable to verify exist constraint for "+s+"! Constraints must refer to existing component!"
            for component in selected:
                # Unique constraints must reference terminal objects for comparison of data
                assert component.isTerminal(), "Exists constraints can only be applied to terminal data components!"

        for t in ec._target:
            selected = self.select(t)
            assert selected is not None, "Unable to verify exists constraint for "+t+"! Constraints must refer to existing component!"
            for component in selected:
                # Unique constraints must reference terminal objects for comparison of data
                assert component.isTerminal(), "Exists constraints can only be applied to terminal data components!"

        if self._exists == None:
            self._exists = []
        self._exists.append(ec)

    def addUniqueConstraint(self, context:'list(str)'):
        '''Add a uniqueness constraint to this input object that requires all referenced context to
        have different data.

        context:list(str) - the paths associated with the data which must be unique
                            E.g., 'x/y/z' means the x child, y granchild, and z greatgrandchild definitions must exist

        Note: This must be called after all context have been created

        Raises: exception if referenced context does not exist
        '''
        # Check each context selects input definition
        for c in context:
            selected = self.select(c)
            assert selected is not None, "Unable to verify uniqueness constraint for "+c+"! Constraints must refer to existing InputObject definitions"
            for inputObject in selected:
                # Unique constraints must reference terminal objects for comparison of data
                assert inputObject.isTerminal(), "Uniqueness constraints for "+c+" can only be applied to terminal data nodes!"

        if self._unique is None:
            self._unique = []
        self._unique.append(context)

    def create(self, inputKey, **kwargs):
        '''Create an object as a child

            Action - function pointer to be executed
            Enums - enumerated values allowed for the child
            Default - the default value if the child is not specified
            Desc - description of the child
            MaxOccurs - maximum occurrence of the child
            MinOccurs - minimum occurrence of the child
        '''
        self._pre_add(inputKey, **kwargs)
        if "MaxOccurs" in kwargs: self._maxOccurs[inputKey] = kwargs.pop("MaxOccurs")
        if "MinOccurs" in kwargs: self._minOccurs[inputKey] = kwargs.pop("MinOccurs")
        if "Default" in kwargs: self._defaults[inputKey] = kwargs.pop("Default")
        inputObject = InputObject(**kwargs)
        return self.add(inputKey, inputObject)

    def createSingle(self, inputKey, **kwargs):
        kwargs["MaxOccurs"] = 1
        return self.create(inputKey, **kwargs)

    def createRequired(self, inputKey, **kwargs):
        kwargs["MinOccurs"] = 1
        return self.create(inputKey, **kwargs)

    def createRequiredSingle(self, inputKey, **kwargs):
        kwargs["MaxOccurs"] = 1
        kwargs["MinOccurs"] = 1
        return self.create(inputKey, **kwargs)

    def _conductAvailableChildChecks(self, childKey, dr:DeserializedResult):
        occurrences = 0
        data = dr[childKey]
        data_type = type(data)
        if data_type is list or data_type is DeserializedResult:
            occurrences = len(data)
        else: # the data
            occurrences = 1
        # min occurs
        mio = self.minOccurs(childKey)
        if  mio and occurrences < mio:
            dr.interpreter.createErrorDiagnostic(dr.node,
                "has "+str(occurrences)+" occurrences of "+childKey+" when "+str(mio)+" are required!")

        # max occurs check was completed in DeserializedResult.addResult

    def _conductChecks(self, dr:DeserializedResult):
        storedResult = dr.storedResult()

        if storedResult is None:
            return

        # Conduct check of enumerated values
        if enums := self._enums:
            if type(storedResult) is list:
                for result in storedResult:
                    if str(result) not in enums:
                        dr.interpreter.createErrorDiagnostic(dr.node,
                            "value of "+str(result)+" is not one of the allows values "+str(enums)+"!")
            elif str(storedResult) not in enums:
                dr.interpreter.createErrorDiagnostic(dr.node,
                    str(storedResult)+" is not one of the allows values "+str(enums)+"!")

        if self._minValInc is not None and float(storedResult) < self._minValInc:
            dr.interpreter.createErrorDiagnostic(dr.node,
                str(storedResult)+" is less than the allowed minimum inclusive value of "+str(self._minValInc)+"!")

        if self._maxValInc is not None and float(storedResult) > self._maxValInc:
            dr.interpreter.createErrorDiagnostic(dr.node,
                str(storedResult)+" is greater than the allowed maximum inclusive value of "+str(self._maxValInc)+"!")

        if self._minValExc is not None and float(storedResult) <= self._minValExc:
            dr.interpreter.createErrorDiagnostic(dr.node,
                str(storedResult)+" is less than or equal to the allowed minimum exclusive value of "+str(self._minValExc)+"!")

        if self._maxValExc is not None and float(storedResult) >= self._maxValExc:
            dr.interpreter.createErrorDiagnostic(dr.node,
                str(storedResult)+" is greater than or equal to the allowed maximum exclusive value of "+str(self._maxValExc)+"!")

    def _conductAvailableChecks(self, dr:DeserializedResult):
        # Either this is leaf or parent
        # Leaf available checks are value range, type, enumeration, etc.
        try:
            if self._children:
                for key in self._children:
                    self._conductAvailableChildChecks(key, dr)

                # conduct child set checks...

                # conduct uniqueness constraints checks
                # Each entry in _unique is a list of context paths
                # for which all data must be unique
                if self._unique:
                    for context in self._unique:
                        errors = set() # set for tracking error emissions
                        # accumulate all context
                        all_context = []
                        for c in context:
                            selection = dr.select(c)
                            if selection: all_context.extend(selection)
                        count = len(all_context)
                        for i, dri in enumerate(all_context):
                            for j in range(i+1, count):
                                drj = all_context[j]
                                driv = dri.storedResult()
                                drjv = drj.storedResult()
                                if str(driv) == str(drjv):
                                    if dri not in errors:
                                        dr.interpreter.createErrorDiagnostic(dri.node, str(driv)+" must be unique but is duplicate to "+drj.node.info())
                                        errors.add(dri)
                                    if drj not in errors:
                                        dr.interpreter.createErrorDiagnostic(drj.node, str(drjv)+" must be unique but is duplicate to "+dri.node.info())
                                        errors.add(drj)

                # conduct exists constraint checks
                if self._exists:
                    for constraint in self._exists:
                        source = constraint.sources(dr)
                        target = constraint.targets(dr)
                        for s in source:
                            sv = str(s.storedResult())
                            targets = []
                            for t in target:
                                # TODO - account for discrete target values (not deserialized result)
                                tv = str(t.storedResult())
                                targets.append(tv)
                            if sv not in targets:
                                dr.interpreter.createErrorDiagnostic(s.node, str(s.node)+" is not one of the required existing targets! Required existing targets are "+", ".join(targets)+"!")
            else:
                self._conductChecks(dr)


        except Exception as exception:
            dr.interpreter.createErrorDiagnostic(dr.node, str(exception))

    def description(self):
        '''The brief description of the input object.
        None if not specified
        '''
        return self._description

    def deserialize(self, node, interpreter):
        '''Deserialize the current node according to this inputObject '''
        thisResult = DeserializedResult(node, interpreter)
        for c in node:
            if self._children is not None and c.name() in self._children:
                childResult = self._children[c.name()].deserialize(c, interpreter)
                thisResult.addResult(childResult, self)
            # 'id', etc. is considered decorative in some langauges but may have constraints
            # so first check if a constraint exists then skip if it is decorative
            elif c.isDecorative(): continue
            else:
                interpreter.createErrorDiagnostic(c, "unknown key!")

        # Check unspecified defaulted parameters
        if self._defaults is not None:
            for key, value in self._defaults.items():
                # If not in the user data it was not specified
                # Force the default value into the user data
                if key not in thisResult.userData:
                    thisResult.userData[key] = DeserializedResult.fromDefault(node, interpreter, value)
        try:
            if self.action():
                self.action()(thisResult)
        except Exception as exception:
            thisResult.interpreter.createErrorDiagnostic(node, str(exception))

        # Conduct set-level diagnostic checks
        self._conductAvailableChecks(thisResult)
        return thisResult

    def _getattr(self, name:str, childKey):
        attr = getattr(self,"_"+name)
        if childKey in attr:
            return attr[childKey]
        return None

    def default(self, childKey):
        return self._getattr('defaults', childKey)

    def enumerations(self):
        return self._enums

    def maxOccurs(self, childKey):
        return self._getattr('maxOccurs', childKey)

    def minOccurs(self, childKey):
        return self._getattr('minOccurs', childKey)

    def minValInc(self, childKey):
        return self._getattr('minValInc', childKey)

    def minValExc(self, childKey):
        return self._getattr('minValExc', childKey)

    def maxValInc(self, childKey):
        return self._getattr('maxValInc', childKey)

    def maxValExc(self, childKey):
        return self._getattr('maxValExc', childKey)

    def serialize(self, io, level=0):

        indent = " "*(level)
        if self.description():
            io.write(indent+"Description='"+self.description()+"'\n")
        if self.enumerations():
            io.write(indent+"ValueEnums["+(" ".join(self._enums))+"]\n")


        if self._children is None:
            return
        for key, child in self._children.items():

            if self.minOccurs(key):
                io.write(indent+"MinOccurs("+key+")="+str(self.minOccurs(key))+"\n")
            if self.maxOccurs(key):
                io.write(indent+"MaxOccurs("+key+")="+str(self.maxOccurs(key))+"\n")
            io.write (" "*level)
            io.write(key+":{\n")
            child.serialize(io, level+2)
            io.write(" "*level)
            io.write("}\n")

    def __bool__(self):
        '''Is this object valid based on if it had children (parent) or if it has an action (leaf)'''
        return self._children is not None or self._action is not None

    def __getitem__(self, key):
        '''Obtain the named child input object.

        Allows interaction with child input object constrains.
        '''
        if self._children is not None and key in self._children:
            return self._children[key]
        # return null/invalid object
        return InputObject()

class ExistsConstraint:
    '''Exists Constraint class provides ability to list data sources that must exist
     in a given target context '''
    def __init__(self, source, **kwargs):
        self._source = source # list(str) source data that must exist in given targets or range
        self._target = None # list(str) - target data that must exist if being referenced
        # TODO add Discrete
        self._target = kwargs.pop("target", None)
        assert type(source) is list, "ExistsConstraints source must be a list of source contexts!"
        assert len(source) > 0, "ExistsConstraints source must not be an empty list of source contexts!"
        assert type(self._target) is list, "ExistsConstraints target attribute must be a list of target contexts!"
        assert len(self._target) > 0, "ExistsConstraints target attribute must not be an empty list of target contexts!"
        assert len(kwargs) == 0, "ExistsConstraints has unknownn keyword arguments! "+str(kwargs)

    def sources(self, queryRoot):
        '''Obtain the set of sources given the queryRoot
            queryRoot:InputObject|DeserializedResult - the point from which to conduct source selection
            returns all existing InputObject or DeserializedResult
        '''
        all_source = []
        for s in self._source:
            all_source.extend(queryRoot.select(s))
        return all_source

    def targets(self, queryRoot):
        '''Obtain the set of targets given the queryRoot
            queryRoot:InputObject|DeserializedResult - the point from which to conduct target selection
            returns all existing InputObject or DeserializedResult
        '''
        all_targets = []
        for t in self._target:
            all_targets.extend(queryRoot.select(t))
        return all_targets

# Free functions for common callback
def storeInt(result):
    result.store(int(result.node))

def storeFloat(result):
    result.store(float(result.node))

def storeStr(result):
    result.store(str(result.node))



