# AttriBox - Python Descriptors the Easy Way

## Installation

Install `AttriBox` easily with pip:

```bash
pip install attribox
```

```markdown
## Quick Start

Imagine having nested custom classes with a requirement of descriptor
protocol implementation. The AI advices you to rethink the design, before
they present you with hundreds of lines of syntactic broccoli. Meanwhile,
your friends are asking you what you are doing with your life. Well, the
AttriBox is here to help!

```python
class SomeGraphics:
  """Imagine you wish to encapsulate a graphical problem in a class. You 
  already have custom classes for the components, but now you wish you 
  had implemented them as descriptors, but of course descriptors are 
  unique to the class and not to the instance. The memories are coming. 
  With them tears begin to form. Never fear! AttriBox is here!"""

  fillColor = AttriBox[RGB](144, 255, 0)
  borderColor = AttriBox[RGB](0, 0, 0)
  centeredDiv = AttriBox[GetRect](69, 420)
```

The above code implements the class attributes as descriptors. The
`AttriBox` holds on to the class for you, until one of your instances
invokes `__get__` at which point `AttriBox` creates a dedicated specimen for
just your instance.

# A More Ambitious Example

Suppose you are designing a graphical user interface. You wish to use
the descriptor protocol to expose the I/O communication directly to the
user interface. You see all of those wonderful numbers over there on the
robot or whatever, and you see those tempting '__set__' methods on your
descriptors.

```python

class MainApp(QMainWindow):
  """The basic application window."""

  mainMenuBar = AttriBox[MenuBar](this)  # yes, 'this' is a thing
  mainStatusBar = AttriBox[StatusBar](this)  # fr

  baseLayout = AttriBox[Grid]()
  baseWidget = AttriBox[QWidget]()
  indicator = AttriBox[Indicator]()
  button = AttriBox[Button]()
  slider = AttriBox[Slider]()

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.baseLayout.addWidget(self.indicator, 0, 0)
    self.baseLayout.addWidget(self.button, 1, 0)
    self.baseLayout.addWidget(self.slider, 2, 0)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    self.setMenuBar(self.mainMenuBar)
    self.setStatusBar(self.mainStatusBar)

  def connectSignals(self) -> None:
    """Connects the signals to the slots."""
    self.button.clicked.connect(self.indicator.toggle)
    self.slider.valueChanged.connect(self.indicator.setValue)
    self.slider.valueChanged.connect(self.mainStatusBar.setValue)

```

