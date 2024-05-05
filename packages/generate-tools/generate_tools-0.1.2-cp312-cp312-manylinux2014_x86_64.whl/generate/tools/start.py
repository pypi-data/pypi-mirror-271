import generate
from generate.exception import IsAuthorized


class Start:
    def start(self: 'generate.Generate'):
        if not self.isAuthorize:
            self.isAuthorize = True
            # print(f'\nGenerateTools v{generate.__version__}\n{generate.__license__}\n{generate.__copyright__}\n\n')
