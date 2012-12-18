import wx

import os

from wx.lib.pubsub import Publisher as pub

import pandac.PandaModules as pm

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
        self.materialsCB.Enable(False)
        self.materialsCB.SetEditable(False)
        #st1 = wx.StaticText(self, label='Materials')
        #box.Add(st1, flag=wx.RIGHT, border=8)
        box.Add(self.materialsCB, flag=wx.RIGHT | wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        box.Add(self.pnlPreview, 1, wx.EXPAND | wx.ALL, 10)

    def OnChooseMaterial(self, event):
        index = self.materialsCB.GetSelection()
        if not index == wx.NOT_FOUND:
            ta_hash = self.materialsCB.GetClientData(index)
            self.pnlPreview.ApplyTextureAttrib(self.materials[ta_hash])

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
            self.materialsCB.Enable(False)
            self.pnlPreview.ResetPreview()
            return
        node = msg.data[0]
        self.materials = self.CollectMaterials(node)
        if not len(self.materials):
            self.materialsCB.Enable(False)
            return
        self.materialsCB.Enable(True)
        self.materialsCB.Clear()
        for ta in self.materials.values():
            self.materialsCB.Append(self.GetMaterialName(ta), ta.getHash())
        self.materialsCB.SetSelection(0)
        ta = self.GetTextureAttrib(node)
        self.pnlPreview.ApplyTextureAttrib(ta)

    def CollectMaterials(self, nodePath):
        materials = dict()
        for np in nodePath.findAllMatches('**/+GeomNode'):
            gn = np.node()
            for gi in range(gn.getNumGeoms()):
                state = gn.getGeomState(gi)
                ta = state.getAttrib(pm.TextureAttrib.getClassType())
                if ta and not ta.isOff():
                    ta_hash = ta.getHash()
                    if ta_hash not in materials:
                        materials[ta_hash] = ta
        return materials

    def GetMaterialName(self, ta):
        parts = [ts.getName() for ts in ta.getOnStages()]
        return ":".join(parts)
