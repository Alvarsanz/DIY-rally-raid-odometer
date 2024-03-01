
class BIESTABLE(object):        
    def __init__(self):
        self.estado = False

    def cambiar_estado(self):
        self.estado = not self.estado
        return(self.estado)
        