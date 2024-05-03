# -*- coding: utf-8 -*- 
#   Copyright (C) 2008-2024 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

import matplotlib
from cycler import cycler

from .pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtGui import QIcon
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    from PyQt6.QtGui import QIcon
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # QtAgg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar QtAgg widget
    from matplotlib.backends.backend_qt5gg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "QtAgg"
# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
import numpy as np
import copy, os
from numpy import arange, ceil, floor, linspace, log10
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm



def log_10_product(x, pos):
    """The two args are the value and tick position.
    Label ticks with the product of the exponentiation"""
    return '%1i' % (x)
def nextPow10Up(val):
    p = int(ceil(log10(val)))
    return p

def nextPow10Down(val):
    p = int(floor(log10(val)))
    return p

class progAdaptivePlot(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            
        self.pchs = ["o", "s", "v", "p", "h", "8", "*", "x", "+", "d", ",", "^", "<", ">", "1", "2", "3", "4", "H", "D", ".", "|", "_"]  


        mpl.rcParams['xtick.major.size'] = 6
        mpl.rcParams['xtick.minor.size'] = 4
        mpl.rcParams['xtick.major.width'] = 1
        mpl.rcParams['xtick.minor.width'] = 1
        mpl.rcParams['ytick.major.size'] = 9
        mpl.rcParams['ytick.minor.size'] = 5
        mpl.rcParams['ytick.major.width'] = 0.8
        mpl.rcParams['ytick.minor.width'] = 0.8
        mpl.rcParams['xtick.direction'] = 'out'
        mpl.rcParams['ytick.direction'] = 'out'
        mpl.rcParams['font.size'] = 14
        mpl.rcParams['figure.facecolor'] = 'white'
        mpl.rcParams['lines.color'] = 'black'
        mpl.rcParams['axes.prop_cycle'] = cycler('color', ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"])

        self.mw = QWidget(self)
        self.vbl = QVBoxLayout(self.mw)
        self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
        self.ntb = NavigationToolbar(self.canvas, self.mw)
      
        
        self.ntbBox = QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.logAxisMidpoint)
        self.ntbBox.addWidget(self.logAxisSlope)
        self.ntbBox.addWidget(self.logAxisLapse)
        self.ntbBox.addWidget(self.updateButton)
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)

        self.getPSIPars()
        if self.stimScaling == "Linear":
            self.logAxisMidpoint.setChecked(False)
            self.plotDataMidpoint()
            self.plotDataStimulus()
        elif self.stimScaling == "Logarithmic":
            self.logAxisMidpoint.setChecked(True)
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()

        if self.slopeSpacing == "Linear":
            self.logAxisSlope.setChecked(False)
            self.plotDataSlope()
        elif self.slopeSpacing == "Logarithmic":
            self.logAxisSlope.setChecked(True)
            self.plotDataSlopeLogAxis()

        if self.lapseSpacing == "Linear":
            self.logAxisLapse.setChecked(False)
            self.plotDataLapse()
        elif self.lapseSpacing == "Logarithmic":
            self.logAxisLapse.setChecked(True)
            self.plotDataLapseLogAxis()

        self.fig.suptitle(self.tr("PSI Parameter Space"))
        self.show()
        self.canvas.draw()



    
    def plotDataMidpoint(self):
        self.ax1.clear()
        self.A = setPrior(self.PSI["a"], self.PSI["par"]["alpha"])
        
        if self.stimScaling == "Linear":
            markerline, stemlines, baseline = self.ax1.stem(self.PSI["alpha"], self.A[:,0,0], 'k')
        elif self.stimScaling == "Logarithmic":
            markerline, stemlines, baseline = self.ax1.stem(exp(self.PSI["alpha"]), self.A[:,0,0], 'k')
            if self.loStim < 0:
                self.ax1.set_xticklabels(list(map(str, -self.ax1.get_xticks())))
                
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

    def plotDataSlope(self):
        self.ax2.clear()
        self.B = setPrior(self.PSI["b"], self.PSI["par"]["beta"])
        markerline, stemlines, baseline = self.ax2.stem(self.PSI["beta"], self.B[0,:,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nBeta = len(self.B[0,:,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataLapse(self):
        self.ax3.clear()
        L = setPrior(self.PSI["l"], self.PSI["par"]["lambda"])
        markerline, stemlines, baseline = self.ax3.stem(self.PSI["lambda"], L[0,0,:], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nLambda = len(L[0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))

    def plotDataStimulus(self):
        self.ax4.clear()

        nStim = len(self.PSI["stims"])
        if self.stimScaling == "Linear":
            markerline, stemlines, baseline = self.ax4.stem(self.PSI["stims"], np.ones(nStim), 'k')
        elif self.stimScaling == "Logarithmic":
            markerline, stemlines, baseline = self.ax4.stem(exp(self.PSI["stims"]), np.ones(nStim), 'k')
            if self.loStim < 0:
                self.ax4.set_xticklabels(list(map(str, -self.ax4.get_xticks())))
            
        plt.setp(markerline, 'markerfacecolor', 'k')
        self.ax4.set_title("Stimulus, #Points " + str(nStim))


    def plotDataMidpointLogAxis(self):
        self.ax1.clear()
        self.A = setPrior(self.PSI["a"], self.PSI["par"]["alpha"])
        
        if self.stimScaling == "Linear":
            x = self.PSI["alpha"]
        elif self.stimScaling == "Logarithmic":
            x = exp(self.PSI["alpha"])
        markerline, stemlines, baseline = self.ax1.stem(log10(x), self.A[:,0,0], 'k')

        powd = nextPow10Down(10.0**(self.ax1.get_xlim()[0]))
        powup = nextPow10Up(10.0**(self.ax1.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax1.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            if self.stimScaling == "Logarithmic" and self.loStim < 0:
                xTickLabels.append(str(-10.0**tick))
            else:
                xTickLabels.append(str(10.0**tick))
        self.ax1.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
        self.ax1.set_xticks(minTicks, minor=True)
            
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

    def plotDataSlopeLogAxis(self):
        self.ax2.clear()
        self.B = setPrior(self.PSI["b"], self.PSI["par"]["beta"])
        markerline, stemlines, baseline = self.ax2.stem(log10(self.PSI["beta"]), self.B[0,:,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')

        powd = nextPow10Down(10.0**(self.ax2.get_xlim()[0]))
        powup = nextPow10Up(10.0**(self.ax2.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax2.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            xTickLabels.append(str(10.0**tick))
        self.ax2.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
        self.ax2.set_xticks(minTicks, minor=True)
        
        nBeta = len(self.B[0,:,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataLapseLogAxis(self):
        self.ax3.clear()
        L = setPrior(self.PSI["l"], self.PSI["par"]["lambda"])
        markerline, stemlines, baseline = self.ax3.stem(log10(self.PSI["lambda"]), L[0,0,:], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')

        powd = nextPow10Down(10.0**(self.ax3.get_xlim()[0]))
        powup = nextPow10Up(10.0**(self.ax3.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax3.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            xTickLabels.append(str(10.0**tick))
        self.ax3.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
        self.ax3.set_xticks(minTicks, minor=True)
        
        nLambda = len(L[0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))

    def plotDataStimulusLogAxis(self):
        self.ax4.clear()

        nStim = len(self.PSI["stims"])
        if self.stimScaling == "Linear":
            x = self.PSI["stims"]
        elif self.stimScaling == "Logarithmic":
            x = exp(self.PSI["stims"])
            
        markerline, stemlines, baseline = self.ax4.stem(log10(x), np.ones(nStim), 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        powd = nextPow10Down(10.0**(self.ax4.get_xlim()[0]))
        powup = nextPow10Up(10.0**(self.ax4.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax4.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            if self.stimScaling == "Logarithmic" and self.loStim < 0:
                xTickLabels.append(str(-10.0**tick))
            else:
                xTickLabels.append(str(10.0**tick))
        self.ax4.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
        self.ax4.set_xticks(minTicks, minor=True)
        
        self.ax4.set_title("Stimulus, #Points " + str(nStim))

    def onClickUpdateButton(self):
        self.getPSIPars()
        
        if self.logAxisMidpoint.isChecked() == False:
            self.plotDataMidpoint()
            self.plotDataStimulus()
        else:
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()

        if self.logAxisSlope.isChecked() == False:
            self.plotDataSlope()
        else:
            self.plotDataSlopeLogAxis()

        if self.logAxisLapse.isChecked() == False:
            self.plotDataLapse()
        else:
            self.plotDataLapseLogAxis()

        self.canvas.draw()
        
    def toggleMidpointLogAxis(self):
        if self.logAxisMidpoint.isChecked() == True:
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()
        else:
            self.plotDataMidpoint()
            self.plotDataStimulus()
        self.canvas.draw()

    def toggleSlopeLogAxis(self):
        if self.logAxisSlope.isChecked() == True:
            self.plotDataSlopeLogAxis()
        else:
            self.plotDataSlope()
        self.canvas.draw()

    def toggleLapseLogAxis(self):
        if self.logAxisLapse.isChecked() == True:
            self.plotDataLapseLogAxis()
        else:
            self.plotDataLapse()
        self.canvas.draw()
           




