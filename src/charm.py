import sys
sys.path.append('lib')  # noqa: E402

from ops.charm import CharmBase
from ops.main import main


class MyCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self.on_start)

     def on_start(self, event):
        # Handle the start event here.


if __name__ == "__main__":
    main(MyCharm)
