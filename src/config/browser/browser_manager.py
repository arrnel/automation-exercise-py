class BrowserStrategy(ABC):

    @abstractmethod
    def create_options(self):
        raise NotImplementedError

    @abstractmethod
    def create_driver(self, options):
        raise NotImplementedError