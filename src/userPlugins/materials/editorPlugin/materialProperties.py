import wx

import os

from wx.lib.pubsub import Publisher as pub

import pandac.PandaModules as pm

from p3d.wxPanda import Viewport
import p3d.geometry

from previewViewport import PreviewViewport


class MaterialProperties(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.pnlPreview = PreviewViewport(self)
        pub.subscribe(self.OnUpdate, 'Update')

    def Initialize(self):
        self.pnlPreview.Initialize(False)
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        self.materialsCB = wx.ComboBox(self, style=wx.CB_DROPDOWN)
        self.materialsCB.Bind(wx.EVT_COMBOBOX, self.OnChooseMaterial)
        st1 = wx.StaticText(self, label='Materials')
        box.Add(st1, flag=wx.RIGHT, border=8)
        box.Add(self.materialsCB, flag=wx.RIGHT, border=8)
        box.Add(self.pnlPreview, 1, wx.EXPAND | wx.ALL, 10)

    def OnChooseMaterial(self, event):
        index = self.materialsCB.GetSelection()
        print index, self.materialsCB.GetValue(), self.materialsCB.GetSelection()
        if not index == wx.NOT_FOUND:
            self.pnlPreview.ApplyTextureAttrib(self.materials[index])

    def GetTextureAttrib(self, model):
        def_ta = pm.TextureAttrib.makeDefault()
        first_ta = None
        for np in model.findAllMatches('**/+GeomNode'):
            gn = np.node()
            for gi in range(gn.getNumGeoms()):
                state = gn.getGeomState(gi)
                ta = state.getAttrib(pm.TextureAttrib.getClassType())
                if ta:
                    first_ta = def_ta.compose(ta)
                    break
        return first_ta

    def OnUpdate(self, msg):
        if not msg.data:
            self.pnlPreview.ResetPreview()
            return
        node = msg.data[0]
        self.materials = self.CollectMaterials(node)
        if not len(self.materials):
            return
        cb_items = [ta.getTexture().getFilename().getBasename() for ta in self.materials]
        self.materialsCB.Clear()
        self.materialsCB.AppendItems(cb_items)
        self.materialsCB.SetSelection(0)
        ta = self.GetTextureAttrib(node)
        self.pnlPreview.ApplyTextureAttrib(ta)

    def CollectMaterials(self, nodePath):
        materials = []
        for np in nodePath.findAllMatches('**/+GeomNode'):
            gn = np.node()
            for gi in range(gn.getNumGeoms()):
                state = gn.getGeomState(gi)
                ta = state.getAttrib(pm.TextureAttrib.getClassType())
                if ta and not ta.isOff():
                    materials.append(ta)
                    print ta
        return materials
