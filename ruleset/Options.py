class Options:

    def __init__(self, rs):
        self.rs = rs
        self.selectedOpts = set()

    def toggle(self, option):
        # print "start toggle:", self.selectedOpts
        if option not in self.selectedOpts:
            # dfs on option and select all visited options
            dfsPath = list(self.rs.forwardDfs(option))
            for dfsOpt in dfsPath:
                self.selectedOpts.add(dfsOpt)
                # get all conflicting options for dfsOpt
                conflicts = self.rs.getConflicts(dfsOpt)
                # print dfsOpt, conflicts
                for conflict in conflicts:
                    self.__removeOption(conflict)
        else:
            self.__removeOption(option)
        # print "end toggle:", self.selectedOpts

    def __removeOption(self, option):
        # reverse dfs on option and deselect all visited options
        reverseDfsPath = list(self.rs.reverseDfs(option))
        # if len(reverseDfsPath) <= 1:
        #     return
        for dfsOpt in reverseDfsPath:
            if dfsOpt in self.selectedOpts:
                self.selectedOpts.remove(dfsOpt)

    def selection(self):
        return self.selectedOpts
