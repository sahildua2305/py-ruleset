class Options:
    """
    Options represents the state of RuleSet and enables selection and
    deselection of options in the RuleSet. It maintains a set of selected
    options.

    Attributes:
        rs: A RuleSet object to use.
        selectedOpts: A set of selected options at any point.
    """

    def __init__(self, rs):
        """
        Returns an empty Options class with a given RuleSet object.

        :param rs: (RuleSet) RuleSet object to use for this Options object
        """
        self.rs = rs
        self.selectedOpts = set()

    def toggle(self, option):
        """
        Implements functionality for toggling any option. It respects all
        the rules defined in the RuleSet object while selecting or deselecting
        any option.

        :param option: (str) option to toggle
        :return: None
        """
        if option not in self.selectedOpts:
            # Forward DFS on `option` and select all visited options
            dfsPath = list(self.rs.forwardDfs(option))
            for dfsOpt in dfsPath:
                self.selectedOpts.add(dfsOpt)
                # Remove all the conflicting options for `dfsOpt`
                conflicts = self.rs.conflicts[dfsOpt]
                for conflict in conflicts:
                    self.__deselectOption(conflict)
        else:
            self.__deselectOption(option)

    def __deselectOption(self, option):
        """
        Deselects options based on the rules defined in the RuleSet object.

        :param option: (str) option to deselect
        :return: None
        """
        # Reverse DFS on `option` and deselect all visited options
        reverseDfsPath = list(self.rs.reverseDfs(option))
        for dfsOpt in reverseDfsPath:
            if dfsOpt in self.selectedOpts:
                self.selectedOpts.remove(dfsOpt)

    def selection(self):
        """
        Returns the `selectedOpts` for the Options object.

        :return: (set) selected options
        """
        return self.selectedOpts
