class PL4:
    def __init__(self, miscData, dfHEAD, data):
        self.miscData = miscData
        self.dfHEAD = self._convertType(dfHEAD)
        self.data = data

    def getFromNode(self):
        from_node = [x for x in self.dfHEAD['FROM'] if not (x == '')]
        return from_node

    def getToNode(self):
        to_node = [x for x in self.dfHEAD['TO'] if not (x == '')]
        return to_node

    def getTypeSinal(self):
        type_signal = [x for x in self.dfHEAD['TYPE'] if not (x == '')]
        return type_signal

    def getDeltaTfromSimulation(self):
        return self.miscData['deltat']

    def getDeltaTfromPlot(self):
        return self.data[:, 0][-1] / (
            self.miscData['steps'] - self.miscData['steps'] % 2
        )

    def getSteps(self):
        return self.miscData['steps']

    def getTmax(self):
        return self.data[:, 0][-1]

    def _convertType(self, df):
        def func(type):
            if type == 4:
                return 'V-node'
            if type == 7:
                return 'E-bran'
            if type == 8:
                return 'V-bran'
            if type == 9:
                return 'I-bran'

            return type

        df['TYPE'] = [func(i) for i in df['TYPE']]
        return df

    def getVarData(self, Type, From, To):
        index = None

        for i in range(len(self.dfHEAD)):
            if (
                self.dfHEAD['TYPE'][i] == Type
                and self.dfHEAD['FROM'][i] == From
                and self.dfHEAD['TO'][i] == To
            ):                
                index = i
                break

        if not index == None:
            return self.data[:, index + 1]
        else:
            print('Variable %s-%s of %s not found!' % (From, To, Type))
            return None
