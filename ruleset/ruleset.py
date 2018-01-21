class RuleSet:
    """
    A RuleSet represents a set of rules between the options. RuleSets have
    following properties:

    Attributes:
        deps: A dictionary representing the dependencies between the options.
        This is a graph representation as a adjacency list.
        reverseDeps: A dictionary representing the reverseDependencies between
        the options. This is used to traverse backwards to unselect options
        on which unselected options depend.
        conflicts: A dictionary representing the conflicts between the options.
    """

    def __init__(self):
        """
        Returns a RuleSet object and initializes deps, reverseDeps and
        conflicts as empty dictionaries.
        """
        self.deps = dict()
        self.reverseDeps = dict()
        self.conflicts = dict()

    def addDep(self, option1, option2):
        """
        Adds a dependency between option1 and option2 to the RuleSet object.

        :param option1: (str) first option which depends on the second option
        :param option2: (str) second option on which first option depends
        :return: None
        """
        self.__addNewOptions(option1, option2)
        self.deps[option1].add(option2)
        self.reverseDeps[option2].add(option1)

    def addConflict(self, option1, option2):
        """
        Adds a confict between option1 and option2 to the RuleSet object.

        :param option1: (str) first option
        :param option2: (str) second option
        :return: None
        """
        self.__addNewOptions(option1, option2)
        self.conflicts[option1].append(option2)
        self.conflicts[option2].append(option1)

    def isCoherent(self):
        """
        Checks if the RuleSet object is coherent, that is, that no option can
        depend, directly or indirectly, on another option and also be mutually
        exclusive with it.

        :return: True if the RuleSet object is coherent, False otherwise
        """
        allOptions = self.deps.keys()
        for option in allOptions:
            # Get all dependencies for option
            deps = list(self.forwardDfs(option))

            # Check if option doesn't have conflict with any of its deps
            for dep in deps:
                if dep != option and dep in self.conflicts[option]:
                    return False

            # make sure no two of the deps for option has a conflict
            for dep1 in deps:
                for dep2 in deps:
                    # print dep1, dep2, option, self.conflicts[option]
                    if dep1 != dep2 and (dep1 in self.conflicts[dep2] or dep2 in self.conflicts[dep1]):
                        return False
        return True

    def forwardDfs(self, start):
        """
        Implements Depth-First Search (DFS) on the basis of `deps` dictionary.
        It's used when we select an option while respecting all the existing
        rules.

        :param start: (str) starting option for Depth-First Search
        :return: Set of options present in the DFS traversal from start option
        """
        return self.__dfs(self.deps, start)

    def reverseDfs(self, start):
        """
        Implements Depth-First Search (DFS) on the basis of `reverseDeps`
        dictionary. It's used when we deselect an option while respecting
        all the existing rules.

        :param start: (str) starting option for Depth-First Search
        :return: Set of options present in the DFS traversal from start option
        """
        return self.__dfs(self.reverseDeps, start)

    def __dfs(self, graph, start):
        """
        Implements Depth-First Search (DFS) on the basis of given graph.

        :param graph: (dict) dictionary containing graph representation
        :param start: (str) starting option for Depth-First Search
        :return: Set of options present in the DFS traversal from start option
        """
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(graph[vertex] - visited)
        return visited

    def __addNewOptions(self, option1, option2):
        """
        Adds any new options to deps, reverseDeps and conflicts dictionaries
        so that we always have all the keys present in all of these three
        data structures.

        :param option1: (str) first option
        :param option2: (str) second option
        :return: None
        """
        if option1 not in self.deps:
            self.deps[option1] = set()
        if option2 not in self.deps:
            self.deps[option2] = set()

        if option1 not in self.reverseDeps:
            self.reverseDeps[option1] = set()
        if option2 not in self.reverseDeps:
            self.reverseDeps[option2] = set()

        if option1 not in self.conflicts:
            self.conflicts[option1] = list()
        if option2 not in self.conflicts:
            self.conflicts[option2] = list()
