"""
===================
imageStackViewer

@author dsbarker
===================

"""
from __future__ import print_function, unicode_literals, division, absolute_import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets
import matplotlib.patches
import mpl_toolkits.axes_grid1

class PageSlider(matplotlib.widgets.Slider):

    def __init__(self, ax, label, numpages = 10, valinit=0, valfmt='%1d',
                 closedmin=True, closedmax=True,
                 dragging=True, **kwargs):

        self.facecolor=kwargs.get('facecolor',"w")
        self.activecolor = kwargs.pop('activecolor',"b")
        self.fontsize = kwargs.pop('fontsize', 10)
        self.numpages = numpages

        super(PageSlider, self).__init__(ax, label, 0, numpages,
                            valinit=valinit, valfmt=valfmt, **kwargs)

        self.poly.set_visible(False)
        self.vline.set_visible(False)
        self.pageRects = []
        for i in range(numpages):
            facecolor = self.activecolor if i==valinit else self.facecolor
            r  = matplotlib.patches.Rectangle((float(i)/numpages, 0), 1./numpages, 1,
                                transform=ax.transAxes, facecolor=facecolor)
            ax.add_artist(r)
            self.pageRects.append(r)
            ax.text(float(i)/numpages+0.5/numpages, 0.5, str(i+1),
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=self.fontsize)
        self.valtext.set_visible(False)

        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        bax = divider.append_axes("right", size="5%", pad=0.05)
        fax = divider.append_axes("right", size="5%", pad=0.05)
        self.button_back = matplotlib.widgets.Button(bax, label='<',
                        color=self.facecolor, hovercolor=self.activecolor)
        self.button_forward = matplotlib.widgets.Button(fax, label='>',
                        color=self.facecolor, hovercolor=self.activecolor)
        self.button_back.label.set_fontsize(self.fontsize)
        self.button_forward.label.set_fontsize(self.fontsize)
        self.button_back.on_clicked(self.backward)
        self.button_forward.on_clicked(self.forward)

    def _update(self, event):
        super(PageSlider, self)._update(event)
        i = int(self.val)
        if i >=self.valmax:
            return
        self._colorize(i)

    def _colorize(self, i):
        for j in range(self.numpages):
            self.pageRects[j].set_facecolor(self.facecolor)
        self.pageRects[i].set_facecolor(self.activecolor)

    def forward(self, event):
        current_i = int(self.val)
        i = current_i+1
        if (i < self.valmin) or (i >= self.valmax):
            return
        self.set_val(i)
        self._colorize(i)

    def backward(self, event):
        current_i = int(self.val)
        i = current_i-1
        if (i < self.valmin) or (i >= self.valmax):
            return
        self.set_val(i)
        self._colorize(i)

class IndexTracker(object):
    def __init__(self, fig, ax, X, scale=False, clim=None):
        self.fig = fig
        fig.subplots_adjust(left=0.05,right=0.875,top=0.85,bottom=0.25)
        self.ind = 0
        self.ax = ax
        ax.set_title('use slider to switch image\n displaying image %s' % (self.ind+1))
        self.X = X
        self.slices, rows, cols = X.shape
        self.scale = scale

        if self.scale:
            if clim is None:
                self.clims = (np.amin(self.X), np.amax(self.X))
            else:
                self.clims = clim

        ax_imSelector = fig.add_axes([0.15, 0.05, 0.8, 0.04])
        self.ax.set_ylabel('y (pixels)')
        self.ax.set_xlabel('x (pixels)')
        self.imSelector = PageSlider(ax_imSelector, 'Image', self.slices, valinit=(self.ind))
        self.imSelector.on_changed(self.changeImage)
        self.im = ax.imshow(self.X[self.ind, :, :])
        ax_cbar = fig.add_axes([0.8, 0.19, 0.05, 0.7])
        self.cbar = fig.colorbar(self.im, cax=ax_cbar)
        self.changeImage(self.imSelector.val)

    def changeImage(self, val):
        self.ind = int(self.imSelector.val)
        self.im.set_data(self.X[self.ind, :, :])
        if self.scale:
            self.im.set_clim((self.clims))
            self.cbar.set_clim((self.clims))
        else:
            self.im.set_clim(vmin=np.min(self.X[self.ind, :, :]),vmax=np.max(self.X[self.ind, :, :]))
            #self.cbar.set_clim(np.min(self.X[self.ind, :, :]),np.max(self.X[self.ind, :, :]))
        self.ax.set_title('use slider to switch image\ndisplaying image %s' % (self.ind+1))
        self.im.axes.figure.canvas.draw()

"""fig, ax = plt.subplots(1, 1)

X = np.random.rand(10, 20, 20)

tracker = IndexTracker(fig, ax, X)


#fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()"""
