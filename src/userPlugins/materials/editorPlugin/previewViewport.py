import os

import pandac.PandaModules as pm

from p3d.wxPanda import Viewport


class PreviewViewport(Viewport):
    def __init__(self, *args, **kwargs):
        Viewport.__init__(self, *args, **kwargs)
        #pub.subscribe(self.OnUpdate, 'Update')

    def Initialize(self, useMainWin=True):
        Viewport.Initialize(self, useMainWin)
        # create new camera for material preview
        self.previewRender = pm.NodePath('materialPreview')
        self.mCam = base.makeCamera(self._win)
        self.mCam.reparentTo(self.previewRender)
        self.mCam.setPos(0, -6, 0)
        # generate and position preview model
        self.PreviewPlane()
        # init directional light
        plight = pm.PointLight('mpLight')
        plight.setColor(pm.VBase4(1.0, 1.0, 1.0, 1.0))
        plight.setAttenuation(pm.Point3(0.5, 0, 0.05))
        self.light = self.previewRender.attachNewNode(plight)
        self.previewRender.setLight(self.light)
        self.light.setPos(-1, -2, 0.5)
        #plight.showFrustum()

    def PreviewPlane(self):
        self.model = loader.loadModel(self.GetModelPath('plane.egg'))
        self.model.reparentTo(self.previewRender)
        self.model.setScale(3)
        self.model.setPos(-1.5, 0, -1.5)
        self.model.setShaderAuto()

    def PreviewCube(self):
        self.model = loader.loadModel(self.GetModelPath('cube.egg'))
        self.model.reparentTo(self.previewRender)
        self.model.setScale(.8)
        self.model.setHpr(0, -45, -45)
        self.model.setShaderAuto()

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

    def ResetPreview(self):
        self.ApplyTextureAttrib(pm.TextureAttrib.makeDefault())

    def ApplyTextureAttrib(self, ta):
        if not ta:
            return
        geomNode = self.model.find('**/+GeomNode').node()
        geomState = geomNode.getGeomState(0)
        if geomState.getAttrib(pm.TextureAttrib.getClassType()) is not None:
            newState = geomState.setAttrib(ta)
        else:
            newState = geomState.addAttrib(ta)
        #print newState.getAttrib(pm.TextureAttrib.getClassType())
        geomNode.setGeomState(0, newState)

    def OnUpdate(self, msg):
        if not msg.data:
            self.ResetPreview()
            return
        self.CollectMaterials(msg.data[0])
        ta = self.GetTextureAttrib(msg.data[0])
        self.ApplyTextureAttrib(ta)

    def GetModelPath(self, fileName):
        """
        Return the model path for the specified file name. Model paths are
        given as absolute paths so there is not need to alter the model search
        path - doing so may give weird results if there is a similarly named
        model in the user's project.
        """
        dirPath = os.path.join(os.path.split(__file__)[0], 'models')
        modelPath = pm.Filename.fromOsSpecific(os.path.join(dirPath, fileName))
        return modelPath
