from PyQt5.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg


class BarGraph(QWidget):
    def __init__(self, *args, **kwargs):
        super(BarGraph, self).__init__(*args, **kwargs)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.container = QHBoxLayout()
        self.plot = pg.plot()
        self. legend = self.plot.addLegend(verSpacing=30)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.getPlotItem().hideAxis('bottom')
        self.plot.getPlotItem().hideAxis('left')
        self.plot.setXRange(-3, 6)
        self.plot.hideButtons()
        self.plot.setLabels(right='%')
        self.legend.setOffset(1)
        self.container.addWidget(self.plot)
        self.setLayout(self.container)

    def update(self, countries):
        self.plot.clear()
        brushes = ['y', 'r', 'b', 'g', 'c']
        for (i, (country, percent)) in enumerate(countries):
            bar = pg.BarGraphItem(x=[i+1], height=[percent],
                                  width=0.6, brush=brushes[i],
                                  name=country)
            self.plot.addItem(bar)
