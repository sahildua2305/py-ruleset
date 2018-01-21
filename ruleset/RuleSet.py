class RuleSet:

    def __init__(self):
        self.allOptions = set()
        self.deps = dict()
        self.reverseDeps = dict()
        self.conflicts = dict()

    def addDep(self, option1, option2):
        self.__addNewOptions(option1, option2)
        self.deps[option1].add(option2)
        self.reverseDeps[option2].add(option1)

    def addConflict(self, option1, option2):
        self.__addNewOptions(option1, option2)
        self.conflicts[option1].append(option2)
        self.conflicts[option2].append(option1)

    def isCoherent(self):
        allOptions = list(self.allOptions)
        for option in allOptions:
            # make list of deps for option
            deps = list(self.forwardDfs(option))

            # make sure option doesn't have conflict with any of its deps
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

    def __addNewOptions(self, option1, option2):
        if option1 not in self.allOptions:
            self.allOptions.add(option1)
        if option2 not in self.allOptions:
            self.allOptions.add(option2)

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

    def forwardDfs(self, start):
        return self.__dfs(self.deps, start)

    def reverseDfs(self, start):
        return self.__dfs(self.reverseDeps, start)

    def __dfs(self, graph, start):
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(graph[vertex] - visited)
        return visited

    def getConflicts(self, option):
        return self.conflicts[option]
