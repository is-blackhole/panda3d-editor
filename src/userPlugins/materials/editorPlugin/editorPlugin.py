import wx

import pandac.PandaModules as pm

from wxExtra import utils as wxUtils

import p3d
from game.plugins.base import Base

from materialProperties import MaterialProperties
from previewViewport import PreviewViewport

ID_CREATE_MATERIAL = wx.NewId()
ID_WIND_MATERIAL_PREVIEW = wx.NewId()


class EditorPlugin(Base):
    def OnInit(self):
        Base.OnInit(self)

        self.mPrim = wx.Menu()
        self.mPrim.Append(ID_CREATE_MATERIAL, '&Material')

        wxUtils.IdBind(self.ui, wx.EVT_MENU, ID_CREATE_MATERIAL, self.OnCreateMaterial)
        # Append to create menu
        self.ui.mCreate.AppendSeparator()
        self.ui.mCreate.AppendSubMenu(self.mPrim, '&Materials')
        self.pnlMaterialProperties = MaterialProperties(self.ui, style=wx.SUNKEN_BORDER)
        #self.pnlMaterialProperties = PreviewViewport(self.ui, style=wx.SUNKEN_BORDER)
        self.pnlMaterialProperties.Initialize()

        self.paneDef = wx.aui.AuiPaneInfo()\
            .Name('pnlMaterialProperties')\
            .Caption('Material')\
            .CloseButton(True)\
            .MaximizeButton(True)\
            .MinSize((100, 100))\
            .Right()\
            .Position(2)

        self.ui.AddPane(self.pnlMaterialProperties, self.paneDef)

        #self.ui.mWind.AppendCheckItem(ID_WIND_MATERIAL_PREVIEW, self.paneDef.caption)

    def OnCreateMaterial(self, evt):
        print evt, self.pnlMaterialProperties
