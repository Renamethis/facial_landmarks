from onvif import ONVIFCamera
class OnvifController:
    def __init__(self, ip, port, user, password, wsdl, profile = 1):
        print('Connection to ONVIFCamera')
        self.camera = ONVIFCamera(ip, port, user, password, wsdl)
        self.media = self.camera.create_media_service()
        self.profile = self.media.GetProfiles()[profile]
        self.ptz = self.camera.create_ptz_service()
        print('Connection to ONVIF established')
    def getRtspUrl(self):
        request = self.media.create_type('GetStreamUri')
        request.ProfileToken = self.profile.token
        request.StreamSetup = {'Stream': 'RTP-Unicast',
                                'Transport': {'Protocol': 'RTSP'}}
        return self.media.GetStreamUri(request)['Uri']
    def moveCamera(self, speedx, speedy):
        status = self.ptz.GetStatus({"ProfileToken": self.profile.token})
        status.Position.PanTilt.x = speedx
        status.Position.PanTilt.y = speedy
        request = self.ptz.create_type("ContinuousMove")
        request.Velocity = status.Position
        request.ProfileToken = self.profile.token
        self.ptz.ContinuousMove(request)
    def stop(self):
        self.ptz.Stop({'ProfileToken': self.profile.token})
